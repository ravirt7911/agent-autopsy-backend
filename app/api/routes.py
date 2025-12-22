"""
API route handlers for the diagnostic endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import DiagnosisRequest, DiagnosisResponse
from app.core.diagnostic_engine import diagnose_agent_failure

router = APIRouter()


@router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Agent Failure Diagnostic System is running",
        "version": "1.0.0"
    }


@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: DiagnosisRequest):
    """
    Main diagnostic endpoint
    
    Accepts agent execution details and returns a diagnosis
    identifying the primary failure type with evidence and a fix.
    """
    try:
        result = await diagnose_agent_failure(request)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Diagnosis failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "ok"}

