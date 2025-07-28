"""
Configuration for CivicMind AI Framework
=======================================

Centralized configuration management for the framework.
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    langsmith_api_key: Optional[str] = Field(None, env="LANGSMITH_API_KEY")
    
    # Model Configuration
    default_model: str = Field("gpt-4o", env="CIVICMIND_MODEL")
    temperature: float = Field(0.1, env="CIVICMIND_TEMPERATURE")
    
    # Server Configuration
    host: str = Field("0.0.0.0", env="CIVICMIND_HOST")
    port: int = Field(8000, env="CIVICMIND_PORT")
    reload: bool = Field(False, env="CIVICMIND_RELOAD")
    
    # Database Configuration
    database_url: Optional[str] = Field(None, env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # Vector Store Configuration
    vector_store_type: str = Field("chroma", env="VECTOR_STORE_TYPE")
    vector_store_path: str = Field("./data/vectorstore", env="VECTOR_STORE_PATH")
    
    # Civic Data Sources
    civic_apis: List[str] = Field(
        default=["seeclickfix", "openstates", "google_civic"],
        env="CIVIC_APIS"
    )
    
    # Security
    secret_key: str = Field("your-secret-key-here", env="SECRET_KEY")
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        env="ALLOWED_ORIGINS"
    )
    
    # Feature Flags
    enable_community_resolution: bool = Field(True, env="ENABLE_COMMUNITY_RESOLUTION")
    enable_multimodal: bool = Field(True, env="ENABLE_MULTIMODAL")
    enable_voice_input: bool = Field(False, env="ENABLE_VOICE_INPUT")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
