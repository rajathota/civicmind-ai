"""
Integration tests for the parking service API endpoints
"""

import pytest
from fastapi import status


class TestParkingServiceAPI:
    """Test suite for parking service API endpoints"""

    def test_root_endpoint(self, client):
        """Test the root endpoint returns service information"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["service"] == "civicmind-parking-service"
        assert "version" in data
        assert data["status"] == "operational"

    def test_health_check(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["service"] == "civicmind-parking-service"
        assert data["status"] == "healthy"

    def test_service_info(self, client):
        """Test the service info endpoint"""
        response = client.get("/info")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "service_name" in data
        assert "capabilities" in data

    def test_parking_analysis(self, client, sample_parking_request):
        """Test parking issue analysis endpoint"""
        response = client.post("/analyze", json=sample_parking_request)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "issue_id" in data
        assert "analysis" in data
        assert "recommendations" in data
        assert "resolution_steps" in data

    def test_invalid_parking_request(self, client):
        """Test analysis with invalid request data"""
        invalid_request = {"invalid": "data"}
        response = client.post("/analyze", json=invalid_request)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_metrics_endpoint(self, client):
        """Test the metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "service" in data
        assert "uptime_seconds" in data
        assert "version" in data

    def test_404_handling(self, client):
        """Test custom 404 error handling"""
        response = client.get("/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "error" in data
        assert "available_endpoints" in data
