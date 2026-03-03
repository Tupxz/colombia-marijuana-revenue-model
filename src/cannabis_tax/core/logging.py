"""
core/logging.py
Configuración centralizada de logging del proyecto.

Proporciona un logger consistente para todos los módulos.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Configura logging centralizado para el proyecto.
    
    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Archivo opcional para guardar logs
        format_string: Formato personalizado para logs
    
    Returns:
        Logger configurado
    """
    if format_string is None:
        format_string = "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"
    
    formatter = logging.Formatter(format_string)
    
    # Logger raíz
    logger = logging.getLogger("cannabis_tax")
    logger.setLevel(level)
    
    # Handler a consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler a archivo (opcional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Logger global por defecto
logger = setup_logging()
