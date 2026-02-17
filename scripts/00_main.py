#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
00_main.py
Orquestador principal del pipeline de procesamiento.

Este script ejecuta los pasos principales en orden:
1. Procesar bases de datos económicas (PIB, IPC, ISE, CDT)
2. Procesar datos de personas

Estructura:
  - 02_process_combined.py: Procesamiento de datos económicos
  - 01_processing.py: Procesamiento de datos de personas
"""

import subprocess
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def run_script(script_path: Path, description: str) -> bool:
    """
    Ejecuta un script de Python y retorna True si fue exitoso.
    """
    logging.info("\n" + "=" * 70)
    logging.info(f"▶️  EJECUTANDO: {description}")
    logging.info(f"   Script: {script_path}")
    logging.info("=" * 70 + "\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent.parent,
            check=True,
            capture_output=False,
            text=True
        )
        
        logging.info(f"\n✅ {description} completado exitosamente\n")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"\n❌ Error al ejecutar {description}")
        logging.error(f"   Código de salida: {e.returncode}\n")
        return False
    except Exception as e:
        logging.error(f"\n❌ Error inesperado en {description}: {str(e)}\n")
        return False


def main():
    """
    Ejecuta el pipeline completo de procesamiento.
    """
    logging.info("\n")
    logging.info("╔" + "=" * 68 + "╗")
    logging.info("║" + " " * 68 + "║")
    logging.info("║" + "  🔄 PIPELINE DE PROCESAMIENTO - COLOMBIA MARIJUANA REVENUE MODEL".center(68) + "║")
    logging.info("║" + " " * 68 + "║")
    logging.info("╚" + "=" * 68 + "╝")
    
    script_dir = Path(__file__).parent
    results = {}
    
    # Paso 1: Procesar bases de datos económicas
    results['bases_economicas'] = run_script(
        script_dir / '02_process_combined.py',
        'PROCESAMIENTO DE BASES ECONÓMICAS'
    )
    
    # Paso 2: Procesar datos de personas
    results['personas'] = run_script(
        script_dir / '01_processing.py',
        'PROCESAMIENTO DE DATOS DE PERSONAS'
    )
    
    # Resumen final
    logging.info("\n" + "╔" + "=" * 68 + "╗")
    logging.info("║" + " RESUMEN DEL PIPELINE".center(68) + "║")
    logging.info("╠" + "=" * 68 + "╣")
    
    for step, success in results.items():
        status = "✅" if success else "❌"
        step_name = step.replace('_', ' ').title()
        logging.info(f"║ {status} {step_name:<65}║")
    
    logging.info("╚" + "=" * 68 + "╝\n")
    
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    if successful == total:
        logging.info(f"🎉 Pipeline completado exitosamente ({successful}/{total} pasos)")
        return 0
    else:
        logging.error(f"⚠️  Pipeline completado con errores ({successful}/{total} pasos exitosos)")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
