# 🚀 Quick Reproducibility Checklist

## En cualquier máquina nueva, ejecuta esto para reproducir el entorno completo:

```bash
# 1. Clonar repo
git clone <repo-url>
cd colombia-marijuana-revenue-model

# 2. Crear venv
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# source .venv/Scripts/activate  # Windows

# 3. Instalar paquete con dev tools
pip install -e ".[dev]"

# 4. Verificar que todo funciona
python -c "import cannabis_tax; print(f'✅ Paquete {cannabis_tax.__version__} listo')"
python -m cannabis_tax.cli --help
pytest -v

# ✅ LISTO PARA DESARROLLAR
```

## Comandos Más Útiles

### Desarrollo
```bash
# Formatear código
black src/ tests/

# Organizar imports
isort src/ tests/

# Verificar estilo
flake8 src/ tests/

# Type checking
mypy src/

# Tests con cobertura
pytest --cov=cannabis_tax --cov-report=html
```

### Ejecución
```bash
# Ver todos los comandos disponibles
python -m cannabis_tax.cli --help

# Procesar datos
python -m cannabis_tax.cli process

# Ejecutar pipeline completo
python -m cannabis_tax.cli pipeline

# En modo verbose (debug)
python -m cannabis_tax.cli process --verbose
```

### Instalar Extras (Opcional)
```bash
# Si necesitas Jupyter
pip install -e ".[jupyter]"

# Si necesitas TODO
pip install -e ".[all]"
```

## Estructura del Proyecto (Post-Refactoring)

```
📦 colombia-marijuana-revenue-model
├── 📂 src/cannabis_tax/              # Código fuente del paquete
│   ├── __init__.py                   # Package root, metadata
│   ├── cli.py                        # Entry point CLI
│   ├── 📂 core/                      # Logging, paths, config
│   ├── 📂 io/                        # Data loading/saving
│   ├── 📂 cleaning/                  # Data cleaning
│   ├── 📂 features/                  # Feature engineering
│   ├── 📂 models/                    # Model implementations
│   ├── 📂 scenarios/                 # Scenario simulation
│   └── 📂 viz/                       # Visualizations
│
├── 📂 tests/                         # Test suite (pytest)
│
├── 📂 configs/                       # Configuration files
│
├── 📂 data/
│   ├── raw/                          # Original data
│   └── processed/                    # Cleaned/processed data
│
├── 📂 reports/
│   ├── paper/                        # Academic paper (LaTeX)
│   └── slides/                       # Presentation (LaTeX)
│
├── 📂 runs/                          # Outputs, figures, tables
│
├── 📄 pyproject.toml                 # Modern Python packaging
├── 📄 README.md                      # Project documentation
├── 📄 PACKAGING_SUMMARY.md           # This packaging guide
├── 📄 REFACTORING_SUMMARY.md         # Repository refactoring details
└── 📄 LICENSE                        # MIT License

```

## Estado de las Herramientas de Desarrollo

| Tool | Version | Status | Command |
|------|---------|--------|---------|
| Python | 3.12.5 | ✅ | `python --version` |
| pytest | 9.0.2 | ✅ | `pytest -v` |
| black | 26.1.0 | ✅ | `black --version` |
| flake8 | 7.3.0 | ✅ | `flake8 --version` |
| mypy | 1.19.1 | ✅ | `mypy --version` |
| isort | 8.0.1 | ✅ | `isort --version` |

## Troubleshooting

### "ModuleNotFoundError: No module named 'cannabis_tax'"
```bash
# Solución: Asegúrate de que venv está activado
source .venv/bin/activate
pip install -e .
```

### "pytest: command not found"
```bash
# Solución: Instala dev dependencies
pip install -e ".[dev]"
```

### "No tests ran"
```bash
# Esto es normal. Los tests aún no están escritos.
# Crea archivos en tests/ siguiendo el naming pattern:
# tests/test_*.py or tests/*_test.py
pytest -v  # Para redescubrir
```

### Los imports en los scripts fallaron
```bash
# Viejo problema: actualizar PYTHONPATH manualmente
# Ahora: pip install -e . lo resuelve automáticamente
# Verifica que estés en venv: which python
```

## Próximos Pasos

1. **Escribir tests**: Crear archivos en `tests/test_*.py`
   ```bash
   pytest tests/test_cleaning.py -v
   ```

2. **Documentar funciones**: Usar docstrings Google style
   ```python
   def my_function(param: str) -> int:
       """Brief description.
       
       Extended description if needed.
       
       Args:
           param: Description of param.
           
       Returns:
           Description of return value.
       """
   ```

3. **Configurar CI/CD**: GitHub Actions, GitLab CI, etc.
   - Ejecutar tests en cada push
   - Verificar style con black/flake8
   - Type checking con mypy

4. **Preparar para distribución**: Cuando esté listo
   ```bash
   pip install build
   python -m build  # Crea wheel y tarball
   # Luego: pip install dist/cannabis_tax-0.1.0-py3-none-any.whl
   ```

---

**Referencia rápida**: Ver `PACKAGING_SUMMARY.md` para detalles completos.
