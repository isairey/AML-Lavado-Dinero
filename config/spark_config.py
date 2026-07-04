"""
===========================================================
 AML Detection System
 Configuración de Apache Spark
===========================================================

Autor: Isai Reyes Peña

Descripción:
Este módulo crea y devuelve una sesión de Spark
configurada para el procesamiento de datos del
sistema de detección de lavado de dinero.
===========================================================
"""

from pyspark.sql import SparkSession

from config.config import (
    SPARK_APP_NAME,
    SPARK_MASTER,
    SPARK_CONFIG
)


def create_spark_session() -> SparkSession:
    """
    Crea una SparkSession con la configuración del proyecto.
    """

    builder = (
        SparkSession.builder
        .appName(SPARK_APP_NAME)
        .master(SPARK_MASTER)
    )

    # Agregar configuración personalizada
    for key, value in SPARK_CONFIG.items():
        builder = builder.config(key, value)

    spark = builder.getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    return spark


def stop_spark_session(spark: SparkSession):
    """
    Finaliza la sesión de Spark.
    """

    if spark:
        spark.stop()


def show_spark_info(spark: SparkSession):
    """
    Muestra información de la sesión de Spark.
    """

    print("=" * 60)
    print("Apache Spark")
    print("=" * 60)
    print(f"Aplicación : {spark.sparkContext.appName}")
    print(f"Master     : {spark.sparkContext.master}")
    print(f"Versión    : {spark.version}")
    print(f"Web UI     : {spark.sparkContext.uiWebUrl}")
    print("=" * 60)


if __name__ == "__main__":

    spark = create_spark_session()

    show_spark_info(spark)

    stop_spark_session(spark)