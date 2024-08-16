from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.schema import MetaData

metadata = MetaData()

ratings = Table(
    "ratings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("rating", Integer),
)
