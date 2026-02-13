#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_process_ipc.py
Procesamiento de datos de IPC (Índice de Precios al Consumidor)
Entrada: data/raw/anex-IPC-Variacion-ene2026.xlsx
Salida: data/processed/ipc_variacion.csv
"""

import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def process_ipc():
    """
    Procesa datos de IPC del DANE.
    """
    logging.info("Procesando IPC...")
    
    try:
        # Leer archivo
        df = pd.read_excel(
            'data/raw/anex-IPC-Variacion-ene2026.xlsx',
            sheet_name='VarNal'
        )
        
        logging.info(f"Dimensiones iniciales: {df.shape}")
        
        # Limpiar espacios en blanco del header
        df.columns = df.columns.str.strip()
        
        # Eliminar filas completamente vacías
        df = df.dropna(how='all')
        
        # Guardar datos procesados
        output_path = 'data/processed/ipc_variacion.csv'
        df.to_csv(output_path, index=False)
        
        logging.info(f"✅ IPC guardado en: {output_path}")
        logging.info(f"   Dimensiones finales: {df.shape}")
        logging.info(f"   Período: Enero 2026")
        
    except Exception as e:
        logging.error(f"Error procesando IPC: {str(e)}")


if __name__ == '__main__':
    process_ipc()
    logging.info("✅ Procesamiento de IPC completado")
