"""
models/evaluate.py
Evaluación de modelos y cálculo de métricas.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def evaluate_forecast(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calcula métricas de evaluación para un pronóstico.
    
    Args:
        y_true: Valores reales
        y_pred: Valores predichos
    
    Returns:
        Diccionario con métricas (MAE, RMSE, MAPE, R²)
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    # MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    r2 = r2_score(y_true, y_pred)
    
    return {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'R2': r2
    }


def cross_validate_model(model, X: pd.DataFrame, y: pd.Series, 
                         cv: int = 5) -> Dict[str, float]:
    """
    Validación cruzada de un modelo.
    
    Args:
        model: Modelo con métodos fit() y predict()
        X: Features
        y: Target
        cv: Número de folds
    
    Returns:
        Métricas promediadas de validación cruzada
    """
    from sklearn.model_selection import cross_val_score
    
    scores = cross_val_score(model, X, y, cv=cv, 
                            scoring='neg_mean_absolute_error')
    
    return {
        'CV_MAE_mean': -scores.mean(),
        'CV_MAE_std': scores.std()
    }


# TODO: Agregar bootstrap, análisis de residuos, backtesting, etc.
