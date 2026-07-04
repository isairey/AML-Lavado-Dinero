"""
===========================================================
 AML Detection System
 Spark Jobs
===========================================================

Autor: Isai Reyes Peña

Descripción:
Procesos ETL utilizando Apache Spark.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    count,
    sum,
    avg,
    stddev,
    max,
    min,
    when,
)

from config.spark_config import create_spark_session


class SparkJobs:

    def __init__(self):
        self.spark = create_spark_session()

    # =====================================================
    # Cargar CSV
    # =====================================================

    def load_csv(self, path: str) -> DataFrame:

        return self.spark.read.csv(
            path,
            header=True,
            inferSchema=True
        )

    # =====================================================
    # Guardar Parquet
    # =====================================================

    def save_parquet(self, df: DataFrame, output: str):

        df.write.mode("overwrite").parquet(output)

    # =====================================================
    # Limpiar transacciones
    # =====================================================

    def clean_transactions(self, df: DataFrame) -> DataFrame:

        df = (
            df
            .dropDuplicates()
            .dropna()
            .filter(col("amount") > 0)
        )

        return df

    # =====================================================
    # Crear variables (Features)
    # =====================================================

    def create_features(self, df: DataFrame) -> DataFrame:

        df = (
            df
            .withColumn(
                "high_value",
                when(col("amount") >= 10000, 1).otherwise(0)
            )
            .withColumn(
                "international",
                when(
                    col("country_origin") != col("country_dest"),
                    1
                ).otherwise(0)
            )
        )

        features = (

            df.groupBy("account_id")

            .agg(

                count("*").alias("transaction_count"),

                sum("amount").alias("total_amount"),

                avg("amount").alias("average_amount"),

                stddev("amount").alias("std_amount"),

                max("amount").alias("max_amount"),

                min("amount").alias("min_amount"),

                sum("high_value").alias("high_value_transactions"),

                sum("international").alias(
                    "international_transactions"
                )

            )

        )

        return features.fillna(0)

    # =====================================================
    # Estadísticas generales
    # =====================================================

    def statistics(self, df: DataFrame):

        print("=" * 60)

        print(f"Total registros : {df.count()}")

        print(f"Columnas         : {len(df.columns)}")

        df.describe().show()

    # =====================================================
    # Mostrar DataFrame
    # =====================================================

    def preview(self, df: DataFrame, rows: int = 10):

        df.show(rows, truncate=False)

    # =====================================================
    # Cerrar Spark
    # =====================================================

    def stop(self):

        self.spark.stop()


# ==========================================================
# Ejemplo de uso
# ==========================================================

if __name__ == "__main__":

    jobs = SparkJobs()

    df = jobs.load_csv("data/raw/transactions.csv")

    df = jobs.clean_transactions(df)

    features = jobs.create_features(df)

    jobs.statistics(features)

    jobs.preview(features)

    jobs.save_parquet(
        features,
        "data/processed/features.parquet"
    )

    jobs.stop()