from pydantic import BaseModel

class RatingCreate(BaseModel):
    movie_id: int
    rating: int

class Rating(BaseModel):
    id: int
    movie_id: int
    user_id: int
    rating: int

    class Config:
        orm_mode = True
