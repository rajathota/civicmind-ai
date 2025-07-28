"""
Parking Service Package
======================

CivicMind Parking Service - Independent microservice for parking-related civic issues.
"""

__version__ = "1.0.0"
__service_name__ = "parking-service"

from .main import app, create_app

__all__ = ["app", "create_app"]
