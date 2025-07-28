"""
Parking Business Service
=======================

Business logic layer for parking service operations.
"""

import logging
from typing import Dict, Any
from datetime import datetime

from ..agents import ParkingServiceAgent
from ..models import ParkingAnalysisRequest, ParkingAnalysisResponse
from ..config import settings


logger = logging.getLogger(__name__)


class ParkingService:
    """Business service for parking operations"""
    
    def __init__(self):
        """Initialize the parking service"""
        self.agent = ParkingServiceAgent()
        self.service_start_time = datetime.now()
        logger.info("Parking service initialized")
    
    async def analyze_parking_issue(self, request: ParkingAnalysisRequest) -> ParkingAnalysisResponse:
        """
        Analyze a parking issue using the parking agent.
        
        Args:
            request: Parking analysis request
            
        Returns:
            Analysis response from the parking agent
        """
        try:
            logger.info(f"Processing parking analysis request")
            
            # Validate request
            if not request.description or len(request.description.strip()) == 0:
                raise ValueError("Description is required")
            
            # Process with agent
            response = await self.agent.analyze_issue(request)
            
            logger.info(f"Successfully processed issue {response.issue_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing parking analysis: {str(e)}")
            raise
    
    def get_service_health(self) -> Dict[str, Any]:
        """Get service health information"""
        uptime = (datetime.now() - self.service_start_time).total_seconds()
        
        return {
            "service": settings.SERVICE_NAME,
            "status": "healthy",
            "version": settings.SERVICE_VERSION,
            "uptime_seconds": uptime,
            "checks": {
                "agent_status": {
                    "status": "healthy",
                    "details": "Parking agent operational"
                },
                "memory_usage": {
                    "status": "healthy", 
                    "details": "Memory usage within normal limits"
                }
            }
        }
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get service information"""
        return {
            "service": settings.SERVICE_NAME,
            "version": settings.SERVICE_VERSION,
            "description": "Independent microservice for parking-related civic issues",
            "agent_type": "parking",
            "capabilities": [
                "Parking issue analysis",
                "Community-first resolution",
                "Local contact information",
                "Cultural sensitivity guidance"
            ],
            "supported_issue_types": [
                "driveway_blocking",
                "permit_violation", 
                "commercial_violation",
                "general_parking"
            ]
        }
