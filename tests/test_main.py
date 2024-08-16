import pytest
from httpx import AsyncClient
from app.main import app
from app.database import database

@pytest.fixture(scope="module")
async def client():
    # Connect to the database
    await database.connect()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    # Disconnect from the database
    await database.disconnect()

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_register_existing_user(client):
    # Register the user first
    await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    # Try to register the same user again
    response = await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"

@pytest.mark.asyncio
async def test_login(client):
    # Register the user first
    await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    # Login with the registered user
    response = await client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_create_movie(client):
    # Register and login the user first
    await client.post("/register", json={"username": "testuser", "password": "testpassword"})
    login_response = await client.post("/token", data={"username": "testuser", "password": "testpassword"})
    token = login_response.json()["access_token"]

    # Create a movie
    response = await client.post(
        "/movies",
        json={"title": "Test Movie", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Movie"