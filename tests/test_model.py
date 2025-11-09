import pytest
import pandas as pd
import joblib
from pathlib import Path
import json


def test_model_exists():
    """Test that model file exists"""
    model_path = Path("models/iris.joblib")
    if not model_path.exists():
        pytest.skip("Model file not found. Run train.py first or use DVC pull.")


def test_model_loads():
    """Test that model can be loaded"""
    model_path = Path("models/iris.joblib")
    if not model_path.exists():
        pytest.skip("Model file not found")
    
    try:
        with open(model_path, "rb") as f:
            model = joblib.load(f)
        assert model is not None
    except Exception as e:
        pytest.fail(f"Failed to load model: {e}")


def test_model_predict():
    """Test that model can make predictions"""
    model_path = Path("models/iris.joblib")
    if not model_path.exists():
        pytest.skip("Model file not found")
    
    with open(model_path, "rb") as f:
        model = joblib.load(f)
    
    # Test data (should be Setosa based on typical values)
    test_data = pd.DataFrame({
        "sepal_length": [5.1],
        "sepal_width": [3.5],
        "petal_length": [1.4],
        "petal_width": [0.2]
    })
    
    prediction = model.predict(test_data)
    assert len(prediction) == 1
    assert prediction[0] in ["setosa", "versicolor", "virginica", "Setosa", "Versicolor", "Virginica"]


def test_model_predict_multiple():
    """Test that model can make predictions on multiple samples"""
    model_path = Path("models/iris.joblib")
    if not model_path.exists():
        pytest.skip("Model file not found")
    
    with open(model_path, "rb") as f:
        model = joblib.load(f)
    
    # Test data with multiple samples
    test_data = pd.DataFrame({
        "sepal_length": [5.1, 6.2, 7.3],
        "sepal_width": [3.5, 3.4, 3.2],
        "petal_length": [1.4, 4.5, 6.3],
        "petal_width": [0.2, 1.5, 2.3]
    })
    
    predictions = model.predict(test_data)
    assert len(predictions) == 3
    for pred in predictions:
        assert pred in ["setosa", "versicolor", "virginica", "Setosa", "Versicolor", "Virginica"]


def test_metrics_file_exists():
    """Test that metrics file exists"""
    metrics_path = Path("metrics.json")
    if not metrics_path.exists():
        pytest.skip("Metrics file not found. Run train.py first.")


def test_metrics_file_valid():
    """Test that metrics file is valid JSON"""
    metrics_path = Path("metrics.json")
    if not metrics_path.exists():
        pytest.skip("Metrics file not found")
    
    try:
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
        assert isinstance(metrics, dict)
        if "accuracy" in metrics:
            assert 0 <= metrics["accuracy"] <= 1
    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON in metrics file: {e}")

