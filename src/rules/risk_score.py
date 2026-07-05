"""
===========================================================
 AML Detection System
 Risk Score Engine
===========================================================

Autor: Isai Reyes Peña

Descripción:
Calcula el Risk Score final combinando el resultado
del modelo de Machine Learning y las reglas AML.
===========================================================
"""

from typing import Dict


class RiskScoreEngine:
    """
    Motor para calcular el riesgo final.
    """

    # Peso del modelo de Machine Learning
    ML_WEIGHT = 0.60

    # Peso del motor de reglas
    RULE_WEIGHT = 0.40

    @classmethod
    def calculate(
        cls,
        anomaly_score: float,
        rules_score: float
    ) -> Dict:
        """
        Calcula el score final de riesgo.

        Parámetros
        ----------
        anomaly_score : float
            Score generado por el modelo ML (0-1).

        rules_score : float
            Score generado por las reglas AML (0-1).
        """

        anomaly_score = max(0.0, min(1.0, anomaly_score))
        rules_score = max(0.0, min(1.0, rules_score))

        final_score = (
            anomaly_score * cls.ML_WEIGHT +
            rules_score * cls.RULE_WEIGHT
        )

        final_score = round(final_score, 2)

        return {
            "risk_score": final_score,
            "risk_level": cls.risk_level(final_score),
            "is_suspicious": final_score >= 0.70
        }

    @staticmethod
    def risk_level(score: float) -> str:
        """
        Convierte el score a un nivel de riesgo.
        """

        if score < 0.30:
            return "LOW"

        elif score < 0.60:
            return "MEDIUM"

        elif score < 0.80:
            return "HIGH"

        return "CRITICAL"

    @staticmethod
    def recommendation(level: str) -> str:
        """
        Devuelve una recomendación según el nivel de riesgo.
        """

        recommendations = {

            "LOW":
                "Registrar la transacción sin acciones adicionales.",

            "MEDIUM":
                "Monitorear la cuenta y revisar operaciones futuras.",

            "HIGH":
                "Enviar la operación a revisión por un analista AML.",

            "CRITICAL":
                "Generar alerta inmediata y bloquear temporalmente la operación."

        }

        return recommendations[level]

    @classmethod
    def evaluate(
        cls,
        anomaly_score: float,
        rules_score: float
    ) -> Dict:
        """
        Evaluación completa del riesgo.
        """

        result = cls.calculate(
            anomaly_score,
            rules_score
        )

        result["recommendation"] = cls.recommendation(
            result["risk_level"]
        )

        return result