"""Helpers to build the modeling base and fit benchmark models."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from ..core.logging import logger
from ..core.paths import paths
from .validation import validate_consumption_target

BASE_PATH = paths.data_processed / "base_consumo_drogas_colombia_limpia.xlsx"
PERSONAS_PATH = paths.data_processed / "personas_processed.csv"
D2_PATH = paths.data_processed / "d2_capitulos.csv"
G_PATH = paths.data_processed / "g_capitulos.csv"
D_PATH = paths.data_processed / "d_capitulos.csv"
MODEL_BASE_PATH = paths.data_processed / "propensity_model_base.csv"
RAW_K_PATH = paths.data_raw / "k_capitulos.csv"

KEY_COLUMNS = ["directorio", "secuencia_encuesta", "secuencia_p", "orden"]
INVALID_NUMERIC_CODES = {8, 9, 98, 99, 998, 999}

SEX_LABELS = {
    1: "Hombre",
    2: "Mujer",
}

EDUCATION_LABELS = {
    1: "Ninguno",
    2: "Preescolar",
    3: "Basica primaria",
    4: "Basica secundaria",
    5: "Media",
    6: "Tecnica/tecnologica",
    7: "Universitaria",
    8: "Postgrado",
    9: "No sabe / No informa",
}

EDUCATION_GROUPS = {
    1: "Baja",
    2: "Baja",
    3: "Baja",
    4: "Media",
    5: "Media",
    6: "Superior",
    7: "Superior",
    8: "Superior",
}

MODEL_LABELS = {
    "lpm_full": "MCO completa",
    "lpm_price": "MCO con precio",
    "probit_full": "Probit completo",
    "probit_price": "Probit con precio",
}

DISPLAY_NAME_MAP = {
    "Intercept": "Constante",
    "log_precio_compra": "Log precio",
    "edad": "Edad",
    "edad_cuadrado": "Edad$^2$",
    "C(sexo_label)[T.Mujer]": "Mujer",
    "C(educacion_grupo)[T.Media]": "Educacion media",
    "C(educacion_grupo)[T.Superior]": "Educacion superior",
}

# ---- Etiquetas para las nuevas variables de red social, percepción y salud ----
ACTIVIDAD_LABELS = {
    1: "Trabajando",
    2: "Buscando empleo",
    3: "Estudiando",
    4: "Oficios del hogar",
    5: "Incapacitado",
    6: "Pensionado",
    7: "Ocio",
    8: "Otra actividad",
}

REGIMEN_SALUD_LABELS = {
    1: "Contributivo",
    2: "Especial",
    3: "Subsidiado",
    9: None,  # No sabe / No informa → NaN
}


def clean_positive_numeric(
    series: pd.Series,
    invalid_codes: Iterable[int] = INVALID_NUMERIC_CODES,
) -> pd.Series:
    """Clean numeric fields that should be positive values."""
    cleaned = pd.to_numeric(series, errors="coerce")
    cleaned = cleaned.where(~cleaned.isin(list(invalid_codes)))
    return cleaned.where(cleaned > 0)


def recode_education_group(series: pd.Series) -> pd.Series:
    """Collapse education into stable groups for benchmark regressions."""
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.map(EDUCATION_GROUPS)


def recode_propensity_target(series: pd.Series) -> pd.Series:
    """
    Build a working binary target.

    Current data encoding:
    - 1.0 -> consumes in the last 12 months  -> mapped to 1
    - NaN -> no reported consumption          -> mapped to 0
    """
    binary = pd.Series(np.zeros(len(series)), index=series.index, dtype="int64")
    binary = binary.where(~series.eq(1), 1)
    return binary


def load_model_sources(
    base_path: Path = BASE_PATH,
    personas_path: Path = PERSONAS_PATH,
    d2_path: Path = D2_PATH,
    g_path: Path = G_PATH,
    d_path: Path = D_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all sources required for the modeling base."""
    base = pd.read_excel(base_path)
    personas = pd.read_csv(personas_path)
    d2 = pd.read_csv(d2_path)
    g = pd.read_csv(g_path)
    d = pd.read_csv(d_path)
    return base, personas, d2, g, d


def merge_model_sources(
    base: pd.DataFrame,
    personas: pd.DataFrame,
    d2: pd.DataFrame,
    g: pd.DataFrame | None = None,
    d: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Merge consumption, person, education and extended socio-behavioral data."""
    base = base.rename(
        columns={
            "id_hogar": "directorio",
            "id_encuesta": "secuencia_encuesta",
            "id_persona": "secuencia_p",
            "orden_persona": "orden",
        }
    )

    personas_columns = KEY_COLUMNS + ["sexo", "edad"]
    d2_columns = KEY_COLUMNS + ["d2_01", "d2_03", "d2_04", "d2_05", "d2_06", "d2_07"]

    merged = base.merge(personas[personas_columns], on=KEY_COLUMNS, how="left", validate="one_to_one")
    merged = merged.merge(d2[d2_columns], on=KEY_COLUMNS, how="left", validate="one_to_one")

    # Capítulo G: red social, actitud, percepción de riesgo
    if g is not None:
        g_cols = KEY_COLUMNS + ["g_01", "g_02", "g_04", "g_09"]
        merged = merged.merge(g[g_cols], on=KEY_COLUMNS, how="left")

    # Capítulo D: situación laboral, régimen de salud, salud mental, percepción riesgo marihuana
    if d is not None:
        d_cols = KEY_COLUMNS + ["d_02", "d_07", "d_09", "d_10", "d_11_f", "d_11_g"]
        merged = merged.merge(d[d_cols], on=KEY_COLUMNS, how="left")

    return merged


def _recode_binary_yesno(series: pd.Series) -> pd.Series:
    """Recodifica variables 1=Sí/2=No a 1/0. Trata 9=NS/NR como NaN."""
    s = pd.to_numeric(series, errors="coerce")
    s = s.where(s != 9, other=np.nan)  # 9 = No sabe → NaN
    return (s == 1).astype(float).where(s.notna(), other=np.nan)


def _recode_risk_perception(series: pd.Series) -> pd.Series:
    """Percepción de riesgo ordinal: 1=ningún riesgo … 4=gran riesgo.
    Devuelve entero 1-4; 5=No sé → NaN."""
    s = pd.to_numeric(series, errors="coerce")
    return s.where(s.between(1, 4))


def build_propensity_dataset(
    save_path: Path | None = MODEL_BASE_PATH,
    validate_target: bool = True,
    strict_target_validation: bool = False,
    raw_k_path: Path | None = RAW_K_PATH,
) -> pd.DataFrame:
    """Build the working dataset used for EDA and benchmark models.

    Fuentes integradas:
    - base_consumo_drogas_colombia_limpia.xlsx  (target + consumo + precio)
    - personas_processed.csv                   (sexo, edad)
    - d2_capitulos.csv                         (educación, hijos, estado civil)
    - g_capitulos.csv                          (red social, actitud, cannabis medicinal)
    - d_capitulos.csv                          (actividad laboral, régimen salud,
                                                salud mental PHQ-2, percepción riesgo)
    """
    base, personas, d2, g, d = load_model_sources()

    if validate_target:
        raw_k_df = pd.read_csv(raw_k_path) if raw_k_path and raw_k_path.exists() else None
        validation_report = validate_consumption_target(base_df=base, raw_k_df=raw_k_df)
        failed_checks = validation_report.loc[validation_report["status"] == "fail"]
        if not failed_checks.empty:
            for row in failed_checks.itertuples(index=False):
                logger.warning("Validacion de target fallo [%s]: %s", row.check, row.detail)
            if strict_target_validation:
                raise ValueError(
                    "Validacion de target fallida. Ejecuta `cannabis_tax validate` "
                    "y corrige inconsistencias antes de modelar."
                )

    df = merge_model_sources(base, personas, d2, g, d)

    # ---- Target ----
    df["propension_12m"] = recode_propensity_target(df["consumo_12m"])
    df["consumo_12m_missing_original"] = df["consumo_12m"].isna().astype(int)

    # ---- Variables originales de consumo/precio ----
    df["precio_compra"] = clean_positive_numeric(df["precio_compra"])
    df["cantidad_consumo"] = clean_positive_numeric(df["cantidad_consumo"])
    df["gasto_valor"] = clean_positive_numeric(df["gasto_valor"])

    # ---- Demográficas base ----
    df["edad"] = pd.to_numeric(df["edad"], errors="coerce").where(lambda s: s.between(10, 108))
    df["edad_cuadrado"] = df["edad"] ** 2
    df["sexo_label"] = df["sexo"].map(SEX_LABELS)
    df["educacion_label"] = df["d2_05"].map(EDUCATION_LABELS)
    df["educacion_grupo"] = recode_education_group(df["d2_05"])
    df["log_precio_compra"] = np.log(df["precio_compra"])
    df["n_hijos"] = pd.to_numeric(df["d2_04"], errors="coerce").clip(lower=0)

    # ---- Nuevas features: red social y actitud (capítulo G) ----
    # G_01: ¿Tiene familiares cercanos que consuman drogas? (1=Sí → 1, 2=No → 0)
    df["familiares_consumen"] = _recode_binary_yesno(df["g_01"])
    # G_02: ¿Tiene amigos que consuman drogas? (1=Sí → 1, 2=No → 0)
    df["amigos_consumen"] = _recode_binary_yesno(df["g_02"])
    # G_04: Si tuviera oportunidad, ¿probaría alguna sustancia? (1=Sí → 1, 2=No → 0)
    df["probaria_sustancias"] = _recode_binary_yesno(df["g_04"])
    # G_09: ¿Ha usado cannabis medicinal? (1=Sí → 1, 2=No → 0)
    df["cannabis_medicinal"] = _recode_binary_yesno(df["g_09"])

    # ---- Nuevas features: situación laboral y régimen de salud (capítulo D) ----
    # D_02: Actividad la semana pasada (1=trabajando … 8=otra actividad) → categórica
    d2_act = pd.to_numeric(df["d_02"], errors="coerce")
    df["actividad_laboral"] = d2_act.map(ACTIVIDAD_LABELS)
    # D_07: Régimen salud (1=contributivo, 2=especial, 3=subsidiado, 9→NaN) → ordinal proxy SES
    d7 = pd.to_numeric(df["d_07"], errors="coerce")
    d7 = d7.where(d7 != 9, other=np.nan)
    df["regimen_salud"] = d7.map(REGIMEN_SALUD_LABELS)

    # ---- Nuevas features: salud mental PHQ-2 (capítulo D) ----
    # D_09: ¿Se ha sentido deprimido los últimos 30 días?
    df["sintomas_depresivos"] = _recode_binary_yesno(df["d_09"])
    # D_10: ¿Ha sentido poco interés o placer al hacer cosas habituales?
    df["anhedonia"] = _recode_binary_yesno(df["d_10"])

    # ---- Nuevas features: percepción de riesgo de marihuana (capítulo D) ----
    # D_11_F: riesgo fumar marihuana ocasionalmente (1=ningún … 4=gran riesgo)
    df["riesgo_marihuana_ocasional"] = _recode_risk_perception(df["d_11_f"])
    # D_11_G: riesgo fumar marihuana frecuentemente
    df["riesgo_marihuana_frecuente"] = _recode_risk_perception(df["d_11_g"])

    ordered_columns = [
        "directorio", "secuencia_encuesta", "secuencia_p", "orden",
        "propension_12m", "consumo_12m", "consumo_12m_missing_original",
        "precio_compra", "log_precio_compra", "cantidad_consumo", "gasto_valor",
        "sexo", "sexo_label", "edad", "edad_cuadrado",
        "d2_05", "educacion_label", "educacion_grupo",
        "n_hijos",
        "familiares_consumen", "amigos_consumen", "probaria_sustancias", "cannabis_medicinal",
        "actividad_laboral", "regimen_salud",
        "sintomas_depresivos", "anhedonia",
        "riesgo_marihuana_ocasional", "riesgo_marihuana_frecuente",
        "frecuencia_consumo", "facil_marihuana",
    ]
    extra_columns = [column for column in df.columns if column not in ordered_columns]
    df = df[ordered_columns + extra_columns]

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_path, index=False)

    return df


def prepare_propensity_regression_data(
    df: pd.DataFrame,
    require_price: bool = True,
) -> pd.DataFrame:
    """Select and clean the columns needed for the benchmark regressions."""
    columns = [
        "propension_12m",
        "edad",
        "edad_cuadrado",
        "sexo_label",
        "educacion_grupo",
    ]
    if require_price:
        columns.append("log_precio_compra")

    regression_df = df.loc[:, columns].dropna().copy()
    regression_df["propension_12m"] = regression_df["propension_12m"].astype(float)
    return regression_df


def _build_formula(include_price: bool) -> str:
    rhs_terms = [
        "edad",
        "edad_cuadrado",
        "C(sexo_label)",
        "C(educacion_grupo)",
    ]
    if include_price:
        rhs_terms.insert(0, "log_precio_compra")
    return "propension_12m ~ " + " + ".join(rhs_terms)


def _load_statsmodels_formula_api():
    try:
        import statsmodels.formula.api as smf
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "statsmodels no esta instalado en este entorno. "
            "Instala dependencias del proyecto antes de correr MCO o Probit."
        ) from exc
    return smf


def fit_lpm(df: pd.DataFrame):
    """Fit the OLS benchmark for the binary propensity target."""
    smf = _load_statsmodels_formula_api()
    formula = _build_formula(include_price="log_precio_compra" in df.columns)
    return smf.ols(formula=formula, data=df).fit(cov_type="HC1")


def fit_probit(df: pd.DataFrame):
    """Fit a probit model for the same propensity target."""
    smf = _load_statsmodels_formula_api()
    formula = _build_formula(include_price="log_precio_compra" in df.columns)
    return smf.probit(formula=formula, data=df).fit(disp=False)


def coefficient_table(result) -> pd.DataFrame:
    """Return a notebook-friendly coefficient table."""
    return pd.DataFrame(
        {
            "coef": result.params,
            "std_err": result.bse,
            "z_or_t": result.tvalues,
            "p_value": result.pvalues,
        }
    ).sort_index()


def average_marginal_effects_table(result) -> pd.DataFrame:
    """Return average marginal effects for probit results."""
    marginal_effects = result.get_margeff(at="overall").summary_frame()
    return marginal_effects.rename(
        columns={
            "dy/dx": "coef",
            "Std. Err.": "std_err",
            "Pr(>|z|)": "p_value",
            "z": "z_or_t",
        }
    ).sort_index()


def run_propensity_specifications(df: pd.DataFrame | None = None) -> dict[str, object]:
    """Run the four benchmark specifications used in the report."""
    if df is None:
        df = build_propensity_dataset(save_path=None)

    full = prepare_propensity_regression_data(df, require_price=False)
    price = prepare_propensity_regression_data(df, require_price=True)

    return {
        "lpm_full": fit_lpm(full),
        "lpm_price": fit_lpm(price),
        "probit_full": fit_probit(full),
        "probit_price": fit_probit(price),
    }


def model_fit_summary(results: dict[str, object]) -> pd.DataFrame:
    """Build a compact summary of sample size and fit metrics."""
    rows = []
    for key, result in results.items():
        if key.startswith("lpm"):
            metric_name = "R2"
            metric_value = result.rsquared
        else:
            metric_name = "Pseudo R2"
            metric_value = result.prsquared
        rows.append(
            {
                "modelo": MODEL_LABELS[key],
                "n_obs": int(result.nobs),
                "metrica": metric_name,
                "valor_metrica": metric_value,
                "incluye_precio": "Si" if "price" in key else "No",
            }
        )
    return pd.DataFrame(rows)


def _format_estimate(coef: float, std_err: float) -> str:
    return f"{coef:.3f} ({std_err:.3f})"


def comparative_results_table(results: dict[str, object]) -> pd.DataFrame:
    """
    Build a comparative table.

    Probit columns report average marginal effects so that all coefficients are in
    probability-point units.
    """
    tables = {
        "lpm_full": coefficient_table(results["lpm_full"]),
        "lpm_price": coefficient_table(results["lpm_price"]),
        "probit_full": average_marginal_effects_table(results["probit_full"]),
        "probit_price": average_marginal_effects_table(results["probit_price"]),
    }

    ordered_variables = [
        "log_precio_compra",
        "C(sexo_label)[T.Mujer]",
        "edad",
        "edad_cuadrado",
        "C(educacion_grupo)[T.Media]",
        "C(educacion_grupo)[T.Superior]",
    ]

    result = pd.DataFrame({"variable": [DISPLAY_NAME_MAP[var] for var in ordered_variables]})
    for key in ["lpm_full", "lpm_price", "probit_full", "probit_price"]:
        table = tables[key]
        values = []
        for variable in ordered_variables:
            if variable in table.index:
                values.append(_format_estimate(table.loc[variable, "coef"], table.loc[variable, "std_err"]))
            else:
                values.append("")
        result[MODEL_LABELS[key]] = values

    return result


def _latex_header_note() -> str:
    return (
        "\\begin{flushleft}\\footnotesize "
        "Nota: la categoría de referencia para educación es Baja. "
        "Las columnas Probit reportan efectos marginales promedio. "
        "Errores estándar entre paréntesis. "
        "La variable dependiente es una medida binaria de propensión a consumir "
        "marihuana en los últimos 12 meses."
        "\\end{flushleft}\n"
    )


def export_propensity_results(
    results: dict[str, object] | None = None,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    """Export benchmark tables in LaTeX format for the report."""
    if results is None:
        results = run_propensity_specifications()
    if output_dir is None:
        output_dir = paths.reports / "tables"

    output_dir.mkdir(parents=True, exist_ok=True)

    fit_df = model_fit_summary(results)
    fit_df = fit_df.rename(
        columns={
            "modelo": "Modelo",
            "n_obs": "N",
            "metrica": "Metrica",
            "valor_metrica": "Valor",
            "incluye_precio": "Incluye precio",
        }
    )
    fit_table_path = output_dir / "propension_fit_summary.tex"
    fit_latex = fit_df.to_latex(index=False, float_format=lambda x: f"{x:.3f}", escape=False)
    fit_table_path.write_text(fit_latex, encoding="utf-8")

    comparison_df = comparative_results_table(results)
    comparison_df = comparison_df.rename(columns={"variable": "Variable"})
    comparison_table_path = output_dir / "propension_benchmark_table.tex"
    comparison_latex = comparison_df.to_latex(index=False, escape=False)
    comparison_table_path.write_text(
        comparison_latex + "\n" + _latex_header_note(),
        encoding="utf-8",
    )

    return {
        "fit_summary": fit_table_path,
        "benchmark_table": comparison_table_path,
    }
