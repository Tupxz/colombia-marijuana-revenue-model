from pathlib import Path
import json
import logging
from typing import Tuple
import pandas as pd

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_processing.py
Procesamiento académico y legible de un CSV de entrada.
Entrada por defecto: data/raw/personas.csv
Salida por defecto: data/processed/personas_processed.csv
Resumen de metadatos: data/processed/personas_metadata.json
"""



# Configuración básica de logging para trazabilidad académica
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def load_csv(path: Path, sep: str = ",") -> pd.DataFrame:
    """
    Cargar CSV con pandas de forma robusta.
    - path: ruta al archivo CSV
    - sep: separador (por defecto ',')
    """
    logging.info("Cargando CSV desde: %s", path)
    df = pd.read_csv(path, sep=sep, header=0, low_memory=False)
    logging.info("Dimensiones cargadas: filas=%d, columnas=%d", df.shape[0], df.shape[1])
    return df


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas: strip, minúsculas, espacios -> guiones bajos.
    Devuelve un nuevo DataFrame (copia de columnas renombradas).
    """
    new_columns = {
        col: col.strip().lower().replace(" ", "_").replace("-", "_")
        for col in df.columns
    }
    df = df.rename(columns=new_columns)
    logging.info("Columnas normalizadas: %s", list(df.columns))
    return df


def infer_and_cast_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Intenta convertir columnas a tipos más apropiados:
    - Detecta y parsea fechas si el nombre de la columna sugiere fecha.
    - Convierte columnas numéricas en caso de que sean strings con dígitos.
    No fuerza conversiones que pierdan demasiada información (usa errors='coerce').
    """
    df = df.copy()
    for col in df.columns:
        series = df[col]
        # Intento de parseo de fecha por nombre de columna
        if any(keyword in col for keyword in ("fecha", "date", "dob", "nacimiento")):
            try:
                df[col] = pd.to_datetime(series, errors="coerce", dayfirst=True)
                logging.info("Columna '%s' parseada como fecha (coerced donde aplique).", col)
                continue
            except Exception:
                logging.debug("No se pudo parsear '%s' como fecha.", col)
        # Intento de conversión a numérico
        if series.dtype == object:
            # Si la columna tiene mayoría de valores numéricos como strings
            sample = series.dropna().astype(str).head(100)
            digits_ratio = sum(s.strip().replace(".", "", 1).replace(",", "").lstrip("+-").isdigit() for s in sample) / max(len(sample), 1)
            if digits_ratio > 0.6:
                df[col] = pd.to_numeric(series.str.replace(",", ""), errors="coerce")
                logging.info("Columna '%s' convertida a numérico (coerced donde aplique).", col)
    return df


def clean_missing_and_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Operaciones sencillas de limpieza:
    - Elimina filas completamente vacías.
    - Elimina duplicados exactos.
    - Mantiene NaNs para procesos posteriores (no imputar automáticamente).
    """
    before = df.shape[0]
    df = df.dropna(how="all")
    after_dropna = df.shape[0]
    logging.info("Filas eliminadas por estar completamente vacías: %d", before - after_dropna)

    before_dups = df.shape[0]
    df = df.drop_duplicates()
    after_dups = df.shape[0]
    logging.info("Filas eliminadas por duplicados exactos: %d", before_dups - after_dups)

    return df


def generate_metadata(df: pd.DataFrame) -> dict:
    """
    Genera un diccionario con metadatos básicos del DataFrame:
    - número de filas/columnas
    - tipos de columnas
    - conteo de nulos por columna
    """
    metadata = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "null_counts": {col: int(df[col].isna().sum()) for col in df.columns},
    }
    return metadata


def save_outputs(df: pd.DataFrame, metadata: dict, out_dir: Path, base_name: str = "personas_processed"):
    """
    Guarda el DataFrame procesado y el archivo de metadatos en out_dir.
    Crea el directorio si no existe.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{base_name}.csv"
    meta_path = out_dir / f"{base_name}_metadata.json"

    # Guardar CSV sin índice y con codificación utf-8
    df.to_csv(csv_path, index=False, encoding="utf-8")
    logging.info("CSV procesado guardado en: %s", csv_path)

    # Guardar metadatos legibles
    with meta_path.open("w", encoding="utf-8") as fh:
        json.dump(metadata, fh, ensure_ascii=False, indent=2)
    logging.info("Metadatos guardados en: %s", meta_path)


def process_personas(
    input_path: Path = Path("data/raw/personas.csv"),
    output_dir: Path = Path("data/processed"),
) -> Tuple[pd.DataFrame, dict]:
    """
    Flujo principal de procesamiento:
    1. Cargar
    2. Normalizar nombres de columnas
    3. Inferir y castear tipos básicos
    4. Limpiar filas vacías y duplicados
    5. Generar metadatos y guardar salidas
    Devuelve (df_procesado, metadata).
    """
    df = load_csv(input_path, sep=",")
    df = normalize_column_names(df)
    df = infer_and_cast_types(df)
    df = clean_missing_and_duplicates(df)
    metadata = generate_metadata(df)
    save_outputs(df, metadata, output_dir)
    return df, metadata


if __name__ == "__main__":
    # Punto de entrada del script cuando se ejecuta directamente.
    INPUT = Path("data/raw/personas.csv")
    OUTPUT_DIR = Path("data/processed")

    try:
        df_processed, meta = process_personas(INPUT, OUTPUT_DIR)
        logging.info("Procesamiento completado correctamente. Filas finales: %d", df_processed.shape[0])
    except FileNotFoundError as e:
        logging.error("Archivo no encontrado: %s", e)
    except Exception as e:
        logging.exception("Ocurrió un error inesperado durante el procesamiento: %s", e)