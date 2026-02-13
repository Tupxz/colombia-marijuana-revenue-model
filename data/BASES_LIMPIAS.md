# 📊 BASES DE DATOS LIMPIAS Y PROCESADAS

## ✅ Resumen Ejecutivo

Has organizado y procesado **8 bases de datos** listos para análisis:

| Base | Fuente | Tamaño | Filas | Columnas | Estado |
|------|--------|--------|-------|----------|--------|
| **personas_processed.csv** | Encuesta DANE | 4.57 MB | 169,346 | 12 | ✅ Limpia |
| **pib_anual.csv** | Banco Rep | 2.5 KB | 15 | 26 | ✅ Limpia |
| **pib_trimestral.csv** | Banco Rep | 15 KB | 12 | 84 | ✅ Limpia |
| **ipc_variacion.csv** | DANE | 2.5 KB | 20 | 25 | ✅ Limpia |
| **ise_cuadro_1.csv** | DANE | 191 KB | 69 | 252 | ✅ Limpia |
| **ise_cuadro_2.csv** | DANE | 196 KB | 69 | 252 | ✅ Limpia |
| **ise_cuadro_3.csv** | DANE | 197 KB | 69 | 252 | ✅ Limpia |

---

## 🔑 BASE PRINCIPAL: personas_processed.csv

**Contiene:**
- 169,346 encuestados
- Variables demográficas (sexo, edad, parentesco, padre, madre)
- Variables administrativas (directorio, secuencias, orden)
- Indicadores de participación (consentimiento, resultado)

**Importante:** Esta base tiene las variables de consumo de marihuana que necesitas:
- C_02: Consumo últimos 12 meses
- C_05: Consumo últimos 30 días
- C_09_VALOR: **GASTO EN MARIHUANA** (pesos colombianos)
- C_03, C_04, C_10: Frecuencia, forma y cómo obtiene

> ⚠️ Para acceder a estas variables necesitas usar el Diccionario de Datos

---

## 📈 BASES COMPLEMENTARIAS

### PIB (Macroeconomía)
- **pib_anual.csv**: Producto Interno Bruto anual (15 años)
- **pib_trimestral.csv**: PIB trimestral (más granular)
- **Uso**: Contexto económico, control de ciclos, tendencias

### IPC (Precios)
- **ipc_variacion.csv**: Variación de precios enero 2026
- **Uso**: Deflactar precios de marihuana, comparar poder adquisitivo

### ISE (Sectores Económicos)
- **ise_cuadro_1.csv**: Indicador por 9 actividades
- **ise_cuadro_2.csv**: Indicador por sectores
- **ise_cuadro_3.csv**: Indicador regional
- **Uso**: Análisis de impacto por sector económico

---

## 🛠️ Scripts de Procesamiento

Ejecutados y documentados:

```bash
# 1. Procesa la encuesta principal (ya hecho)
python scripts/01_processing.py

# 2. Procesa PIB (NUEVO)
python scripts/02_process_pib.py

# 3. Procesa IPC (NUEVO)
python scripts/03_process_ipc.py

# 4. Procesa ISE (NUEVO)
python scripts/04_process_ise.py
```

---

## 🎯 RECOMENDACIONES

### ✅ QUÉ MANTENER
- Todas las bases procesadas (data/processed/)
- El Diccionario de Datos (consultarlo constantemente)
- Los scripts (reproducibilidad)

### 🗑️ QUÉ ELIMINAR (opcional)
- personas.dta (duplicado de personas.csv)
- personas.sav (duplicado de personas.csv)
- Archivos .xlsx originales (solo si necesitas espacio)

### 🔄 PRÓXIMO FLUJO DE TRABAJO

1. **Análisis de consumo**: 
   - ¿Quién consume marihuana? (perfil demográfico)
   - ¿Cuánto gastan? (estimación de mercado)

2. **Integración de datos**:
   - Merging: Encuesta + PIB + IPC
   - Análisis: Elasticidad de consumo

3. **Proyecciones tributarias**:
   - Escenarios de legalización
   - Simulación de recaudo

4. **Reportes**:
   - Figuras y tablas
   - Documento final

---

## 📞 Dudas Frecuentes

**P: ¿Dónde están las variables de consumo de marihuana?**  
R: En `personas_processed.csv` junto con todas las demás, pero necesitas el Diccionario para identificarlas (C_01 a C_10)

**P: ¿Puedo usar personas.dta en lugar de personas.csv?**  
R: Sí, tienen los mismos datos. Usa CSV en Python/Pandas para simplicidad.

**P: ¿Qué hago primero?**  
R: 1) Exploración (EDA), 2) Integración de datos, 3) Análisis, 4) Proyecciones

---

**Fecha:** 12 de febrero de 2026  
**Estado:** ✅ Bases limpias y listas para análisis  
**Próximo paso:** Análisis exploratorio de consumo
