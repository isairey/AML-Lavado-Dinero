"""
===========================================================
 AML Detection System
 Transaction Rules
===========================================================

Autor: Isai Reyes Peña

Descripción:
Reglas de negocio para evaluar transacciones bancarias
antes de calcular el Risk Score.
===========================================================
"""

from typing import Dict


class TransactionRules:
    """
    Motor de reglas para validar una transacción.
    """

    HIGH_VALUE = 10_000
    VERY_HIGH_VALUE = 50_000
    LARGE_CASH = 20_000

    HIGH_RISK_COUNTRIES = {
        "Iran",
        "North Korea",
        "Syria",
        "Afghanistan",
        "Myanmar"
    }

    HIGH_RISK_TYPES = {
        "TRANSFER",
        "WIRE",
        "CRYPTO",
        "INTERNATIONAL"
    }

    # =====================================================
    # Evaluación principal
    # =====================================================

    @classmethod
    def evaluate(cls, transaction) -> Dict:

        score = 0.0
        rules = []

        # -----------------------------------------
        # Monto alto
        # -----------------------------------------

        if transaction.amount >= cls.HIGH_VALUE:

            score += 0.15

            rules.append("HIGH_VALUE_TRANSACTION")

        # -----------------------------------------
        # Monto muy alto
        # -----------------------------------------

        if transaction.amount >= cls.VERY_HIGH_VALUE:

            score += 0.25

            rules.append("VERY_HIGH_VALUE_TRANSACTION")

        # -----------------------------------------
        # Transferencia internacional
        # -----------------------------------------

        if (
            transaction.country_origin.lower()
            != transaction.country_dest.lower()
        ):

            score += 0.15

            rules.append("INTERNATIONAL_TRANSFER")

        # -----------------------------------------
        # País de alto riesgo
        # -----------------------------------------

        if transaction.country_dest in cls.HIGH_RISK_COUNTRIES:

            score += 0.20

            rules.append("HIGH_RISK_COUNTRY")

        # -----------------------------------------
        # Tipo de transacción
        # -----------------------------------------

        if (
            transaction.transaction_type.upper()
            in cls.HIGH_RISK_TYPES
        ):

            score += 0.10

            rules.append("HIGH_RISK_TRANSACTION_TYPE")

        # -----------------------------------------
        # Muchas transacciones
        # -----------------------------------------

        if hasattr(transaction, "transaction_count"):

            if transaction.transaction_count >= 25:

                score += 0.10

                rules.append("HIGH_TRANSACTION_FREQUENCY")

        # -----------------------------------------
        # Muchas internacionales
        # -----------------------------------------

        if hasattr(transaction, "international_transactions"):

            if transaction.international_transactions >= 10:

                score += 0.15

                rules.append(
                    "FREQUENT_INTERNATIONAL_TRANSFERS"
                )

        # -----------------------------------------
        # Muchas de alto valor
        # -----------------------------------------

        if hasattr(transaction, "high_value_transactions"):

            if transaction.high_value_transactions >= 5:

                score += 0.15

                rules.append(
                    "MULTIPLE_HIGH_VALUE_TRANSACTIONS"
                )

        # -----------------------------------------
        # Desviación alta
        # -----------------------------------------

        if hasattr(transaction, "std_amount"):

            if transaction.std_amount >= 5000:

                score += 0.10

                rules.append(
                    "UNUSUAL_TRANSACTION_PATTERN"
                )

        # -----------------------------------------
        # Limitar score
        # -----------------------------------------

        score = min(score, 1.0)

        return {

            "score": round(score, 2),

            "risk_level": cls.risk_level(score),

            "rules_triggered": rules,

            "rules_count": len(rules)

        }

    # =====================================================
    # Nivel de riesgo
    # =====================================================

    @staticmethod
    def risk_level(score):

        if score < 0.30:
            return "LOW"

        if score < 0.60:
            return "MEDIUM"

        if score < 0.80:
            return "HIGH"

        return "CRITICAL"

    # =====================================================
    # Validación básica
    # =====================================================

    @staticmethod
    def validate(transaction):

        errors = []

        if transaction.amount <= 0:

            errors.append(
                "El monto debe ser mayor a cero."
            )

        if not transaction.account_id:

            errors.append(
                "Cuenta origen requerida."
            )

        if not transaction.target_account:

            errors.append(
                "Cuenta destino requerida."
            )

        if (
            transaction.account_id
            == transaction.target_account
        ):

            errors.append(
                "La cuenta origen y destino no pueden ser iguales."
            )

        return errors

    # =====================================================
    # Resumen
    # =====================================================

    @classmethod
    def analyze(cls, transaction):

        validation = cls.validate(transaction)

        if validation:

            return {

                "valid": False,

                "errors": validation

            }

        result = cls.evaluate(transaction)

        result["valid"] = True

        return result