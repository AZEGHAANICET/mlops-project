import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import json

# Data Loading
df  = pd.read_csv("data/iris.csv")

# Prepare data
X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
y = df["species"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression(solver="lbfgs", max_iter=200)
model.fit(X_train, y_train)


# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")

# Save the model and metrics
os.makedirs("models", exist_ok=True)
with open("models/iris.pkl", "wb") as f:
    pickle.dump(model, f)

with open('metrics.json', 'w') as f:
    json.dump({'accuracy': accuracy}, f)