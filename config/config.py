"""
===========================================================
 AML Detection System
 Configuración General del Proyecto
===========================================================

Autor: Isai Reyes Peña
Descripción:
Archivo central de configuración del sistema de detección
de lavado de dinero (AML).

Aquí se definen:
- Rutas del proyecto
- Configuración de Spark
- Parámetros del modelo
- Reglas AML
- Configuración de la API
===========================================================
"""

from pathlib import Path

# ==========================================================
# INFORMACIÓN DEL PROYECTO
# ==========================================================

PROJECT_NAME = "AML Detection System"
VERSION = "1.0.0"
AUTHOR = "Isai Reyes Peña"

# ==========================================================
# RUTAS DEL PROYECTO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODEL_DIR = DATA_DIR / "models"

LOG_DIR = BASE_DIR / "logs"
DOCS_DIR = BASE_DIR / "docs"

# ==========================================================
# ARCHIVOS DE DATOS
# ==========================================================

TRANSACTIONS_FILE = RAW_DATA_DIR / "transactions.csv"
CUSTOMERS_FILE = RAW_DATA_DIR / "customers.csv"
ACCOUNTS_FILE = RAW_DATA_DIR / "accounts.csv"

FEATURES_FILE = PROCESSED_DATA_DIR / "features.parquet"

MODEL_FILE = MODEL_DIR / "isolation_forest.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"

# ==========================================================
# CONFIGURACIÓN DE SPARK
# ==========================================================

SPARK_APP_NAME = "AML Detection"

SPARK_MASTER = "local[*]"

SPARK_EXECUTOR_MEMORY = "2g"
SPARK_DRIVER_MEMORY = "2g"

SPARK_CONFIG = {
    "spark.executor.memory": SPARK_EXECUTOR_MEMORY,
    "spark.driver.memory": SPARK_DRIVER_MEMORY,
    "spark.sql.shuffle.partitions": "8",
    "spark.default.parallelism": "8",
    "spark.sql.execution.arrow.pyspark.enabled": "true",
}

# ==========================================================
# MACHINE LEARNING
# ==========================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20

N_ESTIMATORS = 200

CONTAMINATION = 0.02

MAX_SAMPLES = "auto"

# ==========================================================
# REGLAS AML
# ==========================================================

HIGH_VALUE_TRANSACTION = 10000
VERY_HIGH_TRANSACTION = 50000

MAX_DAILY_TRANSACTIONS = 25

MAX_DAILY_AMOUNT = 75000

MAX_TRANSFER_PER_HOUR = 8

HIGH_RISK_COUNTRIES = [
    "North Korea",
    "Iran",
    "Syria",
    "Afghanistan",
]

# ==========================================================
# RISK SCORE
# ==========================================================

WEIGHT_AMOUNT = 0.35
WEIGHT_COUNTRY = 0.25
WEIGHT_FREQUENCY = 0.20
WEIGHT_ANOMALY = 0.20

RISK_THRESHOLD = 0.70

# ==========================================================
# API
# ==========================================================

API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG = True

# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL = "INFO"

LOG_FILE = LOG_DIR / "aml.log"

# ==========================================================
# DASHBOARD
# ==========================================================

DASHBOARD_TITLE = "AML Detection Dashboard"

REFRESH_INTERVAL = 5

# ==========================================================
# COLORES
# ==========================================================

RISK_COLORS = {
    "LOW": "#2ECC71",
    "MEDIUM": "#F1C40F",
    "HIGH": "#E67E22",
    "CRITICAL": "#E74C3C",
}

# ==========================================================
# CREAR DIRECTORIOS SI NO EXISTEN
# ==========================================================

directories = [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODEL_DIR,
    LOG_DIR,
    DOCS_DIR,
]

for directory in directories:
    directory.mkdir(parents=True, exist_ok=True)

# ==========================================================
# FUNCIÓN PARA MOSTRAR LA CONFIGURACIÓN
# ==========================================================

def show_config():
    """Imprime la configuración principal del sistema."""

    print("=" * 55)
    print(f"{PROJECT_NAME} v{VERSION}")
    print("=" * 55)
    print(f"Proyecto : {BASE_DIR}")
    print(f"Datos     : {DATA_DIR}")
    print(f"Modelos   : {MODEL_DIR}")
    print(f"Logs      : {LOG_DIR}")
    print(f"Spark App : {SPARK_APP_NAME}")
    print(f"Spark     : {SPARK_MASTER}")
    print("=" * 55)


if __name__ == "__main__":
    show_config()