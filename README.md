# Predicción del Recaudo Tributario en Colombia

**Ciencia de Datos – Programa de Economía**  
**Universidad EAFIT | 2026-I**  

**Profesora:** Paula María Almonacid Hurtado  
**Curso:** 5° semestre – Ciencia de Datos  

---

## 1. Descripción general del proyecto

Este proyecto analiza la estructura del **recaudo tributario del Estado colombiano** bajo distintos escenarios de **legalización de la marihuana**. El objetivo principal es **modelar y predecir cambios en los ingresos tributarios** considerando diferentes hipótesis de legalización y consumo, utilizando **Python** para limpieza, análisis, modelado y visualización de datos provenientes de múltiples formatos (CSV, Excel, TXT, etc.).  

El proyecto se desarrolla de manera **replicable y estructurada**, con entregas semanales y fases definidas a lo largo de 16 semanas.  

---

## 2. Pregunta de investigación

> ¿Cómo podría predecirse la estructura del recaudo tributario del Estado colombiano bajo distintos escenarios de legalización de la distribución de la marihuana?

---

## 3. Variables y datos

### Variables principales

- **Recaudo tributario total:** ingresos del Estado por impuestos.  
- **Escenarios de legalización:** distintos niveles de regulación y distribución de marihuana.  
- **Variables de control:** población, PIB, consumo estimado de marihuana, entre otros.  

### Frecuencia y periodo

- **Frecuencia:** anual y trimestral, según disponibilidad de datos.  
- **Periodo de análisis:** determinado según fuentes y calidad de datos, especificado en el documento final.  

### Fuentes de información

- **DIAN** – Dirección de Impuestos y Aduanas Nacionales  
- **DANE** – Departamento Administrativo Nacional de Estadística  
- Otros datos públicos de consumo y fiscalidad  

---

## 4. Metodología

Se emplean **técnicas de ciencia de datos y modelado predictivo** en Python, incluyendo:

- Limpieza y transformación de datos (preprocessing).  
- Análisis exploratorio y visualización.  
- Modelos de predicción y simulación de ingresos tributarios.  
- Comparación de escenarios y evaluación de sensibilidad.  

Todos los pasos son **reproducibles** mediante scripts organizados en la carpeta `scripts/`.  

---

## 5. Resultados esperados

El proyecto permite:

- Estimar cómo variaría el recaudo tributario bajo distintos escenarios de legalización.  
- Analizar el impacto fiscal y económico potencial de la legalización de la marihuana.  
- Proveer una base replicable para futuros análisis o políticas públicas.  

---

## 6. Estructura de carpetas

/data
/raw -> Datos originales sin modificar (CSV, Excel, TXT)
/processed -> Datos limpios y transformados para análisis
/scripts -> Scripts de Python para limpieza, análisis y modelado
/outputs -> Resultados finales,documento de texto, gráficos y tablas
README.md -> Este archivo
.gitignore -> Archivos ignorados por Git


---

## 7. Reproducibilidad

El código incluido permite:

- Cargar datos de diversas fuentes y formatos.  
- Replicar todos los análisis y simulaciones de ingresos tributarios.  
- Generar gráficos, tablas y resultados de manera automática.  

---

## 8. Referencias

Las fuentes de datos, documentación metodológica y referencias académicas se incluyen en el documento escrito del proyecto, siguiendo normas académicas.

## Reproducibility

All results in this project can be reproduced by running the scripts
in the `/scripts` folder in numerical order.
