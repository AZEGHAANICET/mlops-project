import pandas as pd
import json
import logging
from pathlib import Path
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import joblib
from schemas import IrisInput

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Iris Classifier API",
    version="1.0.0",
    description="A complete MLOps pipeline for Iris flower classification",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load model
MODEL_PATH = Path("models/iris.joblib")
METRICS_PATH = Path("metrics.json")

try:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    with open(MODEL_PATH, "rb") as f:
        model = joblib.load(f)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

# Load metrics
metrics = {}
if METRICS_PATH.exists():
    try:
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)
    except Exception as e:
        logger.warning(f"Could not load metrics: {e}")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error": exc.detail, "status_code": exc.status_code},
        status_code=exc.status_code
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=422,
            content={"error": "Validation error", "details": exc.errors()}
        )
    raise HTTPException(status_code=422, detail="Invalid input data")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Home page with prediction form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if model is None:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "message": "Model not loaded"}
        )
    return {"status": "healthy", "model_loaded": True}


@app.get("/metrics")
async def get_metrics():
    """Get model metrics"""
    return metrics


@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    sepal_length: float = Form(...),
    sepal_width: float = Form(...),
    petal_length: float = Form(...),
    petal_width: float = Form(...)
):
    """Predict iris species from form data"""
    if model is None:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": "Model not available. Please check server logs.",
                "status_code": 503
            },
            status_code=503
        )

    try:
        # Validate input
        data = IrisInput(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width
        )

        # Make prediction
        df = pd.DataFrame([data.model_dump()])
        prediction = model.predict(df)
        prediction_str = str(prediction[0])

        logger.info(f"Prediction made: {prediction_str} for input {data.model_dump()}")

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "prediction": prediction_str,
                "sepal_length": sepal_length,
                "sepal_width": sepal_width,
                "petal_length": petal_length,
                "petal_width": petal_width
            }
        )
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": f"Error making prediction: {str(e)}",
                "status_code": 500
            },
            status_code=500
        )


@app.post("/api/predict")
async def predict_api(data: IrisInput):
    """Predict iris species via API (JSON)"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")

    try:
        df = pd.DataFrame([data.model_dump()])
        prediction = model.predict(df)
        prediction_str = str(prediction[0])

        logger.info(f"API prediction made: {prediction_str} for input {data.model_dump()}")

        return {
            "prediction": prediction_str,
            "input": data.model_dump()
        }
    except Exception as e:
        logger.error(f"Error making API prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")