"""Preprocesamiento compartido por todos los notebooks (sin fuga de informacion).

Regla de oro: TODO lo que aprende de los datos (escalado, codificacion, seleccion de
variables, umbrales) se ajusta SOLO con el conjunto de entrenamiento. Por eso el
preprocesador es un objeto de scikit-learn que se mete dentro de un Pipeline.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

RAIZ = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ / "data" / "online_shoppers_intention.csv"
SEMILLA = 42
OBJETIVO = "Revenue"

# Variables numericas de la sesion (conteos, duraciones, tasas y valores de pagina)
NUMERICAS = [
    "Administrative", "Administrative_Duration", "Informational", "Informational_Duration",
    "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues", "SpecialDay",
]
# Variables nominales (aunque vengan como numeros 1, 2, 3...: son codigos, no cantidades)
CATEGORICAS = ["Month", "VisitorType", "OperatingSystems", "Browser", "Region", "TrafficType"]
BINARIAS = ["Weekend"]
# Variables de comportamiento de navegacion usadas para segmentar (sin PageValues ni SpecialDay)
CONDUCTA = [
    "Administrative", "Administrative_Duration", "Informational", "Informational_Duration",
    "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates",
]
MESES_ORDEN = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def cargar_datos(quitar_duplicados: bool = True) -> pd.DataFrame:
    """Lee el CSV. Por defecto elimina las sesiones duplicadas exactas (125)."""
    df = pd.read_csv(RUTA_DATOS)
    if quitar_duplicados:
        df = df.drop_duplicates().reset_index(drop=True)
    return df


def dividir_train_test(df: pd.DataFrame, test_size: float = 0.20):
    """Division estratificada por la variable objetivo, con semilla fija.

    Devuelve X_train, X_test, y_train, y_test. El test NO se toca hasta la evaluacion final.
    """
    y = df[OBJETIVO].astype(int)
    X = df.drop(columns=OBJETIVO)
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=SEMILLA)


def construir_preprocesador(incluir_page_values: bool = True) -> ColumnTransformer:
    """log1p + estandarizacion para numericas, one-hot para nominales, binaria sin tocar."""
    numericas = [c for c in NUMERICAS if incluir_page_values or c != "PageValues"]
    return ColumnTransformer(
        transformers=[
            ("num", Pipeline([("log", FunctionTransformer(np.log1p, feature_names_out="one-to-one")),
                              ("escala", StandardScaler())]), numericas),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAS),
            ("bin", "passthrough", BINARIAS),
        ],
        verbose_feature_names_out=False,
    )


def matriz_conducta(df: pd.DataFrame, columnas=None):
    """Matriz estandarizada (log1p + z-score) de las variables de conducta para agrupamiento.

    El agrupamiento no tiene conjunto de prueba ni usa la variable objetivo; se ajusta el
    escalador sobre todas las sesiones porque no hay etiquetas que filtrar.
    """
    columnas = columnas or CONDUCTA
    X = np.log1p(df[columnas].astype(float))
    escala = StandardScaler().fit(X)
    return escala.transform(X), escala
