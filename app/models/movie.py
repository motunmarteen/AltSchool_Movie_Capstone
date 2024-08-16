from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.schema import MetaData

metadata = MetaData()

movies = Table(
    "movies",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("user_id", Integer, ForeignKey("users.id")),
)