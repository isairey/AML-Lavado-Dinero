"""
===========================================================
 AML Detection System
 Test Machine Learning Model
===========================================================

Autor: Isai Reyes Peña

Descripción:
Pruebas unitarias para el modelo de Machine Learning
(Isolation Forest), entrenamiento, predicción y
evaluación.
===========================================================
"""

import pandas as pd
import pytest

from src.models.anomaly_detection import AnomalyDetector
from src.models.predict import AMLPredictor


# ==========================================================
# DATASET DE PRUEBA
# ==========================================================

@pytest.fixture
def sample_data():

    return pd.DataFrame({

        "transaction_count": [5, 12, 50, 3, 80],

        "total_amount": [
            5000,
            15000,
            500000,
            2000,
            950000
        ],

        "average_amount": [
            1000,
            2500,
            10000,
            500,
            25000
        ],

        "std_amount": [
            200,
            600,
            8000,
            100,
            12000
        ],

        "high_value_transactions": [
            0,
            1,
            12,
            0,
            30
        ],

        "international_transactions": [
            0,
            2,
            20,
            0,
            40
        ]

    })


# ==========================================================
# ENTRENAMIENTO
# ==========================================================

def test_model_training(sample_data):

    detector = AnomalyDetector()

    detector.train(sample_data)

    assert detector.is_trained is True


# ==========================================================
# PREDICCIÓN
# ==========================================================

def test_prediction(sample_data):

    detector = AnomalyDetector()

    detector.train(sample_data)

    predictions = detector.predict(sample_data)

    assert len(predictions) == len(sample_data)

    assert "anomaly_score" in predictions.columns

    assert "is_anomaly" in predictions.columns


# ==========================================================
# GUARDAR MODELO
# ==========================================================

def test_save_model(sample_data):

    detector = AnomalyDetector()

    detector.train(sample_data)

    detector.save_model()

    assert True


# ==========================================================
# CARGAR MODELO
# ==========================================================

def test_load_model():

    predictor = AMLPredictor()

    predictor.load()

    assert predictor.model is not None

    assert predictor.scaler is not None


# ==========================================================
# PREDICCIÓN INDIVIDUAL
# ==========================================================

def test_single_prediction(sample_data):

    detector = AnomalyDetector()

    detector.train(sample_data)

    detector.save_model()

    predictor = AMLPredictor()

    predictor.load()

    result = predictor.predict_single({

        "transaction_count": 12,

        "total_amount": 35000,

        "average_amount": 4000,

        "std_amount": 800,

        "high_value_transactions": 2,

        "international_transactions": 1

    })

    assert "risk_level" in result

    assert "is_anomaly" in result


# ==========================================================
# PREDICCIÓN POR LOTE
# ==========================================================

def test_batch_prediction(sample_data):

    detector = AnomalyDetector()

    detector.train(sample_data)

    detector.save_model()

    predictor = AMLPredictor()

    predictor.load()

    result = predictor.predict_batch(sample_data)

    assert len(result) == len(sample_data)


# ==========================================================
# VALIDACIÓN DE COLUMNAS
# ==========================================================

def test_missing_columns():

    predictor = AMLPredictor()

    predictor.model = object()
    predictor.scaler = object()

    df = pd.DataFrame({

        "amount": [1000]

    })

    with pytest.raises(ValueError):

        predictor._predict(df)


# ==========================================================
# RIESGO
# ==========================================================

def test_risk_level():

    predictor = AMLPredictor()

    assert predictor._risk_level(0.60) == "LOW"

    assert predictor._risk_level(0.15) == "MEDIUM"

    assert predictor._risk_level(-0.10) == "HIGH"

    assert predictor._risk_level(-0.60) == "CRITICAL"


# ==========================================================
# CONSISTENCIA
# ==========================================================

def test_prediction_consistency(sample_data):

    detector = AnomalyDetector()

    detector.train(sample_data)

    first = detector.predict(sample_data)

    second = detector.predict(sample_data)

    assert len(first) == len(second)


# ==========================================================
# DATAFRAME VACÍO
# ==========================================================

def test_empty_dataframe():

    detector = AnomalyDetector()

    df = pd.DataFrame(columns=[

        "transaction_count",

        "total_amount",

        "average_amount",

        "std_amount",

        "high_value_transactions",

        "international_transactions"

    ])

    with pytest.raises(Exception):

        detector.train(df)