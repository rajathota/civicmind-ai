"""
CivicMind Common Library
=======================

Shared models, utilities, and base classes for CivicMind microservices.
This library provides common functionality used across all CivicMind services.

Version: 1.0.0
Author: CivicMind AI Team
License: Apache 2.0
"""

__version__ = "1.0.0"
__author__ = "CivicMind AI Team"

# Export main classes and functions
from .models.base_models import CivicRequest, CivicResponse, CivicIssue
from .models.agent_models import AgentResponse, AgentClassification
from .auth.jwt_handler import JWTHandler
from .utils.logging import setup_logging
from .utils.health_checks import HealthChecker
from .clients.openai_client import OpenAIClient

__all__ = [
    "CivicRequest",
    "CivicResponse", 
    "CivicIssue",
    "AgentResponse",
    "AgentClassification",
    "JWTHandler",
    "setup_logging",
    "HealthChecker",
    "OpenAIClient"
]
