"""
viz/plots.py
Funciones de visualización y graficación.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List


def plot_time_series(df: pd.DataFrame, x_col: str, y_cols: List[str],
                     title: str = None, ylabel: str = None,
                     figsize: tuple = (12, 6)) -> plt.Figure:
    """
    Grafica series temporales.
    
    Args:
        df: DataFrame con datos
        x_col: Nombre de columna para eje X
        y_cols: Lista de columnas para eje Y
        title: Título del gráfico
        ylabel: Etiqueta eje Y
        figsize: Tamaño de figura
    
    Returns:
        Figure de matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for col in y_cols:
        ax.plot(df[x_col], df[col], marker='o', label=col)
    
    ax.set_xlabel(x_col)
    ax.set_ylabel(ylabel or 'Valor')
    ax.set_title(title or f'Serie Temporal')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_scenario_comparison(scenarios_data: dict,
                             figsize: tuple = (12, 6)) -> plt.Figure:
    """
    Compara múltiples escenarios visualmente.
    
    Args:
        scenarios_data: Dict de {escenario: DataFrame}
        figsize: Tamaño de figura
    
    Returns:
        Figure de matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for scenario_name, df in scenarios_data.items():
        if 'year' in df.columns and 'estimated_revenue_pesos' in df.columns:
            ax.plot(df['year'], df['estimated_revenue_pesos'], 
                   marker='s', label=scenario_name)
    
    ax.set_xlabel('Año')
    ax.set_ylabel('Ingresos Tributarios (Pesos)')
    ax.set_title('Comparación de Escenarios de Legalización')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_sensitivity_tornado(sensitivity_df: pd.DataFrame,
                            figsize: tuple = (10, 6)) -> plt.Figure:
    """
    Grafica análisis tornado de sensibilidad.
    
    Args:
        sensitivity_df: DataFrame con resultados de tornado
        figsize: Tamaño de figura
    
    Returns:
        Figure de matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    y_pos = np.arange(len(sensitivity_df))
    
    ax.barh(y_pos, sensitivity_df['range'], color='steelblue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sensitivity_df['parameter'])
    ax.set_xlabel('Rango de Impacto')
    ax.set_title('Análisis de Sensibilidad - Tornado')
    ax.grid(True, alpha=0.3, axis='x')
    
    return fig


# TODO: Agregar distribuciones, boxplots, heatmaps, etc.
