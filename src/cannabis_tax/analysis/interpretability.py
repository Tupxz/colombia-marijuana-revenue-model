"""Interpretabilidad (SHAP) y análisis de robustez del modelo final.

Reproduce el GBM tuneado de la Semana 12 con los hiperparámetros encontrados por
RandomizedSearchCV (notebook 05) y produce:

1. SHAP summary plot y dependence plots — Semana 14.
2. Robustez con Y alternativa estricta Y_alt = 1{K_03==1}, atendiendo el hallazgo
   del AUDIT_REPORT.md sobre la discrepancia entre `consumo_12m` y K_03.
3. Tablas LaTeX exportables a reports/tables/ para el paper final.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
)

from ..core.paths import paths

BASE_PATH = paths.data_processed / "propensity_model_base.csv"
RAW_K_PATH = paths.data_raw / "k_capitulos.csv"
FIG_DIR = paths.reports / "figures"
TAB_DIR = paths.reports / "tables"

FIG_DIR.mkdir(parents=True, exist_ok=True)
TAB_DIR.mkdir(parents=True, exist_ok=True)

FEATURES = [
    # Demográficas base
    "edad", "edad_cuadrado", "sexo_label", "educacion_grupo",
    # Estructura familiar
    "n_hijos",
    # Red social y actitud (capítulo G)
    "familiares_consumen", "amigos_consumen", "probaria_sustancias", "cannabis_medicinal",
    # Situación socioeconómica (capítulo D)
    "actividad_laboral", "regimen_salud",
    # Salud mental PHQ-2 (capítulo D)
    "sintomas_depresivos", "anhedonia",
    # Percepción de riesgo de marihuana (capítulo D)
    "riesgo_marihuana_ocasional", "riesgo_marihuana_frecuente",
]
TARGET = "propension_12m"
KEYS = ["directorio", "secuencia_encuesta", "secuencia_p", "orden"]

GBM_TUNED_PARAMS = {
    "learning_rate": 0.042203621870357574,
    "max_depth": 2,
    "max_features": "log2",
    "min_samples_leaf": 26,
    "n_estimators": 157,
    "subsample": 0.9720067339243328,
    "random_state": 42,
}


def _prepare(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    sub = df[FEATURES + [target]].dropna().copy()
    cat = [c for c in FEATURES if pd.api.types.is_object_dtype(sub[c])]
    sub = pd.get_dummies(sub, columns=cat, drop_first=True)
    feat = [c for c in sub.columns if c != target]
    X = sub[feat].astype(float)
    y = sub[target].astype(int)
    return X, y, feat


def load_data() -> pd.DataFrame:
    df = pd.read_csv(BASE_PATH)
    return df


def attach_k03(df: pd.DataFrame) -> pd.DataFrame:
    """Adjunta K_03 raw al dataset para construir Y alternativa estricta."""
    raw_k = pd.read_csv(RAW_K_PATH)
    raw_k.columns = [c.lower() for c in raw_k.columns]
    out = df.merge(raw_k[KEYS + ["k_03"]], on=KEYS, how="left")
    out["propension_12m_strict"] = (out["k_03"] == 1).astype(int)
    return out


def fit_gbm(X: pd.DataFrame, y: pd.Series) -> GradientBoostingClassifier:
    model = GradientBoostingClassifier(**GBM_TUNED_PARAMS)
    model.fit(X, y)
    return model


def evaluate(model, X_train, X_test, y_train, y_test) -> dict:
    proba_test = model.predict_proba(X_test)[:, 1]
    pred_test = (proba_test >= 0.5).astype(int)
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    cv_auc = cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=-1)
    return {
        "AUC-ROC (test)": roc_auc_score(y_test, proba_test),
        "Accuracy (test)": accuracy_score(y_test, pred_test),
        "F1 (test)": f1_score(y_test, pred_test),
        "CV AUC-10fold (mean)": cv_auc.mean(),
        "CV AUC-10fold (std)": cv_auc.std(),
    }


def shap_analysis(model, X_train, X_test, feat_names: list[str]) -> dict:
    import shap

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # Summary plot — global feature importance
    plt.figure(figsize=(8, 5))
    shap.summary_plot(shap_values, X_test, feature_names=feat_names, show=False, plot_size=None)
    plt.title("SHAP — Importancia global (GBM tuneado)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "shap_summary.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Bar plot — mean(|SHAP|)
    plt.figure(figsize=(7, 4))
    shap.summary_plot(shap_values, X_test, feature_names=feat_names, plot_type="bar", show=False)
    plt.title("SHAP — Importancia media absoluta")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "shap_bar.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Dependence plot para edad
    if "edad" in feat_names:
        plt.figure(figsize=(7, 5))
        shap.dependence_plot(
            "edad", shap_values, X_test, feature_names=feat_names, show=False,
            interaction_index=None,
        )
        plt.title("SHAP — Dependencia: edad")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "shap_dependence_edad.png", dpi=150, bbox_inches="tight")
        plt.close()

    abs_mean = np.abs(shap_values).mean(axis=0)
    importance = (
        pd.DataFrame({"feature": feat_names, "mean_abs_shap": abs_mean})
        .sort_values("mean_abs_shap", ascending=False)
        .reset_index(drop=True)
    )
    return {"importance": importance}


def _escape(s: str) -> str:
    return s.replace("_", "\\_")


def export_robustness_table(results_original: dict, results_strict: dict) -> Path:
    rows = []
    for k in ["AUC-ROC (test)", "Accuracy (test)", "F1 (test)", "CV AUC-10fold (mean)", "CV AUC-10fold (std)"]:
        rows.append({
            "Métrica": k,
            "y_orig": results_original[k],
            "y_strict": results_strict[k],
            "delta": results_strict[k] - results_original[k],
        })
    out = TAB_DIR / "robustez_y_alt.tex"
    lines = [
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Métrica & Y original (\\texttt{consumo\\_12m}) & Y estricta (K\\_03=1) & $\\Delta$ \\\\",
        "\\midrule",
    ]
    for r in rows:
        lines.append(
            f"{_escape(r['Métrica'])} & {r['y_orig']:.4f} & {r['y_strict']:.4f} & {r['delta']:+.4f} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    out.write_text("\n".join(lines))
    return out


def export_shap_table(importance: pd.DataFrame) -> Path:
    out = TAB_DIR / "shap_importance.tex"
    total = importance["mean_abs_shap"].sum()
    lines = [
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "Variable & Importancia SHAP & Participación \\\\",
        "\\midrule",
    ]
    for _, r in importance.iterrows():
        share = 100 * r["mean_abs_shap"] / total
        lines.append(
            f"{_escape(r['feature'])} & {r['mean_abs_shap']:.4f} & {share:.1f}\\% \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    out.write_text("\n".join(lines))
    return out


def main() -> None:
    print("Cargando dataset...")
    df = load_data()
    df = attach_k03(df)

    # ---- Y original ----
    X, y, feat = _prepare(df, TARGET)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    print(f"Y original — train={len(X_tr)}, test={len(X_te)}, prevalencia={y.mean():.3f}")
    gbm = fit_gbm(X_tr, y_tr)
    res_orig = evaluate(gbm, X_tr, X_te, y_tr, y_te)
    print("Métricas Y original:", {k: round(v, 4) for k, v in res_orig.items()})

    # ---- SHAP sobre Y original ----
    print("\nCorriendo SHAP...")
    shap_out = shap_analysis(gbm, X_tr, X_te, feat)
    print("\nImportancia SHAP:")
    print(shap_out["importance"].to_string(index=False))

    # ---- Y alternativa estricta ----
    print("\n=== Robustez con Y_alt = 1{K_03==1} ===")
    X2, y2, feat2 = _prepare(df, "propension_12m_strict")
    X2_tr, X2_te, y2_tr, y2_te = train_test_split(X2, y2, test_size=0.2, stratify=y2, random_state=42)
    print(f"Y estricta — train={len(X2_tr)}, test={len(X2_te)}, prevalencia={y2.mean():.3f}")
    gbm_strict = fit_gbm(X2_tr, y2_tr)
    res_strict = evaluate(gbm_strict, X2_tr, X2_te, y2_tr, y2_te)
    print("Métricas Y estricta:", {k: round(v, 4) for k, v in res_strict.items()})

    # ---- Tablas LaTeX ----
    print("\nExportando tablas LaTeX...")
    tab1 = export_robustness_table(res_orig, res_strict)
    tab2 = export_shap_table(shap_out["importance"])
    print(f"  {tab1}")
    print(f"  {tab2}")

    # Guardar JSON con resultados para referencia
    import json
    out_json = paths.reports / "interpretability_summary.json"
    payload = {
        "gbm_params": GBM_TUNED_PARAMS,
        "y_original": {k: float(v) for k, v in res_orig.items()},
        "y_strict_k03": {k: float(v) for k, v in res_strict.items()},
        "shap_importance": shap_out["importance"].to_dict(orient="records"),
        "n_train_original": int(len(X_tr)),
        "n_test_original": int(len(X_te)),
        "prevalence_original": float(y.mean()),
        "n_train_strict": int(len(X2_tr)),
        "n_test_strict": int(len(X2_te)),
        "prevalence_strict": float(y2.mean()),
        "n_disagreement_y_vs_k03": int(((df[TARGET] == 1) & (df["k_03"] != 1)).sum()),
    }
    out_json.write_text(json.dumps(payload, indent=2, default=str))
    print(f"  {out_json}")

    print("\nFiguras en", FIG_DIR)
    print("Listo.")


if __name__ == "__main__":
    main()
