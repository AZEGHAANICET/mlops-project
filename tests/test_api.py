import pytest
from fastapi.testclient import TestClient
from app import app
import pandas as pd
import joblib
from pathlib import Path

client = TestClient(app)


def test_root():
    """Test root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code in [200, 503]  # 200 if model loaded, 503 if not
    data = response.json()
    assert "status" in data


def test_metrics_endpoint():
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    # Should return metrics dict (can be empty if metrics.json doesn't exist)


def test_api_predict_valid():
    """Test API predict endpoint with valid data"""
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/api/predict", json=payload)
    
    if response.status_code == 503:
        pytest.skip("Model not loaded, skipping prediction test")
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "input" in data
    assert data["prediction"] in ["setosa", "versicolor", "virginica", "Setosa", "Versicolor", "Virginica"]


def test_api_predict_invalid_range():
    """Test API predict endpoint with invalid data (negative values)"""
    payload = {
        "sepal_length": -5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422  # Validation error


def test_api_predict_missing_field():
    """Test API predict endpoint with missing field"""
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4
        # Missing petal_width
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422  # Validation error


def test_api_predict_invalid_type():
    """Test API predict endpoint with invalid type"""
    payload = {
        "sepal_length": "invalid",
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422  # Validation error


def test_form_predict_valid():
    """Test form predict endpoint with valid data"""
    form_data = {
        "sepal_length": "5.1",
        "sepal_width": "3.5",
        "petal_length": "1.4",
        "petal_width": "0.2"
    }
    response = client.post("/predict", data=form_data)
    
    if response.status_code == 503:
        pytest.skip("Model not loaded, skipping prediction test")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_docs_endpoint():
    """Test Swagger docs endpoint"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    """Test ReDoc endpoint"""
    response = client.get("/redoc")
    assert response.status_code == 200

