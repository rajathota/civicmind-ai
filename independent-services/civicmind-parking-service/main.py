"""
CivicMind Parking Service - Independent Microservice
====================================================

Standalone parking service that can be deployed independently.
This service demonstrates the multi-repository architecture approach.

Port: 9300
Version: 1.0.0
"""

import asyncio
import logging
import time
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# In production, this would be: from civicmind_common import ...
# For demo, we'll use relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared-lib'))

try:
    from civicmind_common.models.base_models import (
        CivicRequest, CivicResponse, HealthCheckResponse
    )
    from civicmind_common.utils.logging import setup_logging
    from civicmind_common.utils.health_checks import HealthChecker
except ImportError:
    # Fallback for demo - would not be needed in production
    print("Warning: Using fallback imports for demo")

# Service configuration
SERVICE_NAME = "parking-service"
SERVICE_VERSION = "1.0.0"
SERVICE_PORT = 9300

# Initialize FastAPI app
app = FastAPI(
    title="CivicMind Parking Service",
    description="Independent microservice for parking-related civic issues",
    version=SERVICE_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "parking",
            "description": "Parking issue analysis and resolution"
        },
        {
            "name": "health",
            "description": "Service health and monitoring"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service state
start_time = time.time()
parking_agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    global parking_agent
    
    print(f"🚗 Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    
    # Initialize parking agent (simplified for demo)
    try:
        parking_agent = ParkingServiceAgent()
        print("✅ Parking agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize parking agent: {e}")
        raise
    
    print(f"🚀 {SERVICE_NAME} started successfully on port {SERVICE_PORT}")

class ParkingServiceAgent:
    """Simplified parking agent for independent service"""
    
    def __init__(self):
        self.agent_type = "parking"
        self.version = "1.0.0"
    
    async def analyze_issue(self, description: str, location: str, 
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze parking-related civic issue"""
        
        # Simulate analysis (in production, this would use OpenAI/LangChain)
        analysis = {
            "classification": {
                "type": "parking",
                "confidence": 0.95,
                "subtype": self._classify_parking_issue(description)
            },
            "recommendations": self._get_recommendations(description),
            "next_steps": self._get_next_steps(description),
            "community_first_approach": True,
            "escalation_path": [
                {
                    "level": "Community",
                    "actions": ["Neighbor conversation", "HOA mediation"]
                },
                {
                    "level": "Municipal", 
                    "actions": ["Parking enforcement", "City complaint"]
                }
            ],
            "contacts": self._get_local_contacts(location),
            "cultural_considerations": {
                "note": "Approach with respect and understanding",
                "suggestions": ["Use non-confrontational language"]
            }
        }
        
        return analysis
    
    def _classify_parking_issue(self, description: str) -> str:
        """Classify the type of parking issue"""
        description_lower = description.lower()
        
        if "driveway" in description_lower and "block" in description_lower:
            return "driveway_blocking"
        elif "permit" in description_lower:
            return "parking_permit"
        elif "commercial" in description_lower or "truck" in description_lower:
            return "commercial_parking"
        elif "violation" in description_lower:
            return "parking_violation"
        else:
            return "general_parking"
    
    def _get_recommendations(self, description: str) -> list:
        """Get parking-specific recommendations"""
        return [
            "Document the issue with photos and timestamps",
            "Check local parking regulations and ordinances",
            "Attempt friendly neighbor-to-neighbor resolution first",
            "Contact local parking enforcement if needed"
        ]
    
    def _get_next_steps(self, description: str) -> list:
        """Get actionable next steps"""
        return [
            {
                "step": 1,
                "action": "Document Issue",
                "description": "Take photos showing the parking violation",
                "timeline": "Immediate"
            },
            {
                "step": 2,
                "action": "Community Approach",
                "description": "Speak with neighbor politely about the issue",
                "timeline": "Within 24 hours"
            },
            {
                "step": 3,
                "action": "Official Report",
                "description": "Contact parking enforcement if needed",
                "timeline": "If community approach fails"
            }
        ]
    
    def _get_local_contacts(self, location: str) -> list:
        """Get location-specific contacts"""
        # In production, this would query a database
        return [
            {
                "name": "Local Parking Enforcement",
                "phone": "(XXX) XXX-XXXX",
                "email": "parking@city.gov",
                "hours": "Monday-Friday 8:00 AM - 5:00 PM"
            }
        ]

@app.get("/", tags=["health"])
async def root():
    """Root endpoint with service information"""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "status": "running",
        "port": SERVICE_PORT,
        "agent_type": "parking",
        "endpoints": {
            "analyze": "/analyze",
            "health": "/health",
            "docs": "/docs",
            "metrics": "/metrics"
        },
        "uptime_seconds": round(time.time() - start_time, 2)
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Service health check endpoint"""
    try:
        uptime = round(time.time() - start_time, 2)
        
        status = {
            "service": SERVICE_NAME,
            "status": "healthy" if parking_agent else "unhealthy",
            "version": SERVICE_VERSION,
            "uptime_seconds": uptime,
            "checks": {
                "agent_status": {
                    "status": "healthy" if parking_agent else "error",
                    "details": "Parking agent operational" if parking_agent else "Agent not initialized"
                },
                "memory": {
                    "status": "healthy",
                    "details": "Memory usage within limits"
                }
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/analyze", tags=["parking"])
async def analyze_parking_issue(request: Dict[str, Any]):
    """
    Analyze parking-related civic issue
    
    Provides specialized analysis for:
    - 🚗 Driveway blocking incidents
    - 🅿️ Parking permit applications  
    - 🚛 Commercial vehicle violations
    - 📋 General parking enforcement
    - 🏘️ Residential parking disputes
    """
    if parking_agent is None:
        raise HTTPException(status_code=503, detail="Parking agent not available")
    
    try:
        start_time_analysis = time.time()
        
        # Extract and validate request
        description = request.get("description", "")
        location = request.get("location", "")
        context = request.get("context", {})
        
        if not description:
            raise HTTPException(status_code=400, detail="Description is required")
        
        if len(description) < 10:
            raise HTTPException(status_code=400, detail="Description too short")
        
        print(f"🔍 Analyzing parking issue: {description[:100]}...")
        
        # Perform analysis
        analysis_result = await parking_agent.analyze_issue(
            description=description,
            location=location,
            context=context
        )
        
        processing_time = (time.time() - start_time_analysis) * 1000
        
        # Format response
        response = {
            "issue_id": f"parking-{int(time.time())}",
            "service_info": {
                "service": SERVICE_NAME,
                "version": SERVICE_VERSION,
                "agent_type": "parking",
                "port": SERVICE_PORT
            },
            "analysis": analysis_result,
            "processing_time_ms": round(processing_time, 2),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "completed"
        }
        
        print(f"✅ Analysis completed in {processing_time:.0f}ms")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error analyzing parking issue: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/metrics", tags=["health"])
async def get_metrics():
    """Service metrics endpoint for monitoring"""
    uptime = round(time.time() - start_time, 2)
    
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime_seconds": uptime,
        "uptime_formatted": f"{uptime//3600:.0f}h {(uptime%3600)//60:.0f}m",
        "agent_status": "operational" if parking_agent else "error",
        "memory_usage": "healthy",  # Would implement actual monitoring
        "request_count": "N/A",    # Would implement request counting
        "error_rate": "N/A",       # Would implement error tracking
        "avg_response_time": "N/A" # Would implement timing metrics
    }

@app.get("/info", tags=["parking"])
async def get_service_info():
    """Detailed service information"""
    return {
        "service": {
            "name": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "description": "Independent parking service for civic issues",
            "port": SERVICE_PORT,
            "agent_type": "parking"
        },
        "capabilities": [
            "Driveway blocking analysis",
            "Parking permit guidance",
            "Violation reporting",
            "Community-first resolution",
            "Cultural sensitivity",
            "Local contact information"
        ],
        "endpoints": {
            "POST /analyze": "Analyze parking issues",
            "GET /health": "Health check",
            "GET /metrics": "Service metrics",
            "GET /info": "Service information",
            "GET /docs": "API documentation"
        },
        "architecture": "Independent microservice",
        "deployment": "Can run standalone or in container"
    }

if __name__ == "__main__":
    print("🚗 CivicMind Parking Service")
    print("=" * 50)
    print(f"Version: {SERVICE_VERSION}")
    print(f"Port: {SERVICE_PORT}")
    print(f"Documentation: http://localhost:{SERVICE_PORT}/docs")
    print("=" * 50)
    
    # Run the service
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=SERVICE_PORT,
        reload=False,
        log_level="info"
    )
