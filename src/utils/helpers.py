"""
===========================================================
 AML Detection System
 Helpers
===========================================================

Autor: Isai Reyes Peña

Descripción:
Funciones auxiliares utilizadas en todo el sistema.
===========================================================
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd


# ==========================================================
# DIRECTORIOS
# ==========================================================

def ensure_directory(path: str | Path) -> Path:
    """
    Crea un directorio si no existe.
    """

    directory = Path(path)

    directory.mkdir(parents=True, exist_ok=True)

    return directory


# ==========================================================
# FECHA Y HORA
# ==========================================================

def current_timestamp() -> str:
    """
    Devuelve la fecha y hora actual.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==========================================================
# JSON
# ==========================================================

def save_json(data: Dict[str, Any], filepath: str | Path) -> None:
    """
    Guarda un diccionario como JSON.
    """

    filepath = Path(filepath)

    ensure_directory(filepath.parent)

    with open(filepath, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_json(filepath: str | Path) -> Dict[str, Any]:
    """
    Lee un archivo JSON.
    """

    with open(filepath, "r", encoding="utf-8") as file:

        return json.load(file)


# ==========================================================
# PARQUET
# ==========================================================

def save_parquet(df: pd.DataFrame, filepath: str | Path) -> None:
    """
    Guarda un DataFrame en formato Parquet.
    """

    filepath = Path(filepath)

    ensure_directory(filepath.parent)

    df.to_parquet(filepath, index=False)


def load_parquet(filepath: str | Path) -> pd.DataFrame:
    """
    Carga un DataFrame desde un archivo Parquet.
    """

    return pd.read_parquet(filepath)


# ==========================================================
# CSV
# ==========================================================

def load_csv(filepath: str | Path) -> pd.DataFrame:
    """
    Carga un archivo CSV.
    """

    return pd.read_csv(filepath)


def save_csv(df: pd.DataFrame, filepath: str | Path) -> None:
    """
    Guarda un DataFrame como CSV.
    """

    filepath = Path(filepath)

    ensure_directory(filepath.parent)

    df.to_csv(filepath, index=False)


# ==========================================================
# MODELOS
# ==========================================================

def save_model(model: Any, filepath: str | Path) -> None:
    """
    Guarda un modelo entrenado.
    """

    filepath = Path(filepath)

    ensure_directory(filepath.parent)

    joblib.dump(model, filepath)


def load_model(filepath: str | Path) -> Any:
    """
    Carga un modelo previamente entrenado.
    """

    return joblib.load(filepath)


# ==========================================================
# LOGGING
# ==========================================================

def get_logger(name: str) -> logging.Logger:
    """
    Configura un logger.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )

        handler = logging.StreamHandler()

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


# ==========================================================
# RISK LEVEL
# ==========================================================

def risk_level(score: float) -> str:
    """
    Convierte un score en nivel de riesgo.
    """

    if score < 0.30:

        return "LOW"

    elif score < 0.60:

        return "MEDIUM"

    elif score < 0.80:

        return "HIGH"

    return "CRITICAL"


# ==========================================================
# VALIDACIÓN
# ==========================================================

def clamp(value: float,
          minimum: float = 0.0,
          maximum: float = 1.0) -> float:
    """
    Limita un valor dentro de un rango.
    """

    return max(minimum, min(value, maximum))


# ==========================================================
# DATAFRAME
# ==========================================================

def dataframe_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Devuelve un resumen del DataFrame.
    """

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "memory_mb": round(

            df.memory_usage(deep=True).sum()
            / (1024 ** 2),

            2

        ),

        "missing_values": int(

            df.isna().sum().sum()

        )

    }


# ==========================================================
# RESPUESTA API
# ==========================================================

def api_response(
    success: bool,
    message: str,
    data: Any = None
) -> Dict[str, Any]:
    """
    Construye una respuesta estándar para la API.
    """

    return {

        "success": success,

        "message": message,

        "timestamp": current_timestamp(),

        "data": data

    }


# ==========================================================
# FORMATO MONEDA
# ==========================================================

def currency(amount: float) -> str:
    """
    Formatea un monto.
    """

    return f"${amount:,.2f}"


# ==========================================================
# PORCENTAJE
# ==========================================================

def percentage(value: float) -> str:
    """
    Formatea un porcentaje.
    """

    return f"{value:.2f}%"