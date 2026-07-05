"""
===========================================================
 AML Detection System
 Main
===========================================================

Autor: Isai Reyes Peña

Descripción:
Punto de entrada principal del sistema AML.
Permite entrenar el modelo, realizar predicciones,
evaluar resultados e iniciar la API.
===========================================================
"""

import argparse
import uvicorn

from src.models.train import train_pipeline
from src.models.predict import AMLPredictor
from src.models.evaluate import ModelEvaluator

from src.preprocessing.load_data import load_transactions
from src.preprocessing.clean_data import clean_data

from src.utils.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# ENTRENAMIENTO
# ==========================================================

def train():

    logger.info("Iniciando entrenamiento del modelo...")

    train_pipeline()

    logger.info("Entrenamiento finalizado correctamente.")


# ==========================================================
# PREDICCIÓN
# ==========================================================

def predict():

    logger.info("Realizando predicción de ejemplo...")

    predictor = AMLPredictor()

    predictor.load()

    transaction = {

        "transaction_count": 12,

        "total_amount": 35000,

        "average_amount": 3000,

        "std_amount": 850,

        "high_value_transactions": 2,

        "international_transactions": 1

    }

    result = predictor.predict_single(transaction)

    print("\n========== RESULTADO ==========\n")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("\n===============================\n")


# ==========================================================
# EVALUACIÓN
# ==========================================================

def evaluate():

    logger.info("Evaluando modelo...")

    predictor = AMLPredictor()

    predictor.load()

    df = load_transactions()

    df = clean_data(df)

    result = predictor.predict_batch(df)

    evaluator = ModelEvaluator()

    evaluator.model_summary(result)

    evaluator.high_risk_analysis(result)


# ==========================================================
# API
# ==========================================================

def api():

    logger.info("Iniciando API...")

    uvicorn.run(

        "src.api.app:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )


# ==========================================================
# DASHBOARD
# ==========================================================

def dashboard():

    import subprocess

    logger.info("Iniciando Dashboard...")

    subprocess.run([

        "streamlit",

        "run",

        "src/dashboard/dashboard.py"

    ])


# ==========================================================
# ARGUMENTOS
# ==========================================================

def parse_arguments():

    parser = argparse.ArgumentParser(

        description="AML Detection System"

    )

    parser.add_argument(

        "--train",

        action="store_true",

        help="Entrenar modelo"

    )

    parser.add_argument(

        "--predict",

        action="store_true",

        help="Realizar predicción"

    )

    parser.add_argument(

        "--evaluate",

        action="store_true",

        help="Evaluar modelo"

    )

    parser.add_argument(

        "--api",

        action="store_true",

        help="Iniciar API"

    )

    parser.add_argument(

        "--dashboard",

        action="store_true",

        help="Iniciar Dashboard"

    )

    return parser.parse_args()


# ==========================================================
# MAIN
# ==========================================================

def main():

    args = parse_arguments()

    if args.train:

        train()

    elif args.predict:

        predict()

    elif args.evaluate:

        evaluate()

    elif args.api:

        api()

    elif args.dashboard:

        dashboard()

    else:

        print()

        print("=" * 60)

        print(" AML DETECTION SYSTEM ")

        print("=" * 60)

        print()

        print("Comandos disponibles:\n")

        print("python main.py --train")

        print("python main.py --predict")

        print("python main.py --evaluate")

        print("python main.py --api")

        print("python main.py --dashboard")

        print()


# ==========================================================
# EJECUCIÓN
# ==========================================================

if __name__ == "__main__":

    main()