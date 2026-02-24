"""
API Router Setup
"""

from fastapi import APIRouter
from app.api import leads, health

api_router = APIRouter()

# Include route modules
api_router.include_router(health.router)
api_router.include_router(leads.router)
