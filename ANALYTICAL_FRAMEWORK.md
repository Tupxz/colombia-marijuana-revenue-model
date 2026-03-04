# Marco Analítico y Plan de Trabajo
## Estimación de Recaudo Tributario Incremental por Legalización de Marihuana en Colombia

---

## 1. Formulación del Problema

### 1.1 Objetivo Principal (A)

**Estimar y simular el recaudo tributario incremental anual** que generaría la legalización de la distribución de marihuana en Colombia, bajo diferentes escenarios tributarios y de penetración de mercado legal.

**Variable dependiente Y:**
- $R^{\text{cannabis}}_t(s)$ = Recaudo incremental anual (COP) en el año $t$ bajo escenario $s$
- Componentes: Recaudo por Impuesto al Valor Agregado (IVA) + Impuestos Selectivos al Consumo (ISC) + Renta corporativa

**Variables explicativas X (para estimar consumo y penetración):**
- **Sociodemográficas:** edad, ingresos, educación, región geográfica (de ENCSPA 2019)
- **Opcionales (si hay variación temporal/regional):** proxy de demanda (Google Trends), ciclo macroeconómico (PIB trimestral, IPC, TRM)

**Naturaleza del resultado:**
- Simulación contrafactual: combina datos históricos de consumo ilegal (ENCSPA) con supuestos sobre transición a mercado legal
- No es predicción pura, sino cuantificación de escenarios bajo parámetros de política tributaria y regulatoria

### 1.2 Extensión Futura (B)

Descomposición del recaudo total según estructura tributaria DIAN (vector de tasas e impuestos que suma 1):
- Participación relativa de IVA vs. ISC vs. impuesto a la renta
- Sensibilidad de cada componente a cambios en precios y volúmenes

---

## 2. Bloque de Texto para Paper/README (12–15 líneas)

```
Metodología

Este estudio estima el recaudo tributario incremental anual (R^cannabis_t(s)) 
generado por la legalización de la distribución de marihuana en Colombia bajo 
escenarios tributarios variados. La variable dependiente es el recaudo esperado 
en COP por año, desglosado por tipo de impuesto (IVA, ISC, renta). 

Las variables explicativas incluyen características sociodemográficas de 
consumidores potenciales (edad, ingresos, educación, región) extraídas de la 
ENCSPA 2019, complementadas con proxies de demanda (Google Trends, PIB, IPC) 
si existe variación temporal o regional.

El análisis se basa en una simulación contrafactual que transforma datos 
de consumo ilegal en consumo legal bajo tres supuestos clave: (i) precio 
unitario legal P, (ii) penetración de mercado legal λ [0,1], y (iii) tasa 
de subreporte fiscal. El modelo combina benchmarking fiscal (base tributaria 
× tasas) con modelos de demanda para consumo/gasto, evitando usar ML como 
sustituto de la lógica tributaria sino como herramienta para estimar 
parámetros de entrada.
```

---

## 3. Pipeline por Etapas (6 Fases)

### **Etapa 1: Ingestión y Limpieza – Dataset "market_base"**
**Input:** ENCSPA 2019 (capítulo marihuana) + metadatos DANE  
**Output:** `market_base.csv` (consumo semanal/mensual, gasto mensual, precio implícito, frecuencia, sociodemografía)

**Tareas:**
- Identificar y seleccionar variables de consumo (¿cuántas veces por semana? ¿gasto mensual?)
- Extraer factores de expansión DANE si están disponibles
- Imputar valores faltantes (método: MAR o MCAR según diagnóstico)
- Crear categorías de consumidores: no consumidores, ocasionales, frecuentes
- Output: base microeconómica lista para agregación

**Responsable:** `src/cannabis_tax/io/` + `src/cannabis_tax/cleaning/`

---

### **Etapa 2: Expansión Nacional y Cálculo de Base Consumo**
**Input:** `market_base.csv`  
**Output:** `market_aggregate_annual.csv` (consumo total COP/año, por región y nivel socioeconómico)

**Tareas:**
- Aplicar factores de expansión DANE a nivel nacional
- Estimar consumo anual (COP) mediante:
  - Agregación: $Q_{\text{anual}} = \sum (\text{gasto mensual} \times 12) \times \text{factor expansión}$
  - Validación contra estimaciones indirectas (elasticidad, benchmark internacional)
- Desglosar por:
  - Región geográfica (13 departamentos o agrupaciones)
  - Quintil de ingresos
  - Grupo de edad (18–25, 26–35, 36–50, 50+)
- Outputs:
  - `market_volumes_cop_annual.csv`: consumo total por cohort
  - `market_penetration_baseline.csv`: % consumidores por estrato

**Responsable:** `src/cannabis_tax/features/build_features.py`

---

### **Etapa 3: Modelado de Consumo y Penetración (ML + Supuestos)**
**Input:** `market_aggregate_annual.csv` + sociodemografía + proxies (Google Trends, macro)  
**Output:** `consumption_elasticity_estimates.csv` + `penetration_transition_matrix.csv`

**Tareas:**
- **Modelo de consumo (two-part si hay muchos ceros):**
  - Parte 1: Logit/Probit para P(consumidor = 1 | sociodemografía, macro)
  - Parte 2: GLM o regresión robusta para E[gasto | consumidor=1, sociodemografía]
  - Validar con cross-validation (5-fold) y métricas (MAE, RMSE, MAPE)
  
- **Modelo de penetración legal:**
  - Estimar elasticidad precio del consumo ($\epsilon_P$)
  - Estimar elasticidad de penetración a cambios en penetración legal ($\epsilon_\lambda$)
  - Usar datos internacionales (Canadá, Uruguay, USA) como benchmark si hay brechas
  
- **Supuestos exógenos (input de política):**
  - Precio legal $P$ en COP/gramo (ej: $8,000–15,000)
  - Penetración legal esperada $\lambda \in [0.3, 0.7]$ (qué % del consumo migra al mercado legal)
  - Subreporte $\rho \in [0.05, 0.20]$ (qué % se sigue consumiendo/traficando ilegalmente)

**Outputs:**
  - `elasticity_estimates.csv`: sensibilidad estimada a P y λ
  - `scenarios_penetration.csv`: matriz de penetración por escenario
  - `model_diagnostics.png`: residuales, Q-Q plots, VIF

**Responsable:** `src/cannabis_tax/models/ml.py` (two-part GLM, cross-validation)

---

### **Etapa 4: Cálculo de Recaudo Tributario por Escenario**
**Input:** `market_aggregate_annual.csv` + `elasticity_estimates.csv` + supuestos de política (P, λ, τ)  
**Output:** `revenue_by_scenario.csv` + `revenue_decomposition.csv`

**Tareas:**
- **Fórmula base de recaudo:**
  $$R^{\text{cannabis}}_t(s) = Q^{\text{baseline}} \times (1 + \epsilon_P \cdot \ln(P/P_0)) \times \lambda(s) \times (1 - \rho) \times \tau(s)$$
  
  donde:
  - $Q^{\text{baseline}}$ = consumo base anual (COP)
  - $\epsilon_P$ = elasticidad precio estimada en Etapa 3
  - $P$ = precio legal bajo escenario $s$
  - $P_0$ = precio actual (negro)
  - $\lambda(s)$ = penetración de mercado legal bajo escenario $s$
  - $\rho$ = tasa de subreporte
  - $\tau(s)$ = tasa tributaria efectiva bajo escenario $s$ (IVA 19% + ISC variable + otros)

- **Desglose por tipo de impuesto:**
  - IVA = $R^{\text{cannabis}}_t(s) \times 0.19$ (tasa estándar)
  - ISC = $R^{\text{cannabis}}_t(s) \times \tau_{\text{ISC}}$ (ej: 5–15% según escenario)
  - Renta corporativa = $(R^{\text{cannabis}}_t(s) - \text{costos}) \times 0.30$ (simplificado)

- **Escenarios base:**
  - Conservador: $P = 8,000$ COP/g, $\lambda = 0.40$, $\tau_{\text{ISC}} = 0.05$
  - Base: $P = 12,000$ COP/g, $\lambda = 0.55$, $\tau_{\text{ISC}} = 0.10$
  - Progresivo: $P = 15,000$ COP/g, $\lambda = 0.70$, $\tau_{\text{ISC}} = 0.15$

**Outputs:**
  - `revenue_baseline_2026_2035.csv`: proyección 10 años por escenario
  - `revenue_by_taxtype.csv`: desglose IVA, ISC, renta
  - `revenue_summary.txt`: tabla resumen (COP miles de millones)

**Responsable:** `src/cannabis_tax/models/benchmark.py`

---

### **Etapa 5: Análisis de Sensibilidad y Robustez**
**Input:** `revenue_by_scenario.csv` + elasticity estimates + supuestos  
**Output:** `sensitivity_tornado.png` + `sensitivity_table.csv` + `bootstrap_ci.csv`

**Tareas:**
- **Tornado chart (sensibilidad univariada):**
  - Variar $P \in [7,000 – 18,000]$ COP/g → impacto en recaudo
  - Variar $\lambda \in [0.20 – 0.80]$ → impacto en recaudo
  - Variar $\rho \in [0.00 – 0.30]$ → impacto en recaudo
  - Variar $\tau_{\text{ISC}} \in [0.00 – 0.25]$ → impacto en recaudo
  - Identificar parámetro con mayor influencia

- **Bootstrap (si hay estimaciones de elasticidad):**
  - Remuestrear ENCSPA con reemplazo (B = 1,000 iteraciones)
  - Recalcular elasticidades y recaudo para cada muestra
  - Generar intervalos de confianza (IC 95%) para recaudo

- **Análisis two-way (si hay presupuesto):**
  - Matriz de recaudo para pares (P, λ) con contornos

**Outputs:**
  - `sensitivity_tornado.png`: gráfico de barras horizontal
  - `bootstrap_ci_revenue.csv`: media, percentil 2.5, 97.5
  - `sensitivity_report.txt`: resumen de hallazgos

**Responsable:** `src/cannabis_tax/scenarios/sensitivity.py`

---

### **Etapa 6: Validación, Reportes y Documentación**
**Input:** Todos los outputs anteriores  
**Output:** Paper draft + notebooks Jupyter + tablas finales

**Tareas:**
- **Validación cruzada (si hay predicción micro):**
  - K-fold CV (k=5) para modelos two-part en Etapa 3
  - Reportar MAE, RMSE, MAPE en datos held-out
  
- **Benchmarking fiscal:**
  - Comparar elasticidades estimadas con literatura (Chaloupka & Warner 2000, estudios Canadá/Uruguay)
  - Validar tasa ISC contra otros bienes pecaminosos (cigarrillos, alcohol)
  - Documentar supuestos de precios internacionales

- **Limitaciones y caveats:**
  - ENCSPA 2019: envejecimiento (5+ años), posible cambio de preferencias
  - Subreporte: supuesto exógeno, sin validación
  - No incluye: comercio informal/ilegal post-legalización, canales B2B, exportación
  - Elasticidades: benchmark internacional, no estimado localmente en contexto legal

- **Outputs finales:**
  - `paper_draft.tex`: 15–20 páginas con metodología, resultados, sensibilidad
  - `notebooks/03_revenue_simulation.ipynb`: análisis interactivo
  - `tables/revenue_summary_all_scenarios.xlsx`: tablas para anexo

**Responsable:** `reports/` + `notebooks/`

---

## 4. Benchmark Fiscal Coherente con Objetivo A

### 4.1 Estructura del Benchmark

**Enfoque: Impuesto al Valor Agregado (IVA) + Impuesto Selectivo al Consumo (ISC) + Renta Corporativa**

**Modelo fiscal base:**
$$R_t = B_t \times \tau$$

donde:
- $B_t$ = Base tributaria (gasto de consumidores en marihuana legal, COP)
- $\tau$ = Tasa tributaria efectiva agregada (IVA + ISC + otros)

**Desglose:**
- **IVA:** $\tau_{\text{IVA}} = 0.19$ (tasa estándar en Colombia)
- **ISC:** $\tau_{\text{ISC}} \in [0.05 – 0.15]$ según escenario de política (variable exógena)
- **Renta corporativa:** $\tau_r = 0.30$ (tasa general) aplicada a utilidades (simplificado)

**Agregación:**
$$R_t = B_t \times (0.19 + \tau_{\text{ISC}}) + (\text{Utilidades corporativas}) \times 0.30$$

### 4.2 Two-Part Model para Consumo/Gasto (si hay ceros)

**Parte 1: Decisión de consumo (Logit/Probit)**
$$P(\text{consumidor}_i = 1) = \Phi(\mathbf{X}_i \boldsymbol{\beta})$$

Regresores: edad, ingresos, educación, región

**Parte 2: Intensidad de gasto (GLM con link log)**
$$E[\text{gasto}_i | \text{consumidor}_i = 1, \mathbf{X}_i] = \exp(\mathbf{X}_i \boldsymbol{\gamma})$$

Distribución: Gamma o Poisson (según diagnóstico de datos)

**Recaudo total:**
$$R = \sum_i P(\text{consumidor}_i=1) \times E[\text{gasto}_i | \text{consumidor}_i=1]$$

### 4.3 Validación del Benchmark

- Comparar tasa ISC estimada vs. cigarrillos (15–20% en Colombia) y alcohol (8–12%)
- Validar elasticidad precio contra literatura: bienes pecaminosos típicamente $|\epsilon| \in [0.4 – 1.0]$
- Usar datos de Canadá/Uruguay post-legalización como "out-of-sample" validation

---

## 5. Rol de Machine Learning (Aclaratorio)

### 5.1 ¿Dónde SÍ entra ML?

1. **Estimación de consumo y gasto:**
   - Two-part GLM (o Logit + regresión robusta) con validación cruzada
   - Objetivo: mejorar predicción de E[gasto | sociodemografía, macro] vs. regresión lineal simple

2. **Estimación de elasticidades (opcional):**
   - Modelar consumo como función de precio con efectos no lineales
   - Usar splines o polinomios si hay evidencia de no-linealidad
   - ML tree-based (Random Forest, XGBoost) para feature importance de sociodemografía

3. **Proyección de penetración legal (si hay variación temporal):**
   - ARIMA o suavizado exponencial si hay series temporales de adopción en otros países
   - Redes neuronales solo si hay datos suficientes (n > 1,000 observaciones)

### 5.2 ¿Dónde NO entra ML?

- ❌ **No usar ML como "caja negra" para recaudo total:** El recaudo es función determinística de política (P, τ, λ), no predicción
- ❌ **No reemplazar modelo fiscal con regresión de recaudo:** La estructura tributaria es exógena e interpretable, no debe ser "aprendida"
- ❌ **No usar deep learning sin justificación:** Complejidad no mejoraría resultados si la relación X → Y es lineal/monótona

### 5.3 Implementación

**Archivo principal:** `src/cannabis_tax/models/ml.py`

```python
# Pseudocódigo
def two_part_glm(data, X_cols, y_consumption, y_spending):
    """
    Two-part GLM: Logit para decisión de consumo, GLM para gasto.
    """
    # Parte 1: P(consume=1 | X)
    logit = LogisticRegression()
    logit.fit(data[X_cols], y_consumption)
    
    # Parte 2: E[gasto | consume=1, X]
    consumers = data[y_consumption == 1]
    glm = sm.GLM(consumers[y_spending], consumers[X_cols], 
                 family=sm.families.Gamma(link=sm.genmod.coremod.links.log))
    glm.fit()
    
    # Validación cruzada
    cv_results = cross_validate(logit, data[X_cols], y_consumption, cv=5)
    
    return logit, glm, cv_results
```

---

## 6. Checklist de Robustez

### 6.1 Validación Estadística

- [ ] **Datos:** 
  - [ ] Verificar tasas de respuesta ENCSPA por estrato
  - [ ] Diagnosticar patrón de faltantes (MCAR vs. MAR)
  - [ ] Validar factores de expansión DANE

- [ ] **Modelos de consumo:**
  - [ ] Test de bien especificación (Ramsey RESET para lineales)
  - [ ] VIF < 10 para multicolinealidad
  - [ ] Residuales aproximadamente normales (Shapiro-Wilk p > 0.05)
  - [ ] Cross-validation: MAE < 10% de media de Y

- [ ] **Elasticidades:**
  - [ ] Contrastar con Chaloupka & Warner (2000): rango esperado $|\epsilon| \in [0.4 – 1.2]$
  - [ ] Contrastar con Canada Revenue Agency (post-Cannabis Act 2018)
  - [ ] Analizar heterogeneidad por grupo de edad/ingresos

### 6.2 Sensibilidad y Robustez

- [ ] **Tornado chart:** Identificar parámetros con mayor impacto en recaudo
- [ ] **Bootstrap (B = 1,000):** IC 95% para estimadores de elasticidad
- [ ] **Escenarios alternativos:** 
  - [ ] Pesimista: λ = 0.30, τ_ISC = 0.05
  - [ ] Base: λ = 0.55, τ_ISC = 0.10
  - [ ] Optimista: λ = 0.70, τ_ISC = 0.15
- [ ] **Análisis two-way:** Matriz de recaudo para pares (P, λ)
- [ ] **Validación cruzada:** K-fold CV (k=5) en modelos predictivos

### 6.3 Limitaciones Documentadas

- [ ] **Datos:**
  - [ ] ENCSPA 2019: envejecimiento (5+ años), cambios de preferencias no capturados
  - [ ] Subreporte: supuesto exógeno sin validación empírica local
  
- [ ] **Alcance:**
  - [ ] No incluye: canales B2B, exportación, comercio informal post-legalización
  - [ ] Elasticidades: benchmark internacional, no localmente estimadas en contexto legal
  - [ ] Horizonte: simulaciones 10 años sin ajustes dinámicos de oferta/demanda
  
- [ ] **Modelo:**
  - [ ] Two-part GLM: supone independencia entre decisión de consumo y gasto
  - [ ] Precio legal exógeno: no hay endogeneidad de oferta

### 6.4 Reproducibilidad

- [ ] **Datos:** Código para limpiar ENCSPA en `src/cannabis_tax/io/ingest_sources.py`
- [ ] **Modelos:** Coeficientes y diagnostics guardados en `runs/YYYY-MM-DD__scenario/tables/`
- [ ] **Resultados:** Tablas y figuras reproducibles con `python -m cannabis_tax.cli scenarios`
- [ ] **Paper:** Números en paper = números en outputs (versionado con hash de datos)

---

## 7. Cronograma Estimado y Responsables

| Etapa | Tarea | Plazo | Responsable |
|-------|-------|-------|------------|
| 1 | Limpieza ENCSPA → market_base | 1 sem | Datos/Limpieza |
| 2 | Agregación nacional → consumo anual | 1 sem | Features |
| 3 | Two-part GLM + elasticidades | 2 sem | ML/Modelos |
| 4 | Cálculo de recaudo por escenario | 1 sem | Benchmarking |
| 5 | Sensibilidad + bootstrap | 1.5 sem | Escenarios |
| 6 | Paper + reportes finales | 1 sem | Reporte |
| **TOTAL** | | **~8 semanas** | Team |

---

## 8. Estructura de Archivos del Proyecto

```
src/cannabis_tax/
├── io/ingest_sources.py          ← Etapa 1: Limpiar ENCSPA
├── features/build_features.py    ← Etapa 2: Agregación nacional
├── models/
│   ├── ml.py                     ← Etapa 3: Two-part GLM
│   ├── benchmark.py              ← Etapa 4: Cálculo de recaudo fiscal
│   └── evaluate.py               ← Validación de modelos
├── scenarios/
│   ├── simulate.py               ← Etapa 4: Recaudo por escenario
│   └── sensitivity.py            ← Etapa 5: Tornado + Bootstrap
└── viz/plots.py                  ← Visualización de resultados

configs/
├── scenarios.yaml                ← Definición de escenarios (P, λ, τ)
└── features.yaml                 ← Especificación de variables X

reports/
├── paper.tex                     ← Etapa 6: Paper final
└── figures/                      ← Tornado, boxplots, tablas

runs/
└── YYYY-MM-DD__scenario/
    ├── tables/
    │   ├── market_base.csv
    │   ├── revenue_by_scenario.csv
    │   └── sensitivity_table.csv
    └── figures/
        ├── sensitivity_tornado.png
        └── revenue_projection.png

notebooks/
├── 01_exploratory_encspa.ipynb    ← EDA de datos crudos
├── 02_consumption_modeling.ipynb  ← Exploración two-part GLM
└── 03_revenue_simulation.ipynb    ← Escenarios interactivos
```

---

**Documento versión 1.0 – 3 de marzo de 2026**  
*Marco analítico completo para estimación de recaudo tributario por legalización de cannabis en Colombia.*
