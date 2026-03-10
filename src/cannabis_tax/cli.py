#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI simplificada para el proyecto actual."""

import logging
import sys
from pathlib import Path
import argparse

from .core.logging import setup_logging, logger
from .core.paths import paths


def cmd_process(args):
    """Procesar y limpiar los datos disponibles."""
    from .cleaning.clean import process_capitulos_dane, process_personas

    try:
        process_capitulos_dane(paths.data_raw, paths.data_processed)
        process_personas(paths.data_raw / "personas.csv", paths.data_processed)
        logger.info("Procesamiento completado")
        return 0
    except Exception as exc:
        logger.error("Error durante procesamiento: %s", exc)
        return 1


def cmd_consumption(args):
    """Construir escenarios simples sobre consumidores en los últimos 12 meses."""
    from .analysis.consumption import build_consumption_scenarios

    try:
        table = build_consumption_scenarios()
        logger.info("Escenarios guardados en: %s", paths.data_processed / "consumo_12m_escenarios.csv")
        logger.info("\n%s", table.to_string(index=False))
        return 0
    except Exception as exc:
        logger.error("Error construyendo escenarios de consumo: %s", exc)
        return 1


def cmd_question(args):
    """Ejecutar el flujo mínimo para responder la pregunta actual."""
    process_code = cmd_process(args)
    if process_code != 0:
        return process_code
    return cmd_consumption(args)


def cmd_pipeline(args):
    """Alias del flujo mínimo del proyecto."""
    return cmd_question(args)


def main():
    """Punto de entrada principal de la CLI."""
    parser = argparse.ArgumentParser(
        prog="cannabis_tax",
        description="Proyecto simplificado para analizar consumo de marihuana en Colombia",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo verbose")
    parser.add_argument("--log-file", type=Path, help="Guardar logs en archivo")

    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    sp_process = subparsers.add_parser("process", help="Limpiar y preparar datos")
    sp_process.set_defaults(func=cmd_process)

    sp_consumption = subparsers.add_parser(
        "consumption",
        help="Construir escenarios simples de consumidores en últimos 12 meses",
    )
    sp_consumption.set_defaults(func=cmd_consumption)

    sp_question = subparsers.add_parser(
        "question",
        help="Ejecutar el flujo mínimo para la pregunta principal",
    )
    sp_question.set_defaults(func=cmd_question)

    sp_pipeline = subparsers.add_parser("pipeline", help="Alias de question")
    sp_pipeline.set_defaults(func=cmd_pipeline)

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level, log_file=args.log_file)

    logger.info("Iniciando CLI")
    logger.info("Directorio raíz: %s", paths.root)

    if hasattr(args, "func"):
        return args.func(args)
    return cmd_question(args)


if __name__ == '__main__':
    sys.exit(main())
