"""
Lead Scoring Agent Backend - Main Entry Point

To run the application:
  uvicorn app.main:app --reload --port 8000

Or use the seed script:
  python -m seed_data.init_seed

"""

import sys
from pathlib import Path

# Ensure the backend is importable
backend_path = Path(__file__).parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings
    
    print(f"""
    ╔═══════════════════════════════════════╗
    ║   Lead Scoring Agent API Server      ║
    ║   Version 1.0.0                      ║
    ╚═══════════════════════════════════════╝
    
    Environment: {settings.env}
    Host: {settings.api_host}:{settings.api_port}
    Workers: {settings.api_workers}
    Debug: {settings.debug}
    
    Starting server...
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=settings.debug,
    )
