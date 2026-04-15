#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI simplificada para el proyecto actual."""

import logging
import sys
from pathlib import Path
import argparse

from .core.logging import setup_logging, logger
from .core.paths import paths


def _run_target_validation(
    base_path: Path,
    raw_k_path: Path,
    report_file: Path | None,
    strict: bool,
) -> int:
    from .analysis.validation import run_target_validation

    try:
        passed, report = run_target_validation(base_path=base_path, raw_k_path=raw_k_path)
        if report_file is not None:
            report_file.parent.mkdir(parents=True, exist_ok=True)
            report.to_csv(report_file, index=False)
            logger.info("Reporte de validacion guardado en: %s", report_file)

        status = "OK" if passed else "FALLAS"
        logger.info("Resultado validacion target: %s", status)
        if not report.empty:
            logger.info("\n%s", report.to_string(index=False))

        if strict and not passed:
            return 1
        return 0
    except Exception as exc:
        logger.error("Error ejecutando validacion de target: %s", exc)
        return 1


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
    """Ejecutar proceso + validación estricta + escenarios de consumo."""
    process_code = cmd_process(args)
    if process_code != 0:
        return process_code

    validate_code = _run_target_validation(
        base_path=paths.data_processed / "base_consumo_drogas_colombia_limpia.xlsx",
        raw_k_path=paths.data_raw / "k_capitulos.csv",
        report_file=paths.runs / "pipeline_validation_report.csv",
        strict=True,
    )
    if validate_code != 0:
        logger.error("Pipeline detenido por inconsistencias en validacion de target.")
        return validate_code

    return cmd_consumption(args)


def cmd_validate(args):
    """Validar consistencia del target contra la base raw."""
    base_path = args.base_path
    raw_k_path = args.raw_k_path
    report_file = args.report_file
    strict = args.strict

    return _run_target_validation(
        base_path=base_path,
        raw_k_path=raw_k_path,
        report_file=report_file,
        strict=strict,
    )


def cmd_cleanup(args):
    """Limpiar artefactos generados de forma segura (dry-run por defecto)."""
    from .analysis.validation import cleanup_artifacts

    try:
        result = cleanup_artifacts(root=paths.root, apply=args.apply)
        logger.info("Artefactos detectados: %d", len(result["candidates"]))
        logger.info("Artefactos seguros para borrar: %d", len(result["safe_to_delete"]))
        if result["skipped_tracked"]:
            logger.info("Omitidos por estar trackeados en git: %d", len(result["skipped_tracked"]))

        preview = result["safe_to_delete"][:20]
        if preview:
            logger.info("Vista previa de artefactos:")
            for relative in preview:
                logger.info("  - %s", relative)

        if args.apply:
            logger.info("Artefactos eliminados: %d", len(result["removed"]))
        else:
            logger.info("Dry-run activo. Usa `cleanup --apply` para borrar.")
        return 0
    except Exception as exc:
        logger.error("Error durante cleanup de artefactos: %s", exc)
        return 1


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

    sp_pipeline = subparsers.add_parser(
        "pipeline",
        help="Ejecutar process + validate (estricto) + consumption",
    )
    sp_pipeline.set_defaults(func=cmd_pipeline)

    sp_validate = subparsers.add_parser(
        "validate",
        help="Validar consistencia del target y generar reporte",
    )
    sp_validate.add_argument(
        "--base-path",
        type=Path,
        default=paths.data_processed / "base_consumo_drogas_colombia_limpia.xlsx",
        help="Ruta de la base procesada para validación",
    )
    sp_validate.add_argument(
        "--raw-k-path",
        type=Path,
        default=paths.data_raw / "k_capitulos.csv",
        help="Ruta del capítulo K raw para cross-check",
    )
    sp_validate.add_argument(
        "--report-file",
        type=Path,
        default=paths.runs / "validation_report.csv",
        help="Ruta donde guardar reporte CSV de validación",
    )
    sp_validate.add_argument(
        "--no-strict",
        action="store_false",
        dest="strict",
        help="No fallar con código de error si hay inconsistencias",
    )
    sp_validate.set_defaults(func=cmd_validate, strict=True)

    sp_cleanup = subparsers.add_parser(
        "cleanup",
        help="Limpiar artefactos generados (seguro, dry-run por defecto)",
    )
    sp_cleanup.add_argument(
        "--apply",
        action="store_true",
        help="Aplicar borrado de artefactos seguros",
    )
    sp_cleanup.set_defaults(func=cmd_cleanup)

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
