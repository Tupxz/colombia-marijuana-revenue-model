#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_process_pib.py
Procesamiento de datos de PIB (Banco de la República)
Entrada: data/raw/PIBBanrepAnual.xlsx y data/raw/PIBBanrep.xlsx
Salida: data/processed/pib_anual.csv y data/processed/pib_trimestral.csv
"""

import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def process_pib_anual():
    """
    Procesa datos de PIB anual del Banco de la República.
    """
    logging.info("Procesando PIB anual...")
    
    try:
        # Leer archivo
        df = pd.read_excel(
            'data/raw/PIBBanrepAnual.xlsx',
            sheet_name='Series de datos'
        )
        
        logging.info(f"Dimensiones iniciales: {df.shape}")
        
        # Limpiar espacios en blanco del header
        df.columns = df.columns.str.strip()
        
        # Guardar datos procesados
        output_path = 'data/processed/pib_anual.csv'
        df.to_csv(output_path, index=False)
        
        logging.info(f"✅ PIB anual guardado en: {output_path}")
        logging.info(f"   Dimensiones finales: {df.shape}")
        
    except Exception as e:
        logging.error(f"Error procesando PIB anual: {str(e)}")


def process_pib_trimestral():
    """
    Procesa datos de PIB trimestral del Banco de la República.
    """
    logging.info("Procesando PIB trimestral...")
    
    try:
        # Leer archivo
        df = pd.read_excel(
            'data/raw/PIBBanrep.xlsx',
            sheet_name='Series de datos'
        )
        
        logging.info(f"Dimensiones iniciales: {df.shape}")
        
        # Limpiar espacios en blanco del header
        df.columns = df.columns.str.strip()
        
        # Guardar datos procesados
        output_path = 'data/processed/pib_trimestral.csv'
        df.to_csv(output_path, index=False)
        
        logging.info(f"✅ PIB trimestral guardado en: {output_path}")
        logging.info(f"   Dimensiones finales: {df.shape}")
        
    except Exception as e:
        logging.error(f"Error procesando PIB trimestral: {str(e)}")


if __name__ == '__main__':
    process_pib_anual()
    process_pib_trimestral()
    logging.info("✅ Procesamiento de PIB completado")
