from sqlalchemy import MetaData, Table, Column, String, ForeignKey, Float, Enum, Integer
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.exc import IntegrityError


engine = create_engine("sqlite:///storage/storage.db")

metadata_obj = MetaData()

UserTable = Table(
    "users",
    metadata_obj,
    Column("user_id", String(), primary_key=True),
    Column("user_name", String(128), nullable=False),
    Column("user_plan", Integer, ForeignKey("plans.level"), nullable=False)
)

FileTable = Table(
    "files",
    metadata_obj,
    Column("file_id", String(), primary_key=True),
    Column("user_id", String(), ForeignKey("users.user_id"), nullable=False),
    Column("file_name", String(), nullable=False),
    Column("file_size", Float(), nullable=False)
)

PlanTable = Table(
    "plans",
    metadata_obj,
    Column("level", Integer, primary_key=True),
    Column("name", String(128), nullable=False, unique=True),
    Column("limit", Float(), nullable=False)
)

FileAccess = Table(
    "file_access",
    metadata_obj,
    Column("file_access_id", String(), primary_key=True),
    Column("user_id", String(), ForeignKey("users.user_id"), nullable=False),
    Column("owner_user_id", String(), ForeignKey("users.user_id"), nullable=False),
    Column("file_id", String(), ForeignKey("files.file_id"), nullable=False)
)


metadata_obj.create_all(engine)


storage_plans = [[0, "basic", 10], [1, "silver", 50], [2, "gold", 100], [3, "unlimited", float('inf')]]


def initialize_plans():

    _connection = engine.connect()

    for plan in storage_plans:
        stmt = (
            insert(PlanTable).values(tuple(plan))
        )
        try:
            _connection.execute(stmt)
            _connection.commit()
        except IntegrityError:
            _connection.rollback()

    _connection.close()


initialize_plans()