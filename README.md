# Colombia Marijuana Consumption Model

Proyecto de Ciencia de Datos para responder una pregunta más simple: cómo podría cambiar la cantidad de consumidores de marihuana en Colombia si se legaliza su distribución.

## Qué hay en este repo

- `src/cannabis_tax/`: código principal.
- `data/raw/`: datos originales.
- `data/processed/`: datos limpios o transformados.
- `reports/`: entregables académicos.
- `runs/`: salidas generadas al ejecutar el pipeline.

## Flujo básico

1. Limpiar y preparar datos.
2. Tomar la base de consumo.
3. Estimar consumidores en últimos 12 meses.
4. Simular escenarios simples de cambio tras legalización.

## Uso rápido

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python3 -m cannabis_tax.cli question
```

Comandos disponibles:

```bash
python3 -m cannabis_tax.cli process
python3 -m cannabis_tax.cli consumption
python3 -m cannabis_tax.cli question
python3 -m cannabis_tax.cli pipeline
```

## Estructura simple

```text
data/                Datos
notebooks/           Exploración
reports/             Entregables
runs/                Resultados de ejecución
src/cannabis_tax/    Código Python
tests/               Pruebas
```

## Reglas prácticas

- No editar archivos dentro de `data/raw/`.
- Guardar salidas finales en `data/processed/`.
- Usar `runs/` para resultados temporales o ejecuciones completas.
- Mantener la lógica del proyecto dentro de `src/cannabis_tax/`.
- Para la pregunta actual, el archivo clave es `data/processed/base_consumo_drogas_colombia_limpia.xlsx`.

## Documentos que sí importan

- Este `README.md` para entender el proyecto.
- `data/README.md` para saber qué guardar en cada carpeta de datos.
- `runs/README.md` para entender qué va en las ejecuciones.
- `reports/paper.tex` y `reports/slides/` para la entrega académica.

## Estado actual

La estructura fue reducida para enfocarse en consumo y escenarios simples. El resultado principal de la CLI queda en `data/processed/consumo_12m_escenarios.csv`.
