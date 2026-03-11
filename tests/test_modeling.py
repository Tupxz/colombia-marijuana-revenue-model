import pandas as pd

from cannabis_tax.analysis.modeling import clean_positive_numeric
from cannabis_tax.analysis.modeling import prepare_propensity_regression_data
from cannabis_tax.analysis.modeling import recode_education_group
from cannabis_tax.analysis.modeling import recode_propensity_target


def test_clean_positive_numeric_removes_invalid_codes():
    series = pd.Series([1000, 98, 99, 0, -5, None])
    result = clean_positive_numeric(series)

    assert result.iloc[0] == 1000
    assert result.iloc[1:].isna().all()


def test_recode_propensity_target_builds_binary_working_target():
    series = pd.Series([1, 2, None, 9])
    result = recode_propensity_target(series)

    assert result.tolist() == [1, 0, 0, 0]


def test_recode_education_group_collapses_levels():
    series = pd.Series([1, 4, 7, 9, None])
    result = recode_education_group(series)

    assert result.iloc[0] == "Baja"
    assert result.iloc[1] == "Media"
    assert result.iloc[2] == "Superior"
    assert pd.isna(result.iloc[3])
    assert pd.isna(result.iloc[4])


def test_prepare_propensity_regression_data_keeps_complete_cases():
    df = pd.DataFrame(
        {
            "propension_12m": [1, 0, 1],
            "edad": [20, 21, None],
            "edad_cuadrado": [400, 441, None],
            "sexo_label": ["Hombre", "Mujer", "Hombre"],
            "educacion_grupo": ["Media", "Media", "Superior"],
            "log_precio_compra": [7.0, 8.0, 9.0],
        }
    )

    result = prepare_propensity_regression_data(df, require_price=True)

    assert len(result) == 2
    assert "log_precio_compra" in result.columns
