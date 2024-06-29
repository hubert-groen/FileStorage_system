import uuid
from certifi import where
from sqlalchemy import create_engine, insert, select, update, Row
from sqlalchemy.exc import IntegrityError
from payment.models import PaymentModel
from payment.database_definition import PaymentTable, CostTable
from payment.exceptions import PaymentDataBaseError


class PaymentRepository:
    ENGINE = create_engine("sqlite:///payment/payment.db")

    def __init__(self) -> None:
        self._connection = self.ENGINE.connect()

    def insert_payment(self, payment: PaymentModel) -> str:
        stmt = (
            insert(PaymentTable).values(payment.model_dump())
        )
        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            self._connection.rollback()
            raise PaymentDataBaseError() from None
        finally:
            self._connection.close()
        return payment.payment_id
    
    def get_payments(self, user_id: str, status: str | None = None) -> list[Row]:
        filters = [PaymentTable.c.user_id == user_id]
        if status:
            filters.append(PaymentTable.c.status == status)
        statement = select(PaymentTable).where(*filters)
        payments = self._connection.execute(statement).fetchall()
        return payments

    def update_payment_status(self, payment_id: str, new_status: str) -> str:
        statement = (
            update(PaymentTable)
            .where(PaymentTable.c.payment_id == payment_id)
            .values(status=new_status)
        )
        try:
            self._connection.execute(statement)
            self._connection.commit()
        except IntegrityError:
            self._connection.rollback()
            raise PaymentDataBaseError() from None
        self._connection.close()
        return payment_id
    
    def get_stripe_product(self, plan_name) -> str:
        stmt = (
            select(CostTable.c.price_id).where(CostTable.c.name == plan_name)
        )
        result = self._connection.execute(stmt).fetchone()
        return result.price_id