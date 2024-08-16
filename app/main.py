import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app.database import database, metadata, engine
from app.models import users, movies, ratings, comments
from app.schemas.user import User, UserCreate, Token, TokenData
from app.schemas.movie import Movie, MovieCreate
from app.schemas.rating import Rating, RatingCreate
from app.schemas.comment import Comment, CommentCreate
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from app.dependencies import get_current_user, get_user
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    await database.connect()
    logger.info("Database connected")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("Database disconnected")


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "You are welcome to my AltSchool Capstone Project - A Movie Listing API"}

# User Authentication/Logger

@app.post("/register", response_model=User)
async def register(user: UserCreate):
    try:
        # Check if the username already exists
        query = users.select().where(users.c.username == user.username)
        existing_user = await database.fetch_one(query)
        if existing_user:
            logger.warning(f"Registration failed: Username {user.username} already exists")
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = get_password_hash(user.password)
        query = users.insert().values(username=user.username, password=hashed_password)
        last_record_id = await database.execute(query)
        logger.info(f"User registered with ID: {last_record_id}")
        return {**user.dict(), "id": last_record_id}
    except HTTPException as e:
        raise e  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user:
        logger.warning(f"Login failed for username: {form_data.username} - Incorrect username")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password):
        logger.warning(f"Login failed for username: {form_data.username} - Incorrect password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"Token created for user: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/movies", response_model=Movie)
async def create_movie(movie: MovieCreate, current_user: User = Depends(get_current_user)):
    query = movies.insert().values(title=movie.title, description=movie.description, user_id=current_user.id)
    last_record_id = await database.execute(query)
    logger.info(f"Movie created with ID: {last_record_id} by user: {current_user.username}")
    return {**movie.dict(), "id": last_record_id, "user_id": current_user.id}


@app.get("/movies", response_model=List[Movie])
async def read_movies(skip: int = 0, limit: int = 10):
    logger.info(f"Reading movies with skip={skip} and limit={limit}")
    query = movies.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/movies/{movie_id}", response_model=Movie)
async def read_movie(movie_id: int):
    logger.info(f"Reading movie with ID: {movie_id}")
    query = movies.select().where(movies.c.id == movie_id)
    return await database.fetch_one(query)


@app.put("/movies/{movie_id}", response_model=Movie)
async def update_movie(movie_id: int, movie: MovieCreate, current_user: User = Depends(get_current_user)):
    logger.info(f"Updating movie with ID: {movie_id}")
    query = movies.select().where(movies.c.id == movie_id)
    db_movie = await database.fetch_one(query)
    if db_movie is None or db_movie["user_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Movie not found or not authorized")
    update_query = movies.update().where(movies.c.id == movie_id).values(title=movie.title,
                                                                         description=movie.description)
    await database.execute(update_query)
    return {**db_movie, **movie.dict()}


@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int, current_user: User = Depends(get_current_user)):
    query = movies.select().where(movies.c.id == movie_id)
    db_movie = await database.fetch_one(query)
    if db_movie is None or db_movie["user_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Movie not found or not authorized")
    delete_query = movies.delete().where(movies.c.id == movie_id)
    await database.execute(delete_query)
    return {"message": "Movie deleted successfully"}


@app.post("/ratings", response_model=Rating)
async def create_rating(rating: RatingCreate, current_user: User = Depends(get_current_user)):
    query = ratings.insert().values(movie_id=rating.movie_id, user_id=current_user.id, rating=rating.rating)
    last_record_id = await database.execute(query)
    logger.info(f"Rating created with ID: {last_record_id} by user: {current_user.username}")
    return {**rating.dict(), "id": last_record_id, "user_id": current_user.id}


logger = logging.getLogger(__name__)

@app.get("/ratings/{movie_id}", response_model=List[Rating])
async def read_ratings(movie_id: int):
    logger.info(f"Reading ratings for movie with ID: {movie_id}")
    query = ratings.select().where(ratings.c.movie_id == movie_id)
    return await database.fetch_all(query)


@app.post("/comments", response_model=Comment)
async def create_comment(comment: CommentCreate, current_user: User = Depends(get_current_user)):
    query = comments.insert().values(movie_id=comment.movie_id, user_id=current_user.id, parent_id=comment.parent_id,
                                     text=comment.text)
    last_record_id = await database.execute(query)
    logger.info(f"Comment created with ID: {last_record_id} by user: {current_user.username}")
    return {**comment.dict(), "id": last_record_id, "user_id": current_user.id}


@app.get("/comments/{movie_id}", response_model=List[Comment])
async def read_comments(movie_id: int):
    logger.info(f"Reading comments for movie with ID: {movie_id}")
    query = comments.select().where(comments.c.movie_id == movie_id)
    return await database.fetch_all(query)
