# Formulación Matemática Formal
## Estimación de Recaudo Tributario Incremental por Legalización de Cannabis

---

## 1. Definiciones Formales

### 1.1 Objetivo Principal

**Estimar el recaudo tributario incremental anual** que genera la legalización de la distribución de marihuana en Colombia bajo diferentes escenarios de política tributaria y regulatoria.

**Variable de resultado:**
$$R^{\text{cannabis}}(s) = \text{Recaudo anual en COP bajo escenario } s$$

Donde $s \in \{\text{Conservador, Base, Progresivo}\}$ o cualquier otra parametrización de política.

### 1.2 Componentes del Recaudo

El recaudo total se descompone en:

$$R^{\text{cannabis}}(s) = R^{\text{IVA}}(s) + R^{\text{ISC}}(s) + R^{\text{Corp}}(s)$$

**Donde:**
- $R^{\text{IVA}}(s)$ = Recaudo por Impuesto al Valor Agregado (19% sobre base)
- $R^{\text{ISC}}(s)$ = Recaudo por Impuesto Selectivo al Consumo ($\tau_{\text{ISC}}$ variable por escenario)
- $R^{\text{Corp}}(s)$ = Recaudo por Impuesto a la Renta Corporativa (30% sobre utilidades)

---

## 2. Modelo de Base Tributaria

### 2.1 Demanda de Cannabis Legal

La base tributaria depende del volumen anual consumido que migra del mercado ilegal al legal:

$$B^{\text{legal}}(s) = Q_0 \times \left(1 + \epsilon_P \cdot \ln\frac{P_{\text{legal}}}{P_0}\right) \times \lambda(s) \times (1 - \rho)$$

**Componentes:**
- $Q_0$ = Consumo base anual estimado de la ENCSPA 2019 (COP)
- $\epsilon_P$ = Elasticidad precio de demanda (estimada con two-part GLM)
- $P_{\text{legal}}$ = Precio unitario del producto legal (COP/gramo) bajo escenario $s$
- $P_0$ = Precio actual del mercado ilegal (estimado desde ENCSPA)
- $\lambda(s) \in [0, 1]$ = Tasa de penetración del mercado legal bajo escenario $s$
- $\rho \in [0, 1]$ = Tasa de subreporte/evasión fiscal

### 2.2 Expansión de la Base

Si existen datos regionales o por cohorte, la base se puede desagregar:

$$B^{\text{legal}}(s) = \sum_{r=1}^{R} \sum_{d=1}^{D} B^{\text{legal}}_{r,d}(s)$$

Donde:
- $r$ = región geográfica (13 departamentos de referencia)
- $d$ = decil de ingresos o quintil socioeconómico

---

## 3. Modelo de Dos Partes para Consumo

### 3.1 Probabilidad de Consumo

La decisión de consumir sigue un modelo Logit:

$$P(\text{consumidor}_i = 1 | \mathbf{X}_i) = \frac{e^{\mathbf{X}_i \boldsymbol{\beta}}}{1 + e^{\mathbf{X}_i \boldsymbol{\beta}}} = \Lambda(\mathbf{X}_i \boldsymbol{\beta})$$

**Regresores $\mathbf{X}_i$ incluyen:**
- Edad, edad² (capturar efectos no lineales)
- Log(Ingresos)
- Educación (variable dummy)
- Región de residencia (variables dummy)
- (Opcional) Ciclo macroeconómico: PIB, IPC, TRM

### 3.2 Intensidad de Gasto

Para quienes consumen ($y_i^{\text{consumo}} = 1$), el gasto esperado se modela con una familia GLM:

$$E[y_i^{\text{gasto}} | y_i^{\text{consumo}} = 1, \mathbf{X}_i] = g^{-1}(\mathbf{X}_i \boldsymbol{\gamma})$$

**Donde:**
- $g(\cdot)$ es una función link (típicamente log para bienes normales)
- Distribución de $y_i^{\text{gasto}}$: Gamma o Poisson (diagnosis con gráficos residuales)
- $\boldsymbol{\gamma}$ = parámetros del gasto condicional

### 3.3 Esperanza Conjunta

La esperanza del gasto marginal es:

$$E[y_i^{\text{gasto}} | \mathbf{X}_i] = \Lambda(\mathbf{X}_i \boldsymbol{\beta}) \times E[y_i^{\text{gasto}} | y_i^{\text{consumo}} = 1, \mathbf{X}_i]$$

Agregando sobre toda la población:

$$Q_0 = \sum_{i=1}^{n} w_i \times E[y_i^{\text{gasto}} | \mathbf{X}_i]$$

Donde $w_i$ es el factor de expansión DANE para la observación $i$.

---

## 4. Cálculo de Recaudo por Tipo de Impuesto

### 4.1 Recaudo por IVA

$$R^{\text{IVA}}(s) = B^{\text{legal}}(s) \times \tau_{\text{IVA}} = B^{\text{legal}}(s) \times 0.19$$

El IVA es una tasa fija del 19% en Colombia (salvo excepciones).

### 4.2 Recaudo por Impuesto Selectivo al Consumo (ISC)

$$R^{\text{ISC}}(s) = B^{\text{legal}}(s) \times \tau_{\text{ISC}}(s)$$

Donde $\tau_{\text{ISC}}(s)$ varía por escenario de política:
- **Escenario Conservador:** $\tau_{\text{ISC}} = 0.05$ (5%)
- **Escenario Base:** $\tau_{\text{ISC}} = 0.10$ (10%)
- **Escenario Progresivo:** $\tau_{\text{ISC}} = 0.15$ (15%)

**Nota:** ISC en otros bienes pecaminosos en Colombia: cigarrillos 15–20%, alcohol 8–12%

### 4.3 Recaudo por Impuesto a la Renta Corporativa

Aproximación simplificada:

$$R^{\text{Corp}}(s) = \Pi^{\text{neta}}(s) \times \tau_r = \left[\text{Ingresos} - \text{Costos de producción}\right]_{(s)} \times 0.30$$

**Supuestos simplificadores:**
- Margen de costo de producción estimado en 30–40% de ingresos brutos
- Utilidad neta = $B^{\text{legal}}(s) \times 0.65$
- Tasa de renta: 30% sobre utilidades

Resultado:
$$R^{\text{Corp}}(s) = B^{\text{legal}}(s) \times 0.65 \times 0.30 = B^{\text{legal}}(s) \times 0.195$$

### 4.4 Recaudo Total Agregado

$$R^{\text{cannabis}}(s) = B^{\text{legal}}(s) \times (0.19 + \tau_{\text{ISC}}(s) + 0.195)$$

$$= B^{\text{legal}}(s) \times (0.385 + \tau_{\text{ISC}}(s))$$

**Tasas de recaudo agregadas por escenario:**
- **Conservador:** $\tau_{\text{total}} = 0.435$ (43.5%)
- **Base:** $\tau_{\text{total}} = 0.485$ (48.5%)
- **Progresivo:** $\tau_{\text{total}} = 0.535$ (53.5%)

---

## 5. Elasticidades y Parametrización

### 5.1 Elasticidad Precio

La elasticidad precio de demanda se estima de forma estructural o reducida:

**Enfoque estructural (two-part):**
$$\epsilon_P = \frac{\partial \ln E[y | \mathbf{X}]}{\partial \ln P} = \frac{\partial (\ln \Lambda + \ln E[\cdot | \text{consumidor}=1])}{\partial \ln P}$$

**Esperado (literatura):** $\epsilon_P \in [-1.2, -0.4]$ para bienes pecaminosos

**Datos internacionales de referencia:**
| País | Producto | $\epsilon_P$ | Fuente |
|------|----------|-----------|--------|
| USA | Cigarrillos | -0.35 | Chaloupka & Warner (2000) |
| Canadá | Cigarrillos | -0.52 | TDSB Report (2019) |
| Uruguay | Cannabis (post-legal) | -0.68 | Estimado |
| Canadá | Cannabis | -0.45 a -0.85 | Stehr (2007) adaptado |

### 5.2 Penetración de Mercado Legal

La tasa de penetración $\lambda(s)$ depende de:
- Precio relativo legal vs. ilegal
- Cobertura geográfica de puntos de venta
- Percepción de calidad y seguridad
- Actividad de contrabando/ilegalidad residual

**Parametrización (exógena de política):**
- $\lambda_{\text{Conservador}} = 0.40$ (40% del consumo actual migra a legal)
- $\lambda_{\text{Base}} = 0.55$ (55%)
- $\lambda_{\text{Progresivo}} = 0.70$ (70%)

**Validación:** Comparar con tasas de penetración post-legalización en Canadá (~75%) y Uruguay (~60%).

### 5.3 Subreporte Fiscal

El parámetro $\rho$ representa la fracción que sigue consumiéndose ilegalmente o sin tributar:

$$\rho \in [0.05, 0.20]$$

**Supuesto:** Incluso post-legalización, una fracción sigue la cadena ilegal (competencia de precios, confianza, etc.).

**Sensibilidad:** Tornado chart variará $\rho$ en $[0, 0.30]$ para identificar su impacto.

---

## 6. Validación y Benchmarking

### 6.1 Validación Cruzada (K-Fold)

Para los modelos de consumo y gasto:

$$\text{CV Error} = \frac{1}{K} \sum_{k=1}^{K} \text{MAE}_k$$

**Criterios de aceptación:**
- $\text{MAE}_{\text{gasto}} < 10\%$ de $\bar{y}$
- $\text{MAE}_{\text{logit}} < 0.15$ en desviaciones cuadráticas medias

### 6.2 Benchmarking contra Literatura

1. **Elasticidades:** Comparar $\hat{\epsilon}_P$ con rango $[-1.2, -0.4]$
2. **Tasa ISC:** Validar contra cigarrillos (15–20%) y alcohol (8–12%)
3. **Penetración:** Contrastar con tasas post-legalización Canadá (75%) y Uruguay (60%)

### 6.3 Pruebas de Especificación

- **Ramsey RESET:** Detección de no-linealidades omitidas
- **VIF:** $\text{VIF}_j < 10$ para multicolinealidad
- **Breusch-Pagan:** Homocedasticidad de residuales
- **Shapiro-Wilk:** $p > 0.05$ para normalidad de residuales

---

## 7. Simulación y Proyección

### 7.1 Escenarios Base

Para cada escenario $s$, se proyecta el recaudo sobre horizonte $T = 10$ años:

$$R^{\text{cannabis}}(s, t) = B^{\text{legal}}(s) \times \left(1 + g_t\right)^{t} \times (0.385 + \tau_{\text{ISC}}(s))$$

Donde $g_t$ es una tasa de crecimiento anual (ej: 5% por adopción creciente de mercado legal).

### 7.2 Análisis de Sensibilidad

**Tornado (variación univariada):**

Para cada parámetro $\theta \in \{P, \lambda, \rho, \tau_{\text{ISC}}\}$:

$$\text{Impacto}(\theta) = \frac{R^{\text{cannabis}}(\theta_{\text{alto}}) - R^{\text{cannabis}}(\theta_{\text{bajo}})}{R^{\text{cannabis}}(\theta_{\text{base}})}$$

**Bootstrap (B = 1,000 iteraciones):**

1. Remuestrear ENCSPA con reemplazo
2. Re-estimar elasticidades $\hat{\epsilon}_P$
3. Recalcular $R^{\text{cannabis}}(s)$ para cada muestra
4. Reportar media, percentil 2.5%, 97.5%

---

## 8. Limitaciones y Caveats

### 8.1 Datos

- **Antigüedad:** ENCSPA 2019 (5+ años); posible drift en preferencias
- **Subreporte:** Encuestas autodeclaradas pueden subestimar consumo real
- **Factores de expansión:** Confiabilidad depende de metodología DANE

### 8.2 Modelo

- **Exogeneidad:** Precio legal $P$ y penetración $\lambda$ son exógenas de política
- **Independencia:** Two-part GLM asume independencia entre decisión y gasto
- **Estática:** Sin dinámica de oferta (ej: entrada de productores, cambios de precios ajuste)

### 8.3 Alcance

- **No incluye:** Comercio B2B, exportación, canales informales post-legalización
- **Elasticidades:** Benchmark internacional; no estimadas localmente en contexto legal
- **Agregación:** Simplificaciones en estructura de costos corporativos

---

## 9. Fórmulas Resumen (Quick Reference)

| Concepto | Fórmula |
|----------|---------|
| Base tributaria legal | $B^{\text{legal}}(s) = Q_0 \times \left(1 + \epsilon_P \ln\frac{P}{P_0}\right) \times \lambda \times (1-\rho)$ |
| Recaudo IVA | $R^{\text{IVA}} = B^{\text{legal}} \times 0.19$ |
| Recaudo ISC | $R^{\text{ISC}} = B^{\text{legal}} \times \tau_{\text{ISC}}$ |
| Recaudo Renta | $R^{\text{Corp}} = B^{\text{legal}} \times 0.195$ |
| **Recaudo Total** | $R^{\text{total}} = B^{\text{legal}} \times (0.385 + \tau_{\text{ISC}})$ |
| P(consumidor) | $\Lambda(\mathbf{X}\boldsymbol{\beta})$ (Logit) |
| E[gasto \| consumo] | $g^{-1}(\mathbf{X}\boldsymbol{\gamma})$ (GLM) |
| Consumo agregado | $Q_0 = \sum w_i \Lambda(\cdot) \times E[\cdot \| \text{consumo}=1]$ |

---

## 10. Referencias de Implementación

**Librerías Python recomendadas:**
- **Statsmodels:** GLM, Logit, diagnósticos
- **Scikit-learn:** Cross-validation, métricas
- **Numpy/Pandas:** Manipulación de datos
- **Matplotlib/Seaborn:** Visualización

**Archivos de código:**
- `src/cannabis_tax/models/ml.py` — Two-part GLM
- `src/cannabis_tax/models/benchmark.py` — Cálculo de recaudo fiscal
- `src/cannabis_tax/scenarios/sensitivity.py` — Tornado + Bootstrap
- `notebooks/02_consumption_modeling.ipynb` — Exploración de modelos

---

**Documento versión 1.0 – 3 de marzo de 2026**  
*Formulación matemática completa para estimación de recaudo tributario.*
