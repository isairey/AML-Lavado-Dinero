"""
===========================================================
 AML Detection System
 Rutas de la API
===========================================================

Autor: Isai Reyes Peña
"""

from fastapi import APIRouter, HTTPException

from api.schemas import (
    TransactionRequest,
    PredictionResponse
)

from api.services import (
    predict_transaction,
    system_information
)

router = APIRouter(
    prefix="/api",
    tags=["AML Detection"]
)


# ==========================================================
# Información del sistema
# ==========================================================

@router.get("/info")
def info():
    """
    Información general del sistema.
    """

    return system_information()


# ==========================================================
# Predicción
# ==========================================================

@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(transaction: TransactionRequest):
    """
    Analiza una transacción bancaria.
    """

    try:

        result = predict_transaction(transaction)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# Estado de la API
# ==========================================================

@router.get("/status")
def status():

    return {

        "status": "online",

        "model": "Isolation Forest",

        "version": "1.0.0"

    }


# ==========================================================
# Riesgo
# ==========================================================

@router.get("/risk-levels")
def risk_levels():

    return {

        "LOW": "0.00 - 0.30",

        "MEDIUM": "0.31 - 0.60",

        "HIGH": "0.61 - 0.80",

        "CRITICAL": "0.81 - 1.00"

    }


# ==========================================================
# Simulación
# ==========================================================

@router.post("/simulate")
def simulate(transaction: TransactionRequest):
    """
    Simulación rápida de una transacción.
    """

    result = predict_transaction(transaction)

    return {

        "simulation": True,

        "result": result

    }


# ==========================================================
# Modelo cargado
# ==========================================================

@router.get("/model")
def model():

    return {

        "algorithm": "Isolation Forest",

        "status": "Loaded",

        "anomaly_detection": True

    }


# ==========================================================
# Estadísticas
# ==========================================================

@router.get("/statistics")
def statistics():

    return {

        "processed_transactions": 0,

        "alerts_generated": 0,

        "high_risk_accounts": 0

    }