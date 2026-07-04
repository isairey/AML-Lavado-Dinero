"""
===========================================================
 AML Detection System
 Dashboard - Gráficas
===========================================================

Autor: Isai Reyes Peña

Descripción:
Genera las gráficas utilizadas en el dashboard del
sistema de detección de lavado de dinero.
===========================================================
"""

import matplotlib.pyplot as plt
import pandas as pd


class Charts:

    @staticmethod
    def transactions_by_country(df: pd.DataFrame):
        """
        Gráfico de barras de transacciones por país.
        """

        data = (
            df.groupby("country_origin")
            .size()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(data.index, data.values)

        ax.set_title("Transacciones por País")
        ax.set_xlabel("País")
        ax.set_ylabel("Cantidad")

        plt.xticks(rotation=45)

        return fig

    @staticmethod
    def transaction_types(df: pd.DataFrame):
        """
        Gráfico circular de tipos de transacciones.
        """

        data = df["transaction_type"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 8))

        ax.pie(
            data.values,
            labels=data.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Tipos de Transacciones")

        return fig

    @staticmethod
    def amount_distribution(df: pd.DataFrame):
        """
        Histograma de montos.
        """

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.hist(df["amount"], bins=30)

        ax.set_title("Distribución de Montos")
        ax.set_xlabel("Monto")
        ax.set_ylabel("Frecuencia")

        return fig

    @staticmethod
    def risk_levels(df: pd.DataFrame):
        """
        Cantidad de cuentas por nivel de riesgo.
        """

        data = df["risk_level"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.bar(data.index, data.values)

        ax.set_title("Niveles de Riesgo")
        ax.set_xlabel("Nivel")
        ax.set_ylabel("Cantidad")

        return fig

    @staticmethod
    def top_accounts(df: pd.DataFrame):
        """
        Top 10 cuentas con mayor monto transferido.
        """

        data = (
            df.groupby("account_id")["amount"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(data.index.astype(str), data.values)

        ax.set_title("Top 10 Cuentas por Monto")
        ax.set_xlabel("Cuenta")
        ax.set_ylabel("Monto Total")

        plt.xticks(rotation=45)

        return fig

    @staticmethod
    def suspicious_accounts(df: pd.DataFrame):
        """
        Top cuentas con mayor Risk Score.
        """

        if "risk_score" not in df.columns:
            raise ValueError(
                "El DataFrame debe contener la columna 'risk_score'."
            )

        data = (
            df.sort_values("risk_score", ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(
            data["account_id"].astype(str),
            data["risk_score"]
        )

        ax.set_title("Top 10 Cuentas Sospechosas")
        ax.set_xlabel("Cuenta")
        ax.set_ylabel("Risk Score")

        plt.xticks(rotation=45)

        return fig