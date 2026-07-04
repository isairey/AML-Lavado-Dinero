"""
===========================================================
 AML Detection System
 Evaluación del Modelo
===========================================================

Autor: Isai Reyes Peña

Descripción:
Evalúa el rendimiento del modelo de detección de anomalías
(Isolation Forest) usando métricas básicas y análisis
de resultados.
===========================================================
"""

import numpy as np
import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from config.config import RISK_THRESHOLD


class ModelEvaluator:

    # ======================================================
    # EVALUACIÓN GENERAL
    # ======================================================

    @staticmethod
    def evaluate_anomalies(df: pd.DataFrame):
        """
        Evalúa el modelo comparando predicción vs etiquetas reales
        (si existen).
        """

        if "is_anomaly" not in df.columns:
            raise ValueError("El DataFrame no contiene predicciones del modelo.")

        # ==================================================
        # Convertir anomalías a etiquetas binarias
        # ==================================================

        y_pred = df["is_anomaly"].astype(int)

        # Si no hay labels reales, usamos heurística
        if "true_label" in df.columns:
            y_true = df["true_label"].astype(int)
        else:
            # Simulación (en proyectos reales vendría del banco)
            y_true = (df["anomaly_score"] < df["anomaly_score"].quantile(0.02)).astype(int)

        # ==================================================
        # Métricas
        # ==================================================

        acc = accuracy_score(y_true, y_pred)

        cm = confusion_matrix(y_true, y_pred)

        report = classification_report(y_true, y_pred)

        print("\n" + "=" * 60)
        print("EVALUACIÓN DEL MODELO AML")
        print("=" * 60)

        print(f"Accuracy: {acc:.4f}")

        print("\nMatriz de Confusión:")
        print(cm)

        print("\nReporte de Clasificación:")
        print(report)

        return {
            "accuracy": acc,
            "confusion_matrix": cm,
            "report": report
        }

    # ======================================================
    # DETECCIÓN DE CASOS CRÍTICOS
    # ======================================================

    @staticmethod
    def high_risk_analysis(df: pd.DataFrame):
        """
        Analiza transacciones de alto riesgo.
        """

        if "anomaly_score" not in df.columns:
            raise ValueError("Falta la columna anomaly_score.")

        high_risk = df[df["anomaly_score"] < RISK_THRESHOLD]

        print("\n" + "=" * 60)
        print("TRANSACCIONES DE ALTO RIESGO")
        print("=" * 60)

        print(f"Total detectadas: {len(high_risk)}")

        if "account_id" in df.columns:
            print("\nTop cuentas sospechosas:")

            top_accounts = (
                high_risk["account_id"]
                .value_counts()
                .head(10)
            )

            print(top_accounts)

        return high_risk

    # ======================================================
    # ESTADÍSTICAS DEL MODELO
    # ======================================================

    @staticmethod
    def model_summary(df: pd.DataFrame):

        print("\n" + "=" * 60)
        print("RESUMEN GENERAL")
        print("=" * 60)

        print(f"Total registros analizados: {len(df)}")

        if "is_anomaly" in df.columns:

            anomalies = df["is_anomaly"].sum()

            print(f"Anomalías detectadas: {anomalies}")

            print(f"Porcentaje anomalías: {(anomalies/len(df))*100:.2f}%")

        if "anomaly_score" in df.columns:

            print("\nScore promedio:", df["anomaly_score"].mean())
            print("Score mínimo:", df["anomaly_score"].min())
            print("Score máximo:", df["anomaly_score"].max())