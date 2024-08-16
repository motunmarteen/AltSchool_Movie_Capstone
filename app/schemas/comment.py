from pydantic import BaseModel
from typing import Optional

class CommentCreate(BaseModel):
    movie_id: int
    parent_id: Optional[int] = None
    text: str

class Comment(BaseModel):
    id: int
    movie_id: int
    user_id: int
    parent_id: Optional[int] = None
    text: str

    class Config:
        orm_mode = True
