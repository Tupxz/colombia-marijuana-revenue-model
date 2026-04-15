# Auditoría Integral del Repositorio `colombia-marijuana-revenue-model`

**Fecha:** 24 de marzo de 2026  
**Auditor:** Revisión técnica automatizada (Data Scientist + ML Engineer + Data Engineer + Revisor Académico)  
**Commit auditado:** `8f98e12` (HEAD, main)

---

## A) Resumen Ejecutivo

El repositorio presenta una estructura profesional de proyecto de ciencia de datos con código modular, documentación académica en LaTeX, y un pipeline reproducible desde CLI. Las 6 pruebas unitarias pasan correctamente y el pipeline `build_propensity_dataset → run_propensity_specifications → export_propensity_results` se ejecuta de punta a punta sin errores, generando tablas LaTeX consistentes con las cifras reportadas en el paper (3980/755 observaciones, R²=0.091/0.061).

**Sin embargo, se detectó un hallazgo CRÍTICO:** la variable dependiente `consumo_12m` en la base limpia (`base_consumo_drogas_colombia_limpia.xlsx`) **NO corresponde a K_03** como afirma el paper. K_03 en `data/raw/k_capitulos.csv` tiene 1223 "Sí", 2754 "No" y 5 "No contesta", pero `consumo_12m` en la base limpia tiene 1719 valores `1.0` y 2263 `NaN`. Peor aún, 896 personas con `consumo_12m=1` tienen simultáneamente `frecuencia_consumo=2` (K_03=No) y 1140 personas con `consumo_12m=1` tienen `consumo_vida=NaN`. Esto invalida la premisa central del paper.

Además: cobertura de tests al 25%, 5 módulos vacíos (código muerto), configuración YAML desacoplada del código real, datos binarios de 50MB trackeados directamente en git, y el notebook `02_validation_report.ipynb` nunca fue ejecutado.

---

## B) Top 10 Mejoras Priorizadas (Impacto vs Esfuerzo)

| # | Hallazgo | Severidad | Esfuerzo | Impacto |
|---|----------|-----------|----------|---------|
| 1 | **`consumo_12m` no es K_03**: la variable dependiente está mal documentada o mal derivada | CRÍTICO | M | CRÍTICO |
| 2 | `recode_propensity_target` tiene dead code: maneja códigos 2/9 que nunca aparecen en los datos | ALTO | S | Alto |
| 3 | El paper afirma que "No contesta" (código 9) se trata como 0, pero en la base limpia no hay código 9 ni código 2 | ALTO | S | Alto |
| 4 | Cobertura de tests al 25%: `clean.py` (0%), `cli.py` (0%), `eda.py` (16%), `modeling.py` (32%) | ALTO | M | Alto |
| 5 | 5 módulos vacíos: `features/`, `io/`, `models/`, `scenarios/`, `viz/` | MEDIO | S | Medio |
| 6 | Datos binarios (50MB) trackeados en git sin Git LFS | MEDIO | S | Medio |
| 7 | Configuración YAML (`features.yaml`, `scenarios.yaml`) completamente desacoplada del código real | MEDIO | M | Medio |
| 8 | `02_validation_report.ipynb` nunca ejecutado — no cumple su propósito de validación | MEDIO | S | Alto |
| 9 | `paper.tex` tiene tablas con overfull hbox (11 advertencias LaTeX) | BAJO | S | Bajo |
| 10 | `requirements.txt` es un freeze total (113 paquetes) vs `pyproject.toml` (6 dependencias) | BAJO | S | Bajo |

---

## C) Hallazgos Detallados por Categoría

### C.1 CÓDIGO

#### C.1.1 [CRÍTICO] Variable dependiente `consumo_12m` inconsistente con K_03

- **Problema:** El paper y `variables.tex` documentan que `consumo_12m` proviene de `K_03` ("¿Ha consumido marihuana en los últimos 12 meses?", dominio: 1=Sí, 2=No, 9=No contesta). Sin embargo, en la base limpia `consumo_12m` tiene 1719 valores `1.0` y 2263 `NaN`, mientras que `K_03` en `data/raw/k_capitulos.csv` tiene 1223 Sí, 2754 No, y 5 No contesta.
- **Evidencia:**
  ```
  # data/raw/k_capitulos.csv → K_03
  K_03: 1=1223, 2=2754, 9=5

  # data/processed/base_consumo_drogas_colombia_limpia.xlsx → consumo_12m  
  consumo_12m: 1.0=1719, NaN=2263
  
  # frecuencia_consumo en la misma base limpia → coincide con K_03
  frecuencia_consumo: 1=1223, 2=2754, 9=5
  ```
  Cross-tabulación: **896 personas tienen consumo_12m=1 pero frecuencia_consumo=2 (K_03=No)**.  
  Además, **1140 personas con consumo_12m=1 tienen consumo_vida=NaN** (nunca consumieron según K_01_A).
- **Riesgo:** Los 4 modelos estimados están usando una variable dependiente que no es lo que el paper documenta. Los coeficientes, interpretaciones y conclusiones podrían estar fundamentalmente equivocados.
- **Cambio recomendado:** 
  1. Rastrear exactamente cómo se derivó `consumo_12m` en la base limpia (que fue generada externamente).
  2. Si `consumo_12m` debe ser K_03, reconstruir la variable desde `k_capitulos.csv` directamente.
  3. Si `consumo_12m` es una derivación compuesta, documentar la regla exacta.
- **Esfuerzo:** M | **Impacto:** CRÍTICO

#### C.1.2 [ALTO] `recode_propensity_target` tiene dead code y docstring engañoso

- **Problema:** La función documenta que maneja códigos 1/2/9, pero en la base limpia `consumo_12m` solo tiene valores `1.0` y `NaN`. Los branches para `eq(2)` nunca se ejecutan.
- **Evidencia:** `src/cannabis_tax/analysis/modeling.py` líneas 88-99:
  ```python
  def recode_propensity_target(series: pd.Series) -> pd.Series:
      """Current assumption: 1 -> consumes, 2 -> does not, missing -> treated as 0"""
      binary = pd.Series(np.zeros(len(series)), index=series.index, dtype="int64")
      binary = binary.where(~series.eq(1), 1)
      binary = binary.where(~series.eq(2), 0)  # ← nunca se ejecuta en la práctica
      return binary
  ```
- **Riesgo:** Falsa sensación de que se manejan correctamente todos los códigos del cuestionario.
- **Cambio recomendado:** Agregar assertion o logging que verifique qué valores realmente llegan. Actualizar docstring.
- **Esfuerzo:** S | **Impacto:** Alto

#### C.1.3 [ALTO] Falta validación de datos de entrada en `build_propensity_dataset`

- **Problema:** La función confía ciegamente en que la base limpia contiene las columnas esperadas con los dominios esperados. No hay assertions ni validaciones.
- **Evidencia:** `modeling.py` líneas 133-183 — no hay ningún `assert`, `validate`, ni check de dominio.
- **Riesgo:** Errores silenciosos si la base cambia o si se usa una versión diferente.
- **Cambio recomendado:** Agregar validaciones: (1) verificar columnas requeridas existen, (2) verificar dominio de `consumo_12m`, (3) verificar que merge no pierde/duplica filas.
- **Esfuerzo:** S | **Impacto:** Alto

#### C.1.4 [MEDIO] 5 módulos vacíos son código muerto

- **Problema:** `features/`, `io/`, `models/`, `scenarios/`, `viz/` son directorios vacíos sin siquiera un `__init__.py`.
- **Evidencia:** `list_dir` confirma que los 5 directorios están completamente vacíos.
- **Riesgo:** Confusión para nuevos colaboradores; sugiere funcionalidad que no existe.
- **Cambio recomendado:** Eliminarlos o agregar un `__init__.py` con un `# TODO` claro y timeline.
- **Esfuerzo:** S | **Impacto:** Medio

#### C.1.5 [MEDIO] `clean.py` usa logging propio en lugar del centralizado

- **Problema:** `clean.py` configura su propio `logging.basicConfig()` (línea 24) en lugar de usar `core/logging.py`.
- **Evidencia:** `src/cannabis_tax/cleaning/clean.py` línea 24: `logging.basicConfig(level=logging.INFO, ...)`.
- **Riesgo:** Logs duplicados o inconsistentes cuando se ejecuta desde CLI.
- **Cambio recomendado:** Importar y usar `from ..core.logging import logger`.
- **Esfuerzo:** S | **Impacto:** Bajo

#### C.1.6 [MEDIO] `consumption.py` usa rutas relativas hardcodeadas

- **Problema:** Las rutas por defecto son `Path("data/processed/...")` en lugar de usar `paths.data_processed`.
- **Evidencia:** `consumption.py` líneas 10-11:
  ```python
  DEFAULT_INPUT = Path("data/processed/base_consumo_drogas_colombia_limpia.xlsx")
  DEFAULT_OUTPUT = Path("data/processed/consumo_12m_escenarios.csv")
  ```
- **Riesgo:** Falla si se ejecuta desde un directorio diferente al root del proyecto.
- **Cambio recomendado:** Usar `from ..core.paths import paths` como hace `modeling.py`.
- **Esfuerzo:** S | **Impacto:** Medio

#### C.1.7 [BAJO] `_latex_header_note` tiene tildes inconsistentes

- **Problema:** Mezcla de texto con y sin tildes en la misma nota al pie LaTeX.
- **Evidencia:** `modeling.py` línea 348: `"Errores estandar entre parentesis"` (falta `estándar`, `paréntesis`) pero `"categoría"` y `"propensión"` sí llevan tilde.
- **Riesgo:** Apariencia poco profesional en entrega académica.
- **Cambio recomendado:** Corregir tildes faltantes.
- **Esfuerzo:** S | **Impacto:** Bajo

---

### C.2 DATOS

#### C.2.1 [ALTO] Base limpia externa sin trazabilidad de transformaciones

- **Problema:** `base_consumo_drogas_colombia_limpia.xlsx` fue generada externamente (no por `clean.py` ni ningún script del repo). No existe documentación de cómo se derivó `consumo_12m` a partir de las variables raw.
- **Evidencia:** 
  - `clean.py` procesa `personas.csv` y capítulos DANE, pero NO genera la base de consumo limpia.
  - La base tiene 46 columnas derivadas (`consumo_vida`, `consumo_12m`, `riesgo_*`, `actitud_*`, etc.) que no se generan en ningún script del repo.
- **Riesgo:** Imposible reproducir la base desde raw → todo el pipeline depende de un artefacto opaco.
- **Cambio recomendado:** Documentar el proceso externo O crear un script que regenere la base desde raw.
- **Esfuerzo:** L | **Impacto:** Alto

#### C.2.2 [MEDIO] Datos binarios (50MB) trackeados en git sin LFS

- **Problema:** Archivos `.xlsx`, `.dta`, `.sav` trackeados directamente en el repositorio git.
- **Evidencia:** `git ls-files data/` muestra 31 archivos incluyendo `.xlsx`, `.csv` grandes. Total: ~50MB entre `data/raw/` (23MB) y `data/processed/` (27MB).
- **Riesgo:** Repositorio pesado, historial inflado, clonado lento.
- **Cambio recomendado:** Migrar a Git LFS para binarios o documentar instrucciones de descarga externa.
- **Esfuerzo:** S | **Impacto:** Medio

#### C.2.3 [MEDIO] `propensity_model_base.csv` es un artefacto regenerable trackeado en git

- **Problema:** Este archivo se genera automáticamente por `build_propensity_dataset()` pero está commiteado. Puede quedar desincronizado.
- **Evidencia:** `git ls-files data/processed/propensity_model_base.csv` — está trackeado. Se genera en `modeling.py` línea 177.
- **Riesgo:** Versiones distintas entre el archivo commiteado y lo que genera el código.
- **Cambio recomendado:** Agregar a `.gitignore` y documentar que se regenera con `build_propensity_dataset()`.
- **Esfuerzo:** S | **Impacto:** Medio

#### C.2.4 [BAJO] Archivos auxiliares LaTeX en `data/processed/`

- **Problema:** `variables.aux`, `variables.fdb_latexmk`, `variables.fls`, `variables.log`, `variables.synctex.gz` son artefactos de compilación LaTeX que no pertenecen en `data/processed/`.
- **Evidencia:** Listado de directorio `data/processed/`.
- **Cambio recomendado:** Agregar a `.gitignore` y eliminar.
- **Esfuerzo:** S | **Impacto:** Bajo

---

### C.3 NOTEBOOKS

#### C.3.1 [MEDIO] `02_validation_report.ipynb` nunca fue ejecutado

- **Problema:** El notebook de validación fue creado con 19 celdas bien estructuradas para verificar coherencia de cifras, pero **ninguna celda tiene output**. Su propósito literal es validar los datos y nunca se usó.
- **Evidencia:** `copilot_getNotebookSummary` confirma: "None of the cells have been executed" y ninguna celda tiene outputs.
- **Riesgo:** La validación que el notebook debería proveer no existe. Irónicamente, si se hubiera ejecutado, habría detectado la discrepancia de C.1.1.
- **Cambio recomendado:** Ejecutarlo como parte del pipeline de validación.
- **Esfuerzo:** S | **Impacto:** Alto

#### C.3.2 [BAJO] `01_eda_y_mco_propension.ipynb` tiene outputs guardados pero kernel no conectado

- **Problema:** Las 17 celdas tienen outputs de una ejecución anterior (preserved on disk), pero el kernel actual no está conectado. Los outputs pueden estar desincronizados con el código actual.
- **Evidencia:** `copilot_getNotebookSummary`: "None of the cells have been executed" pero "Cell has outputs with mime types".
- **Riesgo:** Los outputs visibles pueden no reflejar el estado actual del código.
- **Cambio recomendado:** Re-ejecutar el notebook de punta a punta antes de cada entrega.
- **Esfuerzo:** S | **Impacto:** Bajo

---

### C.4 REPORTES

#### C.4.1 [CRÍTICO] Paper documenta K_03 como variable dependiente, pero los datos usan otra cosa

- **Problema:** Todo el paper (secciones 3.2, 3.4, ecuaciones MCO y Probit, discusión de "No contesta"=9) asume que la variable dependiente es `K_03`. Pero como se demostró en C.1.1, `consumo_12m` en la base limpia NO es K_03.
- **Evidencia:** `paper.tex` líneas 128-142 (Tabla Variables), línea 160-172 (discusión de recodificación), ecuaciones en secciones 4.1-4.2.
- **Riesgo:** El paper describe una metodología diferente a la que realmente se ejecuta. Esto es un problema de integridad académica.
- **Cambio recomendado:** Resolver primero C.1.1, luego actualizar el paper para reflejar la realidad.
- **Esfuerzo:** M | **Impacto:** CRÍTICO

#### C.4.2 [ALTO] Paper reporta "603 consumidores y 220 no consumidores con precio" pero datos limpios muestran 559/197

- **Problema:** El paper (sección 3.3) dice "los 823 registros se distribuyen entre 603 personas que reportan consumo y 220 que no". Esto es correcto para la base ANTES de limpiar precios. Pero después de `clean_positive_numeric` (que elimina código 98 en 67 casos), la distribución real es 559/197.
- **Evidencia:**
  ```
  Base original: 603 consumidores + 220 no consumidores = 823
  Post clean_positive_numeric: 559 consumidores + 197 no consumidores = 756
  ```
- **Riesgo:** Las cifras 603/220 corresponden a datos sucios que incluyen el código 98 como precio válido.
- **Cambio recomendado:** Clarificar en el paper que 603/220 son ANTES de depuración, o corregir a 559/197.
- **Esfuerzo:** S | **Impacto:** Alto

#### C.4.3 [MEDIO] `resultados_propension.tex` es un documento paralelo que puede desincronizarse

- **Problema:** Existe tanto `paper.tex` como `resultados_propension.tex` con contenido solapado. Ambos incluyen las mismas tablas y la misma narrativa pero con redacción ligeramente diferente.
- **Evidencia:** Ambos archivos incluyen `\input{tables/propension_fit_summary.tex}` y `\input{tables/propension_benchmark_table.tex}` con secciones equivalentes.
- **Riesgo:** Actualizar uno sin el otro crea inconsistencia.
- **Cambio recomendado:** Consolidar en un solo documento o convertir `resultados_propension.tex` en un archivo incluido por `paper.tex`.
- **Esfuerzo:** S | **Impacto:** Medio

#### C.4.4 [BAJO] 11 advertencias de overfull hbox en `paper.tex`

- **Problema:** Nombres de archivo en `\texttt{}` desbordan columnas de tablas. Afecta presentación profesional.
- **Evidencia:** `pdflatex -interaction=nonstopmode paper.tex` reporta 11 Overfull hbox warnings.
- **Cambio recomendado:** Usar `tabularx` con columnas flexibles (parcialmente aplicado pero incompleto).
- **Esfuerzo:** S | **Impacto:** Bajo

---

### C.5 CONFIGURACIÓN / DEVOPS / REPRODUCIBILIDAD

#### C.5.1 [MEDIO] Configuración YAML completamente desacoplada del código

- **Problema:** `configs/features.yaml` define variables macroeconómicas (PIB, IPC, TRM), fiscales y features engineered que **no se usan en ningún lugar del código**. `configs/scenarios.yaml` define escenarios con parámetros (volumen en toneladas, elasticidad, tasa impositiva) que **no se usan en `consumption.py`**. `configs/base.yaml` define parámetros de modelado (`test_size: 0.2`, `cv_folds: 5`, `random_state: 42`) que **no se usan en `modeling.py`**.
- **Evidencia:**
  - `features.yaml` líneas 8-68: define `pib`, `ipc`, `trm`, `tax_collection` — ninguno aparece en el código.
  - `scenarios.yaml` líneas 16-55: define `annual_volume_tons`, `unit_price_pesos`, `elasticity_demand` — `consumption.py` usa `scenario_changes` hardcodeados.
  - `base.yaml` línea 37: `random_state: 42` — `modeling.py` no usa random state ni config.
  - `core/config.py` carga `base.yaml`, pero nadie importa `config` excepto el propio módulo.
- **Riesgo:** Da la impresión de que la configuración controla el pipeline, pero en realidad es decorativa. Fuente de confusión.
- **Cambio recomendado:** Eliminar configs no usados o integrarlos al código. Si se mantienen como roadmap, documentarlo explícitamente.
- **Esfuerzo:** M | **Impacto:** Medio

#### C.5.2 [MEDIO] `requirements.txt` es un freeze total, no un archivo de dependencias mínimas

- **Problema:** 113 paquetes con versiones pinneadas exactas, incluyendo dependencias transitivas (e.g., `wcwidth==0.6.0`, `tinycss2==1.4.0`). Duplica información con `pyproject.toml` que tiene 6 dependencias abstractas.
- **Evidencia:** `requirements.txt` tiene 113 líneas vs `pyproject.toml` [dependencies] tiene 6 entradas.
- **Riesgo:** Confusión sobre cuál es la fuente de verdad. El freeze puede causar conflictos en otros entornos.
- **Cambio recomendado:** Renombrar a `requirements.lock` o generarlo con `pip freeze > requirements.lock` y documentar que `pyproject.toml` es la fuente de verdad.
- **Esfuerzo:** S | **Impacto:** Bajo

#### C.5.3 [BAJO] CLI `pipeline` y `question` hacen lo mismo

- **Problema:** `cmd_pipeline` simplemente llama `cmd_question`. Son alias sin diferenciación.
- **Evidencia:** `cli.py` líneas 54-56: `def cmd_pipeline(args): return cmd_question(args)`.
- **Riesgo:** Menor, pero puede confundir.
- **Cambio recomendado:** Documentar que son alias o eliminar uno.
- **Esfuerzo:** S | **Impacto:** Bajo

#### C.5.4 [BAJO] `pyproject.toml` description no refleja el alcance actual

- **Problema:** La descripción dice "Predicción de recaudo tributario bajo escenarios de legalización" pero el proyecto actual es un benchmark de propensión al consumo.
- **Evidencia:** `pyproject.toml` línea 8: `description = "Predicción de recaudo tributario bajo escenarios de legalización de marihuana en Colombia"`.
- **Riesgo:** Expectativas incorrectas para quien clone el repo.
- **Cambio recomendado:** Actualizar a algo como "Análisis de propensión al consumo de marihuana en Colombia con modelos de benchmark".
- **Esfuerzo:** S | **Impacto:** Bajo

#### C.5.5 [BAJO] Keywords en `pyproject.toml` incluyen "time-series" y "forecasting" — no aplica

- **Problema:** El proyecto no hace series de tiempo ni forecasting.
- **Evidencia:** `pyproject.toml` líneas 19-21: `"forecasting"`, `"time-series"`.
- **Cambio recomendado:** Reemplazar por keywords relevantes.
- **Esfuerzo:** S | **Impacto:** Bajo

---

## D) Plan de Acción en Fases

### Fase 1: Quick Wins (< 2 horas)

1. **Ejecutar `02_validation_report.ipynb`** para tener un registro concreto de validación. [C.3.1]
2. **Eliminar módulos vacíos** (`features/`, `io/`, `models/`, `scenarios/`, `viz/`). [C.1.4]
3. **Corregir tildes** en `_latex_header_note` de `modeling.py`. [C.1.7]
4. **Limpiar artefactos LaTeX** en `data/processed/` (`.aux`, `.log`, `.fls`, etc.). [C.2.4]
5. **Renombrar** `requirements.txt` → `requirements.lock` y documentar. [C.5.2]
6. **Actualizar** description y keywords en `pyproject.toml`. [C.5.4, C.5.5]
7. **Agregar** `propensity_model_base.csv` a `.gitignore`. [C.2.3]

### Fase 2: Corto Plazo (1-3 días)

8. **RESOLVER C.1.1** — Rastrear la derivación real de `consumo_12m`:
   - Opción A: Si la base limpia usó una regla compuesta, documentarla y actualizar el paper.
   - Opción B: Si hay un error, reconstruir `consumo_12m` desde `K_03` en raw y re-estimar modelos.
9. **Agregar validaciones** en `build_propensity_dataset`: assertions de dominio, counts esperados, merge checks. [C.1.3]
10. **Actualizar docstring** de `recode_propensity_target` reflejando que los datos solo tienen 1/NaN. [C.1.2]
11. **Corregir** cifras 603/220 en paper.tex (aclarar que son pre-limpieza) o usar 559/197. [C.4.2]
12. **Migrar** `consumption.py` a usar `paths.data_processed` en lugar de rutas relativas. [C.1.6]
13. **Migrar** `clean.py` al logging centralizado. [C.1.5]

### Fase 3: Mediano Plazo (1-2 semanas)

14. **Aumentar cobertura de tests** al ≥60%:
    - Tests para `clean.py`: verificar normalización de columnas, limpieza de duplicados.
    - Tests para `cli.py`: verificar que cada subcomando invoca la función correcta.
    - Tests de integración: `build_propensity_dataset` con datos mock.
    - Tests para `export_propensity_results`: verificar que genera archivos LaTeX válidos.
15. **Consolidar o eliminar** `resultados_propension.tex`. [C.4.3]
16. **Resolver configs** desacoplados: eliminar YAMLs no usados o integrarlos al código. [C.5.1]
17. **Crear script de reproducibilidad**: `make all` o similar que regenere todo desde raw. [C.2.1]
18. **Migrar a Git LFS** para archivos binarios de datos. [C.2.2]

---

## E) Cambios Concretos que Haría Primero (Lista Accionable)

En orden estricto de prioridad:

1. **Investigar `consumo_12m`**: ejecutar cross-tabs exhaustivos contra raw para determinar la regla de derivación exacta. Si es un error, PARAR todo y corregir antes de cualquier otra acción.
2. Si no es error: **documentar la regla de derivación** en el paper y en un docstring dentro del código.
3. **Agregar assertion** en `build_propensity_dataset`:
   ```python
   assert set(df["consumo_12m"].dropna().unique()) <= {1.0}, \
       f"consumo_12m tiene valores inesperados: {df['consumo_12m'].dropna().unique()}"
   ```
4. **Ejecutar `02_validation_report.ipynb`** de punta a punta.
5. **Eliminar los 5 módulos vacíos**.
6. **Corregir cifras 603/220** en `paper.tex` sección 3.3.

---

## F) Riesgos Residuales y Preguntas Abiertas

### Riesgos Residuales

1. **Integridad de la variable dependiente.** Hasta que no se resuelva C.1.1, TODOS los resultados del paper son cuestionables. No se puede distinguir si la base limpia fue generada con una regla compuesta válida (e.g., incluye otros tipos de consumo reciente) o si hay un bug en la limpieza externa.

2. **Trazabilidad incompleta.** La base limpia es un artefacto opaco. Si la persona que la generó no recuerda o no documentó las reglas, puede ser necesario reconstruirla desde zero.

3. **Sesgo de selección por precio.** El paper documenta correctamente que la muestra con precio es altamente seleccionada, pero no se explora formalmente (e.g., test de Heckman, comparación de medias observables entre muestra completa y submuestra con precio).

### Preguntas Abiertas

1. ¿Quién generó `base_consumo_drogas_colombia_limpia.xlsx` y con qué regla se derivó `consumo_12m`?
2. ¿Por qué `consumo_12m=1` para 896 personas con `frecuencia_consumo=2` (K_03="No ha consumido en 12 meses")?
3. ¿Por qué `consumo_12m=1` para 1140 personas con `consumo_vida=NaN` (K_01_A no indica consumo alguna vez)?
4. ¿Los YAMLs en `configs/` representan un roadmap futuro o son vestigios de una versión anterior del proyecto?
5. ¿Se planea usar la encuesta completa (K_01_A=2610 alguna vez, K_02 para temporalidad) o solo el módulo K_03?

---

## Anexo: Resultados de Ejecución

### Pruebas Unitarias
```
6 passed in 1.24s
Cobertura total: 25% (484 statements, 352 missed)
```

### Pipeline de Reproducibilidad
```
Dataset: 3982 × 61 (0.99s)
4 modelos estimados (2.28s)
Cifras verificadas: N=3980/755, R²=0.091/0.061, coef_log_precio=0.044
CLI consumption: return code 0
```

### Compilación LaTeX
```
paper.tex: compila con 11 Overfull hbox warnings
```
