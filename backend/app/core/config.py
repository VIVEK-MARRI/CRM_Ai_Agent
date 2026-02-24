"""
Configuration management for the Lead Scoring Agent.
Handles environment variables and application settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses Pydantic BaseSettings for validation and type checking.
    """
    
    # Environment
    env: str = "development"
    debug: bool = True
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_title: str = "Lead Scoring Agent API"
    api_version: str = "1.0.0"
    
    # Database Configuration
    database_url: str = "postgresql://postgres:postgres@localhost:5432/lead_scoring_db"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # Logging Configuration
    log_level: str = "INFO"
    
    # Application paths
    config_path: str = "./config/scoring_weights.yaml"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
