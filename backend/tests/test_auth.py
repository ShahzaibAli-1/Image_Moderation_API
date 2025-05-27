import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import generate_token
from datetime import datetime

client = TestClient(app)

def test_create_token():
    # Create an admin token first
    admin_token = generate_token()
    response = client.post(
        "/auth/tokens",
        json={"is_admin": True},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["is_admin"] is True

def test_list_tokens():
    # Create an admin token
    admin_token = generate_token()
    response = client.get(
        "/auth/tokens",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_revoke_token():
    # Create an admin token
    admin_token = generate_token()
    # Create a token to revoke
    response = client.post(
        "/auth/tokens",
        json={"is_admin": False},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    token_to_revoke = response.json()["token"]
    
    # Revoke the token
    response = client.delete(
        f"/auth/tokens/{token_to_revoke}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Token revoked successfully"

def test_invalid_token():
    response = client.get(
        "/auth/tokens",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_non_admin_access():
    # Create a non-admin token
    non_admin_token = generate_token()
    response = client.get(
        "/auth/tokens",
        headers={"Authorization": f"Bearer {non_admin_token}"}
    )
    assert response.status_code == 403 