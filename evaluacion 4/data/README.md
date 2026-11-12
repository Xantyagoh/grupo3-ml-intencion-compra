# Datos

## Fuente

**Online Shoppers Purchasing Intention Dataset** — UCI Machine Learning Repository (id 468)
- Página: https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset
- DOI: https://doi.org/10.24432/C5F88Q · Autores: C. Sakar y Y. Kastro (donado el 30/08/2018) · Licencia **CC BY 4.0**
- Contenido: 12.330 sesiones de navegación. Cada sesión pertenece a un **usuario distinto** dentro de un periodo de un año (para evitar sesgos por campaña, fecha especial o perfil de usuario). Sin valores faltantes.
- Archivo incluido: `online_shoppers_intention.csv` (1 MB). Si se perdiera, se descarga desde la página de la UCI (botón *Download*).

## Resumen

| | |
|---|---|
| Sesiones | 12.330 (12.205 tras eliminar 125 duplicados exactos) |
| Variables | 17 predictoras + `Revenue` (objetivo) |
| Compras | 1.908 (15,6 % tras quitar duplicados) |
| Faltantes | 0 |

## Diccionario de datos

| Variable | Tipo | Significado |
|---|---|---|
| `Administrative`, `Administrative_Duration` | numérica | Nº de páginas administrativas visitadas y tiempo total en ellas (segundos) |
| `Informational`, `Informational_Duration` | numérica | Ídem para páginas informativas |
| `ProductRelated`, `ProductRelated_Duration` | numérica | Ídem para páginas de producto |
| `BounceRates` | numérica (0–1) | % de visitas que entran por una página y se van sin hacer nada más (Google Analytics) |
| `ExitRates` | numérica (0–1) | % de vistas de la página que fueron la última de la sesión (Google Analytics) |
| `PageValues` | numérica | Valor promedio de las páginas visitadas antes de completar una transacción (Google Analytics). **Posible fuga de información** (ver notebooks 01 y 03) |
| `SpecialDay` | numérica (0–1) | Cercanía de la visita a una fecha especial (1 = máxima) |
| `Month` | categórica | Mes de la visita (10 meses; no hay enero ni abril) |
| `OperatingSystems`, `Browser`, `Region`, `TrafficType` | categórica (códigos) | Sistema operativo, navegador, región y tipo de tráfico (números sin orden) |
| `VisitorType` | categórica | `Returning_Visitor`, `New_Visitor`, `Other` |
| `Weekend` | binaria | ¿Fin de semana? |
| **`Revenue`** | **binaria (objetivo)** | ¿La sesión terminó en compra? |
