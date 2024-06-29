from sqlalchemy import create_engine, MetaData, Table, Column, String, ForeignKey, Enum, Float, Integer
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.exc import IntegrityError
import stripe
from loguru import logger

engine = create_engine("sqlite:///payment/payment.db")

metadata_obj = MetaData()

PaymentTable = Table(
    "payments",
    metadata_obj,
    Column("payment_id", String(), primary_key=True),
    Column("user_id", String(128), nullable=False),
    Column("status", Enum("pending", "completed", "failed"), nullable=False),
)

CostTable = Table(
    "cost",
    metadata_obj,
    Column("level", Integer, primary_key=True),
    Column("name", String(128), nullable=False, unique=True),
    Column("cost", Float(), nullable=False),
    Column("price_id", String(128), nullable=False),
)

metadata_obj.create_all(engine)


storage_plans = [[0, "basic", 10], [1, "silver", 50], [2, "gold", 100], [3, "unlimited", 200]]

def initialize_plans():

    # test key, doesn't need to be hidden
    stripe.api_key = "sk_test_51PATYu089JUuVWC5gd49xLoAkxyGGVYgPevTFjOYpRCaTodm7Fr12sfLvpQXHWzkxcxHvjB8fsRa0UAy7jsgJ9BV00AFn9GUfL"
    endpoint_secret = (
        "whsec_aebc8b1d7e5afc144f59f329d70ea2388058cdf6482cec9a9c69db9dcffc98ac"
    )

    _connection = engine.connect()

    for plan in storage_plans:
        product_name = plan[1]
        try:
            storage_product = stripe.Product.create(name=product_name)
        except stripe.error.InvalidRequestError as e:
            logger.error(e)

        price = stripe.Price.create(
            unit_amount=100 * plan[2],
            currency="usd",
            product=storage_product,
        )

        stmt = (
            insert(CostTable).values(tuple(plan + [price.id]))
        )
        try:
            _connection.execute(stmt)
            _connection.commit()
        except IntegrityError:
            _connection.rollback()

    _connection.close()

initialize_plans()