from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime, Boolean, ForeignKey

engine = create_engine("sqlite:///notification/notification.db")

metadata_obj = MetaData()

UserTable = Table(
    "users",
    metadata_obj,
    Column("user_id", String(), primary_key=True),
    Column("user_name", String(128), nullable=False),
)

FileTable = Table(
    "file",
    metadata_obj,
    Column("file_id", String(), primary_key=True),
    Column("file_name", String(), nullable=False),
)

NotificationTable = Table(
    "notifications",
    metadata_obj,
    Column("timestamp", String(), primary_key=True),
    Column("user_id", String(), nullable=False),
    Column("owner_user_id", String(128), nullable=False),
    Column("file_id", String(), nullable=False),
    Column("status", Boolean(), nullable=False),
)


metadata_obj.create_all(engine)
