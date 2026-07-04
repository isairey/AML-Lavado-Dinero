"""
===========================================================
 AML Detection System
 Esquemas de la API
===========================================================

Autor: Isai Reyes Peña

Descripción:
Modelos Pydantic utilizados para validar la información
de entrada y salida de la API.
===========================================================
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# ==========================================================
# Transacción de entrada
# ==========================================================

class TransactionRequest(BaseModel):
    """
    Información de una transacción bancaria.
    """

    account_id: str = Field(
        ...,
        example="ACC10001",
        description="Cuenta origen"
    )

    target_account: str = Field(
        ...,
        example="ACC20015",
        description="Cuenta destino"
    )

    amount: float = Field(
        ...,
        gt=0,
        example=15000.50,
        description="Monto de la transacción"
    )

    country_origin: str = Field(
        ...,
        example="Mexico"
    )

    country_dest: str = Field(
        ...,
        example="Panama"
    )

    transaction_type: str = Field(
        ...,
        example="Transfer"
    )

    timestamp: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Fecha y hora de la transacción"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_id": "ACC10001",
                "target_account": "ACC20015",
                "amount": 15000.50,
                "country_origin": "Mexico",
                "country_dest": "Panama",
                "transaction_type": "Transfer"
            }
        }
    )


# ==========================================================
# Respuesta del modelo
# ==========================================================

class PredictionResponse(BaseModel):
    """
    Resultado del análisis AML.
    """

    risk_score: float

    risk_level: str

    is_suspicious: bool

    message: str


# ==========================================================
# Información del sistema
# ==========================================================

class SystemInfo(BaseModel):

    project: str

    version: str

    model: str

    status: str


# ==========================================================
# Health Check
# ==========================================================

class HealthResponse(BaseModel):

    status: str

    service: str


# ==========================================================
# Estadísticas
# ==========================================================

class StatisticsResponse(BaseModel):

    processed_transactions: int

    alerts_generated: int

    high_risk_accounts: int


# ==========================================================
# Información del modelo
# ==========================================================

class ModelInfo(BaseModel):

    algorithm: str

    status: str

    anomaly_detection: bool