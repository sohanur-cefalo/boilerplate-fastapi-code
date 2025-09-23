{% if cookiecutter.include_testing == "pytest" and cookiecutter.include_user_model == "yes" -%}
"""
Test user endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_user(client: TestClient, db: Session):
    """Test user creation"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        {% if cookiecutter.include_authentication == "jwt" -%}
        "username": "testuser",
        "password": "testpassword",
        {% endif -%}
        "is_active": True
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    {% if cookiecutter.include_authentication == "jwt" -%}
    assert data["username"] == user_data["username"]
    {% endif -%}
    assert data["is_active"] == user_data["is_active"]
    assert "id" in data
    assert "created_at" in data


def test_get_users(client: TestClient, db: Session):
    """Test getting users list"""
    # Create a test user first
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        {% if cookiecutter.include_authentication == "jwt" -%}
        "username": "testuser",
        "password": "testpassword",
        {% endif -%}
    }
    client.post("/api/v1/users/", json=user_data)
    
    # Get users list
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_user_by_id(client: TestClient, db: Session):
    """Test getting user by ID"""
    # Create a test user first
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        {% if cookiecutter.include_authentication == "jwt" -%}
        "username": "testuser",
        "password": "testpassword",
        {% endif -%}
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    created_user = create_response.json()
    
    # Get user by ID
    response = client.get(f"/api/v1/users/{created_user['id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == created_user["id"]
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]


def test_get_nonexistent_user(client: TestClient):
    """Test getting non-existent user returns 404"""
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404


def test_create_user_duplicate_email(client: TestClient, db: Session):
    """Test creating user with duplicate email fails"""
    user_data = {
        "name": "Test User",
        "email": "duplicate@example.com",
        {% if cookiecutter.include_authentication == "jwt" -%}
        "username": "testuser1",
        "password": "testpassword",
        {% endif -%}
    }
    
    # Create first user
    response1 = client.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 201
    
    # Try to create second user with same email
    user_data2 = user_data.copy()
    {% if cookiecutter.include_authentication == "jwt" -%}
    user_data2["username"] = "testuser2"
    {% endif -%}
    response2 = client.post("/api/v1/users/", json=user_data2)
    assert response2.status_code == 400
    assert "email already exists" in response2.json()["detail"]


{% if cookiecutter.include_authentication == "jwt" -%}
def test_create_user_duplicate_username(client: TestClient, db: Session):
    """Test creating user with duplicate username fails"""
    user_data = {
        "name": "Test User",
        "email": "test1@example.com",
        "username": "duplicateuser",
        "password": "testpassword",
    }
    
    # Create first user
    response1 = client.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 201
    
    # Try to create second user with same username
    user_data2 = user_data.copy()
    user_data2["email"] = "test2@example.com"
    response2 = client.post("/api/v1/users/", json=user_data2)
    assert response2.status_code == 400
    assert "username already exists" in response2.json()["detail"]


def test_login(client: TestClient, db: Session):
    """Test user login"""
    # Create a test user first
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword",
    }
    client.post("/api/v1/users/", json=user_data)
    
    # Login
    login_data = {
        "username": "testuser",
        "password": "testpassword",
    }
    response = client.post("/api/v1/users/token", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword",
    }
    response = client.post("/api/v1/users/token", data=login_data)
    assert response.status_code == 401
{% endif -%}
{% endif -%}

