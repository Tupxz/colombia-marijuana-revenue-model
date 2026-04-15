from pathlib import Path

import numpy as np
import pandas as pd

from cannabis_tax.analysis.validation import cleanup_artifacts
from cannabis_tax.analysis.validation import validate_consumption_target


def _base_df(values):
    return pd.DataFrame(
        {
            "id_hogar": [1, 2],
            "id_encuesta": [10, 20],
            "id_persona": [100, 200],
            "orden_persona": [1, 1],
            "consumo_12m": values,
        }
    )


def _raw_df(k03_values):
    return pd.DataFrame(
        {
            "DIRECTORIO": [1, 2],
            "SECUENCIA_ENCUESTA": [10, 20],
            "SECUENCIA_P": [100, 200],
            "ORDEN": [1, 1],
            "K_03": k03_values,
        }
    )


def test_validate_consumption_target_detects_k03_mismatch():
    report = validate_consumption_target(
        base_df=_base_df([1.0, np.nan]),
        raw_k_df=_raw_df([2, 2]),
    )

    mismatch_row = report.loc[report["check"] == "consumo_12m_yes_matches_k03_yes"].iloc[0]
    assert mismatch_row["status"] == "fail"


def test_validate_consumption_target_passes_when_aligned():
    report = validate_consumption_target(
        base_df=_base_df([1.0, np.nan]),
        raw_k_df=_raw_df([1, 2]),
    )

    assert (report["status"] == "pass").all()


def test_cleanup_artifacts_removes_only_known_generated_files(tmp_path: Path):
    ds_store = tmp_path / ".DS_Store"
    ds_store.write_text("x", encoding="utf-8")
    (tmp_path / "src" / "module").mkdir(parents=True)
    pycache = tmp_path / "src" / "module" / "__pycache__"
    pycache.mkdir()
    (pycache / "foo.cpython-312.pyc").write_bytes(b"x")

    dry_run = cleanup_artifacts(tmp_path, apply=False)
    assert ".DS_Store" in dry_run["safe_to_delete"]
    assert "src/module/__pycache__" in dry_run["safe_to_delete"]

    applied = cleanup_artifacts(tmp_path, apply=True)
    assert ".DS_Store" in applied["removed"]
    assert "src/module/__pycache__" in applied["removed"]
    assert not ds_store.exists()
    assert not pycache.exists()
