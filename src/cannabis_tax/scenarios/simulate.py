"""
scenarios/simulate.py
Simulación de escenarios de legalización de marihuana.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class LegalizationScenario:
    """
    Define y simula un escenario de legalización de marihuana.
    
    Parámetros:
        - Cantidad anual legalizável (toneladas)
        - Precio unitario promedio
        - Tasa impositiva (%)
        - Elasticidad de demanda
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters = {}
    
    def set_parameter(self, key: str, value: float) -> 'LegalizationScenario':
        """Establece un parámetro del escenario."""
        self.parameters[key] = value
        return self
    
    def simulate_revenue(self, years: int = 10) -> pd.DataFrame:
        """
        Simula ingresos tributarios para el escenario.
        
        Args:
            years: Número de años a simular
        
        Returns:
            DataFrame con proyecciones por año
        """
        # Placeholder: implementación simplificada
        volumes = np.linspace(0, self.parameters.get('annual_volume', 500), years)
        prices = np.full(years, self.parameters.get('unit_price', 10000))
        tax_rate = self.parameters.get('tax_rate', 0.19)
        
        revenue = volumes * prices * tax_rate
        
        return pd.DataFrame({
            'year': range(1, years + 1),
            'legalized_volume_tons': volumes,
            'estimated_revenue_pesos': revenue
        })
    
    def __repr__(self) -> str:
        return f"Scenario({self.name}): {self.description}"


class ScenarioComparator:
    """Compara múltiples escenarios."""
    
    def __init__(self):
        self.scenarios = {}
    
    def add_scenario(self, scenario: LegalizationScenario):
        """Añade un escenario a la comparación."""
        self.scenarios[scenario.name] = scenario
    
    def compare_revenues(self, years: int = 10) -> Dict[str, pd.DataFrame]:
        """
        Compara proyecciones de ingresos entre escenarios.
        
        Args:
            years: Número de años
        
        Returns:
            Diccionario con DataFrames de proyecciones por escenario
        """
        results = {}
        for name, scenario in self.scenarios.items():
            results[name] = scenario.simulate_revenue(years)
        return results


# TODO: Implementar modelos de comportamiento del consumidor, equilibrio de mercado, etc.
