import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend/app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../backend/app'))

from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test basic health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "version" in response.json()
    assert response.json()["version"] == "4.0.1"

def test_liveness_probe():
    """Test Kubernetes liveness probe"""
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"
    assert "timestamp" in response.json()

def test_readiness_probe():
    """Test Kubernetes readiness probe"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "checks" in response.json()
    assert "resources" in response.json()["checks"]
    assert "dependencies" in response.json()["checks"]

def test_detailed_health():
    """Test detailed health check"""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    assert "overall_status" in response.json()
    assert "system_resources" in response.json()
    assert "dependencies" in response.json()
    assert response.json()["version"] == "4.0.1"

def test_metrics_endpoint():
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "requests_total" in response.json()
    assert "errors_total" in response.json()
    assert "avg_response_time_ms" in response.json()

def test_root_endpoint():
    """Test root endpoint returns v4.0.1 info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "4.0.1"
    assert data["release_type"] == "stability"
    assert "improvements_v4_0_1" in data
