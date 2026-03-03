"""
core/config.py
Gestor centralizado de configuración del proyecto.

Carga archivos YAML desde configs/ y proporciona acceso a parámetros globales.
"""

from pathlib import Path
from typing import Dict, Any
import yaml


class Config:
    """Gestor de configuración del proyecto."""
    
    def __init__(self, config_path: Path = None):
        """
        Inicializa configuración desde archivo YAML.
        
        Args:
            config_path: Ruta al archivo de configuración base.
                        Si no se proporciona, usa configs/base.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent.parent / "configs" / "base.yaml"
        
        self.config_path = config_path
        self.data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga configuración desde YAML."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def get(self, key: str, default=None) -> Any:
        """Obtiene valor de configuración por clave."""
        return self.data.get(key, default)
    
    def __repr__(self) -> str:
        return f"Config(path={self.config_path}, keys={list(self.data.keys())})"


# Instancia global de configuración
config = Config()
