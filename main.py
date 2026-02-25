from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from agent import analyze_asset

# 1. Initialize the FastAPI app
app = FastAPI(title="MarketSentient AI Engine")

# 2. Configure CORS (Crucial!)
# This tells the backend to accept requests from your Next.js frontend tomorrow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any frontend to connect during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the data structure we expect from the frontend
class AnalyzeRequest(BaseModel):
    ticker: str

# 4. Create the API Endpoint
@app.post("/api/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    """
    This is the exact URL the frontend will hit: http://localhost:8000/api/analyze
    """
    # Trigger your LangGraph AI Agent from agent.py
    ai_response = analyze_asset(request.ticker)
    
    # Return the clean JSON back to the web browser
    return {
        "ticker": request.ticker,
        "analysis": ai_response
    }

# 5. Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)