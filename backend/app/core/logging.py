"""
Logging configuration for the Lead Scoring Agent.
Sets up structured logging for production use.
"""

import logging
import sys
from pythonjsonlogger import jsonlogger
from app.core.config import settings


def setup_logging():
    """
    Configure structured JSON logging for production environments.
    """
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(settings.log_level)
    
    # Console handler with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    json_formatter = jsonlogger.JsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s"
    )
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)
    
    return logger


# Create global logger
logger = setup_logging()
