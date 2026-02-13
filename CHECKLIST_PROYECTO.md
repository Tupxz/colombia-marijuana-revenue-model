# ✅ CHECKLIST DEL PROYECTO

## 📊 FASE 1: OBTENCIÓN Y PROCESAMIENTO DE DATOS
**Estado: ✅ COMPLETADA**

### Datos Descargados
- [x] Encuesta de personas (CSV, STATA, SPSS)
- [x] PIB Banco de la República (anual y trimestral)
- [x] IPC DANE (enero 2026)
- [x] ISE DANE (9 actividades, 3 cuadros)
- [x] Diccionario de variables

### Procesamiento Completado
- [x] Script 01_processing.py (encuesta)
- [x] Script 02_process_pib.py (PIB)
- [x] Script 03_process_ipc.py (IPC)
- [x] Script 04_process_ise.py (ISE)
- [x] Generación de 8 CSV limpios

### Variables Identificadas
- [x] C_02 - Consumo últimos 12 meses
- [x] C_05 - Consumo últimos 30 días
- [x] C_09_VALOR - GASTO EN MARIHUANA ⭐
- [x] Variables demográficas
- [x] Variables laborales

### Documentación
- [x] variables.tex y variables.pdf
- [x] README_DATASETS.md
- [x] BASES_LIMPIAS.md
- [x] PROCESAMIENTO_RESUMEN.md
- [x] INDICE_PROYECTO.md
- [x] CHECKLIST_PROYECTO.md

---

## 📊 FASE 2: ANÁLISIS EXPLORATORIO (EDA)
**Estado: ⏳ PRÓXIMA**

### Exploración Descriptiva
- [ ] Cargar datos principales
- [ ] Revisar dimensiones y tipos
- [ ] Detectar valores faltantes
- [ ] Revisar valores atípicos
- [ ] Estadísticas básicas

### Consumo de Marihuana
- [ ] % de consumidores en muestra
- [ ] Distribución por C_02 (12 meses)
- [ ] Distribución por C_05 (30 días)
- [ ] Análisis de frecuencia (C_03)
- [ ] Cantidad consumida (C_08)
- [ ] Análisis de gasto (C_09_VALOR)

### Análisis Demográfico
- [ ] Perfil de consumidores (edad, sexo)
- [ ] Consumo por educación
- [ ] Consumo por estado civil
- [ ] Consumo por ocupación
- [ ] Consumo por región (si está disponible)

### Visualizaciones
- [ ] Histogramas de consumo
- [ ] Box plots por grupos demográficos
- [ ] Correlaciones entre variables
- [ ] Mapas de calor
- [ ] Series temporales (si aplica)

**Entregable:** Notebook con EDA completo

---

## 📊 FASE 3: INTEGRACIÓN DE DATOS
**Estado: ⏳ PRÓXIMA**

### Merge de Bases
- [ ] Integrar PIB anual a encuesta
- [ ] Integrar IPC
- [ ] Integrar ISE por sector
- [ ] Crear variables de período/año

### Nuevas Variables
- [ ] Deflactar gasto en marihuana con IPC
- [ ] Gasto per cápita
- [ ] Elasticidad de demanda
- [ ] Variables de control económico

### Limpieza Post-Merge
- [ ] Validar integridad del merge
- [ ] Valores faltantes después del merge
- [ ] Análisis de duplicados

**Entregable:** Dataset integrado (CSV)

---

## 📊 FASE 4: MODELADO Y ESTIMACIÓN
**Estado: ⏳ PRÓXIMA**

### Estimación de Mercado
- [ ] Tamaño total del mercado (consumo × precio)
- [ ] Gasto total nacional en marihuana
- [ ] Gasto promedio por consumidor
- [ ] Gasto por región/grupo demográfico

### Elasticidad Tributaria
- [ ] Regresión: Consumo vs variables demográficas
- [ ] Regresión: Gasto vs PIB/IPC
- [ ] Estimación de elasticidad precio
- [ ] Estimación de elasticidad ingreso

### Modelos Predictivos
- [ ] Modelo de probabilidad de consumo
- [ ] Modelo de cantidad consumida
- [ ] Modelo de gasto

### Escenarios de Legalización
- [ ] Escenario 1: IVA estándar (19%)
- [ ] Escenario 2: Impuesto específico (30%)
- [ ] Escenario 3: Impuesto mixto
- [ ] Escenario 4: Sin regulación (baseline)

**Entregable:** Reportes de modelado + código

---

## 📊 FASE 5: PROYECCIONES Y SIMULACIONES
**Estado: ⏳ PRÓXIMA**

### Proyección de Recaudo
- [ ] Recaudo bajo escenario 1
- [ ] Recaudo bajo escenario 2
- [ ] Recaudo bajo escenario 3
- [ ] Comparativa de escenarios

### Análisis de Sensibilidad
- [ ] Sensibilidad a cambios en consumo
- [ ] Sensibilidad a cambios en precio
- [ ] Sensibilidad a cambios en tasa de impuesto
- [ ] Sensibilidad por grupo demográfico

### Tablas y Figuras
- [ ] Tabla 1: Estadísticas descriptivas
- [ ] Tabla 2: Consumo por demografía
- [ ] Tabla 3: Estimación de recaudo
- [ ] Figura 1: Distribución de consumo
- [ ] Figura 2: Comparativa de escenarios
- [ ] Figura 3: Análisis de sensibilidad

**Entregable:** Visualizaciones para paper

---

## 📄 FASE 6: DOCUMENTACIÓN FINAL
**Estado: ⏳ PRÓXIMA**

### Paper Académico
- [ ] Resumen/Abstract
- [ ] Introducción
- [ ] Revisión de literatura
- [ ] Pregunta de investigación
- [ ] Marco teórico
- [ ] Metodología
- [ ] Resultados
- [ ] Discusión
- [ ] Conclusiones
- [ ] Referencias

### Apéndices Técnicos
- [ ] Diccionario de variables
- [ ] Especificaciones de modelos
- [ ] Códigos Python/notebooks
- [ ] Tablas adicionales

### Presentación
- [ ] Diapositivas principales
- [ ] Resultados clave
- [ ] Conclusiones y recomendaciones

**Entregable:** Paper + Presentación

---

## 🎯 MÉTRICAS CLAVE A CALCULAR

- [ ] Prevalencia de consumo (%)
- [ ] Gasto promedio mensual (pesos)
- [ ] Tamaño del mercado (anual)
- [ ] Elasticidad precio de demanda
- [ ] Elasticidad ingreso de demanda
- [ ] Potencial de recaudo (estimado)
- [ ] Distribución geográfica
- [ ] Distribución demográfica

---

## 📚 REFERENCIAS NECESARIAS

### Por Consultar
- [ ] Estudios de legalización en otros países
- [ ] Estructura tributaria colombiana
- [ ] Legislación sobre cannabis
- [ ] Reportes del DANE/DIAN
- [ ] Literatura económica sobre tributación

### Por Mencionar en Paper
- [ ] Al menos 15 referencias académicas
- [ ] Estadísticas oficiales
- [ ] Normativa legal

---

## 💻 HERRAMIENTAS REQUERIDAS

### Instaladas y Listas
- [x] Python 3.12.5
- [x] Pandas
- [x] Openpyxl
- [ ] Numpy *(instalar si falta)*
- [ ] Matplotlib *(instalar si falta)*
- [ ] Seaborn *(instalar si falta)*
- [ ] Scipy *(instalar si falta)*
- [ ] Statsmodels *(instalar si falta)*

### Comandos para Instalar
```bash
pip install numpy matplotlib seaborn scipy statsmodels scikit-learn
```

---

## 📝 NOTAS Y OBSERVACIONES

### Decisiones Tomadas
- [x] Usar personas.csv como base principal
- [x] Descartar personas.dta y personas.sav (duplicados)
- [x] Integrar PIB anual en lugar de trimestral (más datos)
- [x] Usar IPC para deflactación

### Problemas Identificados
- La encuesta personas.csv contiene variables numéricas pero sin nombres descriptivos
  → SOLUCIÓN: Usar Diccionario de Datos para mapear
  
- Variables de consumo (C_*) no están en personas.csv directamente
  → SOLUCIÓN: Están documentadas en Diccionario, necesitan ser extraídas

### Próximas Acciones Inmediatas
1. Abrir personas_processed.csv
2. Revisar Diccionario de Datos para identificar columnas de consumo
3. Crear mapping de variables
4. Iniciar EDA

---

## 📞 CONTACTO Y AYUDA

**Profesor:** Paula María Almonacid Hurtado  
**Curso:** Ciencia de Datos 5° semestre  
**Semestre:** 2026-I  

**Documentación Disponible:**
- PROCESAMIENTO_RESUMEN.md
- INDICE_PROYECTO.md
- data/BASES_LIMPIAS.md
- data/README_DATASETS.md

---

## 🏁 ESTADO GENERAL DEL PROYECTO

```
FASE 1: Obtención y procesamiento ✅ COMPLETADA
FASE 2: Análisis exploratorio      ⏳ POR HACER
FASE 3: Integración de datos       ⏳ POR HACER
FASE 4: Modelado                   ⏳ POR HACER
FASE 5: Proyecciones               ⏳ POR HACER
FASE 6: Documentación final        ⏳ POR HACER

PROGRESO TOTAL: 16.7% (1 de 6 fases)
SEMANAS UTILIZADAS: 2-3 de 16
SEMANAS DISPONIBLES: 13-14
```

---

**Última actualización:** 12 de febrero de 2026  
**Responsable:** Tu nombre  
**Próxima revisión:** Cuando comience EDA

---

*Usa este checklist para seguimiento. Marca con [x] cuando completes cada tarea.*
