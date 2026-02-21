import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def client():
    # Provide a test client for the FastAPI app
    with TestClient(app) as client:
        yield client
