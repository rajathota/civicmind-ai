"""
CivicMind Parking Service - Main Application
===========================================

Standalone parking service that can be deployed independently.
This service demonstrates the multi-repository architecture approach.
"""

import logging
import time
from typing import Dict, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .config import settings
from .services import ParkingService
from .models import ParkingAnalysisRequest, ParkingAnalysisResponse

# Initialize logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global service instance
parking_service = ParkingService()

# Service start time for uptime calculation
service_start_time = time.time()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title="CivicMind Parking Service",
        description="Independent microservice for parking-related civic issues",
        version=settings.SERVICE_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.middleware("http")
    async def add_request_id_header(request: Request, call_next):
        """Add request ID and timing headers"""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Service"] = settings.SERVICE_NAME
        return response
    
    @app.get("/")
    async def root():
        """Root endpoint with service information"""
        return {
            "service": settings.SERVICE_NAME,
            "version": settings.SERVICE_VERSION,
            "status": "operational",
            "message": "CivicMind Parking Service - Community-First Civic Solutions",
            "documentation": "/docs",
            "health_check": "/health"
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        try:
            health_info = parking_service.get_service_health()
            return JSONResponse(
                status_code=200,
                content=health_info
            )
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return JSONResponse(
                status_code=503,
                content={
                    "service": settings.SERVICE_NAME,
                    "status": "unhealthy",
                    "error": str(e)
                }
            )
    
    @app.get("/info")
    async def service_info():
        """Service information endpoint"""
        return parking_service.get_service_info()
    
    @app.get("/metrics")
    async def service_metrics():
        """Service metrics endpoint"""
        uptime = time.time() - service_start_time
        return {
            "service": settings.SERVICE_NAME,
            "uptime_seconds": uptime,
            "version": settings.SERVICE_VERSION,
            "timestamp": datetime.now().isoformat()
        }
    
    @app.post("/analyze", response_model=ParkingAnalysisResponse)
    async def analyze_parking_issue(request: ParkingAnalysisRequest):
        """
        Analyze a parking issue and provide recommendations.
        
        This endpoint accepts a parking issue description and returns
        a comprehensive analysis with community-first resolution steps.
        """
        try:
            logger.info(f"Received analysis request: {request.description[:50]}...")
            
            response = await parking_service.analyze_parking_issue(request)
            
            logger.info(f"Successfully analyzed issue {response.issue_id}")
            return response
            
        except ValueError as e:
            logger.warning(f"Invalid request: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail="Internal server error during analysis"
            )
    
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        """Custom 404 handler"""
        return JSONResponse(
            status_code=404,
            content={
                "error": "Endpoint not found",
                "service": settings.SERVICE_NAME,
                "available_endpoints": [
                    "/",
                    "/health", 
                    "/info",
                    "/metrics",
                    "/analyze",
                    "/docs"
                ]
            }
        )
    
    return app


# Create the app instance
app = create_app()


def main():
    """Main entry point for the service"""
    logger.info(f"Starting {settings.SERVICE_NAME} v{settings.SERVICE_VERSION}")
    logger.info(f"Service will run on port {settings.SERVICE_PORT}")
    
    uvicorn.run(
        "parking_service.main:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
