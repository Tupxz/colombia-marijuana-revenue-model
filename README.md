# Colombia Marijuana Consumption Model

Propensión al consumo de marihuana en Colombia: benchmark MCO y Probit con datos de la Encuesta Nacional de Consumo de Sustancias Psicoactivas.

## Uso rápido

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make test        # correr pruebas
make validate    # validar target vs raw
make pipeline    # process → validate → consumption
```

## Comandos CLI disponibles

```bash
python3 -m cannabis_tax.cli process      # Limpiar datos raw
python3 -m cannabis_tax.cli validate     # Validar consistencia del target
python3 -m cannabis_tax.cli consumption  # Generar escenarios de consumo
python3 -m cannabis_tax.cli pipeline     # process + validate (estricto) + consumption
python3 -m cannabis_tax.cli cleanup      # Vista previa de artefactos a limpiar
python3 -m cannabis_tax.cli cleanup --apply  # Borrar artefactos seguros
```

## Estructura

```text
src/cannabis_tax/       Código Python
  analysis/             Modelado, EDA, consumo, validación
  cleaning/             Limpieza de datos raw
  core/                 Rutas, config, logging
  cli.py                Punto de entrada CLI
data/
  raw/                  Datos originales (no editar)
  processed/            Datos limpios y bases de trabajo
configs/                Configuración YAML
notebooks/              Exploración y validación interactiva
reports/                Entregables académicos (paper, slides, tablas)
tests/                  Pruebas unitarias
```

## Datos clave

| Archivo | Qué contiene |
|---------|-------------|
| `data/processed/base_consumo_drogas_colombia_limpia.xlsx` | Base limpia de consumo (3982 obs) |
| `data/raw/k_capitulos.csv` | Capítulo K raw para cross-check |
| `data/processed/propensity_model_base.csv` | Base de modelado (regenerable) |
| `reports/paper.tex` | Paper principal |

## Make targets

```bash
make help        # Ver todos los targets
make test        # Pruebas unitarias
make test-cov    # Pruebas con cobertura
make validate    # Validación de target
make pipeline    # Pipeline completo
make clean       # Dry-run de limpieza
make clean-apply # Limpieza real
make lint        # Verificar formato
make format      # Auto-formatear
```

## Estado actual

La primera fase (benchmark econométrico MCO + Probit) está completa.
Ver `AUDIT_REPORT.md` para hallazgos de la auditoría técnica.
