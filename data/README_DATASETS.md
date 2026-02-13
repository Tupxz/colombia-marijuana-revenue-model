# Estructura de Datos del Proyecto

## 📊 Archivos en `data/raw/` (Datos Originales)

### Encuesta Principal
| Archivo | Formato | Tamaño | Descripción |
|---------|---------|--------|-------------|
| **personas.csv** | CSV | 4.45 MB | ✅ Base principal - 169,346 encuestados con 12 variables demográficas |
| personas.dta | STATA | 2.42 MB | Mismo contenido (opcional) |
| personas.sav | SPSS | 3.23 MB | Mismo contenido (opcional) |
| Diccionario de datos_02062020_ANONIMIZADO.xlsx | XLSX | 0.07 MB | 🔑 CRÍTICO - Documentación de todas las variables |

### Datos Macroeconómicos (Banco de la República)
| Archivo | Período | Dimensiones | Descripción |
|---------|---------|-------------|-------------|
| **PIBBanrepAnual.xlsx** | Anual | 15 × 26 | ✅ PIB anual para análisis temporal |
| **PIBBanrep.xlsx** | Trimestral | 12 × 84 | ✅ PIB trimestral (más granular) |

### Indicadores de Precios y Actividad (DANE)
| Archivo | Período | Dimensiones | Descripción |
|---------|---------|-------------|-------------|
| **anex-IPC-Variacion-ene2026.xlsx** | Enero 2026 | 23 × 25 | ✅ IPC para deflactar gastos |
| **anex-ISE-9actividades-nov2025.xlsx** | Nov 2025 | 92 × 252 | ✅ ISE por 9 actividades económicas |

---

## 📁 Archivos en `data/processed/` (Datos Procesados)

### Encuesta Procesada
- **personas_processed.csv** - Datos limpios de la encuesta principal
- **personas_processed_metadata.json** - Metadatos del procesamiento

### Datos Macroeconómicos Procesados (nuevos)
- **pib_anual.csv** - PIB anual limpio
- **pib_trimestral.csv** - PIB trimestral limpio
- **ipc_variacion.csv** - IPC limpio
- **ise_cuadro_1.csv** - ISE Cuadro 1 limpio
- **ise_cuadro_2.csv** - ISE Cuadro 2 limpio
- **ise_cuadro_3.csv** - ISE Cuadro 3 limpio

---

## 🎯 Recomendaciones de Uso

### Para tu Investigación sobre Tributación:

1. **Variable principal**: `personas_processed.csv`
   - Consumo de marihuana (C_02, C_05)
   - Gasto en marihuana (C_09_VALOR) ⭐
   - Variables demográficas (sexo, edad, educación)
   - Variables laborales (empleo, consumo en horario laboral)

2. **Variables de control macroeconómico**:
   - PIB anual/trimestral para contexto económico
   - IPC para deflactar precios
   - ISE para análisis por sector económico

3. **Próximos pasos**:
   - Crear dataset integrado: Encuesta + PIB + IPC + ISE
   - Estimar elasticidad tributaria por grupo demográfico
   - Simular recaudo bajo escenarios de legalización

---

## ⚠️ Notas sobre Duplicados

Los archivos `personas.dta` y `personas.sav` contienen **exactamente los mismos datos** que `personas.csv`.  
- Puedes mantenerlos por compatibilidad con STATA/SPSS
- O eliminarlos si solo trabajas con Python

---

## 🔄 Scripts de Procesamiento

| Script | Entrada | Salida | Función |
|--------|---------|--------|---------|
| 01_processing.py | personas.csv | personas_processed.csv | Limpieza y normalización |
| 02_process_pib.py | PIB*.xlsx | pib_*.csv | Procesamiento de PIB |
| 03_process_ipc.py | anex-IPC-*.xlsx | ipc_*.csv | Procesamiento de IPC |
| 04_process_ise.py | anex-ISE-*.xlsx | ise_*.csv | Procesamiento de ISE |

Ejecuta en orden: `01 → 02 → 03 → 04` para un pipeline completo.

---

## 📝 Variables Clave para Tributación

### Consumo de Marihuana
- **C_02**: ¿Ha consumido marihuana en últimos 12 meses?
- **C_05**: ¿Ha consumido marihuana en últimos 30 días?
- **C_03**: Frecuencia de consumo (mensual, semanal, diario, etc.)
- **C_08**: Cantidad consumida al mes (en gramos)
- **C_09_VALOR**: 💰 **GASTO EN MARIHUANA EN LOS ÚLTIMOS 30 DÍAS** (en pesos)
- **C_10_A a C_10_H**: Cómo obtiene la marihuana (Internet, amigos, expendios, etc.)

### Demográficas
- Sexo, edad, parentesco
- Nivel educativo
- Orientación sexual / Identidad de género
- Estado civil

### Laborales
- Empleo / Ocupación
- Accidentes en el trabajo
- Consumo en horario laboral (R_08_C)
- Impacto en rendimiento (R_09)

---

Última actualización: 12 de febrero de 2026
