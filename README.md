# AltSchool of Backend Engineering (Python) Tinyuka 2023 Capstone Project

## Project Overview

The goal of this capstone project is to develop a movie listing API using FastAPI. The API will allow users to list movies, view listed movies, rate them, and add comments. The application will be secured using JWT (JSON Web Tokens), ensuring that only the user who listed a movie can edit it. The application should be hosted on a cloud platform.

## Requirements

- **Language & Framework**: Python using FastAPI
- **Authentication**: JWT for securing endpoints
- **Database**: SQLite
- **Testing**: Include unit tests for the API endpoints
- **Documentation**: API documentation using OpenAPI/Swagger
- **Logging**: Log important details of your application
- **Deployment**: Deploy your application on a cloud server of your choice

## Features

### User Authentication

- User registration
- User login
- JWT token generation

### Movie Listing

- View a movie added (public access)
- Add a movie (authenticated access)
- View all movies (public access)
- Edit a movie (only by the user who listed it)
- Delete a movie (only by the user who listed it)

### Movie Rating

- Rate a movie (authenticated access)
- Get ratings for a movie (public access)

### Comments

- Add a comment to a movie (authenticated access)
- View comments for a movie (public access)
- Add comment to a comment i.e., nested comments (authenticated access)

## Installation

### Local Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create the SQLite database and tables:**

    ```sh
    python create_tables.py
    ```

5. **Run the application:**

    ```sh
    uvicorn app.main:app --reload
    ```

### Docker Setup

1. **Build the Docker image:**

    ```sh
    docker build -t fastapi-sqlite .
    ```

2. **Run the Docker container:**

    ```sh
    docker run -d -p 80:80 fastapi-sqlite
    ```

## Usage

### Endpoints

- **Register a new user:**

    ```http
    POST /register
    ```

    **Request Body:**

    ```json
    {
        "username": "testuser",
        "password": "testpassword"
    }
    ```

    **Response:**

    ```json
    {
        "username": "testuser"
    }
    ```

- **Login a user:**

    ```http
    POST /token
    ```

    **Request Body:**

    ```json
    {
        "username": "testuser",
        "password": "testpassword"
    }
    ```

    **Response:**

    ```json
    {
        "access_token": "123456789"
    }
    ```

- **Create a movie (requires authentication):**

    ```http
    POST /movies
    ```

    **Request Body:**

    ```json
    {
        "title": "Test Movie",
        "description": "Test Description"
    }
    ```

    **Response:**

    ```json
    {
        "title": "Test Movie",
        "description": "Test Description"
    }
    ```

## Running Tests

1. **Install test dependencies:**

    ```sh
    pip install pytest pytest-asyncio httpx
    ```

2. **Run the tests:**

    ```sh
    pytest
    ```