import pandas as pd

from cannabis_tax.analysis.consumption import estimate_baseline_consumers
from cannabis_tax.analysis.consumption import simulate_legalization_scenarios


def test_estimate_baseline_consumers_counts_only_yes_values():
    df = pd.DataFrame({"consumo_12m": [1, 0, 1, None, 2]})
    result = estimate_baseline_consumers(df)

    assert result["total_observaciones"] == 5
    assert result["consumidores_12m"] == 2
    assert result["prevalencia_12m"] == 0.4


def test_simulate_legalization_scenarios_builds_expected_projection():
    result = simulate_legalization_scenarios(
        baseline_consumers=100,
        total_population=1000,
        scenario_changes={"base": 0.10},
    )

    row = result.iloc[0]
    assert row["consumidores_proyectados_12m"] == 110
    assert row["diferencia_absoluta"] == 10
    assert row["prevalencia_proyectada_12m"] == 0.11
