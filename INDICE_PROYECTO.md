# 🗂️ ÍNDICE DE PROYECTO - Predicción del Recaudo Tributario

**Proyecto:** Colombia Marijuana Revenue Model  
**Universidad:** EAFIT - Ciencia de Datos  
**Semestre:** 2026-I (Semana 3)  
**Estado:** ✅ **Bases de datos limpias y documentadas**

---

## 📍 ACCESOS RÁPIDOS

### 🎯 DOCUMENTOS CLAVE
1. **PROCESAMIENTO_RESUMEN.md** (este directorio) ← **EMPEZAR AQUÍ**
2. **data/BASES_LIMPIAS.md** - Guía de bases de datos
3. **data/README_DATASETS.md** - Estructura técnica detallada
4. **data/processed/variables.tex** + **variables.pdf** - Variables documentadas

### 📊 BASES DE DATOS LIMPIAS
- `data/processed/personas_processed.csv` - Encuesta principal (169K registros)
- `data/processed/pib_anual.csv` - PIB anual
- `data/processed/pib_trimestral.csv` - PIB trimestral
- `data/processed/ipc_variacion.csv` - Precios
- `data/processed/ise_cuadro_*.csv` - Indicadores de actividad (x3)

### 🔧 SCRIPTS PYTHON
```bash
cd /Users/santi/Documents/EAFIT/2026-1/Ciencia\ de\ los\ Datos/Repo/colombia-marijuana-revenue-model

# Procesar encuesta
python scripts/01_processing.py

# Procesar datos macroeconómicos
python scripts/02_process_pib.py
python scripts/03_process_ipc.py
python scripts/04_process_ise.py
```

---

## 🎯 VARIABLE CRÍTICA PARA TU INVESTIGACIÓN

```
C_09_VALOR = GASTO EN MARIHUANA EN PESOS (últimos 30 días)
```

**Ubicación:** `data/processed/personas_processed.csv`  
**Importancia:** ⭐⭐⭐⭐⭐ CRÍTICA para tributación  
**Identificación:** Necesitas el Diccionario de Datos para mapear todas las variables

---

## 📋 FLUJO DE TRABAJO RECOMENDADO

### Semana 3-4: EXPLORACIÓN (EDA)
```python
import pandas as pd

# Cargar datos
df = pd.read_csv('data/processed/personas_processed.csv')

# Análisis inicial
print(df.info())
print(df.describe())

# Explorar consumo (necesitas diccionario para identificar variables)
# Buscar: C_02 (consumo 12m), C_05 (consumo 30d), C_09_VALOR (gasto)
```

**Tareas:**
- [ ] Distribución de consumo por demografía
- [ ] Estadísticas de gasto en marihuana
- [ ] Mapeo geográfico
- [ ] Perfiles de consumidores

### Semana 5-6: INTEGRACIÓN
```python
# Merge con datos macroeconómicos
df_pib = pd.read_csv('data/processed/pib_anual.csv')
df_ipc = pd.read_csv('data/processed/ipc_variacion.csv')

# Integración temporal
df_merged = df.merge(df_pib, on='year', how='left')
```

**Tareas:**
- [ ] Integrar PIB, IPC, ISE
- [ ] Deflactar precios
- [ ] Variables de control económico

### Semana 7-9: MODELADO
```python
# Regresiones, elasticidad
# Modelos de predicción de consumo
# Estimación de recaudo tributario
```

**Tareas:**
- [ ] Análisis de elasticidad
- [ ] Estimación de mercado
- [ ] Simulación de impuestos

### Semana 10-12: PROYECCIONES Y REPORTES
```python
# Escenarios de legalización
# Tablas y figuras
# Documento final
```

---

## 🔍 VARIABLES DISPONIBLES EN ENCUESTA

### Consumo de Marihuana
| Código | Pregunta |
|--------|----------|
| C_01 | ¿Cuándo fue la primera vez que consumió? |
| C_02 | ¿Ha consumido en últimos 12 meses? |
| C_03 | ¿Con qué frecuencia en 12 meses? |
| C_04_A-D | ¿Cómo consume? (fumada, inhalada, etc.) |
| C_05 | ¿Ha consumido en últimos 30 días? |
| C_06 | ¿Cuántos días en últimos 30 días? |
| C_07 | ¿Cuánto gastó en últimos 30 días? |
| C_08 | ¿Cuántos gramos consume al mes? |
| **C_09_VALOR** | **¿Conoce el precio por gramo?** ⭐ |
| C_10_A-H | ¿Cómo obtiene? (Internet, amigos, expendios, etc.) |

### Demográficas (en personas_processed.csv)
- sexo (1=Hombre, 2=Mujer)
- edad (0-108 años)
- parentesco (jefe, hijo, pareja, etc.)
- padre (vive en hogar)
- madre (vive en hogar)

### Para Acceder a Más Variables
→ Consultar `data/raw/Diccionario de datos_02062020_ANONIMIZADO.xlsx`

---

## 💾 COMANDOS ÚTILES

```bash
# Ver estructura de datos
head -5 data/processed/personas_processed.csv

# Ver tamaño de archivos
ls -lh data/processed/*.csv

# Contar registros
wc -l data/processed/personas_processed.csv

# Verificar integridad
python -c "import pandas as pd; print(pd.read_csv('data/processed/personas_processed.csv').info())"
```

---

## 🐛 TROUBLESHOOTING

**P: No encuentro la variable C_09_VALOR en personas_processed.csv**  
R: Las variables de las preguntas (C_01-C_10, etc.) están en el Diccionario. 
   `personas_processed.csv` tiene solo variables demográficas básicas.
   Necesitas el archivo Diccionario para mapear todas.

**P: ¿Cómo activo el ambiente virtual?**  
R: `source .venv/bin/activate`

**P: ¿Qué versión de Python?**  
R: 3.12.5 (ver con `python --version`)

**P: ¿Dónde está el Diccionario?**  
R: `data/raw/Diccionario de datos_02062020_ANONIMIZADO.xlsx`

---

## 📞 REFERENCIAS

### Documentación Interna
- `PROCESAMIENTO_RESUMEN.md` - Resumen de lo realizado
- `data/README_DATASETS.md` - Guía técnica de datasets
- `data/BASES_LIMPIAS.md` - Guía de uso de bases

### Fuentes Externas
- **DANE:** [https://www.dane.gov.co](https://www.dane.gov.co)
- **DIAN:** [https://www.dian.gov.co](https://www.dian.gov.co)
- **Banco Rep:** [https://www.banrep.gov.co](https://www.banrep.gov.co)

### Librerías Python
```bash
# Instalar dependencias
pip install pandas openpyxl numpy matplotlib seaborn scipy statsmodels
```

---

## ✅ CHECKLIST ACTUAL

- [x] Exploración de archivos raw
- [x] Variables identificadas
- [x] Scripts de procesamiento creados
- [x] Bases procesadas generadas
- [x] Documentación completada
- [ ] EDA (Próximo paso)
- [ ] Integración de datos
- [ ] Modelado
- [ ] Reportes finales

---

## 📅 CRONOGRAMA SUGERIDO

| Semana | Actividad | Estado |
|--------|-----------|--------|
| 1-2 | Obtención de datos | ✅ Completada |
| 3-4 | Limpieza y procesamiento | ✅ Completada |
| 5-6 | EDA y exploración | ⏳ Próximo |
| 7-8 | Integración de datos | ⏳ Próximo |
| 9-10 | Modelado y proyecciones | ⏳ Próximo |
| 11-12 | Reportes y conclusiones | ⏳ Próximo |
| 13-16 | Revisión, ajustes, entrega | ⏳ Próximo |

---

**Última actualización:** 12 de febrero de 2026  
**Responsable:** Ciencia de Datos - EAFIT  
**Estado:** ✅ Proyecto en ejecución

---

*Archivo de referencia rápida. Para detalles técnicos, ver documentación en `data/`*
