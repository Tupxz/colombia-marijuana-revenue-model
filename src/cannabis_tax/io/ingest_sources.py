"""
io/ingest_sources.py
Ingestión de datos de fuentes externas (DIAN, DANE, etc.)
"""

from pathlib import Path
import pandas as pd
from typing import Optional, Dict
from ..core.paths import paths
from ..core.logging import logger


def load_raw_csv(filename: str, **kwargs) -> pd.DataFrame:
    """
    Carga un archivo CSV desde data/raw/
    
    Args:
        filename: Nombre del archivo CSV
        **kwargs: Argumentos adicionales para pd.read_csv()
    
    Returns:
        DataFrame cargado
    """
    filepath = paths.data_raw / filename
    logger.info(f"Cargando: {filepath}")
    return pd.read_csv(filepath, **kwargs)


def load_raw_excel(filename: str, sheet_name=0, **kwargs) -> pd.DataFrame:
    """
    Carga un archivo Excel desde data/raw/
    
    Args:
        filename: Nombre del archivo Excel
        sheet_name: Hoja a cargar (por defecto la primera)
        **kwargs: Argumentos adicionales para pd.read_excel()
    
    Returns:
        DataFrame cargado
    """
    filepath = paths.data_raw / filename
    logger.info(f"Cargando: {filepath}")
    return pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)


# TODO: Implementar funciones para cargar datos de DIAN, DANE, APIs externas
