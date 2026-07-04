"""
===========================================================
 AML Detection System
 API Principal
===========================================================

Autor: Isai Reyes Peña

Descripción:
Punto de entrada de la API REST utilizando FastAPI.
===========================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

app = FastAPI(
    title="AML Detection System API",
    description="API para detección de posibles operaciones de lavado de dinero.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Rutas
# =====================================================

app.include_router(router)

# =====================================================
# Endpoint raíz
# =====================================================

@app.get("/", tags=["Inicio"])
def home():
    return {
        "project": "AML Detection System",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }

# =====================================================
# Health Check
# =====================================================

@app.get("/health", tags=["Sistema"])
def health():
    return {
        "status": "OK",
        "service": "AML Detection API"
    }

# =====================================================
# Ejecutar aplicación
# =====================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )