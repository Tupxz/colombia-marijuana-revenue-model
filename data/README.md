# Datos

Regla simple para este proyecto:

- `raw/`: datos originales. No se editan.
- `interim/`: pasos intermedios o pruebas.
- `processed/`: datos finales listos para análisis.
- `external/`: fuentes externas adicionales si aparecen después.

## Qué guardar en cada carpeta

- Si descargaste un archivo nuevo, va primero en `raw/`.
- Si transformaste un archivo pero todavía no es el resultado final, va en `interim/`.
- Si el dataset ya quedó limpio y se va a usar en análisis o modelado, va en `processed/`.

## Convención recomendada

- Mantener nombres claros y estables.
- Si un archivo procesado es importante, agregar su metadata en JSON.
- No duplicar el mismo dataset en muchos formatos sin necesidad.

## Fuentes actuales

- DANE
- Banco de la República
- Algunas series auxiliares ya copiadas al proyecto
