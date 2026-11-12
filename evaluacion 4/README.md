# Evaluación 4 — Predicción de intención de compra y segmentación de visitantes

**Grupo 3 · Análisis de Datos · ITM 2026-2 · Docente: Daniel Alexis Nieto Mora**

| Integrante | Usuario de GitHub |
|---|---|
| Santiago Betancur | [@Xantyagoh](https://github.com/Xantyagoh) |
| Diego Alzate | [@DiegoA1123](https://github.com/DiegoA1123) |
| Carlos Mendez | [@carmarisx](https://github.com/carmarisx) |
| Sebastian Cadavid | [@Exmen9](https://github.com/Exmen9) |
| Daniel Martinez | [@danielmmnez](https://github.com/danielmmnez) |

---

## Descripción del problema

Un comercio electrónico registra miles de **sesiones de navegación** (páginas vistas, tiempo, tasa de rebote, procedencia del tráfico…) y solo una pequeña parte termina en compra. Este proyecto aborda dos preguntas complementarias con el mismo conjunto de datos:

| Componente | Pregunta | Tipo de aprendizaje |
|---|---|---|
| **Supervisado** | Dada una sesión, ¿**terminará en compra**? (variable objetivo `Revenue`) | Clasificación binaria con desbalance (15,6 % de compras) |
| **No supervisado** | ¿Qué **tipos de visitantes** existen según su forma de navegar? (sin usar `Revenue`) | Agrupamiento (segmentación) |

**Preguntas que guían el análisis**
1. ¿Qué tan desbalanceada está la compra y cómo afecta la elección de métricas?
2. ¿Qué características de la sesión se relacionan con comprar?
3. ¿Qué tan bien se puede predecir la compra y cuánto depende de una sola variable (`PageValues`)?
4. ¿Existen segmentos de visitantes con comportamientos claramente distintos?
5. ¿Los segmentos descubiertos *sin etiquetas* coinciden con quienes compran?
6. ¿Qué enfoque recomendaríamos para una aplicación real?

## Fuente de datos

**Online Shoppers Purchasing Intention Dataset** — UCI Machine Learning Repository (id 468)
- Enlace: https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset
- Cita: Sakar, C. & Kastro, Y. (2018). *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository. https://doi.org/10.24432/C5F88Q · Licencia CC BY 4.0
- Artículo asociado: Sakar, C. O., Polat, S. O., Katircioglu, M., & Kastro, Y. (2019). Real-time prediction of online shoppers' purchasing intention using multilayer perceptron and LSTM recurrent neural networks. *Neural Computing and Applications*, 31, 6893–6908.
- 12.330 sesiones (12.205 sin duplicados) · 17 variables + `Revenue`. El archivo está incluido en [`data/`](data/); detalle en [`data/README.md`](data/README.md).

## Estructura del proyecto

```
evaluacion 4/
├── README.md
├── requirements.txt
├── data/
│   ├── online_shoppers_intention.csv     datos originales (1 MB)
│   └── README.md                         ficha y diccionario de datos
├── src/
│   └── preprocesamiento.py               division train/test y preprocesador sin fuga de informacion
├── notebooks/
│   ├── 01_problema_y_eda.ipynb           problema, calidad de datos y EDA
│   ├── 02_preprocesamiento.ipynb         decisiones, pipeline anti-fuga, seleccion de variables y PCA
│   ├── 03_supervisado.ipynb              regresion logistica, Random Forest, Gradient Boosting
│   ├── 04_no_supervisado.ipynb           K-Means, Gaussian Mixture, Aglomerativo, PCA/t-SNE, perfiles
│   └── 05_comparacion_y_conclusiones.ipynb   8 preguntas comparativas y recomendacion
├── figuras/                              graficos generados por los notebooks
├── resultados/                           metricas y segmentos (CSV/JSON)
└── docs/
    └── decisiones_tecnicas.md            decisiones tecnicas, metricas y resultados
```

## Instrucciones de ejecución

```bash
git clone https://github.com/Xantyagoh/grupo3-ml-intencion-compra.git
cd grupo3-ml-intencion-compra
python -m venv venv
venv\Scripts\activate                     # Mac/Linux: source venv/bin/activate
pip install -r "evaluacion 4/requirements.txt"
cd "evaluacion 4/notebooks"
jupyter notebook                          # ejecutar 01, 02, 03, 04 y 05 en orden (Restart & Run All)
```

- Los notebooks **03 y 04 generan** los archivos de `resultados/` que lee el **05**: ejecutarlos antes.
- El notebook 03 tarda ~3–4 minutos (búsqueda de hiperparámetros); el resto, menos de un minuto cada uno.
- Todas las semillas están fijadas (`SEMILLA = 42`), así que los resultados son reproducibles.

## Video de presentación

_(se agrega el enlace al final del proyecto)_

## Referencias

- Sakar, C. & Kastro, Y. (2018). *Online Shoppers Purchasing Intention Dataset* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5F88Q
- Sakar, C. O., Polat, S. O., Katircioglu, M., & Kastro, Y. (2019). Real-time prediction of online shoppers' purchasing intention using multilayer perceptron and LSTM recurrent neural networks. *Neural Computing and Applications*, 31, 6893–6908.
