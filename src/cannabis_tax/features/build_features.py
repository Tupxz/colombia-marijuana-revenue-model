"""
features/build_features.py
Ingeniería de features (variables derivadas).
"""

import pandas as pd
import numpy as np
from typing import List


def create_lagged_features(df: pd.DataFrame, target_col: str, lags: List[int]) -> pd.DataFrame:
    """
    Crea features retrasados (lagged).
    
    Args:
        df: DataFrame
        target_col: Columna objetivo
        lags: Lista de retrasos (ej: [1, 2, 3])
    
    Returns:
        DataFrame con features retrasados
    """
    df = df.copy()
    for lag in lags:
        df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
    return df


def create_rolling_features(df: pd.DataFrame, col: str, windows: List[int]) -> pd.DataFrame:
    """
    Crea features de media móvil.
    
    Args:
        df: DataFrame
        col: Columna sobre la que calcular
        windows: Tamaños de ventanas
    
    Returns:
        DataFrame con features de media móvil
    """
    df = df.copy()
    for window in windows:
        df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window).mean()
    return df


# TODO: Implementar normalizaciones, transformaciones, one-hot encoding, etc.
