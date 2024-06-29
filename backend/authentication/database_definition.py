from sqlalchemy import MetaData, Table, Column, String, ForeignKey, Float, Enum, Integer
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError


engine = create_engine("sqlite:///authentication/authentication.db")

metadata_obj = MetaData()

UserTable = Table(
    "users",
    metadata_obj,
    Column("user_id", String(), primary_key=True),
    Column("user_name", String(128), nullable=False),
    Column("user_plan", Integer, nullable=False),
    Column("user_email", String(128), nullable=False)
)

metadata_obj.create_all(engine)