import os
os.environ["DATABASE_URL"] = "sqlite:///./test_bookpilot_v1.db"
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine
import pytest

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine); yield; Base.metadata.drop_all(engine)

@pytest.fixture
def client(): return TestClient(app)

@pytest.fixture
def auth(client):
    return client.post("/api/auth/register", json={"email":"owner@example.com", "password":"password123", "display_name":"Owner"}).json()["token"]
