from pyspark.sql.functions import (
    col,
    count,
    avg,
    sum,
    max,
    min,
    stddev,
    when
)

from config.spark_config import create_spark_session
from config.config import (
    TRANSACTIONS_FILE,
    FEATURES_FILE,
    HIGH_VALUE_TRANSACTION,
)

spark = create_spark_session()

# ======================================================
# Cargar transacciones
# ======================================================

df = spark.read.csv(
    str(TRANSACTIONS_FILE),
    header=True,
    inferSchema=True
)

# ======================================================
# Crear variables auxiliares
# ======================================================

df = df.withColumn(
    "high_value",
    when(col("amount") >= HIGH_VALUE_TRANSACTION, 1).otherwise(0)
)

df = df.withColumn(
    "international",
    when(col("country_origin") != col("country_dest"), 1).otherwise(0)
)

# ======================================================
# Feature Engineering por cuenta
# ======================================================

features = (
    df.groupBy("account_id")
    .agg(
        count("*").alias("transaction_count"),
        avg("amount").alias("average_amount"),
        sum("amount").alias("total_amount"),
        max("amount").alias("max_amount"),
        min("amount").alias("min_amount"),
        stddev("amount").alias("std_amount"),
        sum("high_value").alias("high_value_transactions"),
        sum("international").alias("international_transactions")
    )
)

# Reemplazar valores nulos
features = features.fillna(0)

# ======================================================
# Guardar como Parquet
# ======================================================

features.write.mode("overwrite").parquet(str(FEATURES_FILE))

print("Archivo generado correctamente:")
print(FEATURES_FILE)

spark.stop()