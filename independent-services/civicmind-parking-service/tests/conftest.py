"""
Test configuration for the parking service
"""

import pytest
from fastapi.testclient import TestClient

from parking_service.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_parking_request():
    """Sample parking analysis request for testing"""
    return {
        "description": "Cars are illegally parked on the sidewalk blocking pedestrians",
        "location": "Main Street and 1st Avenue",
        "priority": "high",
        "user_type": "resident"
    }
