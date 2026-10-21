"""
Test setup: a fresh in-memory database for every test, and a fake AI.
"""

import os

# Must be set before the app is imported.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

import app.routes.analyze as analyze_route
from app.database import Base, engine
from app.main import app
from tests.sample import SAMPLE_TEXT, sample_reading


@pytest.fixture
def client(monkeypatch):
    Base.metadata.drop_all(engine)
    # No real file reading or AI in tests
    monkeypatch.setattr(analyze_route, "extract_text", lambda data, name: SAMPLE_TEXT)
    monkeypatch.setattr(
        analyze_route,
        "read_with_ai",
        lambda text, jd, role: sample_reading(title="Frontend Developer", required_skills=["React", "TypeScript"]),
    )
    with TestClient(app) as test_client:  # "with" runs startup → creates tables
        yield test_client


def sign_up(client, email="priya@example.com", password="secret123") -> dict:
    """Creates an account and returns the Authorization header."""
    response = client.post("/auth/register", json={"name": "Priya", "email": email, "password": password})
    return {"Authorization": f"Bearer {response.json()['token']}"}


def upload(client, headers=None) -> dict:
    files = {"resume": ("cv.pdf", b"fake pdf", "application/pdf")}
    response = client.post("/analyze", files=files, data={"job_description": "We need React"}, headers=headers or {})
    assert response.status_code == 200, response.text
    return response.json()
