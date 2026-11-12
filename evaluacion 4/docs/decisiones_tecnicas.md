# Decisiones técnicas, métricas y resultados

> **Destino en el repositorio:** `evaluacion 4/docs/decisiones_tecnicas.md`
> Resume **qué decidimos, por qué y con qué evidencia**. Las cifras salen de los notebooks 01–05 y de `resultados/`; si cambian al re-ejecutar, actualízalas aquí.

## 1. Datos y preparación

| # | Decisión | Justificación | Evidencia |
|---|---|---|---|
| D1 | Eliminar **125 duplicados exactos** antes de dividir | Un duplicado en train y otro en test es fuga; además todos eran sesiones sin compra | Notebook 01 (3) |
| D2 | División **estratificada 80/20**, semilla 42 | La compra es solo 15,6 %: sin estratificar el test podría quedar con muy pocos positivos | 9.764 train (1.526 compras) · 2.441 test (382 compras) |
| D3 | `log(1+x)` + estandarización en las 10 numéricas | Asimetría 1,9–7,5 y 46–90 % de ceros en varias | Notebook 01 (5.2) |
| D4 | **One-hot** en `Month`, `VisitorType`, `OperatingSystems`, `Browser`, `Region`, `TrafficType` | Son códigos sin orden: tratarlos como números sería un error | 17 variables → 73 columnas |
| D5 | **No imputar, no eliminar atípicos** | No hay faltantes; los atípicos son visitantes muy activos reales y `log1p` los controla | Notebook 01 (3, 5.2) |
| D6 | Todo el preprocesamiento **dentro de un `Pipeline`** y ajustado solo con train | Evita fuga en la validación cruzada y en el test | Notebook 02 (3): media 0 / desv. 1 exactas en train, no en test |
| D7 | **No usar PCA como entrada de los modelos** | 10 componentes solo conservan 80 % de la varianza; se pierde interpretabilidad | Notebook 02 (5) |
| D8 | **No eliminar variables por VIF o por baja información mutua** | VIF < 8; árboles y regularización L2 lo manejan; mejor medir con permutación | Notebook 02 (4) |
| D9 | **`PageValues` con y sin**, y excluida del agrupamiento | Se calcula con información del resultado; domina la información mutua (0,164 vs 0,038 de la segunda) | Notebooks 01, 02, 03 |

## 2. Componente supervisado

| # | Decisión | Justificación | Evidencia |
|---|---|---|---|
| S1 | Métrica principal **PR-AUC** (además de F1, Recall, Precision, ROC-AUC y matriz de confusión) | Con 84,4 % de negativos, el accuracy engaña (un "siempre no" saca 84,4 %); la ROC-AUC es optimista | Notebook 03 (2, 3) |
| S2 | **3 modelos**: regresión logística, Random Forest, Gradient Boosting | Lineal interpretable frente a dos de árboles que captan no linealidades | Notebook 03 (1) |
| S3 | Desbalance con **pesos de clase + umbral** (sin remuestreo) | Remuestrear antes de dividir causa fuga; los pesos no empeoran el ranking y suben el recall | Notebook 03 (4) |
| S4 | **Búsqueda aleatoria** de hiperparámetros optimizando PR-AUC, solo con train | Evita usar el test en el ajuste | Notebook 03 (6) |
| S5 | **Umbral** elegido con predicciones fuera de muestra en train (máx. F1) | El test no interviene | Notebook 03 (7) |
| S6 | **Modelo elegido por PR-AUC fuera de muestra en train** (no por test) | Evita seleccionar sobre el test | RF 0,752 · GB 0,749 · LR 0,662 |
| S7 | **Ablación de `PageValues`** | Medir cuánto depende el modelo de una variable con riesgo de fuga | Notebook 03 (10) |

**Resultados (test, 2.441 sesiones / 382 compras):**

| Modelo | Umbral | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Regresión logística | 0,608 | 0,602 | 0,764 | 0,674 | 0,926 | 0,678 |
| **Random Forest (elegido)** | 0,673 | 0,653 | 0,728 | 0,688 | 0,936 | 0,751 |
| Gradient Boosting | 0,703 | 0,643 | 0,736 | 0,686 | 0,934 | 0,754 |

- El modelo elegido detecta **278 de 382 compras** (recall 72,8 %) con precision de 65,3 %: **4,8 veces la PR-AUC del azar** (0,156).
- **`PageValues` explica más de la mitad del desempeño:** sin ella la PR-AUC baja a **0,37** (2,4 veces el azar); ROC-AUC 0,94 → 0,79.
- Importancia por permutación: `PageValues` (0,54 de caída de PR-AUC) ≫ `Month` (0,05) > `ExitRates` > `BounceRates`.

## 3. Componente no supervisado

| # | Decisión | Justificación | Evidencia |
|---|---|---|---|
| U1 | **`Revenue` no entra** al agrupamiento; se usa solo después | Requisito del enunciado | Notebook 04 (7) |
| U2 | **8 variables de conducta** (sin `PageValues`, `SpecialDay` ni categóricas) | `PageValues` contiene el resultado; el agrupamiento por distancias necesita numéricas comparables | Notebook 04 (inicio) |
| U3 | **3 algoritmos**: K-Means, Gaussian Mixture, Aglomerativo (Ward) | Tres supuestos distintos de forma del grupo; si coinciden, la estructura es robusta | Notebook 04 (1) |
| U4 | **k = 4** | Davies-Bouldin mínimo (0,850) y Calinski-Harabasz máximo (9.436); silhouette 0,409 (k = 3 da 0,434 pero fusiona perfiles) | Notebook 04 (3) |
| U5 | **K-Means** como algoritmo de análisis | Mejor silhouette (0,409) y CH; centroides interpretables | Notebook 04 (4.2) |
| U6 | PCA y **t-SNE (muestra de 5.000)** solo para visualizar | PCA conserva 73,7 % de la varianza; t-SNE pierde distancias globales | Notebook 04 (5) |

**Resultados (k = 4):**

| Algoritmo | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---|---|---|---|
| K-Means | 0,409 | 0,850 | 9.436 |
| Gaussian Mixture | 0,377 | 0,865 | 7.923 |
| Aglomerativo (Ward) | 0,395 | 0,836 | 8.521 |

- Acuerdo entre algoritmos (ARI): 0,79 – 0,91. Estabilidad de K-Means: ARI 1,000 (semillas) y 0,997 (submuestras del 80 %).
- **Segmentos:** Rebotadores (6,5 % de sesiones · 0,5 % compra), Consultores rápidos de producto (40,9 % · 10,6 %), Exploradores con cuenta (34,5 % · 20,1 % · aportan el 44 % de las compras), Navegantes intensos (18,1 % · 23,9 %).
- Relación con la etiqueta: **ARI 0,011, NMI 0,025** (no coinciden como partición, pero la tasa de compra sube con el compromiso del grupo).

## 4. Lista de verificación anti-fuga de información

- [x] Duplicados eliminados **antes** de dividir.
- [x] División estratificada hecha una sola vez; el test no se usa para elegir variables, hiperparámetros, umbral ni modelo.
- [x] Escalado, codificación e imputación (inexistente) **dentro del `Pipeline`**, ajustados por pliegue.
- [x] Información mutua, VIF y PCA del notebook 02 calculados **solo con train**.
- [x] Umbral elegido con predicciones fuera de muestra de train.
- [x] Modelo elegido por PR-AUC fuera de muestra de train.
- [x] Variable con riesgo de fuga (`PageValues`) evaluada con ablación y excluida del agrupamiento.
- [x] `Revenue` fuera del agrupamiento.

## 5. Reproducibilidad

Semilla fija (`SEMILLA = 42`) en la división, los modelos, la validación cruzada, K-Means, GMM, PCA y t-SNE. Versiones usadas: ver `requirements.txt`. Cambios de versión de scikit-learn pueden alterar levemente los decimales.
