"""Simple analysis for marijuana consumption in the last 12 months."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..core.paths import paths

DEFAULT_INPUT = paths.data_processed / "base_consumo_drogas_colombia_limpia.xlsx"
DEFAULT_OUTPUT = paths.data_processed / "consumo_12m_escenarios.csv"


def load_consumption_base(path: Path = DEFAULT_INPUT) -> pd.DataFrame:
    """Load the cleaned base used for consumption analysis."""
    df = pd.read_excel(path)
    required = {"consumo_12m"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {sorted(missing)}")
    return df


def estimate_baseline_consumers(df: pd.DataFrame) -> dict:
    """
    Estimate the observed number of consumers in the last 12 months.

    Assumption:
    `consumo_12m == 1` means reported consumption in the last 12 months.
    """
    total = int(len(df))
    consumers = int(df["consumo_12m"].fillna(0).eq(1).sum())
    prevalence = consumers / total if total else 0.0
    return {
        "total_observaciones": total,
        "consumidores_12m": consumers,
        "prevalencia_12m": prevalence,
    }


def simulate_legalization_scenarios(
    baseline_consumers: int,
    total_population: int,
    scenario_changes: dict[str, float] | None = None,
) -> pd.DataFrame:
    """
    Simulate simple percentage changes after legalization.

    `scenario_changes` is interpreted as proportional change in consumers.
    Example: `0.10` means a 10% increase over baseline consumers.
    """
    if scenario_changes is None:
        scenario_changes = {
            "conservador": 0.05,
            "base": 0.10,
            "alto": 0.20,
        }

    rows = []
    for name, change in scenario_changes.items():
        projected = round(baseline_consumers * (1 + change))
        prevalence = projected / total_population if total_population else 0.0
        rows.append(
            {
                "escenario": name,
                "cambio_pct": change,
                "consumidores_proyectados_12m": int(projected),
                "diferencia_absoluta": int(projected - baseline_consumers),
                "prevalencia_proyectada_12m": prevalence,
            }
        )
    return pd.DataFrame(rows).sort_values("cambio_pct").reset_index(drop=True)


def build_consumption_scenarios(
    input_path: Path = DEFAULT_INPUT,
    output_path: Path = DEFAULT_OUTPUT,
) -> pd.DataFrame:
    """Build and save a simple scenario table for the research question."""
    df = load_consumption_base(input_path)
    baseline = estimate_baseline_consumers(df)
    scenarios = simulate_legalization_scenarios(
        baseline_consumers=baseline["consumidores_12m"],
        total_population=baseline["total_observaciones"],
    )
    scenarios.insert(0, "baseline_consumidores_12m", baseline["consumidores_12m"])
    scenarios.insert(1, "baseline_prevalencia_12m", baseline["prevalencia_12m"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scenarios.to_csv(output_path, index=False)
    return scenarios
