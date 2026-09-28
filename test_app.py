import os
os.environ["DEMO_MODE"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./test_fitbuddy.db"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Create your plan" in response.text


def test_generate_plan():
    response = client.post("/api/generate-workout", json={
        "name": "Test User", "user_id": "test001", "age": 20,
        "weight": 65, "goal": "muscle gain", "intensity": "medium"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["plan_id"]
    assert "DAY 1" in data["workout_plan"]
    assert data["nutrition_tip"]


def test_feedback():
    response = client.post("/api/submit-feedback", json={
        "user_id": "test001", "feedback": "Include more rest days"
    })
    assert response.status_code == 200
    assert "workout_plan" in response.json()
