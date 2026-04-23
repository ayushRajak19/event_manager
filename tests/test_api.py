"""
Unit and integration tests for the Event Management System.

Run tests with: pytest
Run specific test: pytest tests/test_auth.py::test_user_signup
Run with coverage: pytest --cov=app tests/
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.db.base import Base
from app.db import get_db
from app.models import User, Admin, Vendor
from app.core.security import hash_password

# Create test database
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create test tables
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestAuthentication:
    """Test authentication endpoints."""

    def test_admin_signup(self):
        """Test admin signup."""
        response = client.post(
            "/api/v1/auth/admin/signup",
            json={
                "name": "Test Admin",
                "email": "admin@test.com",
                "password": "TestPassword123"
            }
        )
        assert response.status_code == 200
        assert response.json()["role"] == "admin"
        assert response.json()["access_token"]

    def test_user_signup(self):
        """Test user signup."""
        response = client.post(
            "/api/v1/auth/user/signup",
            json={
                "name": "Test User",
                "email": "user@test.com",
                "password": "TestPassword123",
                "phone": "1234567890"
            }
        )
        assert response.status_code == 200
        assert response.json()["role"] == "user"

    def test_user_login(self):
        """Test user login."""
        # First create a user
        client.post(
            "/api/v1/auth/user/signup",
            json={
                "name": "Test User",
                "email": "login@test.com",
                "password": "TestPassword123"
            }
        )
        
        # Then login
        response = client.post(
            "/api/v1/auth/user/login",
            json={
                "email": "login@test.com",
                "password": "TestPassword123"
            }
        )
        assert response.status_code == 200
        assert response.json()["access_token"]

    def test_invalid_login(self):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/user/login",
            json={
                "email": "nonexistent@test.com",
                "password": "WrongPassword"
            }
        )
        assert response.status_code == 401


class TestProducts:
    """Test product endpoints."""

    def setup_method(self):
        """Setup test data before each test."""
        # Clear database
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)
        
        # Create admin for auth token
        admin_response = client.post(
            "/api/v1/auth/admin/signup",
            json={
                "name": "Test Admin",
                "email": "admin@test.com",
                "password": "TestPassword123"
            }
        )
        self.admin_token = admin_response.json()["access_token"]

    def test_get_products(self):
        """Test getting products list."""
        response = client.get(
            "/api/v1/products",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        assert response.status_code == 200
        assert "items" in response.json()

    def test_search_products(self):
        """Test searching products."""
        response = client.get(
            "/api/v1/products/search/?query=test",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        assert response.status_code == 200

    def test_get_categories(self):
        """Test getting categories."""
        response = client.get(
            "/api/v1/products/categories",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        assert response.status_code == 200


class TestHealthCheck:
    """Test health check endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
