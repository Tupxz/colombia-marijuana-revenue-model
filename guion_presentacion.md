# Guión de Presentación
## Propensión al Consumo de Marihuana en Colombia: Benchmark Econométrico y ML con SHAP
**Santiago Tupaz · Moisés Quintero · Vanessa Rodrigues — Universidad EAFIT**

> **Duración estimada:** 25–30 minutos + preguntas  
> **Formato:** Las indicaciones entre corchetes son para el presentador, no se leen en voz alta.

---

## SLIDE 1 — Portada
*(~30 segundos)*

Buenos días. Somos Santiago Tupaz, Moisés Quintero y Vanessa Rodrigues, del programa de Economía de EAFIT. Hoy les presentamos un trabajo sobre propensión al consumo de marihuana en Colombia, construido a partir de la Encuesta Nacional de Consumo de Sustancias Psicoactivas. El título completo es "Benchmark Econométrico y Modelos de Machine Learning con Interpretabilidad SHAP", y los profesores a quienes está dirigido son Paula María Almonacid y Carlos Alberto Cerro.

---

## SLIDE 2 — Contexto y motivación
*(~1 min)*

¿Por qué este tema ahora? El debate sobre la regulación del cannabis en Colombia ya no es solo jurídico ni moral: incorpora preguntas económicas muy concretas. ¿Cuántas personas consumen? ¿Qué perfil tienen? ¿Cuánto recaudaría el Estado si hubiera un impuesto? Antes de simular cualquier escenario fiscal, hay que responder una pregunta previa: **¿quién consume y con qué probabilidad?** Y la herramienta natural para responderla es la ENCSPA, la encuesta nacional de consumo de sustancias psicoactivas.

---

## SLIDE 3 — Brecha que aborda este trabajo
*(~1 min)*

La literatura para Colombia es escasa en tres frentes. Primero, casi nadie ha hecho una comparación rigurosa entre un benchmark econométrico y modelos de machine learning en este dominio. Segundo, los estudios existentes rara vez discuten explícitamente los sesgos y los riesgos éticos de usar modelos predictivos con datos de encuesta sobre comportamientos estigmatizados. Y tercero, en política pública no basta con saber que un modelo predice bien: hay que entender *por qué* predice bien, qué variables mueve y en qué dirección.

Nuestra contribución responde a las tres brechas: pipeline reproducible, comparación honesta entre modelos, interpretabilidad SHAP, y una frontera ética explícita.

---

## SLIDE 4 — ¿Por qué importa?
*(~45 segundos)*

Las implicaciones tienen dos dimensiones. En lo económico: estimar el tamaño del mercado potencial, proyectar una base tributaria bajo distintos escenarios regulatorios, y entender la sensibilidad al precio del segmento consumidor. En lo social: focalizar campañas de prevención en los grupos de mayor propensión, reducir el estigma a través de evidencia estructurada, y hacerlo con herramientas de inteligencia artificial que sean responsables y transparentes.

---

## SLIDE 5 — Pregunta central
*(~1 min)*

La pregunta central tiene dos componentes. El primero es descriptivo: ¿qué factores sociodemográficos observables se asocian con la probabilidad de reportar consumo en los últimos doce meses? El segundo es predictivo: ¿cuánto mejora esa predicción cuando pasamos de cuatro variables demográficas básicas a un feature set ampliado que incluye red social, actitud, salud mental y percepción de riesgo?

---

## SLIDE 6 — Variable objetivo y unidad de análisis
*(~45 segundos)*

La variable dependiente es binaria: uno si el individuo reportó consumo de marihuana en los últimos doce meses, cero si no. La unidad de análisis es cada individuo encuestado. Hay una nota crítica que vale la pena mencionar: la variable que construimos difiere de la pregunta directa K\_03 en 898 casos, aproximadamente el 23% de los consumidores declarados. Documentamos esto como limitación, y dedicamos un slide a mostrar que las conclusiones son robustas ante esa diferencia.

---

## SLIDE 7 — Objetivos
*(~45 segundos)*

Los objetivos específicos son cinco: integrar y limpiar la base, estimar los benchmarks y los modelos ML, validar con validación cruzada y tunear hiperparámetros, interpretar con SHAP y verificar robustez, y finalmente discutir sesgos y usos legítimos. Todo esto está implementado en un pipeline reproducible que cualquiera puede correr.

---

## SLIDE 8 — Datos y fuentes
*(~1 min)*

La base integra cinco módulos de la ENCSPA. El capítulo K es la fuente de la variable objetivo. Los módulos de personas y D2 aportan las variables demográficas. El módulo G es donde están las variables de red social y actitud —que resultan ser fundamentales, como veremos después. Y el módulo D contribuye situación laboral, salud mental y percepción de riesgo. En total, 3.982 individuos, 16 features, con una sola variable que tiene nulos significativos: régimen de salud, con 11.2%, lo que reduce la muestra efectiva a 3.401 observaciones para los modelos ampliados.

---

## SLIDE 9 — Pipeline reproducible
*(~30 segundos)*

Todo el trabajo está estructurado en un pipeline CLI y cinco notebooks. Desde la limpieza hasta el análisis SHAP, cada paso es replicable con un solo comando. Esto no es un detalle menor: en investigación con datos de encuesta, la reproducibilidad es parte de la credibilidad del resultado.

---

## SLIDE 10 — Benchmark econométrico
*(~1 min)*

El benchmark es un MCO con modelo de probabilidad lineal y un Probit, ambos con las mismas cuatro variables demográficas: edad, edad al cuadrado, sexo y educación. El modelo es sencillo, interpretable, y —como veremos— sorprendentemente difícil de superar. La especificación incluye la edad al cuadrado porque la relación entre edad y consumo no es lineal: es mayor en cohortes jóvenes y cae con la edad.

---

## SLIDE 11 — Feature set ampliado — 16 variables
*(~1 min)*

Las 16 variables están organizadas en siete grupos teóricos. Los cuatro primeros son los mismos del benchmark más estructura familiar. Los grupos cinco a siete son los nuevos: red social —si familiares y amigos consumen—, actitud —si el individuo probaría sustancias y su opinión sobre el cannabis medicinal—, situación socioeconómica, salud mental con el PHQ-2, y percepción de riesgo ante el consumo ocasional y frecuente. Este diseño teórico no es arbitrario: viene de la Teoría del Aprendizaje Social y del Health Belief Model, que predicen que el entorno y las creencias son tan determinantes como la posición en el ciclo de vida.

---

## SLIDE 12 — Modelos de Machine Learning
*(~45 segundos)*

Estimamos Random Forest, XGBoost y Gradient Boosting, todos sobre el mismo split estratificado. Las métricas de comparación son Accuracy, AUC-ROC, F1 y la validación cruzada de cinco y diez pliegues. Ese último punto es importante: el AUC en un único split de prueba puede ser engañoso con muestras moderadas; el CV5 es el estimador de referencia.

---

## SLIDE 13 — Validación y selección
*(~30 segundos)*

La estrategia de validación tiene cuatro pasos: CV-10 para estabilidad, curvas de aprendizaje para controlar sobreajuste, RandomizedSearchCV para tuning, y criterios múltiples que incluyen plausibilidad económica. No estamos seleccionando el modelo que maximiza un solo número: estamos buscando el que generaliza mejor con argumentación sólida.

---

## SLIDE 14 — Benchmark: una referencia exigente
*(~1.5 min)*

Aquí está el primer hallazgo y probablemente el más sorprendente. Con solo cuatro variables demográficas, el Probit alcanza un AUC-ROC de 0.70 y un CV5 de 0.66. Los modelos de machine learning con esas mismas cuatro variables y parámetros por defecto **no lo superan**. El Random Forest queda por debajo del benchmark; el Gradient Boosting apenas lo empata. El benchmark no es una formalidad que uno pone para justificar el ML. Es una restricción activa que cualquier modelo más complejo tiene que superar para justificarse.

---

## SLIDE 15 — ¿Por qué el ML no supera al benchmark por defecto?
*(~1 min)*

La razón es estadística. Con solo cuatro variables, la relación subyacente es aproximadamente aditiva: el MCO minimiza el sesgo sin pagar un costo relevante. Los modelos de ML sin regularización pagan un costo de varianza sin ganar en sesgo. El gráfico de CV-10 lo ilustra: las cajas se solapan. La diferencia entre modelos no es robusta en el espacio reducido. Esto confirma la teoría: la ganancia del ML vendrá de ampliar el feature set, no del algoritmo en sí.

---

## SLIDE 16 — Búsqueda de hiperparámetros sobre 4 variables
*(~45 segundos)*

Tuneamos el GBM sobre la especificación de cuatro variables como referencia. El patrón de los hiperparámetros es interpretable: árboles muy superficiales —profundidad dos—, tasa de aprendizaje baja, submuestra alta. Es regularización agresiva. El modelo gana no por mayor complejidad sino por mejor control del compromiso sesgo-varianza. Pero la ganancia sobre el benchmark es de solo 0.007 en CV5: insuficiente para establecer ventaja estructural del ML en el espacio reducido.

---

## SLIDE 17 — Modelo ampliado: resultados
*(~1.5 min)*

Acá está el resultado central de la parte predictiva. Cuando ampliamos a 16 variables y tuneamos los modelos directamente sobre ese espacio, el panorama cambia. El RF Tuneado con regularización explícita obtiene un CV5 AUC de **0.703 con una desviación estándar de apenas 0.007**. Eso es una ganancia de 0.038 sobre el benchmark Probit y de 0.032 sobre el GBM tuneado de cuatro variables.

Noten dos cosas en la tabla. Primero, el GBM Tuneado de 16 variables tiene un CV5 de 0.704, prácticamente idéntico al RF. Entonces, ¿por qué elegimos el RF? La respuesta está en la columna de varianza: el GBM tiene ±0.021, el RF tiene ±0.007. Tres veces menos varianza entre pliegues. En política pública, un modelo que da resultados consistentes en distintas particiones de los datos vale más que uno que gana en promedio pero fluctúa.

---

## SLIDE 18 — ¿Por qué RF Tuneado?
*(~1.5 min)*

Cuatro razones concurrentes para elegir el RF. Primera: CV5 AUC más estable, con la menor varianza de todos los candidatos. Segunda: la brecha entre entrenamiento y prueba es de 0.060. Eso puede sonar preocupante —y lo fue, antes de investigarlo. La profundidad inicial era de 25, lo que generaba una brecha de 0.094. La redujimos a 0.060 restringiendo `max_depth` a 15 y `min_samples_leaf` a 25. Tercera: el mecanismo de bagging del RF —400 árboles con submuestreo de 30% de variables por árbol— es teóricamente superior cuando el feature set es amplio y la señal es moderada. Cuarta: el TreeExplainer de SHAP produce valores exactos para el RF sin ninguna penalidad en calidad de interpretabilidad.

---

## SLIDE 19 — Curva de aprendizaje
*(~1 min)*

Esta figura responde la pregunta de si el sobreajuste residual es memorización o es estructural. La brecha entre la curva de entrenamiento y la de validación se mantiene estable alrededor de 0.057 en todo el rango de tamaños muestrales, desde 500 observaciones hasta las 2.700 del entrenamiento completo. Si fuera memorización, la brecha disminuiría al aumentar n. No lo hace. Lo que vemos es el optimismo estructural del bagging: los árboles se construyen sobre muestras bootstrap y al evaluarse sobre el entrenamiento completo mezclan observaciones que vieron y que no vieron, sobreestimando el desempeño. El CV5 de 0.703 es el estimador limpio.

Noten también que la curva de validación supera al benchmark Probit —línea punteada en 0.665— desde aproximadamente 500 observaciones en adelante.

---

## SLIDE 20 — ¿Por qué SHAP?
*(~45 segundos)*

Pasamos ahora a la parte que —creemos— es la más valiosa del trabajo: la interpretabilidad. El RF Tuneado predice bien, pero es una caja negra. Sin entender por qué predice, el modelo no sirve para política pública. SHAP descompone cada predicción individual como suma de contribuciones exactas por variable. La importancia global de cada variable es simplemente el valor absoluto promedio de esas contribuciones. Y la ventaja del TreeExplainer es que para árboles de decisión —Random Forest o GBM— calcula esos valores de manera exacta, sin aproximación.

---

## SLIDE 21 — Del modelo demográfico al modelo social
*(~1 min)*

Esta comparación es el hallazgo interpretativo central. A la izquierda, el modelo de cuatro variables: edad y edad al cuadrado concentran el 76.5% de la importancia SHAP. Es un modelo demográfico puro. La propensión al consumo la explica casi exclusivamente la posición en el ciclo de vida. El sexo ocupa el tercer lugar con 15%.

A la derecha, el modelo de 16 variables. El perfil se diversifica radicalmente. Aparecen dos variables que antes no existían en el modelo, y su importancia es comparable a la de la edad.

---

## SLIDE 22 — Top 10 variables SHAP
*(~2 min)*

Miremos los números con precisión. Las cuatro primeras variables concentran el 72% de la importancia total. Edad en primer lugar con 19.9%, edad al cuadrado en segundo con 19.3%. Hasta ahí, nada nuevo. Pero en tercero está `probaria_sustancias` con 17.1%, y en cuarto `amigos_consumen` con 16.2%.

Esto es de primera relevancia para política pública. Significa que la disposición actitudinal hacia el consumo —si una persona dice que probaría sustancias— y la exposición al consumo en el entorno de pares son predictores de propensión **tan informativos como la edad**. No son variables secundarias. Son el segundo factor explicativo del modelo.

Y fíjense en el sexo: en el modelo de cuatro variables era el tercer predictor con 15%. En el modelo ampliado cae al sexto lugar con 4%. Esto no significa que el sexo no importe: significa que gran parte de lo que el modelo de cuatro variables le atribuía al sexo en realidad era un artefacto de la ausencia de información sobre la red social. Al controlar por el entorno de pares y la actitud, el género aporta señal residual. Esto valida exactamente lo que predice la Teoría del Aprendizaje Social de Bandura.

---

## SLIDE 23 — SHAP summary plot
*(~45 segundos)*

Este gráfico muestra la distribución de contribuciones individuales para las observaciones del conjunto de prueba. Cada punto es una persona. El color rojo indica valor alto de la variable, azul indica valor bajo. El eje horizontal muestra cuánto contribuye esa variable a la predicción.

Las observaciones de mayor edad tienden a contribuciones negativas —reducen la propensión—, mientras que los jóvenes contribuyen positivamente. Para `probaria_sustancias` y `amigos_consumen`, el patrón es el esperado: valores altos aumentan la propensión a reportar consumo.

---

## SLIDE 24 — Dependencia parcial SHAP: edad
*(~45 segundos)*

Esta figura confirma que la relación entre edad y propensión no es lineal ni monótona. La contribución es positiva y alta en las cohortes jóvenes, decae con la edad, y se vuelve fuertemente negativa en las personas mayores. Esta forma funcional es exactamente por la que incluimos el término cuadrático en el benchmark, y también justifica empíricamente el uso de un modelo no lineal sobre la regresión logística cuando el feature set incluye variables de ciclo de vida.

---

## SLIDE 25 — Análisis de robustez
*(~1 min)*

La preocupación sobre la variable objetivo es legítima: 898 casos —el 23% de los consumidores declarados— difieren entre nuestra variable construida y la pregunta directa K\_03. Para verificar que los resultados no dependen de esa decisión de construcción, reentrenamos el GBM tuneado con la variable estricta.

El AUC de prueba cae apenas 0.009. El CV5 mejora 0.027. Esto es una señal positiva: cuando la operacionalización de la variable objetivo es más limpia, la generalización del modelo mejora. Las relaciones estructurales son estables ante la elección de Y. El hallazgo sobre el papel de la red social y la actitud no es un artefacto de cómo construimos la variable.

---

## SLIDE 26 — Cuatro conclusiones sustantivas
*(~1.5 min)*

Resumimos en cuatro conclusiones. Primera: el benchmark econométrico es una restricción activa, no una formalidad. Con cuatro variables demográficas, el Probit alcanza CV5 de 0.665 y ningún ML lo supera sin tuning disciplinado.

Segunda: el tuning es condición necesaria pero no suficiente. Con pocas variables bien modeladas, el ML no tiene ventaja estructural sobre la regresión lineal.

Tercera: las 16 variables y el RF Tuneado regularizado generalizan mejor. CV5 de 0.703 con varianza de solo ±0.007. Brecha train-test de 0.060, reducida desde 0.094 con regularización explícita.

Cuarta, y la más valiosa: `probaria_sustancias` y `amigos_consumen` tienen importancia comparable a la edad. El sexo cae tres puestos. La red social y la actitud co-determinan la propensión tanto como el ciclo de vida.

---

## SLIDE 27 — Lecciones metodológicas
*(~1 min)*

Cinco lecciones para llevar. El tuning importa más que el algoritmo: la diferencia entre RF y GBM es secundaria respecto a calibrarlos bien. La riqueza de features es complementaria al tuning, no sustituta: ampliar el feature set con variables teóricamente justificadas cambia la estructura interpretativa y mejora la generalización. El CV AUC es más informativo que el AUC en prueba con muestras moderadas. La interpretabilidad no es decorativa: sin SHAP, no habríamos detectado que el género cae tres posiciones al controlar por la red social. Y documentar limitaciones es parte del trabajo, no una debilidad.

---

## SLIDE 28 — Próximos pasos
*(~45 segundos)*

Hay cinco líneas de trabajo futuro claras. Reconciliar la variable objetivo resolviendo las 898 discrepancias. Imputar régimen de salud para recuperar 581 observaciones. Re-estimar el RF Tuneado con la variable objetivo reconciliada. Estimar elasticidad-precio con un diseño que corrija el sesgo de selección de la submuestra con datos de precio. Y finalmente estimar un modelo hurdle que separe la decisión de consumir de la intensidad, conectando directamente con la simulación de recaudo tributario.

---

## SLIDE 29 — Sesgos del dato
*(~45 segundos)*

Tres sesgos que hay que tener presentes. El autoreporte subestima el consumo real, especialmente donde el riesgo legal o social percibido es alto. La submuestra con precio está seleccionada hacia personas más expuestas al mercado, por lo que el análisis de elasticidad que hacemos con esos datos es exploratorio. Y la discrepancia en la variable objetivo introduce ruido que el análisis de robustez acota pero no elimina.

---

## SLIDE 30 — Riesgos del uso del modelo
*(~1 min)*

Hay tres riesgos que queremos nombrar explícitamente. El primero es el perfilado individual: con un AUC de 0.70, las distribuciones de propensión entre grupos se solapan sustancialmente. Usar este modelo para decisiones sobre personas —perfilado policial, decisiones laborales, vigilancia escolar— sería un mal uso. El costo social del falso positivo en un dominio estigmatizado es inaceptable. Segundo: las asociaciones SHAP no son causales. Que el modelo asigne más peso a los jóvenes no implica que ser joven cause el consumo; hay factores no observados correlacionados con la edad. Tercero: publicar mapas o perfiles de consumo sin contexto puede reforzar estereotipos.

---

## SLIDE 31 — Uso responsable propuesto
*(~45 segundos)*

El modelo sí es útil como herramienta agregada. Para estimar tamaños de mercado bajo escenarios regulatorios. Para apoyar el diseño tributario simulando bases de contribuyentes por estratos amplios. Para priorizar segmentos en política preventiva. Lo que no recomendamos es usarlo para decisiones individuales ni para focalización geográfica fina sin un análisis de equidad adicional.

---

## SLIDE 32 — Implicaciones de política
*(~1 min)*

Dos implicaciones concretas. En diseño tributario: la base de contribuyentes está concentrada en cohortes jóvenes. La elasticidad-precio en ese segmento probablemente es alta, lo que significa que un impuesto demasiado alto desplazaría la demanda al mercado ilegal y anularía el efecto recaudatorio. Una proyección de recaudo creíble requiere acoplar este modelo de propensión con una elasticidad-precio estimada limpiamente —algo que la submuestra disponible aún no permite hacer con rigor.

En política preventiva: focalizar en el rango 18–25 años es lo que indican los datos, con diferenciación por sexo y —lo que agrega este trabajo— con énfasis en el entorno de pares y la actitud, no solo en el perfil demográfico.

---

## SLIDE 33 — Cierre: preguntas y discusión
*(~30 segundos)*

Eso es todo de nuestra parte. Para resumir en una línea: con cuatro variables, el benchmark es difícil de superar; con dieciséis y tuning riguroso, el RF Tuneado lo supera y además revela que la red social y la actitud importan tanto como la edad —un resultado que no habríamos visto sin SHAP. Quedamos abiertos a preguntas.

---

## NOTAS GENERALES PARA LA PRESENTACIÓN

**Distribución sugerida del tiempo (25 min):**

| Sección | Slides | Tiempo |
|---|---|---|
| Portada + Introducción | 1–4 | 3 min |
| Pregunta de investigación | 5–7 | 2.5 min |
| Metodología | 8–13 | 5 min |
| Resultados | 14–19 | 7 min |
| Interpretabilidad SHAP | 20–25 | 5 min |
| Conclusiones | 26–28 | 3 min |
| Ética e implicaciones | 29–32 | 3 min |
| Cierre | 33 | 0.5 min |

**Slides que más preguntas suelen generar:**
- Slide 14 (benchmark vs ML): es contraintuitivo que el ML no gane
- Slide 17 (resultados 16-var): pueden preguntar por qué la varianza importa
- Slide 22 (SHAP top-10): el hallazgo del sexo suele generar debate
- Slide 25 (robustez): pueden preguntar qué significa la discrepancia en Y

**Frases de transición útiles:**
- *"Antes de ver si el ML gana, hay que saber contra qué compite..."* → Slide 14
- *"Ampliar el feature set solo ayuda si los hiperparámetros están bien calibrados..."* → Slide 17
- *"El número importa, pero la estructura importa más..."* → Slide 20
- *"Con AUC de 0.70, el modelo predice; con SHAP, entendemos..."* → Slide 22
