"""
===========================================================
 AML Detection System
 Predicción del Modelo
===========================================================

Autor: Isai Reyes Peña

Descripción:
Realiza predicciones de anomalías utilizando el modelo
entrenado (Isolation Forest) y el scaler.
===========================================================
"""

import pandas as pd
import numpy as np

from config.config import MODEL_FILE, SCALER_FILE

import joblib


class AMLPredictor:

    def __init__(self):

        self.model = None
        self.scaler = None

    # ======================================================
    # CARGAR MODELO
    # ======================================================

    def load(self):

        self.model = joblib.load(MODEL_FILE)
        self.scaler = joblib.load(SCALER_FILE)

        print("Modelo y scaler cargados correctamente.")

    # ======================================================
    # PREDECIR UNA TRANSACCIÓN
    # ======================================================

    def predict_single(self, transaction: dict):

        """
        Predicción para una sola transacción.
        """

        df = pd.DataFrame([transaction])

        return self._predict(df).iloc[0].to_dict()

    # ======================================================
    # PREDECIR LOTE DE DATOS
    # ======================================================

    def predict_batch(self, df: pd.DataFrame):

        """
        Predicción para múltiples transacciones.
        """

        return self._predict(df)

    # ======================================================
    # LÓGICA INTERNA
    # ======================================================

    def _predict(self, df: pd.DataFrame):

        required_features = [

            "transaction_count",
            "total_amount",
            "average_amount",
            "std_amount",
            "high_value_transactions",
            "international_transactions"

        ]

        # Validar columnas
        missing = [col for col in required_features if col not in df.columns]

        if missing:

            raise ValueError(
                f"Faltan features necesarias: {missing}"
            )

        X = df[required_features]

        # Escalado
        X_scaled = self.scaler.transform(X)

        # Predicción
        anomaly_score = self.model.decision_function(X_scaled)

        prediction = self.model.predict(X_scaled)

        # ==================================================
        # Construcción del resultado
        # ==================================================

        result = df.copy()

        result["anomaly_score"] = anomaly_score

        result["is_anomaly"] = prediction == -1

        result["risk_level"] = result["anomaly_score"].apply(
            self._risk_level
        )

        return result

    # ======================================================
    # NIVEL DE RIESGO
    # ======================================================

    def _risk_level(self, score):

        if score > 0.3:
            return "LOW"

        elif score > 0.0:
            return "MEDIUM"

        elif score > -0.3:
            return "HIGH"

        else:
            return "CRITICAL"