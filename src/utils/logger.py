"""
===========================================================
 AML Detection System
 Logger Configuration
===========================================================

Autor: Isai Reyes Peña

Descripción:
Configuración centralizada del sistema de logging.
===========================================================
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

LOG_DIR = Path("logs")

LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "aml_system.log"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ==========================================================
# LOGGER
# ==========================================================

def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado.

    Parameters
    ----------
    name : str
        Nombre del módulo.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        fmt=LOG_FORMAT,

        datefmt=DATE_FORMAT

    )

    # ------------------------------------------------------
    # Consola
    # ------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(formatter)

    # ------------------------------------------------------
    # Archivo
    # ------------------------------------------------------

    file_handler = RotatingFileHandler(

        filename=LOG_FILE,

        maxBytes=5 * 1024 * 1024,

        backupCount=5,

        encoding="utf-8"

    )

    file_handler.setLevel(logging.INFO)

    file_handler.setFormatter(formatter)

    # ------------------------------------------------------
    # Agregar handlers
    # ------------------------------------------------------

    logger.addHandler(console_handler)

    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# ==========================================================
# CAMBIAR NIVEL
# ==========================================================

def set_level(level: str) -> None:
    """
    Cambia el nivel global del logger.
    """

    logging.getLogger().setLevel(level.upper())


# ==========================================================
# LOGGER POR DEFECTO
# ==========================================================

logger = get_logger("AML-System")


# ==========================================================
# EJEMPLO
# ==========================================================

if __name__ == "__main__":

    logger.debug("Mensaje DEBUG")

    logger.info("Sistema iniciado correctamente.")

    logger.warning("Advertencia de prueba.")

    logger.error("Error de prueba.")

    logger.critical("Error crítico.")