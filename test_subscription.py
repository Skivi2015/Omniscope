"""Tests for the subscription system."""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_owner_access():
    """Test that owner can login and has unlimited access."""
    # Login as owner
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "admin",
        "password": "omniscope_admin_2024"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Check subscription status
    response = requests.get(f"{BASE_URL}/subscription/status", 
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    status = response.json()
    assert status["status"] == "owner"
    assert status["access"] == True
    
    # Test bot access
    response = requests.post(f"{BASE_URL}/solve", 
                           headers={"Authorization": f"Bearer {token}"},
                           json={"bot": "scouty", "task": "test task"})
    assert response.status_code == 200
    print("✓ Owner access test passed")

def test_user_registration_and_subscription():
    """Test user registration creates subscription."""
    # Use timestamp to ensure unique username
    username = f"testuser_{int(time.time())}"
    email = f"test_{int(time.time())}@example.com"
    
    # Register new user
    response = requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "email": email, 
        "password": "testpass123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Check subscription status
    response = requests.get(f"{BASE_URL}/subscription/status",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    status = response.json()
    assert status["status"] == "active"
    assert status["access"] == True
    assert status["monthly_fee"] == 29.99
    
    # Test bot access
    response = requests.post(f"{BASE_URL}/solve",
                           headers={"Authorization": f"Bearer {token}"},
                           json={"bot": "seomi", "task": "create SEO content"})
    assert response.status_code == 200
    print("✓ User registration and subscription test passed")

def test_unauthorized_access():
    """Test that unauthorized access is blocked."""
    # Try to access without token
    response = requests.post(f"{BASE_URL}/solve", 
                           json={"bot": "scouty", "task": "test"})
    assert response.status_code == 403  # FastAPI returns 403 for missing auth
    
    # Try with invalid token
    response = requests.post(f"{BASE_URL}/solve",
                           headers={"Authorization": "Bearer invalid_token"},
                           json={"bot": "scouty", "task": "test"})
    assert response.status_code == 401  # This should be 401 for invalid token
    print("✓ Unauthorized access test passed")

if __name__ == "__main__":
    print("Running subscription system tests...")
    test_owner_access()
    test_user_registration_and_subscription()
    test_unauthorized_access()
    print("All tests passed! 🎉")