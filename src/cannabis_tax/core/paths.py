"""
core/paths.py
Gestor centralizado de rutas del proyecto.

Define todas las rutas relativas al directorio raíz del repositorio.
Evita paths hardcodeados en el código.
"""

from pathlib import Path
from typing import Optional


class ProjectPaths:
    """Gestor de rutas del proyecto."""
    
    def __init__(self, root_dir: Optional[Path] = None):
        """
        Inicializa gestor de rutas.
        
        Args:
            root_dir: Directorio raíz del proyecto.
                     Si no se proporciona, lo infiere desde este archivo.
        """
        if root_dir is None:
            # Infiere raíz: este archivo está en src/cannabis_tax/core/paths.py
            root_dir = Path(__file__).parent.parent.parent.parent
        
        self.root = root_dir
    
    # Data directories
    @property
    def data_raw(self) -> Path:
        """data/raw/"""
        return self.root / "data" / "raw"
    
    @property
    def data_interim(self) -> Path:
        """data/interim/"""
        return self.root / "data" / "interim"
    
    @property
    def data_processed(self) -> Path:
        """data/processed/"""
        return self.root / "data" / "processed"
    
    @property
    def data_external(self) -> Path:
        """data/external/"""
        return self.root / "data" / "external"
    
    # Config directories
    @property
    def configs(self) -> Path:
        """configs/"""
        return self.root / "configs"
    
    # Reports and outputs
    @property
    def reports(self) -> Path:
        """reports/"""
        return self.root / "reports"
    
    @property
    def reports_figures(self) -> Path:
        """reports/figures/"""
        return self.reports / "figures"
    
    @property
    def reports_slides(self) -> Path:
        """reports/slides/"""
        return self.reports / "slides"
    
    # Runs (execution outputs)
    @property
    def runs(self) -> Path:
        """runs/"""
        return self.root / "runs"
    
    # Source code
    @property
    def src(self) -> Path:
        """src/"""
        return self.root / "src"
    
    @property
    def cannabis_tax(self) -> Path:
        """src/cannabis_tax/"""
        return self.src / "cannabis_tax"
    
    # Notebooks and tests
    @property
    def notebooks(self) -> Path:
        """notebooks/"""
        return self.root / "notebooks"
    
    @property
    def tests(self) -> Path:
        """tests/"""
        return self.root / "tests"
    
    def __repr__(self) -> str:
        return f"ProjectPaths(root={self.root})"


# Instancia global de rutas
paths = ProjectPaths()
