# Colombia Marijuana Revenue Tax Forecasting Model

**Predicción del Recaudo Tributario bajo Escenarios de Legalización de Marihuana en Colombia**

*Curso: Ciencia de Datos – 5° semestre | Universidad: EAFIT | Semestre: 2026-I*

---

## 📋 Descripción

Análisis del **recaudo tributario colombiano** bajo escenarios de legalización de marihuana. Pipeline reproducible que integra datos del DANE, Banco de la República y DIAN para:

- Limpiar y transformar múltiples fuentes
- Análisis exploratorio de series temporales
- Modelos predictivos de ingresos tributarios
- Simulación de escenarios de legalización
- Evaluación de sensibilidad

**Pregunta de investigación:** ¿Cómo predecir la estructura del recaudo tributario bajo distintos escenarios de legalización de marihuana?

---

## 🚀 Instalación Rápida

### 1. Entorno Virtual

```bash
git clone https://github.com/Tupxz/colombia-marijuana-revenue-model.git
cd colombia-marijuana-revenue-model

python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate          # Windows
```

### 2. Instalar Paquete

```bash
# Instalación básica
pip install -e .

# Con herramientas de desarrollo (recomendado)
pip install -e ".[dev]"

# Con Jupyter (para notebooks)
pip install -e ".[jupyter]"

# Todo
pip install -e ".[all]"
```

### 3. Verificar Instalación

```bash
python -c "import cannabis_tax; print(f'✅ Paquete {cannabis_tax.__version__}')"
python -m cannabis_tax.cli --help
```

---

## 📋 Comandos CLI

```bash
# Pipeline completo
python -m cannabis_tax.cli pipeline

# Pasos individuales
python -m cannabis_tax.cli process        # Procesar datos
python -m cannabis_tax.cli analyze        # Análisis EDA
python -m cannabis_tax.cli model          # Entrenar modelos
python -m cannabis_tax.cli scenarios -s 5 # Simular escenarios
python -m cannabis_tax.cli evaluate       # Evaluar
python -m cannabis_tax.cli viz            # Visualizar

# Con verbose logging
python -m cannabis_tax.cli pipeline --verbose
```

---

## 📁 Estructura del Proyecto

```
src/cannabis_tax/          Código productivo (paquete Python)
├── cli.py                 Interfaz de línea de comandos
├── core/                  Logging, paths, configuración
├── io/                    Ingestión de datos
├── cleaning/              Limpieza de datos
├── features/              Feature engineering
├── models/                Benchmarks y modelos ML
├── scenarios/             Simulación de escenarios
└── viz/                   Visualizaciones

configs/                   Archivos YAML de configuración

data/
├── raw/                   Datos originales (no editar)
├── processed/             Datos procesados limpios
└── README.md              Diccionario de datos

reports/                   Documentación académica
├── paper.tex / paper.pdf  Artículo principal
├── slides/                Presentación Beamer
└── figures/               Figuras estáticas

runs/                      Resultados de ejecuciones (timestamped)
tests/                     Suite de pruebas (pytest)
notebooks/                 Exploración (Jupyter)
```

---

## 🧪 Testing y Desarrollo

```bash
# Ejecutar tests
pytest tests/ -v

# Con cobertura
pytest --cov=cannabis_tax --cov-report=html

# Formatear código
black src/ tests/

# Verificar estilo
flake8 src/
mypy src/
```

---

## 📊 Datos

**Fuentes:** DANE (Encuestas, Capítulos Fiscales), Banco de la República (Series Macroeconómicas), DIAN (Estadísticas Tributarias).

**Diccionario de datos y política de gestión:** Ver [`data/README.md`](data/README.md)

---

## 📝 Notas de Refactorización

Este repositorio fue refactorizado el 3 de marzo de 2026 hacia una arquitectura modular y reproducible:

- Migración `scripts/` → `src/cannabis_tax/` (PEP 420 layout)
- Reorganización `docs/` → `reports/`
- Implementación `pyproject.toml` (PEP 517/518)
- Consolidación de configuraciones YAML
- Testing con pytest, code quality con black/flake8/mypy

Esto permite instalación editable (`pip install -e .`), reproducibilidad garantizada y mantenibilidad a largo plazo.

---

## 📦 Dependencias Principales

**Producción:** pandas, numpy, pyyaml, matplotlib, scikit-learn  
**Desarrollo:** pytest, black, flake8, mypy, isort  
**Jupyter:** jupyter, jupyterlab (opcional)

Ver `pyproject.toml` para versiones específicas.

---

## 👥 Autores

- **Estudiantes:** Economía 5° semestre, EAFIT, 2026-I
- **Profesor:** Paula María Almonacid Hurtado
- **Institución:** Universidad EAFIT

---

## 📄 Licencia

MIT License. Los datos utilizados están bajo licencias públicas (CC-BY-4.0, dominio público).

---

## 📚 Referencias Bibliográficas

Ver `reports/references.bib` para la bibliografía completa. Lecturas recomendadas:
- Documentación DANE sobre metodología de encuestas
- Working Papers del Banco de la República
- Estudios de legalización en Canadá y Uruguay
- Elasticidad de demanda de bienes pecaminosos (Chaloupka & Warner, 2000)

---

**Última actualización:** 2026-03-03 | **Versión:** 0.1.0
