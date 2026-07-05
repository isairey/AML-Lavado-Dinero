"""
===========================================================
 AML Detection System
 Entrenamiento del Modelo
===========================================================

Autor: Isai Reyes Peña

Descripción:
Pipeline completo de entrenamiento del modelo de
detección de anomalías usando Isolation Forest.
===========================================================
"""

import pandas as pd

from config.config import FEATURES_FILE

from src.models.anomaly_detection import AnomalyDetector
from src.models.evaluate import ModelEvaluator

# ==========================================================
# CARGAR FEATURES
# ==========================================================

def load_features():

    print("Cargando dataset de features...")

    df = pd.read_parquet(FEATURES_FILE)

    print(f"Registros cargados: {len(df)}")

    return df


# ==========================================================
# PIPELINE DE ENTRENAMIENTO
# ==========================================================

def train_pipeline():

    print("\n======================================")
    print("INICIANDO PIPELINE DE ENTRENAMIENTO AML")
    print("======================================\n")

    # 1. Cargar datos
    df = load_features()

    # 2. Inicializar modelo
    detector = AnomalyDetector()

    # 3. Entrenar modelo
    print("\nEntrenando modelo...")
    detector.train(df)

    # 4. Predicción sobre los mismos datos (baseline)
    print("\nGenerando predicciones...")
    df_pred = detector.predict(df)

    # 5. Guardar modelo
    print("\nGuardando modelo...")
    detector.save_model()

    # 6. Evaluación
    print("\nEvaluando modelo...")

    evaluator = ModelEvaluator()

    evaluator.model_summary(df_pred)

    evaluator.high_risk_analysis(df_pred)

    # 7. Guardar dataset con predicciones (opcional)
    output_path = "data/processed/predictions.parquet"

    df_pred.to_parquet(output_path, index=False)

    print("\n======================================")
    print("ENTRENAMIENTO COMPLETADO")
    print(f"Predicciones guardadas en: {output_path}")
    print("======================================\n")


# ==========================================================
# EJECUCIÓN
# ==========================================================

if __name__ == "__main__":

    train_pipeline()