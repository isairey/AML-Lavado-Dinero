# ==========================================================
# AML Detection System
# Dockerfile
# ==========================================================

# Imagen base
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-jdk \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configuración de Java (requerido por Spark)
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Puerto de la API
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]