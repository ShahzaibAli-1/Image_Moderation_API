import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import generate_token
import os
from PIL import Image
import io

client = TestClient(app)

def create_test_image():
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_moderate_image():
    # Create a token
    token = generate_token()
    
    # Create test image
    image_data = create_test_image()
    
    # Test moderation
    response = client.post(
        "/moderate",
        files={"file": ("test.png", image_data, "image/png")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "safe" in data
    assert "categories" in data
    assert "confidence" in data

def test_moderate_invalid_file():
    # Create a token
    token = generate_token()
    
    # Test with invalid file
    response = client.post(
        "/moderate",
        files={"file": ("test.txt", b"not an image", "text/plain")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400

def test_moderate_large_file():
    # Create a token
    token = generate_token()
    
    # Create a large image (6MB)
    img = Image.new('RGB', (2000, 2000), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG', quality=100)
    img_byte_arr.seek(0)
    
    # Test moderation
    response = client.post(
        "/moderate",
        files={"file": ("large.png", img_byte_arr, "image/png")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400

def test_moderate_no_token():
    # Test without token
    image_data = create_test_image()
    response = client.post(
        "/moderate",
        files={"file": ("test.png", image_data, "image/png")}
    )
    assert response.status_code == 401

def test_moderate_invalid_token():
    # Test with invalid token
    image_data = create_test_image()
    response = client.post(
        "/moderate",
        files={"file": ("test.png", image_data, "image/png")},
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401 