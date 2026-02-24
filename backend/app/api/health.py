"""
API Health Check Route
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Lead Scoring Agent API",
        "version": "1.0.0"
    }
