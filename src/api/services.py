"""
===========================================================
 AML Detection System
 Servicios de la API
===========================================================

Autor: Isai Reyes Peña

Descripción:
Contiene la lógica del negocio para evaluar
transacciones bancarias y calcular el nivel de riesgo.
===========================================================
"""

from config.config import (
    HIGH_VALUE_TRANSACTION,
    VERY_HIGH_TRANSACTION,
    HIGH_RISK_COUNTRIES,
    RISK_THRESHOLD
)


# ==========================================================
# Información del sistema
# ==========================================================

def system_information():

    return {
        "project": "AML Detection System",
        "version": "1.0.0",
        "model": "Rule-Based AML Engine",
        "status": "Running"
    }


# ==========================================================
# Calcular riesgo
# ==========================================================

def calculate_risk(transaction):

    score = 0.0

    # -----------------------------------------
    # Regla 1: Monto alto
    # -----------------------------------------

    if transaction.amount >= HIGH_VALUE_TRANSACTION:
        score += 0.35

    if transaction.amount >= VERY_HIGH_TRANSACTION:
        score += 0.25

    # -----------------------------------------
    # Regla 2: Transferencia internacional
    # -----------------------------------------

    if transaction.country_origin.lower() != transaction.country_dest.lower():
        score += 0.20

    # -----------------------------------------
    # Regla 3: País de alto riesgo
    # -----------------------------------------

    if transaction.country_dest in HIGH_RISK_COUNTRIES:
        score += 0.30

    # -----------------------------------------
    # Regla 4: Tipo de transacción
    # -----------------------------------------

    risky_types = [
        "TRANSFER",
        "WIRE",
        "CRYPTO",
        "INTERNATIONAL"
    ]

    if transaction.transaction_type.upper() in risky_types:
        score += 0.10

    return min(score, 1.0)


# ==========================================================
# Clasificación
# ==========================================================

def classify(score):

    if score < 0.30:
        return "LOW"

    if score < 0.60:
        return "MEDIUM"

    if score < 0.80:
        return "HIGH"

    return "CRITICAL"


# ==========================================================
# Mensaje
# ==========================================================

def message(level):

    messages = {

        "LOW":
            "Transacción normal.",

        "MEDIUM":
            "La transacción requiere monitoreo.",

        "HIGH":
            "Posible actividad sospechosa.",

        "CRITICAL":
            "Posible operación de lavado de dinero."

    }

    return messages[level]


# ==========================================================
# Predicción principal
# ==========================================================

def predict_transaction(transaction):

    risk_score = calculate_risk(transaction)

    level = classify(risk_score)

    suspicious = risk_score >= RISK_THRESHOLD

    return {

        "risk_score": round(risk_score, 2),

        "risk_level": level,

        "is_suspicious": suspicious,

        "message": message(level)

    }