"""
models/ml.py
Modelos de machine learning principales.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional


class LinearRegressionRevenue:
    """
    Modelo de regresión lineal para predicción de recaudo tributario.
    
    Estructura:
        Revenue = β₀ + β₁*PIB + β₂*IPC + β₃*Población + ...
    """
    
    def __init__(self):
        self.coefficients = None
        self.intercept = None
        self.feature_names = None
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'LinearRegressionRevenue':
        """
        Entrena el modelo.
        
        Args:
            X: Features (DataFrame)
            y: Target (Series)
        """
        from sklearn.linear_model import LinearRegression
        
        self.feature_names = X.columns.tolist()
        model = LinearRegression()
        model.fit(X, y)
        
        self.intercept = model.intercept_
        self.coefficients = model.coef_
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Genera predicciones."""
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(np.zeros((len(self.feature_names), len(self.feature_names))), 
                 np.zeros(len(self.feature_names)))
        model.intercept_ = self.intercept
        model.coef_ = self.coefficients
        return model.predict(X)
    
    def coefficients_summary(self) -> pd.DataFrame:
        """Devuelve resumen de coeficientes."""
        return pd.DataFrame({
            'feature': self.feature_names,
            'coefficient': self.coefficients
        }).sort_values('coefficient', key=abs, ascending=False)


# TODO: Implementar ARIMA, Random Forest, XGBoost, LSTM, etc.
