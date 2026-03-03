"""
features/diagnostics.py
Diagnósticos y validación de datos.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def check_missing_values(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Diagnóstico de valores faltantes.
    
    Args:
        df: DataFrame
    
    Returns:
        Diccionario con estadísticas de valores faltantes
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    
    return {
        'missing_counts': missing.to_dict(),
        'missing_percentages': missing_pct.to_dict(),
        'total_missing': missing.sum(),
        'total_cells': df.shape[0] * df.shape[1]
    }


def check_data_types(df: pd.DataFrame) -> Dict[str, int]:
    """
    Resumen de tipos de datos.
    
    Args:
        df: DataFrame
    
    Returns:
        Diccionario con conteos de tipos
    """
    return df.dtypes.value_counts().to_dict()


def detect_outliers(df: pd.DataFrame, col: str, method: str = 'iqr') -> pd.Series:
    """
    Detecta outliers usando IQR o Z-score.
    
    Args:
        df: DataFrame
        col: Columna a analizar
        method: 'iqr' o 'zscore'
    
    Returns:
        Serie booleana indicando outliers
    """
    if method == 'iqr':
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        return (df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))
    elif method == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(df[col].dropna()))
        return z_scores > 3
    else:
        raise ValueError(f"Método desconocido: {method}")


# TODO: Agregar más diagnósticos (distribuciones, colinealidad, etc.)
