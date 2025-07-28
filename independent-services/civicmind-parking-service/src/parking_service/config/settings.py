"""
Parking Service Configuration
============================

Configuration settings for the parking service.
"""

import os
from typing import Optional


class Settings:
    """Service configuration settings"""
    
    # Service Identity
    SERVICE_NAME: str = "parking-service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 9300
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    
    # Health Check Configuration
    HEALTH_CHECK_INTERVAL: int = 30
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # External Services
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Database (if needed in future)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Cache
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")


# Global settings instance
settings = Settings()
