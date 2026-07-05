"""
===========================================================
 AML Detection System
 Constants
===========================================================

Autor: Isai Reyes Peña

Descripción:
Constantes globales utilizadas en todo el sistema.
===========================================================
"""

from pathlib import Path

# ==========================================================
# RUTAS DEL PROYECTO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = BASE_DIR / "models"

LOGS_DIR = BASE_DIR / "logs"

REPORTS_DIR = BASE_DIR / "reports"

# ==========================================================
# ARCHIVOS
# ==========================================================

TRANSACTIONS_FILE = RAW_DATA_DIR / "transactions.csv"

FEATURES_FILE = PROCESSED_DATA_DIR / "features.parquet"

PREDICTIONS_FILE = PROCESSED_DATA_DIR / "predictions.parquet"

MODEL_FILE = MODELS_DIR / "isolation_forest.pkl"

SCALER_FILE = MODELS_DIR / "scaler.pkl"

# ==========================================================
# BASE DE DATOS
# ==========================================================

DEFAULT_DB_HOST = "localhost"

DEFAULT_DB_PORT = 5432

DEFAULT_DB_NAME = "aml_db"

DEFAULT_DB_USER = "postgres"

DEFAULT_DB_PASSWORD = "postgres"

# ==========================================================
# MACHINE LEARNING
# ==========================================================

RANDOM_STATE = 42

CONTAMINATION = 0.02

N_ESTIMATORS = 200

TEST_SIZE = 0.20

RISK_THRESHOLD = 0.70

# ==========================================================
# REGLAS AML
# ==========================================================

HIGH_VALUE_TRANSACTION = 10_000

VERY_HIGH_TRANSACTION = 50_000

LARGE_CASH_TRANSACTION = 20_000

MAX_DAILY_TRANSACTIONS = 30

MAX_HIGH_VALUE_TRANSACTIONS = 5

MAX_INTERNATIONAL_TRANSACTIONS = 10

# ==========================================================
# PAÍSES DE ALTO RIESGO
# ==========================================================

HIGH_RISK_COUNTRIES = [

    "Iran",

    "North Korea",

    "Syria",

    "Afghanistan",

    "Myanmar"

]

# ==========================================================
# TIPOS DE TRANSACCIÓN
# ==========================================================

TRANSACTION_TYPES = [

    "TRANSFER",

    "WIRE",

    "DEPOSIT",

    "WITHDRAWAL",

    "PAYMENT",

    "CRYPTO"

]

# ==========================================================
# NIVELES DE RIESGO
# ==========================================================

LOW = "LOW"

MEDIUM = "MEDIUM"

HIGH = "HIGH"

CRITICAL = "CRITICAL"

RISK_LEVELS = [

    LOW,

    MEDIUM,

    HIGH,

    CRITICAL

]

# ==========================================================
# API
# ==========================================================

API_TITLE = "AML Detection API"

API_VERSION = "1.0.0"

API_DESCRIPTION = (
    "API para detección de lavado de dinero utilizando "
    "Machine Learning y reglas AML."
)

API_PREFIX = "/api"

# ==========================================================
# DASHBOARD
# ==========================================================

DASHBOARD_TITLE = "AML Detection Dashboard"

DEFAULT_PAGE_SIZE = 25

# ==========================================================
# SPARK
# ==========================================================

SPARK_APP_NAME = "AML Detection"

SPARK_MASTER = "local[*]"

SPARK_DRIVER_MEMORY = "2g"

SPARK_EXECUTOR_MEMORY = "2g"

# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL = "INFO"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# ==========================================================
# COLUMNAS DEL DATASET
# ==========================================================

FEATURE_COLUMNS = [

    "transaction_count",

    "total_amount",

    "average_amount",

    "std_amount",

    "high_value_transactions",

    "international_transactions"

]

# ==========================================================
# RESPUESTAS API
# ==========================================================

SUCCESS_MESSAGE = "Operación realizada correctamente."

ERROR_MESSAGE = "Ha ocurrido un error."

MODEL_NOT_FOUND = "Modelo no encontrado."

INVALID_TRANSACTION = "Transacción inválida."

# ==========================================================
# CÓDIGOS HTTP
# ==========================================================

HTTP_OK = 200

HTTP_CREATED = 201

HTTP_BAD_REQUEST = 400

HTTP_NOT_FOUND = 404

HTTP_INTERNAL_SERVER_ERROR = 500