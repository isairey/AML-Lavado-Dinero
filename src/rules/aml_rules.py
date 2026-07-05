"""
===========================================================
 AML Detection System
 AML Rules Engine
===========================================================

Autor: Isai Reyes Peña

Descripción:
Motor de reglas para detectar posibles operaciones
de lavado de dinero.
===========================================================
"""

from typing import Dict, List

from config.config import (
    HIGH_VALUE_TRANSACTION,
    VERY_HIGH_TRANSACTION,
    HIGH_RISK_COUNTRIES,
)


class AMLRulesEngine:
    """
    Motor de reglas AML.
    """

    @staticmethod
    def evaluate(transaction) -> Dict:
        """
        Evalúa una transacción y devuelve
        un score basado en reglas.
        """

        score = 0.0
        rules_triggered: List[str] = []

        # ==================================================
        # Regla 1
        # Transacción de alto valor
        # ==================================================

        if transaction.amount >= HIGH_VALUE_TRANSACTION:

            score += 0.25

            rules_triggered.append(
                "HIGH_VALUE_TRANSACTION"
            )

        # ==================================================
        # Regla 2
        # Transacción extremadamente alta
        # ==================================================

        if transaction.amount >= VERY_HIGH_TRANSACTION:

            score += 0.30

            rules_triggered.append(
                "VERY_HIGH_TRANSACTION"
            )

        # ==================================================
        # Regla 3
        # Transferencia internacional
        # ==================================================

        if (
            transaction.country_origin.lower()
            != transaction.country_dest.lower()
        ):

            score += 0.15

            rules_triggered.append(
                "INTERNATIONAL_TRANSFER"
            )

        # ==================================================
        # Regla 4
        # País de alto riesgo
        # ==================================================

        if transaction.country_dest in HIGH_RISK_COUNTRIES:

            score += 0.30

            rules_triggered.append(
                "HIGH_RISK_COUNTRY"
            )

        # ==================================================
        # Regla 5
        # Transferencias frecuentes
        # ==================================================

        if hasattr(transaction, "transaction_count"):

            if transaction.transaction_count > 30:

                score += 0.15

                rules_triggered.append(
                    "HIGH_TRANSACTION_VOLUME"
                )

        # ==================================================
        # Regla 6
        # Muchas operaciones internacionales
        # ==================================================

        if hasattr(transaction, "international_transactions"):

            if transaction.international_transactions > 10:

                score += 0.20

                rules_triggered.append(
                    "FREQUENT_INTERNATIONAL_TRANSFERS"
                )

        # ==================================================
        # Regla 7
        # Muchas operaciones de alto valor
        # ==================================================

        if hasattr(transaction, "high_value_transactions"):

            if transaction.high_value_transactions > 5:

                score += 0.20

                rules_triggered.append(
                    "MULTIPLE_HIGH_VALUE_OPERATIONS"
                )

        # Limitar score

        score = min(score, 1.0)

        return {

            "rules_score": round(score, 2),

            "rules_triggered": rules_triggered,

            "rules_count": len(rules_triggered)

        }

    @staticmethod
    def risk_level(score: float):

        """
        Convierte el score en nivel de riesgo.
        """

        if score < 0.30:
            return "LOW"

        if score < 0.60:
            return "MEDIUM"

        if score < 0.80:
            return "HIGH"

        return "CRITICAL"