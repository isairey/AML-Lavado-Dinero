"""
===========================================================
 AML Detection System
 Modelos de Base de Datos
===========================================================

Autor: Isai Reyes Peña

Descripción:
Modelos ORM utilizando SQLAlchemy.
===========================================================
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.connection import Base

from datetime import datetime


# ==========================================================
# CLIENTES
# ==========================================================

class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(100), nullable=False)

    last_name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True)

    phone = Column(String(20))

    country = Column(String(100))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    accounts = relationship(
        "Account",
        back_populates="customer"
    )


# ==========================================================
# CUENTAS
# ==========================================================

class Account(Base):

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)

    account_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    balance = Column(
        Float,
        default=0
    )

    account_type = Column(
        String(50)
    )

    status = Column(
        String(30),
        default="ACTIVE"
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    customer = relationship(
        "Customer",
        back_populates="accounts"
    )

    outgoing_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.account_id",
        back_populates="source_account"
    )

    incoming_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.target_account_id",
        back_populates="destination_account"
    )


# ==========================================================
# TRANSACCIONES
# ==========================================================

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    account_id = Column(
        Integer,
        ForeignKey("accounts.id")
    )

    target_account_id = Column(
        Integer,
        ForeignKey("accounts.id")
    )

    amount = Column(Float)

    transaction_type = Column(String(50))

    country_origin = Column(String(100))

    country_dest = Column(String(100))

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    risk_score = Column(
        Float,
        default=0.0
    )

    risk_level = Column(
        String(20),
        default="LOW"
    )

    suspicious = Column(
        Boolean,
        default=False
    )

    source_account = relationship(
        "Account",
        foreign_keys=[account_id],
        back_populates="outgoing_transactions"
    )

    destination_account = relationship(
        "Account",
        foreign_keys=[target_account_id],
        back_populates="incoming_transactions"
    )

    alerts = relationship(
        "Alert",
        back_populates="transaction"
    )


# ==========================================================
# ALERTAS AML
# ==========================================================

class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(
        Integer,
        ForeignKey("transactions.id")
    )

    level = Column(String(30))

    description = Column(String(255))

    resolved = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    transaction = relationship(
        "Transaction",
        back_populates="alerts"
    )