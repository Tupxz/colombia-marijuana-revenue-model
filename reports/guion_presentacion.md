# Guión de la presentación — Propensión al consumo de marihuana en Colombia

**Duración estimada total:** 18–22 minutos (≈ 40 s por slide promedio).
**Audiencia:** compañeros de curso (pregrado, mezcla de Economía y Estadística). Asumir que conocen MCO y Probit pero no necesariamente Random Forest, Gradient Boosting o SHAP.

---

## Cómo usar este guión

Cada bloque tiene tres partes:

- **Qué decir** — el texto que vas a hablar en voz alta. Está escrito en lenguaje natural, no leas literal; úsalo como guía.
- **Punto a hacer pasar** — la idea central que la audiencia debe quedarse después de la slide.
- **Si te preguntan** — preguntas que pueden caer en esa slide y respuestas cortas.

Al final del guión hay una sección de **preguntas frecuentes globales** con respuestas más largas.

Tip general: cuando aparezcan números, **diles en voz alta** (por ejemplo "el GBM tuneado alcanzó un AUC-ROC de 0.7278, casi 0.73"). Eso ancla la atención.

---

## Bloque 0 — Portada (slide 1)

**Qué decir:** "Buenos días. Vamos a presentarles nuestro trabajo final del curso de Ciencia de Datos para las Finanzas, la Economía y los Negocios. El proyecto se titula *Propensión al Consumo de Marihuana en Colombia* y combina un benchmark econométrico con modelos de machine learning e interpretabilidad SHAP. Somos Santiago Tupaz, Moisés Quintero y Vanessa Rodrigues, supervisados por la profesora Paula María Almonacid Hurtado."

**Tiempo:** 20 segundos.

---

## Bloque 1 — Motivación (slides 2–4)

### Slide 2: "Contexto y motivación"

**Qué decir:** "El debate sobre la regulación del cannabis en Colombia ya no es sólo penal o de salud pública: hoy se discute en términos económicos. Más de 40 países han legalizado el cannabis en alguna forma, y eso abre tres preguntas concretas para Colombia: ¿qué tan grande sería el mercado si se regulara?, ¿qué base tributaria generaría?, y ¿en qué población conviene focalizar la prevención? Antes de responder cualquiera de esas preguntas hay que hacer algo más básico: caracterizar empíricamente quién consume y con qué propensión. Ese es nuestro trabajo. Usamos la Encuesta Nacional de Consumo de Sustancias Psicoactivas como insumo."

**Punto a hacer pasar:** este trabajo es un paso *previo* a la simulación tributaria, no la simulación misma.

**Si te preguntan:**

- *¿Por qué no hicieron la simulación tributaria directamente?* — Porque la elasticidad-precio que requiere una simulación creíble exige una submuestra que aquí está fuertemente seleccionada. Por eso nos enfocamos en modelar bien la propensión y dejamos la simulación como trabajo futuro.

### Slide 3: "Brecha que aborda este trabajo"

**Qué decir:** "Identificamos tres brechas en la literatura colombiana. Primera: pocos trabajos comparan rigurosamente un benchmark econométrico clásico con machine learning para este problema. Segunda: casi no hay discusión estructurada de ética y sesgos en estudios de consumo de drogas con encuestas — y este dominio es particularmente sensible. Tercera: cuando se usa machine learning para política pública, la interpretabilidad no es opcional. Nuestro aporte cubre las tres: pipeline reproducible, comparación honesta, interpretabilidad SHAP, y una frontera ética explícita."

**Punto a hacer pasar:** no es sólo "corrimos ML"; es "ML responsable con su frontera ética".

### Slide 4: "¿Por qué importa?"

**Qué decir:** "El trabajo tiene dos dimensiones. La económica: cuántos consumidores hay, qué base tributaria potencial, qué elasticidad-precio esperar. Y la social: dónde focalizar prevención, cómo evitar reforzar estigmas usando datos, y cómo usar inteligencia artificial responsablemente en política pública."

**Tiempo total bloque 1:** 2 minutos.

---

## Bloque 2 — Pregunta de investigación (slides 5–7)

### Slide 5: "Pregunta central"

**Qué decir:** "Nuestra pregunta es: *¿qué factores sociodemográficos observables se asocian con la probabilidad de reportar consumo de marihuana en los últimos doce meses en Colombia, y cuánto mejora la predicción al pasar de un benchmark econométrico a modelos de machine learning?* Tiene dos componentes. Uno descriptivo-causal: identificar variables, signos y magnitudes. Otro predictivo: cuantificar la ganancia del ML manteniendo el mismo conjunto de variables explicativas que el lineal — eso hace la comparación limpia."

**Punto a hacer pasar:** la comparación es justa porque el lineal y el ML usan exactamente el mismo conjunto de variables.

**Si te preguntan:**

- *¿Por qué no le dan más variables al ML para que gane más fácil?* — Porque entonces no estaríamos comparando el algoritmo sino la información. Queríamos aislar la ganancia atribuible al algoritmo.

### Slide 6: "Variable objetivo y unidad de análisis"

**Qué decir:** "La variable dependiente es binaria: 1 si la persona reportó consumo de marihuana en los últimos doce meses, 0 si no. La unidad de análisis es el individuo encuestado. Esto convierte el problema en clasificación binaria. Una nota crítica: la variable `consumo_12m` que vamos a usar difiere en 898 casos de la pregunta K_03 del cuestionario original. Más adelante explicamos cómo lo atendemos."

**Punto a hacer pasar:** somos transparentes sobre la inconsistencia de la variable objetivo.

**Si te preguntan:**

- *¿Cuál es la diferencia exacta entre `consumo_12m` y K_03?* — K_03 dice 1.223 "Sí" y 2.754 "No" en los datos crudos. La base limpia que recibimos tiene 1.719 "Sí". Probablemente la base agregó otras señales de consumo (consumo de vida, último mes). No la rehicimos porque eso reabriría toda la limpieza; lo que sí hicimos fue un análisis de robustez reentrenando el modelo con K_03 directo.

### Slide 7: "Objetivos"

**Qué decir:** "El objetivo general es construir un pipeline reproducible que compare benchmark y ML, con interpretabilidad y reflexión ética. Los específicos son cinco pasos del CRISP-DM: integrar y limpiar la base; estimar benchmark y modelos ML comparables; validar con cross-validation de 10 pliegues y tunear hiperparámetros; interpretar con SHAP y verificar robustez; discutir sesgos y usos legítimos."

**Tiempo total bloque 2:** 2 minutos.

---

## Bloque 3 — Metodología (slides 8–12)

### Slide 8: "Datos y fuentes"

**Qué decir:** "Trabajamos con 3.982 individuos encuestados. Integramos tres archivos: la base limpia de consumo derivada de la ENCSPA, el módulo de personas (sexo, edad) y el módulo D2 (educación). La cobertura es casi del 100% para edad, sexo y educación, pero el precio sólo aparece en 823 personas. Decisión metodológica clave: entrenamos los modelos de ML sobre la muestra amplia sin precio, que tiene 3.980 observaciones, porque la submuestra con precio está fuertemente sesgada."

**Punto a hacer pasar:** sacrificamos precio para tener una muestra representativa.

**Si te preguntan:**

- *¿Por qué la submuestra con precio está sesgada?* — Porque las personas que conocen y reportan el precio del producto suelen ser personas más expuestas al mercado. Si modeláramos sobre ese subconjunto, el modelo aprendería sobre "personas expuestas", no sobre la población general.

### Slide 9: "Pipeline reproducible"

**Qué decir:** "Todo el proyecto está empaquetado como un CLI. Con un solo comando — `python -m cannabis_tax.cli pipeline` — se ejecuta limpieza, validación y construcción de la base. Tenemos seis notebooks numerados: el 01 hace EDA y benchmark, el 03 entrena los modelos ML, el 04 explora con PCA, el 05 hace validación cruzada y tuning, y el 06 hace SHAP, robustez y ética. Y tenemos tests unitarios que corren con `make test` para asegurar que el pipeline no se rompe."

**Punto a hacer pasar:** la reproducibilidad no es opcional — es una práctica profesional que evaluamos.

### Slide 10: "Benchmark econométrico"

**Qué decir:** "Como referencia usamos dos modelos clásicos. El primero es el Modelo Lineal de Probabilidad — MCO sobre la variable binaria — con errores robustos HC1. El segundo es Probit, donde la probabilidad se modela como la función de distribución normal acumulada de una combinación lineal de las variables. Los dos usan exactamente las mismas variables: edad, edad al cuadrado, sexo y educación agrupada. El MCO se interpreta como cambio en probabilidad; el Probit lo reportamos en efectos marginales para que la comparación sea directa."

**Punto a hacer pasar:** dos benchmarks, mismas variables, una comparación directa.

**Si te preguntan:**

- *¿Por qué usar MCO si la variable es binaria? ¿No es mejor logit?* — El MCO sobre binaria se llama LPM y tiene la ventaja de que sus coeficientes se interpretan como cambios en probabilidad. Sí tiene desventajas — la predicción puede salirse de [0,1] — pero como benchmark interpretable es estándar en la literatura.

### Slide 11: "Modelos de Machine Learning"

**Qué decir:** "Entrenamos tres familias. Random Forest: 300 árboles, bagging, robusto a outliers. XGBoost: boosting secuencial, estado del arte en datos tabulares. Gradient Boosting de scikit-learn: boosting más conservador con árboles pequeños. Las reglas de comparación son tres: mismo conjunto de variables que el benchmark, mismo split de train/test 80/20 estratificado con semilla 42, y mismas métricas: Accuracy, AUC-ROC, F1 y CV AUC con 5 y 10 pliegues."

**Punto a hacer pasar:** comparación justa = mismas variables + mismo split + mismas métricas.

**Si te preguntan:**

- *¿Qué es exactamente "bagging" y "boosting"?* — Bagging entrena árboles en paralelo con muestras bootstrap y promedia sus predicciones; reduce varianza. Boosting entrena árboles en secuencia, cada uno corrigiendo los errores del anterior; reduce sesgo. Random Forest es bagging; XGBoost y GBM son boosting.

### Slide 12: "Validación y selección"

**Qué decir:** "El proceso de validación tiene cuatro pasos. Primero CV-10 para ver estabilidad. Segundo curvas de aprendizaje para detectar sobreajuste. Tercero búsqueda aleatoria de hiperparámetros con `RandomizedSearchCV`. Cuarto, selección razonada según AUC-ROC, F1, brecha train-validación y plausibilidad económica. Algo clave: no evaluamos sólo precisión. La argumentación pesa tanto como el número."

**Tiempo total bloque 3:** 4 minutos.

---

## Bloque 4 — Resultados (slides 13–17)

### Slide 13: "Tabla comparativa — benchmark vs. ML"

**Qué decir:** "Aquí está el resultado que más nos sorprendió. Con los hiperparámetros por defecto, ninguno de los tres modelos de machine learning supera al benchmark. MCO y Probit alcanzan AUC-ROC 0.7232. Random Forest queda en 0.7063, Gradient Boosting en 0.7093, XGBoost en 0.7001. El benchmark gana de manera consistente. Pero la última fila muestra el GBM después de tunear: alcanza 0.7278 en AUC-ROC y 0.6129 en F1. Es decir, la ganancia del ML existe pero no aparece sola; requiere búsqueda disciplinada de hiperparámetros."

**Punto a hacer pasar:** ML por defecto = pérdida; ML con tuning = ganancia modesta pero real.

**Si te preguntan:**

- *¿Por qué el ML por defecto pierde?* — Porque con sólo 4 variables y 4.000 observaciones, la relación es bastante lineal. El MCO paga un costo mínimo de sesgo y el ML paga mucho costo de varianza. El tuning del GBM con árboles muy poco profundos (max_depth=2) y regularización fuerte reduce esa varianza.

### Slide 14: "Comparación visual benchmark vs. ML"

**Qué decir:** "Esta gráfica visualiza la tabla anterior. Lo que vale la pena destacar: las diferencias entre modelos son pequeñas. Estamos hablando de centésimas de AUC, no de décimas. Eso justifica nuestra postura en las conclusiones: con este feature set, el techo está cerca."

### Slide 15: "Validación cruzada de 10 pliegues"

**Qué decir:** "Las cajas muestran la distribución de AUC en CV-10. La línea punteada azul es el CV de MCO, en 0.673. Lo que vemos es que las medianas de Random Forest y Gradient Boosting están muy cerca de esa referencia, y sus cajas se solapan sustancialmente con ella. Conclusión: antes del tuning no hay una diferencia estadísticamente convincente entre ML y benchmark."

**Si te preguntan:**

- *¿Por qué CV-10 y no CV-5?* — Más pliegues = menor sesgo pero más varianza por fold. Con n=4.000 podemos pagar el costo computacional y obtener una estimación más estable. CV-10 es estándar en la literatura para datasets de este tamaño.

### Slide 16: "Búsqueda de hiperparámetros (GBM)"

**Qué decir:** "Usamos `RandomizedSearchCV` con 60 combinaciones aleatorias por 5 pliegues, son 300 ajustes totales. Los hiperparámetros óptimos son reveladores: árboles de profundidad sólo 2 (muy poco profundos), learning rate de 0.042 (paso pequeño), 157 árboles, y min_samples_leaf de 26 (regularización fuerte por hoja). El patrón es claro: árboles cortos más mucha regularización para controlar la varianza."

**Punto a hacer pasar:** el tuning ganador es ultra-conservador, no exuberante.

**Si te preguntan:**

- *¿Por qué `RandomizedSearchCV` y no `GridSearchCV`?* — Con 6 hiperparámetros, el grid completo sería intratable. La búsqueda aleatoria es más eficiente cuando el espacio es grande y la mayoría de hiperparámetros no son críticos.

### Slide 17: "Modelo final — GBM tuneado"

**Qué decir:** "La curva ROC del GBM tuneado se separa modestamente pero consistentemente del benchmark. Las cifras finales: AUC-ROC en test 0.7278, F1 0.6129, CV-10 AUC 0.6756. Comparado con el MCO (0.7232 en AUC, 0.5982 en F1), la ganancia es de 4–5 décimas porcentuales en AUC y 1.5 puntos en F1. Es modesta. Pero es consistente."

**Tiempo total bloque 4:** 4–5 minutos.

---

## Bloque 5 — Interpretabilidad (slides 18–22)

### Slide 18: "¿Por qué SHAP?"

**Qué decir:** "El GBM funciona pero es una caja gris: ¿qué variable está pesando más? ¿qué pasa con cada individuo? Sin esa lectura el modelo no sirve para política. SHAP, de un paper de 2017 de Lundberg y Lee, resuelve esto. Cada predicción se descompone como una suma de contribuciones por variable, con una propiedad matemática limpia: la suma de las contribuciones más un valor base reproduce exactamente la predicción del modelo. La importancia global es simplemente el promedio del valor absoluto de las contribuciones."

**Punto a hacer pasar:** SHAP convierte el GBM de caja negra en algo leíble.

**Si te preguntan:**

- *¿SHAP es lo mismo que feature importance de sklearn?* — No. La feature importance tradicional mide cuánto reduce la impureza un split; es global y aproximada. SHAP es por-individuo y tiene fundamento en teoría de juegos cooperativos (valor de Shapley): es la única descomposición que satisface tres propiedades deseables al mismo tiempo (consistencia, eficiencia local y simetría).

### Slide 19: "Importancia SHAP — global"

**Qué decir:** "Este es el resultado más revelador del análisis. Edad concentra el 41% de la importancia, edad al cuadrado el 35%. Sumadas, edad explica el 77% del modelo. Sexo aporta el 15%. Educación, el 8% sumando las dos dummies. La interpretación es clara: con cuatro variables sociodemográficas, el modelo se reduce esencialmente a un segmentador edad-sexo."

**Punto a hacer pasar:** el modelo es honestamente delgado — no descubre patrones nuevos, sólo modela mejor la edad.

**Si te preguntan:**

- *¿Por qué edad al cuadrado pesa tanto como edad?* — Porque la relación no es monótona. Hay un pico de propensión en cohortes jóvenes (~20–25 años) y decae. Un término lineal solo no captura ese pico; necesita el cuadrático. Lo verán en la siguiente gráfica.

### Slide 20: "SHAP summary — distribución individual"

**Qué decir:** "Esta gráfica enseña algo que la tabla de importancia no enseña: la dirección y la dispersión. Cada punto es una persona. La posición horizontal es la contribución SHAP a la propensión predicha. El color codifica el valor de la variable: rojo es alto, azul bajo. Mirando edad: los puntos rojos (mayores) están a la izquierda — empujan la predicción hacia abajo. Los azules (jóvenes) están a la derecha — empujan hacia arriba. Sexo `Mujer=1` está mayoritariamente a la izquierda: ser mujer reduce la propensión predicha. Educación tiene un efecto pequeño y mixto."

**Punto a hacer pasar:** el modelo predice "joven y hombre" como propensión alta; "mujer mayor" como propensión baja.

### Slide 21: "Dependencia parcial — edad"

**Qué decir:** "Esta es la forma funcional que el GBM aprendió para edad. Sube en cohortes jóvenes hasta un máximo en torno a los 20–22 años, y luego baja monótonamente. El MCO con edad + edad² aproxima esto pero como parábola; el GBM lo hace por tramos y captura mejor la forma. Aquí es donde se materializa la ganancia del ML."

**Punto a hacer pasar:** la ganancia predictiva del GBM proviene de capturar mejor esta curva, no de descubrir relaciones nuevas.

### Slide 22: "Robustez — Y alternativa estricta"

**Qué decir:** "Atendemos aquí el hallazgo crítico que mencionamos antes. La auditoría detectó 898 casos donde la variable que usamos como Y dice 'consumió' pero la pregunta directa del cuestionario K_03 dice 'no'. Para verificar que nuestros resultados no dependen de esa inconsistencia, reentrenamos el GBM tuneado con una Y alternativa estricta: igual a 1 sólo si K_03=1. Resultado: el CV AUC-10fold incluso mejora ligeramente, de 0.6685 a 0.6951. La AUC en test cae poco (–0.031) y se mantiene sobre el azar. Conclusión: las relaciones estructurales no dependen de la operacionalización elegida."

**Punto a hacer pasar:** detectamos un problema, lo documentamos honestamente, y verificamos que las conclusiones no cambian.

**Si te preguntan:**

- *¿Por qué no rehicieron la base con K_03 directo y listo?* — Porque la base limpia que recibimos es un insumo que ya tiene una construcción definida; rehacer eso reabre toda la fase 1. Académicamente, lo correcto en este punto del semestre es documentar la limitación y demostrar robustez, no rehacer.

**Tiempo total bloque 5:** 4 minutos.

---

## Bloque 6 — Ética e implicaciones (slides 23–26)

### Slide 23: "Sesgos del dato"

**Qué decir:** "Tres sesgos para tener en cuenta. Uno: autoreporte. Las encuestas de consumo de drogas subestiman porque hay estigma; por construcción, el modelo aprende propensión a *reportar* consumo, no propensión a *consumir*. Dos: selección por precio. La submuestra que reporta precio está sesgada hacia personas más expuestas al mercado, por eso no la usamos para entrenar. Tres: medición en Y. La discrepancia entre `consumo_12m` y K_03 introduce ruido en la variable objetivo; el análisis de robustez mostró que no domina, pero es una limitación que dejamos declarada."

**Punto a hacer pasar:** los sesgos los nombramos, los cuantificamos donde se puede, y los atendemos donde es factible.

### Slide 24: "Riesgos del uso del modelo"

**Qué decir:** "El modelo tiene un AUC de 0.73. Eso es razonable, pero implica solapamiento sustancial entre grupos. Tres riesgos. Uno: perfilado individual. Usar este modelo para decisiones sobre personas — vigilancia, contratación, escuela — sería un mal uso porque el costo social del falso positivo es severo dado el estigma. Dos: confundir asociación con causalidad. Que el modelo prediga mayor probabilidad para hombres jóvenes no significa que el sexo o la edad *causen* el consumo. Tres: reforzar estigma. Publicar mapas o perfiles puede consolidar estereotipos."

**Punto a hacer pasar:** un modelo predictivo bueno no es necesariamente un modelo *utilizable* para cualquier decisión.

### Slide 25: "Uso responsable propuesto"

**Qué decir:** "Marcamos una frontera explícita. Sí: análisis agregado para tamaño de mercado, diseño tributario por estratos amplios, priorización de segmentos para prevención. No: decisiones individuales, focalización geográfica fina sin análisis de equidad, predicciones puntuales sin intervalos de incertidumbre."

**Punto a hacer pasar:** decir explícitamente para qué no usar el modelo es parte del trabajo, no un anexo.

### Slide 26: "Implicaciones de política"

**Qué decir:** "Dos implicaciones concretas. Diseño tributario: si Colombia legalizara, la base estaría concentrada en cohortes jóvenes-masculinas, con elasticidad-precio probablemente alta. Un impuesto demasiado alto desplazaría la demanda al mercado ilegal. Una proyección de recaudo creíble requiere acoplar este modelo con una elasticidad-precio estimada limpiamente, lo cual no pudimos hacer con la submuestra disponible. Política preventiva: las cohortes de 18 a 25 son las de mayor propensión y las más sensibles a intervenciones tempranas; conviene focalizar campañas ahí y diferenciar por sexo."

**Tiempo total bloque 6:** 3 minutos.

---

## Bloque 7 — Conclusiones (slides 27–30)

### Slide 27: "Hallazgos clave"

**Qué decir:** "Cinco hallazgos en orden. Uno: el benchmark MCO/Probit alcanza AUC 0.7232 — es un piso difícil de superar con sólo cuatro variables. Dos: los modelos ML por defecto no superan al benchmark. Tres: el GBM tuneado sí lo hace, con AUC 0.7278 y F1 0.6129. Cuatro: SHAP muestra que edad y edad² concentran 77% de la importancia — modelo honestamente delgado. Cinco: el análisis de robustez con Y alternativa confirma que las relaciones son estables."

### Slide 28: "Lecciones metodológicas"

**Qué decir:** "Cuatro lecciones que generalizan más allá de este proyecto. Primera: la flexibilidad sin regularización adecuada introduce varianza que opaca cualquier ganancia de sesgo. Segunda: el tuning disciplinado importa más que la elección del algoritmo en datasets chicos. Tercera: la interpretabilidad no es opcional — define qué tan utilizable es el modelo. Cuarta: documentar limitaciones — como nuestra Y discrepante — es parte del trabajo, no un anexo."

**Punto a hacer pasar:** estas lecciones aplican a cualquier proyecto de ciencia de datos del curso.

### Slide 29: "Próximos pasos"

**Qué decir:** "Cuatro líneas de trabajo futuro. Reconciliar la construcción de `consumo_12m` con K_03 directo. Ampliar el feature set con variables de entorno: geografía, red social, ingreso del hogar. Estimar elasticidad-precio con un diseño que corrija el sesgo de selección de la submuestra. Y finalmente, acoplar el modelo con proyecciones poblacionales del DANE para hacer la simulación tributaria que motivó originalmente el proyecto."

### Slide 30: "Preguntas y discusión"

**Qué decir:** "Eso es todo. Quedamos atentos a sus preguntas." *(Pausa, sonrisa.)*

**Tiempo total bloque 7:** 2 minutos.

---

## Preguntas frecuentes globales (con respuestas largas)

### "¿Cuál fue la parte más difícil del proyecto?"

Sin dudar: la fase de validación y tuning. Es fácil correr `model.fit()` y reportar el AUC; lo difícil es entender por qué el ML pierde por defecto, decidir qué hiperparámetros importan, y justificar la selección. La fase ética también fue difícil porque obliga a decir explícitamente para qué *no* sirve un modelo que tú mismo construiste.

### "¿Qué harían diferente si empezaran de nuevo?"

Lo primero, definir la variable objetivo desde K_03 directo, no desde una base limpia preexistente. Lo segundo, incluir desde el inicio variables de entorno (geografía, ingreso del hogar) en lugar de quedarnos en cuatro variables demográficas. Lo tercero, separar desde el principio un conjunto de holdout que no se toca hasta el final, para tener una evaluación verdaderamente independiente.

### "¿Por qué Gradient Boosting y no Neural Networks?"

Para datos tabulares con n ≈ 4.000 y 4 variables, una red neuronal no aporta. La literatura empírica sobre datos tabulares (por ejemplo, los benchmarks de Shwartz-Ziv y Armon de 2021) muestra que los métodos basados en árboles ganan en este régimen.

### "¿Cómo asegurarían la equidad del modelo?"

Hicimos un primer paso: comparar prevalencias predichas por subgrupos. Un trabajo más serio implicaría calcular métricas formales de fairness (equal opportunity, demographic parity), idealmente sobre subgrupos definidos por estrato socioeconómico y geográfico, no sólo por las variables del modelo. Eso requiere variables que no tenemos aquí.

### "¿Qué pasaría si el modelo se usara para vigilancia policial?"

Sería un mal uso. La razón técnica: el AUC de 0.73 implica que las distribuciones de propensión de "consumidores" y "no consumidores" se solapan mucho. Si fijas un umbral para "alerta", obtienes muchos falsos positivos. La razón ética: el costo social del falso positivo en un dominio estigmatizado es severo. Por eso lo declaramos explícitamente como uso no recomendado.

### "¿Por qué la educación pesa tan poco en el modelo?"

Es un hallazgo interesante. Una hipótesis es que la variación en consumo de marihuana en cohortes jóvenes en Colombia hoy no se explica tanto por educación como por entorno y red social — variables que no tenemos. Otra hipótesis: la educación está confundida con la edad (gente más joven en promedio tiene más educación reciente), y al ya tener edad en el modelo, la educación pierde su poder marginal.

### "¿Cuál es la diferencia entre AUC-ROC y F1?"

AUC-ROC mide qué tan bien el modelo *ordena* a los individuos por probabilidad — es independiente del umbral. F1 mide qué tan bien clasifica binariamente a un umbral fijo (por defecto 0.5). Si la prevalencia es desbalanceada, F1 puede ser bajo aun con AUC alto, simplemente porque el umbral está mal calibrado. En nuestro caso, prevalencia de 0.43 es moderada, así que F1 y AUC dan historias consistentes.

### "¿Su modelo extrapola fuera de Colombia o de la ENCSPA?"

No. Está entrenado sobre la ENCSPA, que tiene una representatividad poblacional y temporal específica. Aplicarlo a otro país o a la misma Colombia en otro año requiere re-validación. Esto es estándar en ML: lo que aprendiste sobre una distribución no necesariamente vale en otra.

### "¿Qué pasa con quienes contestaron 'No sabe / No responde'?"

En K_03 son sólo 5 personas. En la versión `consumo_12m` quedan tratadas como 0 por convención. Es una decisión defensible cuando son pocas observaciones, pero la documentamos explícitamente en el paper.

### "¿Por qué publicar este trabajo si el modelo puede ser mal usado?"

Por dos razones. Primera: el conocimiento agregado es valioso para diseño de política, y el debate sobre regulación del cannabis en Colombia avanza con o sin nuestro paper. Mejor que avance con evidencia. Segunda: la sección de ética que escribimos hace explícita la frontera de uso responsable, lo cual es justamente el tipo de discusión que debería acompañar cualquier modelo aplicado a política.

---

## Tips finales para el día de la presentación

1. **Tiempo:** mantén ritmo. 30 slides en 20 minutos = 40 segundos por slide promedio. Si te demoras más de 1 minuto en una slide, salta.
2. **Tablas grandes:** no leas todas las cifras. Señala la fila clave (por ejemplo, la del GBM tuneado en negrita) y di sólo dos o tres números.
3. **Gráficas:** explica los ejes antes de explicar la conclusión. Audiencia que no entiende los ejes no entiende la conclusión.
4. **Si te bloqueas:** vuelve al punto-a-hacer-pasar de esa slide. Está diseñado para ser la idea mínima que la audiencia debe llevarse.
5. **Q&A:** si no sabes la respuesta, dilo. "Buena pregunta, no lo hicimos pero sería un siguiente paso natural" es mejor que inventar.
6. **Cierre:** después de la slide de "Preguntas", quédate callado. No llenes el silencio. Los compañeros van a preguntar.

Suerte con la presentación.
