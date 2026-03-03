# Execution Runs Directory

Este directorio contiene resultados de ejecuciones del pipeline.

## Estructura de Directorios de Runs

Cada ejecución se organiza con timestamp y etiqueta descriptiva:

```
runs/
├── YYYY-MM-DD__HH-MM-SS_<tag>/
│   ├── config_snapshot.yaml
│   ├── logs/
│   │   └── execution.log
│   ├── tables/
│   │   ├── predictions.csv
│   │   ├── metrics.csv
│   │   └── ...
│   └── figures/
│       ├── forecast_plot.png
│       ├── scenario_comparison.png
│       └── ...
└── 2026-03-03__initial/
    ├── config_snapshot.yaml
    ├── logs/
    ├── tables/
    │   └── .gitkeep
    └── figures/
        └── .gitkeep
```

## Convención de Nombres

- **Formato:** `YYYY-MM-DD__HH-MM-SS_<descripcion>`
- **Ejemplo:** `2026-03-03__10-30-45_baseline_scenario`
- **Descripción:** Etiqueta corta (sin espacios, con guiones bajos)

## Contenido de cada Run

### `config_snapshot.yaml`
Copia de los archivos de configuración usados en esa ejecución.
Permite reproducir exactamente qué parámetros generaron ese resultado.

### `logs/execution.log`
Log completo de la ejecución del pipeline.
Útil para debugging y auditoría.

### `tables/`
Archivos CSV/Excel con resultados tabulares:
- Predicciones
- Métricas de evaluación
- Datos procesados intermedios

### `figures/`
Visualizaciones PNG/PDF generadas:
- Gráficos de pronósticos
- Comparaciones de escenarios
- Análisis de sensibilidad

## Cómo Ejecutar una Configuración

```bash
# Pipeline con configuración por defecto
python -m src.cannabis_tax.cli pipeline

# Procesar datos específicamente
python -m src.cannabis_tax.cli process

# Simular escenarios con verbose logging
python -m src.cannabis_tax.cli scenarios --scenarios 5 --verbose
```

## Versioning / Control de Cambios

- Cada run genera automáticamente un identificador único (timestamp)
- No se sobrescriben runs anteriores
- Es posible comparar resultados entre diferentes ejecuciones
- Usa `git` para versionar cambios en configs, no en runs

## Ignorar en Git

Esta carpeta normalmente se ignora en `.gitignore`:

```bash
# En .gitignore
runs/
```

Esto evita que resultados voluminosos (figuras, logs) se agreguen al repositorio.
Sin embargo, sí podría incluirse una run de referencia (ej: `runs/2026-03-03__baseline/`) como benchmark.

## Cleanup

Para limpiar runs antiguos:

```bash
# Eliminar runs de hace más de 30 días (Linux/Mac)
find runs/ -type d -mtime +30 -exec rm -rf {} +
```

---

**Nota:** Los datos en `runs/` se consideran efímeros y pueden ser regenerados ejecutando el pipeline nuevamente.
