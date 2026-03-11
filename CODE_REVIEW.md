# Code Review y Revisión Académica
## Proyecto: colombia-marijuana-revenue-model

**Fecha**: 10 de marzo de 2026  
**Enfoque**: Coherencia documentación, código, datos y reproducibilidad

---

## 1. FINDINGS (Hallazgos)

### 1.1 CRÍTICO: Discrepancia en tamaño muestral reportado

**Ubicación**: 
- `reports/resultados_propension.tex`: "3980 observaciones"
- `reports/tables/propension_fit_summary.tex`: "N = 3980"
- `reports/paper.tex`: "3980 observaciones"
- `src/cannabis_tax/analysis/modeling.py`: implícito en `merge_model_sources()`

**Problema**: 
El paper (línea ~90) dice:
> "La verificación de llaves mostró coincidencia completa entre la base de consumo y las tablas personas y d2 para las 3982 observaciones disponibles"

Pero luego reporta 3980 para MCO completo. **¿Se perdieron 2 observaciones en alguna etapa de limpieza?**

**Impacto**: Bajo (diferencia mínima), pero afecta reproducibilidad. Necesita explicación clara en el texto.

---

### 1.2 INCONSISTENCIA: Especificación sin precio no está clara en el código

**Ubicación**: `src/cannabis_tax/analysis/modeling.py`, función `_build_formula()`

**Problema**: 
- La función detecta si `log_precio_compra` está en las columnas para decidir si incluirlo
- Pero el paper dice "Se estimaron cuatro especificaciones" (dos sin precio, dos con precio)
- El código de `prepare_propensity_regression_data()` con `require_price=True` es lo que hace que desaparezcan observaciones
- **No está claro en qué punto exacto se generan las dos muestras (amplia y restringida)**

**Riesgo metodológico**: Un reproductor podría no darse cuenta de que hay dos caminos de datos distintos.

---

### 1.3 ADVERTENCIA: Educación binaria vs. tres categorías

**Ubicación**:
- `data/processed/variables.tex`: "agrupar categorias si la muestra por nivel educativo es pequeña"
- `src/cannabis_tax/analysis/modeling.py`: `EDUCATION_GROUPS` agrupa en 3 categorías (Baja, Media, Superior)
- `reports/paper.tex`: Menciona "tres categorías estables"
- Tabla de benchmark: Reporta "Educacion media" y "Educacion superior" (omitiendo la referencia base "Baja")

**Problema**: 
La tabla está reportando dos dummies educativas. **¿Cuál es la categoría de referencia?** El texto no lo aclara. ¿Es "Baja"? Esto es estándar en econometría, pero debe estar explícito.

---

### 1.4 Incoherencia menor: Nombres de modelos

**Ubicación**: 
- `results_propension.tex`: "MCO completa", "MCO con precio", "Probit completo", "Probit con precio"
- `src/cannabis_tax/analysis/modeling.py`: MODEL_LABELS tiene "MCO completa" pero en inglés los comentarios dicen "OLS benchmark"
- `paper.tex`: Más formal, llama "modelo lineal de probabilidad" al LPM

**Impacto**: Muy bajo. Solo se nota en la consistencia de nombres.

---

### 1.5 CRÍTICO: La variable precio no explica por qué desaparece

**Ubicación**: `reports/resultados_propension.tex` y `paper.tex` mencionan reducción de 3980 a 755, pero no explican:

1. ¿Por qué 755 casos tienen precio válido?
2. ¿Cuál es la distribución de casos con precio entre consumidores y no consumidores?
3. `variables.tex` menciona "220 casos con precio no nulo entre observaciones no consumidoras en 12 meses y 603 entre consumidoras" → Esto debería estar en el paper principal para entender la selección

**Impacto**: Alto. Es crucial para interpretar el coeficiente de precio.

---

### 1.6 Falta de validación cruzada de números

**Ubicación**: Comparar `variables.tex` (tabla de disponibilidad) con outputs actuales

**Problema**:
- `variables.tex` (línea 107-110): reporta números de cobertura de variables basados en inspección anterior
- No hay una tabla en el notebook o en el paper que valide si estos números siguen siendo correctos en la base construida
- El merge podría haber alterado la estructura

**Riesgo**: Desincronización silenciosa entre documentación y estado actual del código.

---

### 1.7 MENOR: Logaritmo de precio sin comentario sobre el rango

**Ubicación**: 
- `src/cannabis_tax/analysis/modeling.py`: `df["log_precio_compra"] = np.log(df["precio_compra"])`
- `reports/paper.tex`: Ecuaciones usan \(\log(precio_i)\)

**Problema**: 
No hay validación visible de que `precio_compra` sea estrictamente positivo antes del logaritmo. La función `clean_positive_numeric()` lo asegura, pero esto no está documentado en el texto.

---

## 2. OPEN QUESTIONS

### 2.1 ¿Qué pasó con 2 observaciones?
En `variables.tex` se dice "3982 observaciones disponibles", pero luego se reportan 3980. ¿Dónde se pierden? ¿En la limpieza? ¿En el merge?

### 2.2 ¿La variable de respuesta es binaria o tiene categorías?
- `recode_propensity_target()` convierte a binaria (1/0)
- Pero ¿qué pasa con "No contesta"? Se convierte a 0, lo cual es un supuesto importante no documentado.
- ¿Es correcto asumir que no responder = no consumir?

### 2.3 ¿Por qué la Pseudo-R² baja cuando se agrega precio?
- MCO completo: R² = 0.091
- MCO con precio: R² = 0.061
- ¿Es por selección muestral, o porque el precio es endógeno y confunde la relación?

### 2.4 ¿Hay problemas de multicolinealidad?
El paper no reporta matriz de correlación, VIF, o test de multicolinealidad. ¿Edad y edad² son colineales? (Probablemente sí, pero es normal.)

### 2.5 ¿La muestra con precio es aleatoria?
La teoría econométrica requiere que la selección en precio sea independiente de las variables no observadas. ¿Hay evidencia de esto? ¿O es un supuesto implícito que falta validar?

---

## 3. PROBLEMAS DE REPRODUCIBILIDAD

### 3.1 Carga relativa de rutas
- El notebook usa `project_root = Path.cwd()` y chequea si es 'notebooks'
- Esto es frágil: ¿qué pasa si se ejecuta desde otro lugar?
- Mejor: usar `pyproject.toml` o una variable de entorno

### 3.2 Falta archivo `.gitignore` para archivos generados
- Los archivos de tablas en `reports/tables/` se generan pero no está claro si están en git
- Si están en git, los cambios locales en el código causan diffs enormes
- Se debería generar las tablas en CI/CD, no en git

---

## 4. INCONSISTENCIAS DE REDACCIÓN

### 4.1 En `variables.tex` todavía hay tildes viejas
**Líneas 20-30**: 
- "queda asi" → debería ser "queda así"
- "ultimos" → "últimos"
- "sera" → "será"
- "caractéristicas" → "características"

Nota: Parece que ya fue parcialmente revisado, pero no todo.

### 4.2 El paper es muy técnico para introducción
No es un error, pero `paper.tex` es bastante denso en especificación econométrica para una introducción de Ciencia de Datos. Está bien, pero podría beneficiarse de un párrafo más accesible antes de la Tabla 1.

---

## 5. SHORT SUMMARY (Resumen Breve)

### ✅ Bien hecho:
1. **Estructura reproducible**: El flujo `modeling.py` → `notebook` → `paper.tex` es claro y bien organizado
2. **Documentación de variables**: `variables.tex` es exhaustivo y bien pensado
3. **Transparencia de limitaciones**: El paper explica claramente por qué la muestra con precio es problemática
4. **Coherencia general**: Los tres archivos (paper, resultados, variables) narran una historia consistente

### ⚠️ Problemas que requieren atención:
1. **Discrepancia 3982 vs. 3980**: Explicar dónde se pierden 2 observaciones
2. **Selección muestral en precio**: Documentar mejor por qué baja de 3980 a 755 (los números 603 y 220 deberían estar en el paper)
3. **Supuestos implícitos**: El tratamiento de "No contesta" como no-consumidor debería ser explícito
4. **Reproducibilidad de rutas**: Hacer más robusta la carga de rutas en el notebook

### 🟡 Cosas a revisar opcionalmente:
- Validar diagnósticos de regresión (multicolinealidad, homocedasticidad)
- Incluir una tabla de correlación de variables
- Especificar si la selección en precio es exógena o requiere corrección
- Limpiar acentos residuales en `variables.tex`

---

## 6. PRÓXIMOS PASOS

Enfócate en estos puntos para hacer el documento completamente defensible:

### Nivel 1 - Crítico (Esta semana):
- [ ] Sección "Disponibilidad y calidad de datos": explicar por qué 3982 → 3980
- [ ] Sección "Disponibilidad de datos": incluir "603 consumidores y 220 no-consumidores con precio"
- [ ] Sección "Reglas de limpieza": documentar cómo se codifican K_03 y qué pasa con "No contesta"

### Nivel 2 - Importante (Antes de enviar):
- [ ] Agregar nota al pie en tabla benchmark: especificar categoría de referencia en educación
- [ ] Sección "Especificaciones estimadas": hacer explícita la lógica de dos muestras (amplia vs. restringida)
- [ ] Validar que números en `variables.tex` sigan siendo correctos (ejecutar notebook 02_validation_report)

### Nivel 3 - Opcional (Para siguiente etapa):
- [ ] Limpiar acentos residuales en `variables.tex`
- [ ] Agregar tabla de cobertura de variables en apéndice
- [ ] Considerar discusión de endogeneidad del precio (Heckman u otro método)

---

## Conclusión General

El proyecto tiene una **base metodológica sólida** y **documentación cuidadosa**. Los hallazgos no son bloqueadores, pero sí requieren clarificaciones puntuales para que sea completamente reproducible y defensible académicamente. La estructura actual es un buen punto de partida para agregar machine learning en la siguiente fase.

