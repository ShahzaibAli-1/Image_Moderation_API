import pytest
import os
import shutil
import time
import httpx

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up the test environment"""
    # Wait for services to be ready
    retries = 30
    api_url = "http://localhost:7000"
    while retries > 0:
        try:
            response = httpx.get(f"{api_url}/health")
            if response.status_code == 200:
                break
        except httpx.RequestError:
            pass
        time.sleep(1)
        retries -= 1
    
    if retries == 0:
        raise Exception("API did not start")
    
    yield
    
    # Cleanup after tests
    if os.path.exists("tests/test_files"):
        shutil.rmtree("tests/test_files") 