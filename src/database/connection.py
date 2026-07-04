"""
===========================================================
 AML Detection System
 Conexión a la Base de Datos
===========================================================

Autor: Isai Reyes Peña

Descripción:
Módulo encargado de crear la conexión con PostgreSQL
utilizando SQLAlchemy.
===========================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "aml_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================================
# ENGINE
# ==========================================================

engine = create_engine(

    DATABASE_URL,

    echo=False,

    pool_size=10,

    max_overflow=20

)

# ==========================================================
# SESIÓN
# ==========================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

# ==========================================================
# BASE PARA LOS MODELOS
# ==========================================================

Base = declarative_base()

# ==========================================================
# DEPENDENCIA PARA FASTAPI
# ==========================================================


def get_db():
    """
    Obtiene una sesión de base de datos.
    """

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ==========================================================
# PRUEBA DE CONEXIÓN
# ==========================================================

if __name__ == "__main__":

    try:

        db = SessionLocal()

        print("=" * 50)
        print("Conexión exitosa a PostgreSQL")
        print("=" * 50)

        db.close()

    except Exception as e:

        print("=" * 50)
        print("Error de conexión")
        print("=" * 50)
        print(e)