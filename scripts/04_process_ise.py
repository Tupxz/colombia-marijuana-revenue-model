#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_process_ise.py
Procesamiento de datos de ISE (Indicador de Seguimiento Económico)
Entrada: data/raw/anex-ISE-9actividades-nov2025.xlsx
Salida: data/processed/ise_actividades.csv
"""

import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def process_ise():
    """
    Procesa datos de ISE por actividades económicas del DANE.
    """
    logging.info("Procesando ISE...")
    
    try:
        # Intentar leer la primera hoja con datos
        for sheet_name in ['Cuadro 1', 'Cuadro 2', 'Cuadro 3']:
            try:
                df = pd.read_excel(
                    'data/raw/anex-ISE-9actividades-nov2025.xlsx',
                    sheet_name=sheet_name
                )
                
                if len(df) > 0:
                    logging.info(f"Procesando hoja: {sheet_name}")
                    logging.info(f"   Dimensiones: {df.shape}")
                    
                    # Limpiar espacios en blanco del header
                    df.columns = df.columns.str.strip()
                    
                    # Eliminar filas completamente vacías
                    df = df.dropna(how='all')
                    
                    # Guardar datos procesados
                    output_path = f'data/processed/ise_{sheet_name.lower().replace(" ", "_")}.csv'
                    df.to_csv(output_path, index=False)
                    
                    logging.info(f"✅ {sheet_name} guardado en: {output_path}")
                    
            except Exception as e:
                logging.debug(f"Hoja {sheet_name} vacía o no procesable: {str(e)}")
        
    except Exception as e:
        logging.error(f"Error procesando ISE: {str(e)}")


if __name__ == '__main__':
    process_ise()
    logging.info("✅ Procesamiento de ISE completado")
