"""
Training script for Iris Classification Model.

This script loads the Iris dataset, trains a Logistic Regression model,
evaluates its performance, and saves the model and metrics.
"""
import os
import json
import logging
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main training function"""
    logger.info("Starting model training...")
    
    # Data Loading
    data_path = Path("data/iris.csv")
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at {data_path}")
    
    logger.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} samples")
    
    # Prepare data
    X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    y = df["species"]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logger.info(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples")
    
    # Train the model
    logger.info("Training Logistic Regression model...")
    model = LogisticRegression(solver="lbfgs", max_iter=500, random_state=42)
    model.fit(X_train, y_train)
    logger.info("Model training completed")
    
    # Evaluate the model
    logger.info("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    logger.info(f"Model Accuracy: {accuracy:.4f}")
    logger.info("\nClassification Report:")
    logger.info(classification_report(y_test, y_pred))
    logger.info("\nConfusion Matrix:")
    logger.info(confusion_matrix(y_test, y_pred))
    
    # Save the model and metrics
    model_dir = Path("models")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = model_dir / "iris.joblib"
    logger.info(f"Saving model to {model_path}")
    with open(model_path, "wb") as f:
        joblib.dump(model, f)
    
    metrics_path = Path("metrics.json")
    metrics = {
        "accuracy": float(accuracy),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "model_type": "LogisticRegression",
        "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    }
    
    logger.info(f"Saving metrics to {metrics_path}")
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logger.info("Training pipeline completed successfully!")


if __name__ == "__main__":
    main()