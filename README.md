# Colombia Marijuana Revenue Tax Forecasting Model

**Predicción del Recaudo Tributario bajo Escenarios de Legalización de Marihuana en Colombia**

---

## 📋 Overview

Este proyecto analiza la estructura del **recaudo tributario del Estado colombiano** bajo distintos escenarios de **legalización de la marihuana**. Utilizando **Python**, desarrollamos un pipeline reproducible para:

1. **Limpiar y transformar** datos de múltiples fuentes (DANE, Banco de la República, DIAN)
2. **Analizar exploratorio** de series temporales fiscales y macroeconómicas
3. **Construir modelos** predictivos de ingresos tributarios
4. **Simular escenarios** de legalización con diferentes parámetros
5. **Evaluar sensibilidad** de proyecciones a variaciones en supuestos clave

**Curso:** Ciencia de Datos – 5° semestre  
**Universidad:** EAFIT  
**Semestre:** 2026-I  
**Profesor:** Paula María Almonacid Hurtado

---

## 🎯 Pregunta de Investigación

> ¿Cómo podría predecirse la estructura del recaudo tributario del Estado colombiano bajo distintos escenarios de legalización de la distribución de la marihuana?

---

## 📁 Estructura del Proyecto

```
.
├── configs/                    # Archivos de configuración YAML
│   ├── base.yaml              # Config general del proyecto
│   ├── scenarios.yaml         # Definición de escenarios
│   └── features.yaml          # Especificación de variables
│
├── data/                       # Datos (raw → interim → processed)
│   ├── raw/                   # Datos originales sin modificar
│   ├── interim/               # Datos intermedios en transformación
│   ├── processed/             # Datos finales limpios
│   ├── external/              # Datos de fuentes externas (APIs, etc.)
│   └── README.md              # Diccionario y política de datos
│
├── src/cannabis_tax/          # Código fuente (paquete Python)
│   ├── __init__.py
│   ├── cli.py                 # Interfaz de línea de comandos (CLI)
│   ├── core/                  # Módulos centrales
│   │   ├── config.py          # Gestor de configuración
│   │   ├── paths.py           # Gestor de rutas
│   │   └── logging.py         # Logging centralizado
│   ├── io/                    # Input/Output: ingestión de datos
│   │   ├── ingest_sources.py  # Cargar datos de fuentes
│   │   └── trends.py          # Procesamiento de series temporales
│   ├── cleaning/              # Limpieza de datos
│   │   └── clean.py           # Script principal de limpieza
│   ├── features/              # Feature engineering
│   │   ├── build_features.py  # Crear variables derivadas
│   │   └── diagnostics.py     # Análisis de calidad de datos
│   ├── models/                # Modelos predictivos
│   │   ├── benchmark.py       # Modelos baseline
│   │   ├── ml.py              # Modelos ML (regresión, ARIMA, etc.)
│   │   └── evaluate.py        # Evaluación y métricas
│   ├── scenarios/             # Simulación de escenarios
│   │   ├── simulate.py        # Simulación de escenarios
│   │   └── sensitivity.py     # Análisis de sensibilidad
│   └── viz/                   # Visualización
│       └── plots.py           # Funciones de graficación
│
├── reports/                    # Reportes y documentación
│   ├── paper.tex              # Paper académico
│   ├── paper.pdf              # PDF compilado
│   ├── references.bib         # Referencias bibliográficas
│   ├── figures/               # Figuras para documentos
│   └── slides/                # Presentación en Beamer
│
├── notebooks/                  # Notebooks Jupyter (exploración)
│   ├── 01_eda_tax_revenue.ipynb
│   ├── 02_scenario_analysis.ipynb
│   └── README.md
│
├── runs/                       # Resultados de ejecuciones
│   ├── 2026-03-03__initial/   # Run de referencia
│   └── README.md              # Convención de ejecuciones
│
├── tests/                      # Tests automatizados (pytest)
│   ├── unit/
│   └── integration/
│
├── README.md                   # Este archivo
├── requirements.txt            # Dependencias Python
├── LICENSE                     # Licencia del proyecto
└── .gitignore                  # Archivos ignorados por Git
```

---

## 🚀 Quick Start

### 1. Clonar y configurar entorno

```bash
git clone https://github.com/Tupxz/colombia-marijuana-revenue-model.git
cd colombia-marijuana-revenue-model

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar pipeline

```bash
# Ejecutar pipeline completo (default)
python -m src.cannabis_tax.cli

# O específicamente: procesar datos
python -m src.cannabis_tax.cli process

# Simular escenarios
python -m src.cannabis_tax.cli scenarios --scenarios 5

# Ver ayuda
python -m src.cannabis_tax.cli --help
```

### 3. Comandos disponibles

| Comando | Descripción |
|---------|------------|
| `python -m src.cannabis_tax.cli pipeline` | Ejecutar pipeline completo |
| `python -m src.cannabis_tax.cli process` | Procesar datos raw → processed |
| `python -m src.cannabis_tax.cli analyze` | Análisis exploratorio |
| `python -m src.cannabis_tax.cli model` | Entrenar modelos |
| `python -m src.cannabis_tax.cli scenarios -s 5` | Simular 5 escenarios |
| `python -m src.cannabis_tax.cli evaluate` | Evaluar modelos |
| `python -m src.cannabis_tax.cli viz` | Generar visualizaciones |

---

## 📊 Datos

### Fuentes Principales

| Fuente | Tipo | Frecuencia | Archivos |
|--------|------|-----------|----------|
| **DANE** | Encuestas, Capítulos Fiscales | Anual | `d_capitulos.csv`, `personas.csv`, etc. |
| **Banco de la República** | Series Macroeconómicas | Anual/Trimestral | `PIBBanrep.xlsx`, `TRM_limpia_copia.csv` |
| **IPC** | Índice de Precios | Mensual | `IPC_limpio_copia.xlsx` |

### Estructura de Carpetas de Datos

- **`data/raw/`**: Datos originales sin modificar (NUNCA editar aquí)
- **`data/interim/`**: Transformaciones intermedias
- **`data/processed/`**: Datasets finales limpios + metadatos JSON
- **`data/external/`**: Datos de APIs o fuentes externas (reservado)

**Ver [`data/README.md`](data/README.md) para detalles completos.**

---

## 🔧 Configuración

### Archivos de Configuración

Los parámetros del proyecto se definen en YAML:

- **`configs/base.yaml`**: Configuración general (rutas, logging, etc.)
- **`configs/scenarios.yaml`**: Escenarios de legalización (parámetros de simulación)
- **`configs/features.yaml`**: Definición de variables y features

### Ejemplo: Crear un nuevo escenario

Editar `configs/scenarios.yaml`:

```yaml
scenarios:
  custom_scenario:
    name: "Mi Escenario Personalizado"
    parameters:
      annual_volume_tons: 600
      unit_price_pesos: 11000
      tax_rate: 0.22
```

Luego: `python -m src.cannabis_tax.cli scenarios`

---

## 📈 Metodología

### Pipeline de Análisis

```
raw data → clean & transform → EDA → feature engineering
    ↓
features → model selection → train/validate → evaluation
    ↓
scenarios → sensitivity analysis → visualization
    ↓
reports & papers
```

### Modelos Utilizados

- **Benchmarks:** Naive Forecast, Seasonal Naive
- **Regresión:** Linear Regression, Ridge, Lasso
- **Series Temporales:** ARIMA (por implementar)
- **Avanzados:** Random Forest, XGBoost (por implementar)

### Validación

- Validación cruzada (k-fold, default k=5)
- Métricas: MAE, RMSE, MAPE, R²
- Backtesting en datos históricos

---

## 📚 Variables Principales

### Fiscales
- **Recaudo tributario total** (COP)
- **Capítulos de impuestos:** Directos (D), Indirectos (G), Contribuciones (K)
- **Impuestos específicos por fuente**

### Macroeconómicas
- **PIB** (anual y trimestral, COP)
- **IPC** (Índice de Precios al Consumidor, base 2018)
- **TRM** (Tasa Representativa del Mercado, USD/COP)
- **Población**

### De Legalización
- **Volumen legal anual** (toneladas)
- **Precio unitario** (COP/tonelada)
- **Tasa tributaria efectiva** (%)
- **Elasticidad de demanda**

**Ver [`configs/features.yaml`](configs/features.yaml) para especificación completa.**

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=html

# Tests específicos
pytest tests/unit/test_models.py -v
```

---

## 📝 Resultados y Entregables

### Ejecuciones (`runs/`)
Cada ejecución del pipeline genera:
- Snapshot de configuración usado
- Logs de ejecución
- Tablas de resultados (CSV)
- Figuras de visualización (PNG/PDF)

Ver [`runs/README.md`](runs/README.md) para convención de nombres.

### Documentación (`reports/`)
- **Paper académico:** `reports/paper.tex` (LaTeX)
- **Presentación:** `reports/slides/` (Beamer)
- **Figuras:** `reports/figures/`

---

## 👥 Autores

- **Estudiantes:** Economía 5° semestre, EAFIT, 2026-I
- **Profesor:** Paula María Almonacid Hurtado
- **Institución:** Universidad EAFIT

---

## 📄 Licencia

Este proyecto se distribuye bajo licencia [MIT](LICENSE).  
Los datos utilizados (DANE, Banco de la República) están bajo licencias públicas (CC-BY-4.0, de dominio público).

---

## 📚 Referencias Bibliográficas

Ver [`reports/references.bib`](reports/references.bib)

Lecturas recomendadas:
- Documentación de DANE sobre metodología de encuestas
- Working Papers del Banco de la República
- Estudios de legalización en Canadá y Uruguay
- Elasticidad de demanda de bienes pecaminosos (Chaloupka & Warner, 2000)

---

## 🔗 Enlaces Útiles

- [DANE - Datos Abiertos](https://www.dane.gov.co/)
- [Banco de la República - Series Estadísticas](https://www.banrep.gov.co/)
- [DIAN - Estadísticas Tributarias](https://www.dian.gov.co/)

---

## ❓ FAQ / Troubleshooting

### ¿Cómo agrego nuevos datos?
1. Descargar archivo → `data/raw/`
2. Crear script de limpieza en `src/cannabis_tax/io/`
3. Guardar resultado procesado en `data/processed/` con metadatos JSON
4. Actualizar `configs/features.yaml`

### ¿Los datos son muy grandes y no puedo commitearlos?
- Agregar patrones a `.gitignore` (ej: `data/raw/*.csv`)
- Usar [Git LFS](https://git-lfs.com/) para archivos grandes
- Documentar en `data/README.md` cómo descargar datos

### ¿Cómo agrego un nuevo modelo?
- Implementar en `src/cannabis_tax/models/ml.py` o nuevo módulo
- Incluir métodos `.fit(X, y)` y `.predict(X)`
- Crear tests en `tests/unit/test_models.py`
- Documentar parámetros y supuestos en docstring

### ¿Cómo genero un nuevo reporte?
- Crear notebook en `notebooks/`
- Usar rutas relativas con `src.cannabis_tax.core.paths`
- Exportar figuras a `reports/figures/`
- Incluir en LaTeX si es documentación oficial

---

## 🛠️ Desarrollo

### Estructura de Commits

```bash
git add <cambios>
git commit -m "tipo(scope): descripción"
```

Tipos: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`

Ejemplo: `feat(models): agregar ARIMA con validación cruzada`

### Branch Workflow

```bash
# Feature branch
git checkout -b feature/nueva-funcionalidad

# Después de terminar, PR a main
```

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisar este README
2. Consultar docstrings en el código
3. Abrir un issue en GitHub
4. Contactar al profesor

---

**Última actualización:** 2026-03-03  
**Versión:** 0.1.0
