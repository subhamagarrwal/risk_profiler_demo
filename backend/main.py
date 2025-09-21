from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from models import *
from services import RiskProfilerService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Risk Profiler API",
    description="Financial Risk Profiling and Portfolio Analytics API",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
risk_profiler = RiskProfilerService()

@app.get("/")
async def root():
    return {"message": "Risk Profiler API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "risk-profiler-api"}

@app.post("/profile", response_model=ProfileResponse)
async def generate_profile(request: ProfileRequest):
    """
    Generate risk profile from user conversational answers
    """
    try:
        logger.info(f"Processing profile request for answers: {request.answers}")
        result = risk_profiler.generate_profile(request.answers)
        logger.info(f"Generated profile: {result.label} with score {result.score}")
        return result
    except Exception as e:
        logger.error(f"Error generating profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate profile: {str(e)}")

@app.post("/weights", response_model=WeightsResponse)
async def calculate_weights(request: WeightsRequest):
    """
    Calculate investment weights from risk profile with guardrails
    """
    try:
        logger.info(f"Calculating weights for label: {request.label}, variant: {request.variant}")
        result = risk_profiler.calculate_weights(request)
        logger.info(f"Generated weights: {result.weights}")
        return result
    except Exception as e:
        logger.error(f"Error calculating weights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to calculate weights: {str(e)}")

@app.post("/analytics", response_model=AnalyticsResponse)
async def run_analytics(request: AnalyticsRequest):
    """
    Run backtesting analytics and generate performance comparisons
    """
    try:
        logger.info(f"Running analytics for weights: {request.user_weights}")
        result = risk_profiler.run_analytics(request)
        logger.info(f"Generated analytics for {len(result.portfolios)} portfolios")
        return result
    except Exception as e:
        logger.error(f"Error running analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to run analytics: {str(e)}")

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)