"""
===========================================================
 AML Detection System
 Dashboard
===========================================================

Autor: Isai Reyes Peña

Dashboard para visualizar información sobre
transacciones bancarias y posibles casos
de lavado de dinero.
===========================================================
"""

import streamlit as st
import pandas as pd

from dashboard.charts import Charts

# ==========================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="AML Detection Dashboard",
    page_icon="🏦",
    layout="wide"
)

# ==========================================================
# CARGA DE DATOS
# ==========================================================

@st.cache_data
def load_data():

    try:
        return pd.read_parquet(
            "data/processed/features.parquet"
        )

    except:

        return pd.read_csv(
            "data/raw/transactions.csv"
        )


df = load_data()

# ==========================================================
# TÍTULO
# ==========================================================

st.title("🏦 AML Detection Dashboard")

st.markdown(
    """
Sistema de detección de posibles operaciones
de **Lavado de Dinero** utilizando Python,
Apache Spark y Machine Learning.
"""
)

st.divider()

# ==========================================================
# MÉTRICAS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Transacciones",
        len(df)
    )

with col2:

    if "amount" in df.columns:
        st.metric(
            "Monto Total",
            f"${df['amount'].sum():,.2f}"
        )

with col3:

    if "account_id" in df.columns:
        st.metric(
            "Cuentas",
            df["account_id"].nunique()
        )

with col4:

    if "risk_score" in df.columns:

        suspicious = len(
            df[df["risk_score"] >= 0.70]
        )

        st.metric(
            "Alertas AML",
            suspicious
        )

    else:

        st.metric(
            "Alertas AML",
            "N/D"
        )

st.divider()

# ==========================================================
# PRIMERA FILA
# ==========================================================

left, right = st.columns(2)

with left:

    if "country_origin" in df.columns:

        st.subheader("🌍 Transacciones por País")

        fig = Charts.transactions_by_country(df)

        st.pyplot(fig)

with right:

    if "transaction_type" in df.columns:

        st.subheader("💳 Tipos de Transacciones")

        fig = Charts.transaction_types(df)

        st.pyplot(fig)

# ==========================================================
# SEGUNDA FILA
# ==========================================================

left, right = st.columns(2)

with left:

    if "amount" in df.columns:

        st.subheader("💰 Distribución de Montos")

        fig = Charts.amount_distribution(df)

        st.pyplot(fig)

with right:

    if "risk_level" in df.columns:

        st.subheader("⚠️ Niveles de Riesgo")

        fig = Charts.risk_levels(df)

        st.pyplot(fig)

# ==========================================================
# TOP CUENTAS
# ==========================================================

if "account_id" in df.columns and "amount" in df.columns:

    st.divider()

    st.subheader("🏦 Top 10 Cuentas")

    fig = Charts.top_accounts(df)

    st.pyplot(fig)

# ==========================================================
# CUENTAS SOSPECHOSAS
# ==========================================================

if "risk_score" in df.columns:

    st.divider()

    st.subheader("🚨 Top 10 Cuentas Sospechosas")

    fig = Charts.suspicious_accounts(df)

    st.pyplot(fig)

# ==========================================================
# TABLA
# ==========================================================

st.divider()

st.subheader("📋 Datos")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "AML Detection System © 2026 | Python • Spark • Streamlit • Machine Learning"
)