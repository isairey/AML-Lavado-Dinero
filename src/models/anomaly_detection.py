"""
===========================================================
 AML Detection System
 Detección de Anomalías
===========================================================

Autor: Isai Reyes Peña

Descripción:
Modelo de Machine Learning para detectar anomalías
en transacciones bancarias utilizando Isolation Forest.
===========================================================
"""

import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from config.config import (
    MODEL_FILE,
    SCALER_FILE,
    CONTAMINATION,
    RANDOM_STATE
)


class AnomalyDetector:

    def __init__(self):

        self.model = IsolationForest(
            n_estimators=200,
            contamination=CONTAMINATION,
            random_state=RANDOM_STATE
        )

        self.scaler = StandardScaler()

        self.is_trained = False

    # ======================================================
    # ENTRENAMIENTO
    # ======================================================

    def train(self, df: pd.DataFrame):

        """
        Entrena el modelo con features numéricas.
        """

        features = df[[
            "transaction_count",
            "total_amount",
            "average_amount",
            "std_amount",
            "high_value_transactions",
            "international_transactions"
        ]]

        # Escalado
        X_scaled = self.scaler.fit_transform(features)

        # Entrenar modelo
        self.model.fit(X_scaled)

        self.is_trained = True

        print("Modelo de anomalías entrenado correctamente.")

    # ======================================================
    # PREDICCIÓN
    # ======================================================

    def predict(self, df: pd.DataFrame):

        """
        Retorna score de anomalía y etiqueta.
        """

        features = df[[
            "transaction_count",
            "total_amount",
            "average_amount",
            "std_amount",
            "high_value_transactions",
            "international_transactions"
        ]]

        X_scaled = self.scaler.transform(features)

        anomaly_score = self.model.decision_function(X_scaled)

        prediction = self.model.predict(X_scaled)

        df_result = df.copy()

        # -1 = anomalía, 1 = normal
        df_result["anomaly_score"] = anomaly_score

        df_result["is_anomaly"] = prediction == -1

        return df_result

    # ======================================================
    # GUARDAR MODELO
    # ======================================================

    def save_model(self):

        joblib.dump(self.model, MODEL_FILE)
        joblib.dump(self.scaler, SCALER_FILE)

        print("Modelo guardado correctamente.")

    # ======================================================
    # CARGAR MODELO
    # ======================================================

    def load_model(self):

        self.model = joblib.load(MODEL_FILE)
        self.scaler = joblib.load(SCALER_FILE)

        self.is_trained = True

        print("Modelo cargado correctamente.")