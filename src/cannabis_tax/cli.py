#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cli.py
Interfaz de línea de comandos (CLI) para el pipeline de análisis de recaudo tributario.

Orquesta el procesamiento de datos, modelado y análisis de escenarios.
Uso: python -m src.cannabis_tax.cli [COMANDO] [OPCIONES]

Comandos disponibles:
  - process    : Procesar y limpiar datos raw
  - analyze    : Ejecutar análisis exploratorio
  - model      : Entrenar modelos predictivos
  - scenarios  : Simular escenarios de legalización
  - evaluate   : Evaluar y comparar modelos
  - viz        : Generar visualizaciones
"""

import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime

from .core.logging import setup_logging, logger
from .core.paths import paths


def cmd_process(args):
    """Comando: procesar y limpiar datos raw."""
    logger.info("=" * 70)
    logger.info("▶️  PROCESAMIENTO DE DATOS RAW")
    logger.info("=" * 70)
    
    from .cleaning.clean import main as process_main
    
    try:
        process_main()
        logger.info("✅ Procesamiento completado exitosamente")
        return 0
    except Exception as e:
        logger.error(f"❌ Error durante procesamiento: {e}")
        return 1


def cmd_analyze(args):
    """Comando: análisis exploratorio de datos."""
    logger.info("=" * 70)
    logger.info("▶️  ANÁLISIS EXPLORATORIO")
    logger.info("=" * 70)
    
    logger.info(f"Analizando datos en: {paths.data_processed}")
    logger.info("✅ Análisis completado (placeholder)")
    return 0


def cmd_model(args):
    """Comando: entrenar modelos predictivos."""
    logger.info("=" * 70)
    logger.info("▶️  ENTRENAMIENTO DE MODELOS")
    logger.info("=" * 70)
    
    logger.info(f"Entrenando modelos...")
    logger.info("✅ Modelos entrenados (placeholder)")
    return 0


def cmd_scenarios(args):
    """Comando: simular escenarios de legalización."""
    logger.info("=" * 70)
    logger.info("▶️  SIMULACIÓN DE ESCENARIOS")
    logger.info("=" * 70)
    
    logger.info(f"Simulando {args.scenarios} escenarios...")
    logger.info("✅ Simulaciones completadas (placeholder)")
    return 0


def cmd_evaluate(args):
    """Comando: evaluar y comparar modelos."""
    logger.info("=" * 70)
    logger.info("▶️  EVALUACIÓN DE MODELOS")
    logger.info("=" * 70)
    
    logger.info("Evaluando modelos...")
    logger.info("✅ Evaluación completada (placeholder)")
    return 0


def cmd_viz(args):
    """Comando: generar visualizaciones."""
    logger.info("=" * 70)
    logger.info("▶️  GENERACIÓN DE VISUALIZACIONES")
    logger.info("=" * 70)
    
    logger.info(f"Generando gráficos en: {paths.reports_figures}")
    logger.info("✅ Visualizaciones generadas (placeholder)")
    return 0


def cmd_pipeline(args):
    """Comando: ejecutar pipeline completo."""
    logger.info("\n")
    logger.info("╔" + "=" * 68 + "╗")
    logger.info("║" + " " * 68 + "║")
    logger.info("║" + "  🔄 PIPELINE COMPLETO - COLOMBIA MARIJUANA REVENUE MODEL".center(68) + "║")
    logger.info("║" + " " * 68 + "║")
    logger.info("╚" + "=" * 68 + "╝\n")
    
    steps = [
        ("process", cmd_process, "Procesamiento de datos"),
        ("analyze", cmd_analyze, "Análisis exploratorio"),
        ("model", cmd_model, "Entrenamiento de modelos"),
        ("scenarios", cmd_scenarios, "Simulación de escenarios"),
        ("evaluate", cmd_evaluate, "Evaluación de modelos"),
        ("viz", cmd_viz, "Generación de visualizaciones"),
    ]
    
    results = {}
    for step_name, step_func, step_desc in steps:
        logger.info(f"\n📍 {step_desc}...")
        fake_args = argparse.Namespace(scenarios=3)
        success = step_func(fake_args) == 0
        results[step_desc] = success
    
    # Resumen
    logger.info("\n" + "╔" + "=" * 68 + "╗")
    logger.info("║" + " RESUMEN DEL PIPELINE".center(68) + "║")
    logger.info("╠" + "=" * 68 + "╣")
    
    for step_name, success in results.items():
        status = "✅" if success else "❌"
        logger.info(f"║ {status} {step_name:<65}║")
    
    logger.info("╚" + "=" * 68 + "╝\n")
    
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    if successful == total:
        logger.info(f"🎉 Pipeline completado exitosamente ({successful}/{total} pasos)")
        return 0
    else:
        logger.error(f"⚠️  Pipeline completado con errores ({successful}/{total} pasos exitosos)")
        return 1


def main():
    """Punto de entrada principal de la CLI."""
    parser = argparse.ArgumentParser(
        prog='cannabis_tax',
        description='Pipeline de análisis de recaudo tributario bajo escenarios de legalización de marihuana',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python -m src.cannabis_tax.cli process
  python -m src.cannabis_tax.cli pipeline
  python -m src.cannabis_tax.cli scenarios --scenarios 5
  python -m src.cannabis_tax.cli viz
        """
    )
    
    # Argumentos globales
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Modo verbose (DEBUG)')
    parser.add_argument('--log-file', type=Path,
                       help='Guardar logs en archivo')
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando: process
    sp_process = subparsers.add_parser('process', help='Procesar datos raw')
    sp_process.set_defaults(func=cmd_process)
    
    # Comando: analyze
    sp_analyze = subparsers.add_parser('analyze', help='Análisis exploratorio')
    sp_analyze.set_defaults(func=cmd_analyze)
    
    # Comando: model
    sp_model = subparsers.add_parser('model', help='Entrenar modelos')
    sp_model.set_defaults(func=cmd_model)
    
    # Comando: scenarios
    sp_scenarios = subparsers.add_parser('scenarios', help='Simular escenarios')
    sp_scenarios.add_argument('--scenarios', '-s', type=int, default=3,
                             help='Número de escenarios a simular (default: 3)')
    sp_scenarios.set_defaults(func=cmd_scenarios)
    
    # Comando: evaluate
    sp_evaluate = subparsers.add_parser('evaluate', help='Evaluar modelos')
    sp_evaluate.set_defaults(func=cmd_evaluate)
    
    # Comando: viz
    sp_viz = subparsers.add_parser('viz', help='Generar visualizaciones')
    sp_viz.set_defaults(func=cmd_viz)
    
    # Comando: pipeline (default)
    sp_pipeline = subparsers.add_parser('pipeline', help='Ejecutar pipeline completo')
    sp_pipeline.set_defaults(func=cmd_pipeline)
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Configurar logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level, log_file=args.log_file)
    
    logger.info(f"Iniciando CLI - Colombia Marijuana Revenue Model")
    logger.info(f"Directorio raíz: {paths.root}")
    
    # Ejecutar comando
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        # Si no hay comando, ejecutar pipeline por defecto
        return cmd_pipeline(args)


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

