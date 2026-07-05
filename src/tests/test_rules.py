"""
===========================================================
 AML Detection System
 Test Rules Engine
===========================================================

Autor: Isai Reyes Peña

Descripción:
Pruebas unitarias para las reglas AML y el cálculo
del Risk Score.
===========================================================
"""

import pytest

from src.rules.aml_rules import AMLRulesEngine
from src.rules.risk_score import RiskScoreEngine
from src.rules.transaction_rules import TransactionRules


# ==========================================================
# TRANSACCIÓN DE PRUEBA
# ==========================================================

class MockTransaction:

    def __init__(self, **kwargs):

        self.account_id = kwargs.get("account_id", "ACC001")

        self.target_account = kwargs.get("target_account", "ACC002")

        self.amount = kwargs.get("amount", 5000)

        self.transaction_type = kwargs.get(
            "transaction_type",
            "TRANSFER"
        )

        self.country_origin = kwargs.get(
            "country_origin",
            "Mexico"
        )

        self.country_dest = kwargs.get(
            "country_dest",
            "Mexico"
        )

        self.transaction_count = kwargs.get(
            "transaction_count",
            5
        )

        self.high_value_transactions = kwargs.get(
            "high_value_transactions",
            0
        )

        self.international_transactions = kwargs.get(
            "international_transactions",
            0
        )

        self.average_amount = kwargs.get(
            "average_amount",
            1000
        )

        self.std_amount = kwargs.get(
            "std_amount",
            300
        )


# ==========================================================
# TRANSACCIÓN NORMAL
# ==========================================================

def test_normal_transaction():

    tx = MockTransaction()

    result = TransactionRules.analyze(tx)

    assert result["valid"] is True

    assert result["risk_level"] == "LOW"


# ==========================================================
# TRANSACCIÓN ALTO VALOR
# ==========================================================

def test_high_value_transaction():

    tx = MockTransaction(

        amount=80000

    )

    result = TransactionRules.analyze(tx)

    assert result["score"] > 0

    assert "HIGH_VALUE_TRANSACTION" in result["rules_triggered"]


# ==========================================================
# TRANSACCIÓN INTERNACIONAL
# ==========================================================

def test_international_transaction():

    tx = MockTransaction(

        country_dest="United States"

    )

    result = TransactionRules.analyze(tx)

    assert "INTERNATIONAL_TRANSFER" in result["rules_triggered"]


# ==========================================================
# PAÍS DE ALTO RIESGO
# ==========================================================

def test_high_risk_country():

    tx = MockTransaction(

        amount=900000,

        country_dest="Iran"

    )

    result = AMLRulesEngine.evaluate(tx)

    assert result["rules_score"] > 0

    assert "HIGH_RISK_COUNTRY" in result["rules_triggered"]


# ==========================================================
# MUCHAS TRANSACCIONES
# ==========================================================

def test_high_frequency():

    tx = MockTransaction(

        transaction_count=120

    )

    result = AMLRulesEngine.evaluate(tx)

    assert "HIGH_TRANSACTION_VOLUME" in result["rules_triggered"]


# ==========================================================
# RISK SCORE
# ==========================================================

def test_risk_score():

    result = RiskScoreEngine.evaluate(

        anomaly_score=0.80,

        rules_score=0.60

    )

    assert "risk_score" in result

    assert "risk_level" in result

    assert "recommendation" in result


# ==========================================================
# SCORE BAJO
# ==========================================================

def test_low_score():

    result = RiskScoreEngine.evaluate(

        anomaly_score=0.10,

        rules_score=0.10

    )

    assert result["risk_level"] == "LOW"

    assert result["is_suspicious"] is False


# ==========================================================
# SCORE CRÍTICO
# ==========================================================

def test_critical_score():

    result = RiskScoreEngine.evaluate(

        anomaly_score=1.0,

        rules_score=1.0

    )

    assert result["risk_level"] == "CRITICAL"

    assert result["is_suspicious"] is True


# ==========================================================
# VALIDACIÓN
# ==========================================================

def test_validation():

    tx = MockTransaction(

        amount=-100,

        account_id="",

        target_account=""

    )

    result = TransactionRules.analyze(tx)

    assert result["valid"] is False

    assert len(result["errors"]) > 0


# ==========================================================
# RECOMENDACIONES
# ==========================================================

@pytest.mark.parametrize(
    "level",
    [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]
)
def test_recommendations(level):

    recommendation = RiskScoreEngine.recommendation(level)

    assert isinstance(recommendation, str)

    assert len(recommendation) > 5


# ==========================================================
# RISK LEVELS
# ==========================================================

def test_risk_levels():

    assert RiskScoreEngine.risk_level(0.10) == "LOW"

    assert RiskScoreEngine.risk_level(0.45) == "MEDIUM"

    assert RiskScoreEngine.risk_level(0.70) == "HIGH"

    assert RiskScoreEngine.risk_level(0.95) == "CRITICAL"


# ==========================================================
# LÍMITE DEL SCORE
# ==========================================================

def test_score_limit():

    result = RiskScoreEngine.calculate(

        anomaly_score=5,

        rules_score=5

    )

    assert result["risk_score"] <= 1.0


# ==========================================================
# TRANSACCIÓN MUY SOSPECHOSA
# ==========================================================

def test_suspicious_transaction():

    tx = MockTransaction(

        amount=950000,

        country_dest="Iran",

        transaction_count=150,

        high_value_transactions=50,

        international_transactions=60,

        std_amount=18000

    )

    aml = AMLRulesEngine.evaluate(tx)

    trx = TransactionRules.analyze(tx)

    risk = RiskScoreEngine.evaluate(

        anomaly_score=0.95,

        rules_score=aml["rules_score"]

    )

    assert aml["rules_count"] > 0

    assert trx["risk_level"] in [

        "HIGH",

        "CRITICAL"

    ]

    assert risk["is_suspicious"] is True