from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
import uvicorn
import logging

# --- Data Schemas (Pydantic) ---
class UserData(BaseModel):
    user_id: str
    username: str
    account_status: str
    lifetime_value: float = Field(..., gt=0)

# --- Mock Database ---
MOCK_USER_DB = {
    "u-123": UserData(user_id="u-123", username="alice", account_status="active", lifetime_value=150.75),
    "u-456": UserData(user_id="u-456", username="bob", account_status="pending", lifetime_value=10.00),
}
# --- API Key Security ---
API_KEY = "super-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(key: str = Security(api_key_header)):
    """Validates the API key."""
    if key == API_KEY:
        return key
    else:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")

# --- FastAPI App ---
app = FastAPI(title="Real-time Data Serving API")
logging.basicConfig(level=logging.INFO)

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.get("/users/{user_id}", response_model=UserData)
async def get_user_data(user_id: str, api_key: str = Depends(get_api_key)):
    """
    Serves low-latency user data for a single user ID.
    This endpoint is secured and provides a data SLA guarantee.
    """
    logging.info(f"Request received for user: {user_id}")
    
    user = MOCK_USER_DB.get(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

if __name__ == "__main__":
    # Run with: uvicorn data_api:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
