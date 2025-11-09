import pandas as pd
from fastapi import FastAPI
import joblib
from schemas import IrisInput

app = FastAPI(title="Iris Classifier API", version="1.0")

# Load model
with open("models/iris.joblib", "rb") as f:
    model = joblib.load(f)
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/predict")
def predict(data:IrisInput):
    df= pd.DataFrame([data.model_dump()])

    prediction = model.predict(df)

    return {"prediction": str(prediction[0])}