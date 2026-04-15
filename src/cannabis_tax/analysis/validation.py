"""Validation and safe-cleanup helpers for the project pipeline."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

import pandas as pd

from ..core.paths import paths

DEFAULT_BASE_PATH = paths.data_processed / "base_consumo_drogas_colombia_limpia.xlsx"
DEFAULT_RAW_K_PATH = paths.data_raw / "k_capitulos.csv"

BASE_KEYS = ["id_hogar", "id_encuesta", "id_persona", "orden_persona"]
RAW_KEYS = ["directorio", "secuencia_encuesta", "secuencia_p", "orden"]

LATEX_ARTIFACT_SUFFIXES = (
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
)


def _build_check_rows() -> list[dict[str, str]]:
    return []


def _append_check(rows: list[dict[str, str]], check: str, passed: bool, detail: str) -> None:
    rows.append(
        {
            "check": check,
            "status": "pass" if passed else "fail",
            "detail": detail,
        }
    )


def validate_consumption_target(
    base_df: pd.DataFrame,
    raw_k_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Validate target assumptions used in the propensity pipeline.

    Returns a DataFrame with one row per check:
    `check`, `status` (`pass`/`fail`), `detail`.
    """
    rows = _build_check_rows()

    if "consumo_12m" not in base_df.columns:
        _append_check(
            rows,
            "base_has_consumo_12m",
            False,
            "Falta columna 'consumo_12m' en la base procesada.",
        )
        return pd.DataFrame(rows)

    observed_values = sorted(base_df["consumo_12m"].dropna().unique().tolist())
    unexpected = [value for value in observed_values if value != 1 and value != 1.0]
    _append_check(
        rows,
        "consumo_12m_domain_is_only_1_or_na",
        not unexpected,
        f"Valores observados (no nulos): {observed_values}",
    )

    non_null = int(base_df["consumo_12m"].notna().sum())
    yes_count = int(base_df["consumo_12m"].eq(1).sum())
    _append_check(
        rows,
        "consumo_12m_non_null_equals_yes_count",
        non_null == yes_count,
        f"no_nulos={non_null}, iguales_a_1={yes_count}",
    )

    if raw_k_df is None:
        _append_check(
            rows,
            "crosscheck_against_raw_k03_available",
            False,
            "No se recibió raw_k_df para validar consistencia con K_03.",
        )
        return pd.DataFrame(rows)

    raw_df = raw_k_df.copy()
    raw_df.columns = [column.lower() for column in raw_df.columns]

    required_raw = set(RAW_KEYS + ["k_03"])
    missing_raw = required_raw - set(raw_df.columns)
    _append_check(
        rows,
        "raw_has_keys_and_k03",
        not missing_raw,
        f"Faltantes en raw: {sorted(missing_raw)}",
    )
    if missing_raw:
        return pd.DataFrame(rows)

    missing_base_keys = [column for column in BASE_KEYS if column not in base_df.columns]
    _append_check(
        rows,
        "base_has_expected_keys",
        not missing_base_keys,
        f"Faltantes en base: {sorted(missing_base_keys)}",
    )
    if missing_base_keys:
        return pd.DataFrame(rows)

    base_for_merge = base_df.loc[:, BASE_KEYS + ["consumo_12m"]].copy()
    base_for_merge.columns = RAW_KEYS + ["consumo_12m"]

    merged = base_for_merge.merge(
        raw_df.loc[:, RAW_KEYS + ["k_03"]],
        on=RAW_KEYS,
        how="left",
        validate="one_to_one",
    )

    null_k03 = int(merged["k_03"].isna().sum())
    _append_check(
        rows,
        "merge_preserves_k03_for_all_rows",
        null_k03 == 0,
        f"Filas sin K_03 tras merge: {null_k03}",
    )

    mismatches = int(((merged["consumo_12m"] == 1) & (merged["k_03"] != 1)).sum())
    _append_check(
        rows,
        "consumo_12m_yes_matches_k03_yes",
        mismatches == 0,
        f"Casos con consumo_12m=1 y K_03!=1: {mismatches}",
    )

    k03_yes = int((merged["k_03"] == 1).sum())
    _append_check(
        rows,
        "consumo_12m_yes_count_matches_k03_yes_count",
        yes_count == k03_yes,
        f"consumo_12m_yes={yes_count}, k03_yes={k03_yes}",
    )

    return pd.DataFrame(rows)


def run_target_validation(
    base_path: Path = DEFAULT_BASE_PATH,
    raw_k_path: Path = DEFAULT_RAW_K_PATH,
) -> tuple[bool, pd.DataFrame]:
    """Load data files and run target validation checks."""
    base_df = pd.read_excel(base_path)
    raw_k_df = pd.read_csv(raw_k_path) if raw_k_path.exists() else None
    report = validate_consumption_target(base_df=base_df, raw_k_df=raw_k_df)
    passed = bool((report["status"] == "pass").all()) if not report.empty else False
    return passed, report


def _git_tracked_paths(root: Path) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return set()

    decoded = result.stdout.decode("utf-8", errors="ignore")
    return {entry for entry in decoded.split("\0") if entry}


def _is_tracked_path(relative_path: str, is_dir: bool, tracked_paths: set[str]) -> bool:
    if relative_path in tracked_paths:
        return True
    if not is_dir:
        return False
    prefix = relative_path.rstrip("/") + "/"
    return any(path.startswith(prefix) for path in tracked_paths)


def _collect_artifact_candidates(root: Path) -> list[Path]:
    candidates: set[Path] = set()

    for pattern in ("**/.DS_Store", ".coverage"):
        for path in root.glob(pattern):
            if path.exists():
                candidates.add(path)

    for pattern in ("reports/**", "data/**"):
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            if path.name.endswith(LATEX_ARTIFACT_SUFFIXES):
                candidates.add(path)

    for scoped_root in (root / "src", root / "tests", root / "notebooks"):
        if scoped_root.exists():
            for path in scoped_root.rglob("__pycache__"):
                if path.is_dir():
                    candidates.add(path)

    if (root / ".pytest_cache").exists():
        candidates.add(root / ".pytest_cache")

    return sorted(candidates, key=lambda path: path.as_posix())


def cleanup_artifacts(root: Path, apply: bool = False) -> dict[str, list[str] | bool]:
    """
    Cleanup known generated artifacts.

    Safety rule: never delete tracked files/directories.
    """
    tracked_paths = _git_tracked_paths(root)
    candidates = _collect_artifact_candidates(root)

    safe_to_delete: list[Path] = []
    skipped_tracked: list[str] = []

    for path in candidates:
        relative = path.relative_to(root).as_posix()
        if _is_tracked_path(relative, path.is_dir(), tracked_paths):
            skipped_tracked.append(relative)
            continue
        safe_to_delete.append(path)

    removed: list[str] = []
    if apply:
        for file_path in [path for path in safe_to_delete if path.is_file()]:
            relative = file_path.relative_to(root).as_posix()
            file_path.unlink(missing_ok=True)
            removed.append(relative)

        directories = sorted(
            [path for path in safe_to_delete if path.is_dir()],
            key=lambda path: len(path.parts),
            reverse=True,
        )
        for dir_path in directories:
            relative = dir_path.relative_to(root).as_posix()
            if dir_path.exists():
                shutil.rmtree(dir_path)
            removed.append(relative)

    return {
        "apply": apply,
        "candidates": [path.relative_to(root).as_posix() for path in candidates],
        "safe_to_delete": [path.relative_to(root).as_posix() for path in safe_to_delete],
        "skipped_tracked": sorted(skipped_tracked),
        "removed": sorted(removed),
    }
