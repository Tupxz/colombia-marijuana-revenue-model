# Data Directory Guide

## Estructura de Datos

Este directorio organiza todos los datos del proyecto en tres niveles según el nivel de procesamiento:

### `raw/`
**Datos originales sin modificar**

Contiene archivos descargados de fuentes externas:
- **DANE** (Departamento Administrativo Nacional de Estadística)
  - `d_capitulos.csv` - Capítulos de impuestos directos
  - `d2_capitulos.csv` - Subcapítulos de impuestos directos
  - `g_capitulos.csv` - Capítulos de impuestos indirectos
  - `k_capitulos.csv` - Capítulos de contribuciones a la seguridad social
  - `personas.csv` / `personas.dta` / `personas.sav` - Microdatos de hogares
  - `CPIAUCSL.xlsx` - Índices de precios

- **Banco de la República**
  - `PIBBanrep.xlsx` - PIB trimestral
  - `PIBBanrepAnual.xlsx` - PIB anual

**Política:**
- ❌ NO modificar directamente archivos aquí
- ✅ Todos los cambios van a `interim/` y `processed/`
- ✅ Mantener nombre y formato original

### `interim/`
**Datos intermedios en proceso de transformación**

Contiene resultados de:
- Unión de múltiples fuentes raw
- Transformaciones parciales
- Datos de prueba o debugging
- Archivos temporales que serán consumidos por pasos posteriores

**Política:**
- No es necesario documentar metadatos detallados aquí
- Archivos pueden ser descartados y regenerados
- Ideal para compartir estados intermedios entre scripts

### `processed/`
**Datos finales, limpios y listos para análisis/modelado**

Contiene:
- Datasets finales consolidados
- Archivos con sufijo `_processed` o `_clean`
- Metadatos JSON asociados: `*_metadata.json`
- Diccionarios de datos en Excel

**Archivos clave:**
- `personas_processed.csv` + `personas_processed_metadata.json` - Datos de personas limpios
- `d_capitulos.csv`, `d2_capitulos.csv`, `g_capitulos.csv`, `k_capitulos.csv` + metadatos - Capítulos de recaudo
- `pib_anual.csv`, `pib_trimestral.csv` - PIB procesado
- `IPC_limpio_copia.xlsx` - IPC limpio
- `TRM_limpia_copia.csv` - TRM limpia
- `CDT_limpia_copia.xlsx` - CDT limpio
- `Diccionario de datos_ANONIMIZADO.xlsx` - Documentación de variables

**Metadatos asociados (`*_metadata.json`):**
```json
{
  "source": "DANE / Banco de la República",
  "download_date": "YYYY-MM-DD",
  "description": "Descripción breve",
  "rows": 1000,
  "columns": 10,
  "column_descriptions": {...},
  "data_quality_issues": [...],
  "last_updated": "YYYY-MM-DD HH:MM:SS"
}
```

**Política:**
- ✅ Incluir siempre un archivo `*_metadata.json` con cada dataset
- ✅ Documentar en el metadata qué transformaciones se realizaron
- ✅ Usar tipos de dato apropiados (fechas como datetime, moneda como float, etc.)
- ❌ No incluir información personal identificable (PII) sin anonimizar

### `external/`
**Datos de fuentes externas (APIs, descargas manuales futuras)**

Reservado para:
- Datos descargados de APIs públicas (FRED, World Bank, etc.)
- Datos externos que no provienen de DANE/DIAN
- Información complementaria para enriquecimiento de análisis

---

## Fuentes de Datos Actuales

| Fuente | Tipo | Frecuencia | Archivo(s) | Estado |
|--------|------|-----------|-----------|--------|
| **DANE** | Encuesta | - | `personas.csv`, `d_capitulos.csv`, etc. | ✅ Incluido |
| **Banco Rep.** | Series Macroeconómicas | Trimestral/Anual | `PIBBanrep*.xlsx` | ✅ Incluido |
| **CPIAUCSL** | Índice de Precios | Mensual | `CPIAUCSL.xlsx` | ✅ Incluido |
| **DIAN** | Recaudo Tributario | Anual | `*_capitulos.csv` (DANE proxy) | ⚠️ Parcial |

---

## Datos Faltantes / Por Obtener

- [ ] **Datos DIAN detallados por sector** (marihuana, cannabis medicinal)
- [ ] **Precios históricos de marihuana en mercados legales** (Canadá, Uruguay)
- [ ] **Elasticidad de demanda** (estudios econométricos)
- [ ] **Datos de consumo** (encuestas NIDA, OMS)

---

## Cómo Agregar Nuevos Datos

1. **Descargar archivo** → `data/raw/` con nombre descriptivo
2. **Documentar fuente** → Crear `data/raw/README.md` con metadatos
3. **Procesar si es necesario:**
   - Crear script en `src/cannabis_tax/io/ingest_sources.py`
   - Guardar versión limpia en `data/processed/`
   - Incluir `*_metadata.json`
4. **Actualizar configs** en `configs/features.yaml` si aplica

---

## Licencias y Atribuciones

- **DANE**: Datos públicos bajo licencia CC-BY-4.0
- **Banco de la República**: Datos públicos
- **Otros**: Verificar términos de uso antes de publicar

---

## Tamaño Aproximado de Archivos

```
data/raw/       ~50 MB (datasets crudos)
data/interim/   ~100 MB (datos intermedios)
data/processed/ ~30 MB (datos finales)
data/external/  0 MB (reservado)
```

**Nota:** Archivos > 100 MB pueden ser ignorados en Git. Ver `.gitignore`.
