"""
pca_prep.py
-----------
Construye el dataset limpio (sin NAs, sin identificadores) para PCA.

Variables incluidas
-------------------
Sociodemográficas (disponibles para toda la muestra):
  sexo              1=Hombre, 2=Mujer
  edad              18–65
  d2_01             Identidad étnica (1–5, 9=ninguna)
  d2_03             Estado civil (1–6)
  d2_04             Número de hijos (0–12)
  d2_05             Nivel educativo (1=Ninguno … 8=Postgrado; 9→NA)
  d2_06             Orientación sexual (1=Hetero, 2=Gay/Lesbiana, 3=Bisexual, 4=Otra)
  d2_07             Identidad de género (1=Masc, 2=Fem, 3=Trans, 4=Otro)

Variable de etiqueta (no entra al PCA, sirve para colorear):
  propension_12m    1=consumidor en últimos 12 m, 0=no consumidor

Resultado
---------
  data/processed/pca_base.csv   — 3 844 obs × 9 columnas, cero NAs
"""

from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from cannabis_tax.core.paths import ProjectPaths
    _PATHS_AVAILABLE = True
except ImportError:
    _PATHS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Columnas que entran al PCA (solo numéricas, sin identificadores)
PCA_FEATURES: list[str] = [
    "sexo",
    "edad",
    "d2_01",   # identidad étnica
    "d2_03",   # estado civil
    "d2_04",   # número de hijos
    "d2_05",   # nivel educativo
    "d2_06",   # orientación sexual
    "d2_07",   # identidad de género
]

# Etiqueta de clase (no entra al PCA, pero se guarda para colorear biplots)
TARGET = "propension_12m"

# Etiquetas legibles para cada variable (útil en biplots)
FEATURE_LABELS: dict[str, str] = {
    "sexo":   "Sexo",
    "edad":   "Edad",
    "d2_01":  "Identidad étnica",
    "d2_03":  "Estado civil",
    "d2_04":  "Núm. hijos",
    "d2_05":  "Nivel educativo",
    "d2_06":  "Orientación sexual",
    "d2_07":  "Identidad de género",
}


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------

def build_pca_dataset(
    source_csv: str | None = None,
    save_path: str | None = "auto",
) -> pd.DataFrame:
    """
    Lee ``propensity_model_base.csv``, limpia los códigos 9 = 'No sabe'
    en ``d2_05`` y devuelve un DataFrame sin NAs listo para PCA.

    Parameters
    ----------
    source_csv:
        Ruta al CSV fuente. Si es ``None`` se resuelve con ``ProjectPaths``.
    save_path:
        Ruta de destino para guardar el CSV limpio.
        ``"auto"`` → ``data/processed/pca_base.csv``.
        ``None`` → no guarda.

    Returns
    -------
    pd.DataFrame con columnas [TARGET] + PCA_FEATURES, sin NAs.
    """
    # --- 1. Resolver rutas ---------------------------------------------------
    if source_csv is None:
        if _PATHS_AVAILABLE:
            paths = ProjectPaths()
            source_csv = str(paths.data_processed / "propensity_model_base.csv")
        else:
            raise FileNotFoundError(
                "Indica la ruta al CSV o instala el paquete cannabis_tax."
            )

    if save_path == "auto":
        if _PATHS_AVAILABLE:
            paths = ProjectPaths()
            save_path = str(paths.data_processed / "pca_base.csv")
        else:
            save_path = None

    # --- 2. Cargar -----------------------------------------------------------
    df = pd.read_csv(source_csv)

    # --- 3. Seleccionar columnas necesarias ----------------------------------
    cols = [TARGET] + PCA_FEATURES
    pca_df = df[cols].copy()

    # --- 4. Limpiar códigos especiales --------------------------------------
    # d2_05 código 9 = "No sabe / No informa" → NaN  (los demás 9 son válidos)
    pca_df["d2_05"] = pca_df["d2_05"].replace({9: np.nan})

    # --- 5. Eliminar filas con NA -------------------------------------------
    n_before = len(pca_df)
    pca_df = pca_df.dropna().reset_index(drop=True)
    n_after = len(pca_df)

    print(f"Filas originales : {n_before:,}")
    print(f"Filas en pca_base: {n_after:,}  (eliminadas: {n_before - n_after})")
    print(f"Prevalencia consumo 12m: {pca_df[TARGET].mean():.3f}")
    print(f"Variables PCA ({len(PCA_FEATURES)}): {PCA_FEATURES}")

    # --- 6. Guardar ---------------------------------------------------------
    if save_path is not None:
        pca_df.to_csv(save_path, index=False)
        print(f"Guardado en: {save_path}")

    return pca_df


# ---------------------------------------------------------------------------
# CLI mínimo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    build_pca_dataset()
