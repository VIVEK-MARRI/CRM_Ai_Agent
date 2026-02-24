"""
FastAPI Application Factory and Configuration

Creates and configures the main FastAPI application with:
- CORS middleware
- Error handlers
- Database initialization
- Logging setup
- Route mounting
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import logger
from app.db.database import init_db
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management.
    
    Startup: Initialize database
    Shutdown: Cleanup
    """
    # Startup
    logger.info("Starting Lead Scoring Agent API")
    init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Lead Scoring Agent API")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI instance
    """
    
    # Create app with lifespan
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="AI-powered Lead Scoring Agent for CRM Integration",
        lifespan=lifespan,
        debug=settings.debug,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Production: specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router)
    
    logger.info("FastAPI application created successfully")
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    logger.info(
        f"Starting server on {settings.api_host}:{settings.api_port} "
        f"with {settings.api_workers} workers"
    )
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=settings.debug,
    )
