# Resumen Ejecutivo del Análisis

## 1. Objetivo del Proyecto

**Estimar el recaudo tributario incremental anual** que generaría la legalización de la distribución de marihuana en Colombia bajo diferentes escenarios de política tributaria y penetración de mercado legal.

---

## 2. Pregunta de Investigación

¿Cuántos COP anuales podría recaudar el Estado colombiano bajo distintos escenarios de legalización (precio legal, tasa de penetración del mercado legal, tasas de impuestos selectivos)?

---

## 3. Datos Principales

- **ENCSPA 2019 (capítulo marihuana):** Consumo actual, gasto, frecuencia, variables sociodemográficas
- **Factores de expansión DANE:** Proyección nacional
- **Datos macroeconómicos:** PIB, IPC, TRM (opcional para validación)
- **Benchmarks internacionales:** Elasticidades de Canadá, Uruguay, USA

---

## 4. Metodología en 6 Etapas

| Etapa | Entrada | Salida | Responsable |
|-------|---------|--------|------------|
| 1. Limpieza | ENCSPA raw | market_base.csv | IO + Cleaning |
| 2. Expansión | market_base | market_aggregate_annual.csv | Features |
| 3. Modelado | Datos + sociodemografía | elasticity_estimates.csv | ML |
| 4. Recaudo fiscal | Elasticidades + supuestos | revenue_by_scenario.csv | Benchmark |
| 5. Sensibilidad | Revenue estimates | sensitivity_tornado.png | Scenarios |
| 6. Reportes | Todos | paper_draft.tex + tablas | Reports |

---

## 5. Modelo Fiscal

**Fórmula de recaudo:**

$$R^{\text{cannabis}}(s) = B^{\text{legal}}(s) \times (0.385 + \tau_{\text{ISC}})$$

Donde:
- $B^{\text{legal}}$ = Base tributaria (gasto de consumidores que migran a legal)
- $0.385$ = Suma de IVA (19%) + Renta corporativa (19.5%)
- $\tau_{\text{ISC}}$ = Impuesto selectivo variable por escenario (5%–15%)

**Base tributaria:**

$$B^{\text{legal}}(s) = Q_0 \times (1 + \epsilon_P \ln P/P_0) \times \lambda \times (1-\rho)$$

Parámetros clave:
- $Q_0$ = Consumo base (ENCSPA expandido)
- $\epsilon_P$ = Elasticidad precio (estimada con two-part GLM)
- $P$ = Precio legal (exógeno de política)
- $\lambda$ = Penetración legal (40%–70% según escenario)
- $\rho$ = Subreporte (5%–20%)

---

## 6. Escenarios Base

| Escenario | Precio Legal | Penetración | ISC | Recaudo % |
|-----------|-------------|------------|-----|----------|
| Conservador | $8,000/g | 40% | 5% | 43.5% |
| Base | $12,000/g | 55% | 10% | 48.5% |
| Progresivo | $15,000/g | 70% | 15% | 53.5% |

*Nota: % es tasa tributaria agregada sobre base legal*

---

## 7. Machine Learning (Rol Específico)

✅ **SÍ entra ML para:**
- Estimar consumo y gasto mediante two-part GLM con validación cruzada
- Detectar heterogeneidad en elasticidades por sociodemografía
- Proyectar penetración legal si hay datos temporales

❌ **NO entra ML para:**
- Predecir recaudo como "caja negra" (es función determinística de política)
- Reemplazar estructura fiscal (es exógena e interpretable)
- Usar deep learning sin datos suficientes

---

## 8. Validación y Robustez

### Validación Estadística
- Cross-validation (K=5): MAE < 10% de media
- Pruebas de especificación: Ramsey RESET, VIF, homocedasticidad
- Benchmarking: elasticidades vs. Chaloupka & Warner (2000), Canadá, Uruguay

### Sensibilidad
- **Tornado chart:** Variar $P$, $\lambda$, $\rho$, $\tau_{\text{ISC}}$ → identificar impacto
- **Bootstrap:** 1,000 remuestreos ENCSPA → IC 95% de recaudos
- **Escenarios two-way:** Matriz de recaudo para pares (P, λ)

### Limitaciones
- ENCSPA 2019: envejecimiento (5+ años)
- Subreporte: asumido exógenamente sin validación local
- Alcance: no incluye canales B2B, exportación, comercio informal post-legal
- Elasticidades: benchmark internacional, no estimadas localmente en contexto legal

---

## 9. Salidas Esperadas

### Tablas y Datos
- `market_base.csv`: 10K–50K obs., variables de consumo + sociodemografía
- `revenue_by_scenario.csv`: Recaudo anual 10 años × 3 escenarios
- `sensitivity_table.csv`: Impacto de cada parámetro en recaudo

### Figuras
- `sensitivity_tornado.png`: Barras horizontales de elasticidad de recaudo
- `revenue_projection.png`: Líneas de proyección 10 años por escenario
- `bootstrap_ci.png`: Intervalos de confianza de elasticidades

### Documentación
- `paper_draft.tex`: 15–20 páginas metodología + resultados + sensibilidad
- `notebooks/02_consumption_modeling.ipynb`: Two-part GLM exploratorio
- `notebooks/03_revenue_simulation.ipynb`: Escenarios interactivos

---

## 10. Cronograma

| Semana | Hito |
|--------|-----|
| 1 | Limpieza ENCSPA → market_base |
| 2 | Agregación nacional |
| 3–4 | Two-part GLM + elasticidades |
| 5 | Cálculo de recaudo |
| 6–7 | Sensibilidad + bootstrap |
| 8 | Paper + reportes finales |

---

## 11. Referencias de Implementación

**Archivos principales:**
- `src/cannabis_tax/models/ml.py` — Two-part GLM (Logit + GLM)
- `src/cannabis_tax/models/benchmark.py` — Cálculo fiscal de recaudo
- `src/cannabis_tax/scenarios/sensitivity.py` — Tornado + Bootstrap

**Configuración:**
- `configs/scenarios.yaml` — Definición de escenarios (P, λ, τ)
- `configs/features.yaml` — Especificación de variables X

---

## 12. Pasos Inmediatos

1. [ ] Revisar ANALYTICAL_FRAMEWORK.md (plan completo con 6 etapas)
2. [ ] Revisar METHODOLOGY_FORMAL.md (fórmulas matemáticas)
3. [ ] Iniciar Etapa 1: Limpieza ENCSPA → `market_base.csv`
4. [ ] Explorar datos con `notebooks/01_exploratory_encspa.ipynb`
5. [ ] Definir escenarios finales en `configs/scenarios.yaml`

---

**Versión: 1.0 | Fecha: 3 de marzo de 2026**

Para detalles completos, ver:
- 📋 **ANALYTICAL_FRAMEWORK.md** — Plan de trabajo detallado (6 etapas, checklist, cronograma)
- 📐 **METHODOLOGY_FORMAL.md** — Formulación matemática completa y validación
