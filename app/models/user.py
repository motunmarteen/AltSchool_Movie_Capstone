from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.schema import MetaData

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String),
)