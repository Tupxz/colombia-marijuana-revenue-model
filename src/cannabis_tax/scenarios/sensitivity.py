"""
scenarios/sensitivity.py
Análisis de sensibilidad de los modelos frente a variaciones en parámetros.
"""

import pandas as pd
import numpy as np
from typing import Dict, Callable, Tuple


class SensitivityAnalyzer:
    """
    Realiza análisis de sensibilidad: variaciones de un parámetro
    y su impacto en el output.
    """
    
    def __init__(self, model_func: Callable):
        """
        Args:
            model_func: Función que calcula el output dado parámetros
        """
        self.model_func = model_func
    
    def one_way_sensitivity(self, param_name: str, param_range: np.ndarray,
                           base_params: Dict, target_var: str = None) -> pd.DataFrame:
        """
        Análisis de sensibilidad uni-direccional.
        
        Args:
            param_name: Parámetro a variar
            param_range: Rango de valores para el parámetro
            base_params: Parámetros base
            target_var: Variable de output a seguir
        
        Returns:
            DataFrame con resultados de sensibilidad
        """
        results = []
        for value in param_range:
            params = base_params.copy()
            params[param_name] = value
            output = self.model_func(params)
            results.append({
                param_name: value,
                'output': output
            })
        
        return pd.DataFrame(results)
    
    def tornado_analysis(self, param_variations: Dict[str, Tuple[float, float]],
                        base_params: Dict) -> pd.DataFrame:
        """
        Análisis tornado: variación simultánea de múltiples parámetros.
        
        Args:
            param_variations: Dict de parámetros con (min, max)
            base_params: Parámetros base
        
        Returns:
            DataFrame con rangos de impacto ordenados
        """
        impacts = []
        for param, (min_val, max_val) in param_variations.items():
            base = self.model_func(base_params)
            
            # Impacto al mínimo
            params_min = base_params.copy()
            params_min[param] = min_val
            output_min = self.model_func(params_min)
            
            # Impacto al máximo
            params_max = base_params.copy()
            params_max[param] = max_val
            output_max = self.model_func(params_max)
            
            impact_range = output_max - output_min
            impacts.append({
                'parameter': param,
                'min_impact': output_min - base,
                'max_impact': output_max - base,
                'range': impact_range
            })
        
        return pd.DataFrame(impacts).sort_values('range', ascending=False)


# TODO: Implementar Monte Carlo, análisis de elasticidad, etc.
