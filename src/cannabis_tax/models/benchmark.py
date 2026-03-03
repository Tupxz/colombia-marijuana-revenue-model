"""
models/benchmark.py
Modelos baseline y benchmarks.
"""

import pandas as pd
import numpy as np
from typing import Tuple


class NaiveForecast:
    """
    Modelo naive: proyecta el último valor o usa media móvil.
    Benchmark básico para comparación.
    """
    
    def __init__(self, method: str = 'last'):
        """
        Args:
            method: 'last' (último valor) o 'mean' (promedio)
        """
        self.method = method
        self.last_value = None
        self.mean_value = None
    
    def fit(self, y: pd.Series) -> 'NaiveForecast':
        """Entrena el modelo."""
        self.last_value = y.iloc[-1]
        self.mean_value = y.mean()
        return self
    
    def predict(self, steps: int) -> np.ndarray:
        """Genera predicción."""
        if self.method == 'last':
            return np.full(steps, self.last_value)
        elif self.method == 'mean':
            return np.full(steps, self.mean_value)
        else:
            raise ValueError(f"Método desconocido: {self.method}")


class SeasonalNaive:
    """
    Modelo seasonal naive: repite el mismo período del año anterior.
    """
    
    def __init__(self, season_length: int = 12):
        """
        Args:
            season_length: Longitud de la estación (12 para mensual, 4 para trimestral)
        """
        self.season_length = season_length
        self.seasonal_pattern = None
    
    def fit(self, y: pd.Series) -> 'SeasonalNaive':
        """Aprende el patrón estacional."""
        n = len(y)
        self.seasonal_pattern = y.iloc[-self.season_length:].values
        return self
    
    def predict(self, steps: int) -> np.ndarray:
        """Genera predicción repitiendo patrón estacional."""
        predictions = []
        for i in range(steps):
            predictions.append(self.seasonal_pattern[i % self.season_length])
        return np.array(predictions)


# TODO: Implementar modelos de regresión simple, ARIMA, etc.
