# 🏦 AML Detection System

Sistema de detección de lavado de dinero (Anti-Money Laundering - AML) usando Python, Spark y Machine Learning.

---

## 📌 Descripción

Este sistema permite detectar transacciones sospechosas mediante:

- Procesamiento de datos con Apache Spark
- Generación de features financieras
- Modelo de Machine Learning (Isolation Forest)
- API REST con FastAPI
- Dashboard interactivo con Streamlit
- Persistencia con PostgreSQL

---

## 🧠 Arquitectura del sistema

```text
transactions.csv
        │
        ▼
Spark ETL (clean + feature engineering)
        │
        ▼
features.parquet
        │
        ▼
Isolation Forest Model
        │
        ├──────────────┬───────────────┐
        ▼              ▼               ▼
     FastAPI      Streamlit       Evaluación
```

---

## 🚀 Tecnologías

- Python 3.10+
- Apache Spark
- Scikit-learn
- FastAPI
- Streamlit
- Pandas / NumPy
- SQLAlchemy
- PostgreSQL
- Matplotlib

---

## 📂 Estructura del proyecto

```text
src/
│
├── api/
│   ├── app.py
│   ├── routes.py
│   ├── schemas.py
│   └── services.py
│
├── database/
│   ├── connection.py
│   ├── models.py
│   └── repository.py
│
├── models/
│   ├── anomaly_detection.py
│   ├── train.py
│   ├── predict.py
│   └── evaluate.py
│
├── preprocessing/
│   ├── load_data.py
│   ├── spark_jobs.py
│   └── clean_data.py
│
├── dashboard/
│   ├── dashboard.py
│   └── charts.py
│
config/
│   ├── config.py
│   ├── spark_config.py
│   └── settings.yaml
```

---

## ⚙️ Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/isairey/AML-Lavado-Dinero.git
cd AML-Lavado-Dinero
```

---

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🧪 Ejecución del proyecto

### 🔹 1. Procesar datos con Spark

```bash
python src/preprocessing/spark_jobs.py
```

---

### 🔹 2. Entrenar modelo

```bash
python src/models/train.py
```

---

### 🔹 3. Ejecutar API

```bash
uvicorn src.api.app:app --reload
```

📍 Swagger:
```
http://127.0.0.1:8000/docs
```

---

### 🔹 4. Ejecutar Dashboard

```bash
streamlit run src/dashboard/dashboard.py
```

---

## 📡 Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/info | Información del sistema |
| GET | /api/status | Estado del modelo |
| GET | /api/model | Información del modelo |
| GET | /api/risk-levels | Rangos de riesgo |
| POST | /api/predict | Predicción AML |
| POST | /api/simulate | Simulación de transacción |

---

## 📊 Ejemplo de request

```json
{
  "account_id": "ACC1001",
  "target_account": "ACC5001",
  "amount": 25000,
  "country_origin": "Mexico",
  "country_dest": "Iran",
  "transaction_type": "Transfer"
}
```

---

## 📊 Respuesta

```json
{
  "risk_score": 0.92,
  "risk_level": "CRITICAL",
  "is_suspicious": true,
  "message": "Posible operación de lavado de dinero."
}
```

---

## 📈 Dashboard

Incluye:

- Distribución de montos
- Transacciones por país
- Tipos de transacciones
- Niveles de riesgo
- Top cuentas
- Cuentas sospechosas

---

## 🤖 Modelo ML

- Algoritmo: Isolation Forest
- Tipo: Detección de anomalías
- Features:
  - transaction_count
  - total_amount
  - average_amount
  - std_amount
  - high_value_transactions
  - international_transactions

---

## 🔐 Casos de uso

- Bancos
- Fintech
- Anti-fraude
- Cumplimiento AML/KYC
- Auditoría financiera

---

## 🚀 Futuras mejoras

- Kafka streaming en tiempo real
- Spark Streaming
- Autoencoders (Deep Learning)
- MLflow tracking
- SHAP explainability
- Grafos de relaciones entre cuentas

---

## 👨‍💻 Autor

Isai Reyes Peña

---

## 📄 Licencia

Proyecto educativo y demostrativo.
