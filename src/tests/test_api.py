"""
===========================================================
 AML Detection System
 Test API
===========================================================

Autor: Isai Reyes Peña

Descripción:
Pruebas automáticas para la API REST utilizando pytest
y FastAPI TestClient.
===========================================================
"""

import pytest
from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


# ==========================================================
# HEALTH CHECK
# ==========================================================

def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "message" in data


# ==========================================================
# INFO
# ==========================================================

def test_info():

    response = client.get("/api/info")

    assert response.status_code == 200

    data = response.json()

    assert "project" in data
    assert "version" in data


# ==========================================================
# STATUS
# ==========================================================

def test_status():

    response = client.get("/api/status")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data


# ==========================================================
# RISK LEVELS
# ==========================================================

def test_risk_levels():

    response = client.get("/api/risk-levels")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


# ==========================================================
# PREDICCIÓN CORRECTA
# ==========================================================

def test_prediction():

    payload = {

        "account_id": "ACC001",

        "target_account": "ACC002",

        "amount": 25000,

        "transaction_type": "TRANSFER",

        "country_origin": "Mexico",

        "country_dest": "United States",

        "transaction_count": 12,

        "high_value_transactions": 2,

        "international_transactions": 1,

        "average_amount": 3500,

        "std_amount": 1200,

        "total_amount": 42000

    }

    response = client.post(
        "/api/predict",
        json=payload
    )

    assert response.status_code == 200

    result = response.json()

    assert "risk_score" in result
    assert "risk_level" in result
    assert "is_suspicious" in result


# ==========================================================
# VALIDACIÓN
# ==========================================================

def test_invalid_transaction():

    payload = {

        "account_id": "",

        "target_account": "",

        "amount": -100,

        "transaction_type": "",

        "country_origin": "",

        "country_dest": ""

    }

    response = client.post(
        "/api/predict",
        json=payload
    )

    assert response.status_code in [400, 422]


# ==========================================================
# TRANSACCIÓN DE ALTO RIESGO
# ==========================================================

def test_high_risk_transaction():

    payload = {

        "account_id": "ACC999",

        "target_account": "ACC888",

        "amount": 900000,

        "transaction_type": "WIRE",

        "country_origin": "Mexico",

        "country_dest": "Iran",

        "transaction_count": 120,

        "high_value_transactions": 35,

        "international_transactions": 50,

        "average_amount": 55000,

        "std_amount": 12000,

        "total_amount": 980000

    }

    response = client.post(
        "/api/predict",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_level"] in [
        "HIGH",
        "CRITICAL"
    ]

    assert data["is_suspicious"] is True


# ==========================================================
# ENDPOINT NO EXISTENTE
# ==========================================================

def test_not_found():

    response = client.get("/api/does-not-exist")

    assert response.status_code == 404


# ==========================================================
# MÉTODO NO PERMITIDO
# ==========================================================

def test_method_not_allowed():

    response = client.put("/api/info")

    assert response.status_code == 405


# ==========================================================
# PRUEBA DE RENDIMIENTO BÁSICA
# ==========================================================

def test_multiple_requests():

    payload = {

        "account_id": "ACC001",

        "target_account": "ACC002",

        "amount": 15000,

        "transaction_type": "TRANSFER",

        "country_origin": "Mexico",

        "country_dest": "Canada",

        "transaction_count": 10,

        "high_value_transactions": 1,

        "international_transactions": 2,

        "average_amount": 2500,

        "std_amount": 500,

        "total_amount": 25000

    }

    for _ in range(20):

        response = client.post(
            "/api/predict",
            json=payload
        )

        assert response.status_code == 200