from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    description: str

class Movie(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

    class Config:
        orm_mode = True
