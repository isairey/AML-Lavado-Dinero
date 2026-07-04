"""
===========================================================
 AML Detection System
 Limpieza de Datos
===========================================================

Autor: Isai Reyes Peña

Descripción:
Limpia las transacciones bancarias eliminando registros
inválidos, duplicados y valores nulos.
"""

from pyspark.sql.functions import (
    col,
    trim,
    upper,
    to_timestamp,
    when
)

from config.spark_config import create_spark_session
from config.config import (
    TRANSACTIONS_FILE,
    PROCESSED_DATA_DIR
)


def clean_transactions():

    spark = create_spark_session()

    print("Cargando transacciones...")

    df = spark.read.csv(
        str(TRANSACTIONS_FILE),
        header=True,
        inferSchema=True
    )

    print(f"Registros originales: {df.count()}")

    # ==========================================
    # Eliminar registros duplicados
    # ==========================================

    df = df.dropDuplicates()

    # ==========================================
    # Eliminar registros con datos críticos nulos
    # ==========================================

    df = df.dropna(
        subset=[
            "account_id",
            "target_account",
            "amount",
            "timestamp"
        ]
    )

    # ==========================================
    # Limpiar espacios en blanco
    # ==========================================

    df = (
        df
        .withColumn("account_id", trim(col("account_id")))
        .withColumn("target_account", trim(col("target_account")))
        .withColumn("country_origin", trim(col("country_origin")))
        .withColumn("country_dest", trim(col("country_dest")))
        .withColumn("transaction_type", trim(col("transaction_type")))
    )

    # ==========================================
    # Convertir países a mayúsculas
    # ==========================================

    df = (
        df
        .withColumn("country_origin", upper(col("country_origin")))
        .withColumn("country_dest", upper(col("country_dest")))
    )

    # ==========================================
    # Convertir fecha
    # ==========================================

    df = df.withColumn(
        "timestamp",
        to_timestamp(col("timestamp"))
    )

    # ==========================================
    # Eliminar montos negativos o iguales a cero
    # ==========================================

    df = df.filter(col("amount") > 0)

    # ==========================================
    # Eliminar montos extremadamente altos
    # (posibles errores de captura)
    # ==========================================

    df = df.filter(col("amount") < 100000000)

    # ==========================================
    # Rellenar valores faltantes
    # ==========================================

    df = df.fillna({

        "transaction_type": "UNKNOWN",

        "country_origin": "UNKNOWN",

        "country_dest": "UNKNOWN"

    })

    # ==========================================
    # Crear bandera internacional
    # ==========================================

    df = df.withColumn(

        "is_international",

        when(
            col("country_origin") != col("country_dest"),
            1
        ).otherwise(0)

    )

    # ==========================================
    # Guardar datos limpios
    # ==========================================

    output = PROCESSED_DATA_DIR / "transactions_clean.parquet"

    df.write.mode("overwrite").parquet(str(output))

    print("--------------------------------------------")
    print("Limpieza finalizada")
    print(f"Registros finales : {df.count()}")
    print(f"Archivo guardado  : {output}")
    print("--------------------------------------------")

    spark.stop()


if __name__ == "__main__":
    clean_transactions()