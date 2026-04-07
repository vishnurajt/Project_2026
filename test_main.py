from fastapi.testclient import TestClient
from main import app
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Use a separate test database
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the real database with test database
app.dependency_overrides[get_db] = override_get_db

# Create tables before tests, drop after
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    # Runs before each test — fresh tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Runs after each test — clean up
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
        "age": 24,
        "is_active": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password not in data"

def test_register_duplicate_user():
    client.post("/auth/register", json ={
        "username": "dupeuser",
        "email": "dupe@example.com",
        "password": "test123",
        "age": 25,
        "is_active": True
    })
    response = client.post("/auth/register", json ={
        "username": "dupeuser",
        "email": "dupe@example.com",
        "password": "test123",
        "age": 25,
        "is_active": True
    })
    assert response.status_code == 400


def test_login():
    client.post("/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "test123",
        "age": 25,
        "is_active": True
    })
    # Then login
    response = client.post("/auth/login", data={
        "username": "loginuser",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_me():
    # Register and login to get token
    client.post("/auth/register", json={
        "username": "meuser",
        "email": "me@example.com",
        "password": "test123",
        "age": 25,
        "is_active": True
    })
    login_response = client.post("/auth/login", data={
        "username": "meuser",
        "password": "test123"
    })
    token = login_response.json()["access_token"]

    # Hit protected endpoint with token
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "meuser"

def test_get_user_not_found():
    response = client.get("/users/99999")
    assert response.status_code == 404
