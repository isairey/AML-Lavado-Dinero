"""
===========================================================
 AML Detection System
 Repositorio de Base de Datos
===========================================================

Autor: Isai Reyes Peña

Descripción:
Capa de acceso a datos (Repository Pattern).
Encargada de todas las operaciones CRUD.
===========================================================
"""

from sqlalchemy.orm import Session

from database.models import Customer, Account, Transaction, Alert


# ==========================================================
# CLIENTES
# ==========================================================

class CustomerRepository:

    @staticmethod
    def create(db: Session, customer: Customer):

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def get_by_id(db: Session, customer_id: int):

        return db.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def get_all(db: Session):

        return db.query(Customer).all()


# ==========================================================
# CUENTAS
# ==========================================================

class AccountRepository:

    @staticmethod
    def create(db: Session, account: Account):

        db.add(account)
        db.commit()
        db.refresh(account)

        return account

    @staticmethod
    def get_by_account_number(db: Session, account_number: str):

        return db.query(Account).filter(
            Account.account_number == account_number
        ).first()

    @staticmethod
    def get_by_customer(db: Session, customer_id: int):

        return db.query(Account).filter(
            Account.customer_id == customer_id
        ).all()


# ==========================================================
# TRANSACCIONES
# ==========================================================

class TransactionRepository:

    @staticmethod
    def create(db: Session, transaction: Transaction):

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def get_by_id(db: Session, transaction_id: int):

        return db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()

    @staticmethod
    def get_all(db: Session):

        return db.query(Transaction).all()

    @staticmethod
    def get_suspicious(db: Session):

        return db.query(Transaction).filter(
            Transaction.suspicious == True
        ).all()


# ==========================================================
# ALERTAS AML
# ==========================================================

class AlertRepository:

    @staticmethod
    def create(db: Session, alert: Alert):

        db.add(alert)
        db.commit()
        db.refresh(alert)

        return alert

    @staticmethod
    def get_open_alerts(db: Session):

        return db.query(Alert).filter(
            Alert.resolved == False
        ).all()

    @staticmethod
    def resolve_alert(db: Session, alert_id: int):

        alert = db.query(Alert).filter(
            Alert.id == alert_id
        ).first()

        if alert:

            alert.resolved = True
            db.commit()

        return alert