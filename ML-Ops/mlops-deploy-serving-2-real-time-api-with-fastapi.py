from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn

# --- Data Schemas ---
# Pydantic models validate the input and output
class FeatureInput(BaseModel):
    """Features for a single prediction request."""
    feature_1: float
    feature_2: int
    feature_3: str
    
    class Config:
        schema_extra = {
            "example": {
                "feature_1": 10.5,
                "feature_2": 4,
                "feature_3": "category_A"
            }
        }

class PredictionOutput(BaseModel):
    """Prediction result."""
    prediction: int
    probability: float

# --- Model Loading ---
def load_model(model_path="model.joblib"):
    """Load the model at startup."""
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        # If model can't load, the app can't serve
        raise RuntimeError(f"Failed to load model: {e}")

# --- API Initialization ---
app = FastAPI(title="Real-time Prediction API")
model = load_model()

@app.on_event("startup")
async def startup_event():
    logging.info("API started and model is loaded.")

@app.post("/predict", response_model=PredictionOutput)
async def predict(data: FeatureInput):
    """
    Run a single prediction.
    Input data is validated by the FeatureInput model.
    """
    try:
        # 1. Convert Pydantic model to DataFrame for the scikit-learn pipeline
        input_df = pd.DataFrame([data.dict()])
        
        # 2. Get predictions
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1] # Prob for class 1
        
        # 3. Format and return
        return PredictionOutput(
            prediction=int(prediction),
            probability=float(probability)
        )
    except Exception as e:
        # Handle prediction-time errors
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "model_loaded": model is not None}

if __name__ == "__main__":
    # Run with: uvicorn realtime_api:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
