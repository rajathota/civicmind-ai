"""
Models package for parking service.
"""

from .requests import (
    ParkingAnalysisRequest,
    ParkingAnalysisResponse,
    ParkingClassification,
    ParkingRecommendation,
    ParkingContact,
    ServiceHealthResponse
)

__all__ = [
    "ParkingAnalysisRequest",
    "ParkingAnalysisResponse", 
    "ParkingClassification",
    "ParkingRecommendation",
    "ParkingContact",
    "ServiceHealthResponse"
]
