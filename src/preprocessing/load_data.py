"""
===========================================================
 AML Detection System
 Carga de Datos
===========================================================

Autor: Isai Reyes Peña

Descripción:
Módulo encargado de cargar los diferentes conjuntos
de datos utilizados por el sistema de detección
de lavado de dinero.
===========================================================
"""

from pyspark.sql import DataFrame

from config.spark_config import create_spark_session
from config.config import (
    TRANSACTIONS_FILE,
    CUSTOMERS_FILE,
    ACCOUNTS_FILE,
    FEATURES_FILE
)

# Crear una única sesión de Spark
spark = create_spark_session()


class DataLoader:
    """
    Clase encargada de cargar los datasets del proyecto.
    """

    @staticmethod
    def load_transactions() -> DataFrame:
        """Carga las transacciones bancarias."""

        print("Cargando transacciones...")

        return spark.read.csv(
            str(TRANSACTIONS_FILE),
            header=True,
            inferSchema=True
        )

    @staticmethod
    def load_customers() -> DataFrame:
        """Carga la información de los clientes."""

        print("Cargando clientes...")

        return spark.read.csv(
            str(CUSTOMERS_FILE),
            header=True,
            inferSchema=True
        )

    @staticmethod
    def load_accounts() -> DataFrame:
        """Carga las cuentas bancarias."""

        print("Cargando cuentas...")

        return spark.read.csv(
            str(ACCOUNTS_FILE),
            header=True,
            inferSchema=True
        )

    @staticmethod
    def load_features() -> DataFrame:
        """Carga el dataset de características."""

        print("Cargando features...")

        return spark.read.parquet(
            str(FEATURES_FILE)
        )

    @staticmethod
    def show_info(df: DataFrame, name: str):
        """
        Muestra información básica de un DataFrame.
        """

        print("\n" + "=" * 60)
        print(name)
        print("=" * 60)

        print(f"Registros : {df.count()}")
        print(f"Columnas  : {len(df.columns)}")

        df.printSchema()

        df.show(5, truncate=False)


if __name__ == "__main__":

    transactions = DataLoader.load_transactions()
    DataLoader.show_info(transactions, "TRANSACCIONES")

    customers = DataLoader.load_customers()
    DataLoader.show_info(customers, "CLIENTES")

    accounts = DataLoader.load_accounts()
    DataLoader.show_info(accounts, "CUENTAS")

    # Si ya existe features.parquet
    try:
        features = DataLoader.load_features()
        DataLoader.show_info(features, "FEATURES")
    except Exception:
        print("\n⚠️  features.parquet aún no ha sido generado.")

    spark.stop()