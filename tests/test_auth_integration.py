import json
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_solve_without_auth():
    """Test that solve endpoint works without authentication (for backward compatibility)"""
    response = client.post("/solve", json={
        "bot": "scouty",
        "task": "test task"
    })
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "scouty completed: test task" in data["result"]

def test_solve_with_user_context():
    """Test that solve endpoint accepts user context"""
    response = client.post("/solve", 
        json={
            "bot": "scouty",
            "task": "test task with user",
            "user": {
                "uid": "test-uid",
                "email": "test@example.com",
                "displayName": "Test User"
            }
        },
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "user_context" in data
    assert data["user_context"]["user_id"] == "test-uid"
    assert data["user_context"]["user_email"] == "test@example.com"
    assert data["user_context"]["user_name"] == "Test User"

def test_solve_missing_bot():
    """Test error handling for missing bot parameter"""
    response = client.post("/solve", json={
        "task": "test task"
    })
    assert response.status_code == 400
    assert "bot and task are required" in response.json()["detail"]

def test_solve_missing_task():
    """Test error handling for missing task parameter"""
    response = client.post("/solve", json={
        "bot": "scouty"
    })
    assert response.status_code == 400
    assert "bot and task are required" in response.json()["detail"]

def test_solve_invalid_bot():
    """Test error handling for invalid bot name"""
    response = client.post("/solve", json={
        "bot": "nonexistent",
        "task": "test task"
    })
    assert response.status_code == 404
    assert "bot not found" in response.json()["detail"]

def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "available_bots" in data
    assert isinstance(data["available_bots"], list)
    assert "scouty" in data["available_bots"]