#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_processing.py
Procesamiento académico y legible de datos raw:
- Capítulos de la encuesta DANE (d_capitulos, d2_capitulos, g_capitulos, k_capitulos)
- Datos de personas (personas.csv)

Entradas: data/raw/
Salidas: data/processed/
Metadatos: data/processed/*_metadata.json
"""

from pathlib import Path
import json
import logging
from typing import Tuple, Dict
import pandas as pd

try:
    from ..core.logging import logger as project_logger

    logger = project_logger.getChild("cleaning")
except (ImportError, ValueError):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
    )
    logger = logging.getLogger("cannabis_tax.cleaning")


# ============================================================================
# FUNCIONES AUXILIARES GENERALES
# ============================================================================

def load_csv(path: Path, sep: str = ",") -> pd.DataFrame:
    """
    Cargar CSV con pandas de forma robusta.
    - path: ruta al archivo CSV
    - sep: separador (por defecto ',')
    """
    logger.info("Cargando CSV: %s", path.name)
    df = pd.read_csv(path, sep=sep, header=0, low_memory=False)
    logger.info("  -> Dimensiones: %s filas x %s columnas", df.shape[0], df.shape[1])
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
    logger.info("  -> Columnas normalizadas: %s... (%s total)", list(df.columns)[:5], len(df.columns))
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
                logger.debug("  -> Columna '%s' parseada como fecha", col)
                continue
            except Exception:
                logger.debug("  -> No se pudo parsear '%s' como fecha", col)
        # Intento de conversión a numérico
        if series.dtype == object:
            # Si la columna tiene mayoría de valores numéricos como strings
            sample = series.dropna().astype(str).head(100)
            digits_ratio = sum(s.strip().replace(".", "", 1).replace(",", "").lstrip("+-").isdigit() for s in sample) / max(len(sample), 1)
            if digits_ratio > 0.6:
                df[col] = pd.to_numeric(series.str.replace(",", ""), errors="coerce")
                logger.debug("  -> Columna '%s' convertida a numérico", col)
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
    logger.info("  -> Filas eliminadas (completamente vacias): %s", before - after_dropna)

    before_dups = df.shape[0]
    df = df.drop_duplicates()
    after_dups = df.shape[0]
    logger.info("  -> Filas eliminadas (duplicados exactos): %s", before_dups - after_dups)

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


def save_outputs(df: pd.DataFrame, metadata: dict, out_dir: Path, base_name: str) -> None:
    """
    Guarda el DataFrame procesado y el archivo de metadatos en out_dir.
    Crea el directorio si no existe.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{base_name}.csv"
    meta_path = out_dir / f"{base_name}_metadata.json"

    # Guardar CSV sin índice y con codificación utf-8
    df.to_csv(csv_path, index=False, encoding="utf-8")
    logger.info("  -> CSV guardado: %s", csv_path.name)

    # Guardar metadatos legibles
    with meta_path.open("w", encoding="utf-8") as fh:
        json.dump(metadata, fh, ensure_ascii=False, indent=2)
    logger.info("  -> Metadatos guardados: %s", meta_path.name)


# ============================================================================
# BLOQUE 1: PROCESAMIENTO DE CAPÍTULOS DANE
# ============================================================================

def process_capitulos_dane(
    input_dir: Path = Path("data/raw"),
    output_dir: Path = Path("data/processed"),
) -> Dict[str, Tuple[pd.DataFrame, dict]]:
    """
    Procesa todos los archivos de capítulos de la encuesta DANE:
    - d_capitulos.csv
    - d2_capitulos.csv
    - g_capitulos.csv
    - k_capitulos.csv
    
    Flujo para cada archivo:
    1. Cargar
    2. Normalizar nombres de columnas
    3. Inferir y castear tipos
    4. Limpiar filas vacías y duplicados
    5. Generar metadatos y guardar
    
    Returns: diccionario con {nombre: (df_procesado, metadata)}
    """
    capitulos_files = ["d_capitulos", "d2_capitulos", "g_capitulos", "k_capitulos"]
    results = {}
    
    logger.info("=" * 70)
    logger.info("BLOQUE 1: PROCESAMIENTO DE CAPITULOS DANE")
    logger.info("=" * 70)
    
    for cap_name in capitulos_files:
        try:
            input_path = input_dir / f"{cap_name}.csv"
            logger.info("\nProcesando: %s", cap_name)
            
            # Pipeline de procesamiento
            df = load_csv(input_path, sep=",")
            df = normalize_column_names(df)
            df = infer_and_cast_types(df)
            df = clean_missing_and_duplicates(df)
            
            # Metadatos y guardado
            metadata = generate_metadata(df)
            save_outputs(df, metadata, output_dir, base_name=cap_name)
            
            results[cap_name] = (df, metadata)
            logger.info("OK %s completado\n", cap_name)
            
        except FileNotFoundError:
            logger.error("Archivo no encontrado: %s.csv", cap_name)
        except Exception as e:
            logger.error("Error procesando %s: %s", cap_name, e)
    
    return results


# ============================================================================
# BLOQUE 2: PROCESAMIENTO DE DATOS DE PERSONAS
# ============================================================================

def process_personas(
    input_path: Path = Path("data/raw/personas.csv"),
    output_dir: Path = Path("data/processed"),
) -> Tuple[pd.DataFrame, dict]:
    """
    Procesa el archivo de personas.csv:
    
    Flujo:
    1. Cargar
    2. Normalizar nombres de columnas
    3. Inferir y castear tipos
    4. Limpiar filas vacías y duplicados
    5. Generar metadatos y guardar
    
    Returns: (df_procesado, metadata)
    """
    logger.info("=" * 70)
    logger.info("BLOQUE 2: PROCESAMIENTO DE DATOS DE PERSONAS")
    logger.info("=" * 70)
    
    try:
        logger.info("\nProcesando: personas.csv")
        
        # Pipeline de procesamiento
        df = load_csv(input_path, sep=",")
        df = normalize_column_names(df)
        df = infer_and_cast_types(df)
        df = clean_missing_and_duplicates(df)
        
        # Metadatos y guardado
        metadata = generate_metadata(df)
        save_outputs(df, metadata, output_dir, base_name="personas_processed")
        
        logger.info("OK Personas completado\n")
        return df, metadata
        
    except FileNotFoundError:
        logger.error("Archivo no encontrado: personas.csv")
        raise
    except Exception as e:
        logger.error("Error procesando personas: %s", e)
        raise


if __name__ == "__main__":
    """
    Punto de entrada del script.
    Ejecuta los pipelines de procesamiento en orden:
    1. Capítulos DANE
    2. Personas
    """
    RAW_DIR = Path("data/raw")
    OUTPUT_DIR = Path("data/processed")
    
    logger.info("\n")
    logger.info("INICIO DEL PROCESAMIENTO DE DATOS")
    
    try:
        # Ejecutar bloques de procesamiento
        capitulos_results = process_capitulos_dane(RAW_DIR, OUTPUT_DIR)
        personas_df, personas_meta = process_personas(Path("data/raw/personas.csv"), OUTPUT_DIR)
        
        logger.info("\n")
        logger.info("PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        logger.info("\nResumen:")
        logger.info("  - Capitulos DANE procesados: %s", len(capitulos_results))
        logger.info("  - Personas: %s filas x %s columnas", personas_df.shape[0], personas_df.shape[1])
        logger.info("\n")
        
    except FileNotFoundError as e:
        logger.error("Archivo no encontrado: %s", e)
    except Exception as e:
        logger.exception("Error inesperado durante el procesamiento: %s", e)
