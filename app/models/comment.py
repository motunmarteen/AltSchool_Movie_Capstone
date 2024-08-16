from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.schema import MetaData

metadata = MetaData()

comments = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("parent_id", Integer, ForeignKey("comments.id"), nullable=True),
    Column("text", String),
)