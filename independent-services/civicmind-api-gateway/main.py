"""
CivicMind API Gateway - Independent Service
==========================================

Standalone API Gateway that routes requests to independent civic services.
This gateway demonstrates the multi-repository architecture approach.

Port: 8300
Version: 1.0.0
"""

import asyncio
import time
import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import uvicorn

# Service configuration
SERVICE_NAME = "api-gateway"
SERVICE_VERSION = "1.0.0"
SERVICE_PORT = 8300

# Service registry - in production, this would be dynamic discovery
CIVIC_SERVICES = {
    "parking": {
        "url": "http://localhost:9300",
        "name": "parking-service",
        "version": "1.0.0",
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze"
    },
    "permits": {
        "url": "http://localhost:9301", 
        "name": "permits-service",
        "version": "1.0.0",
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze"
    },
    "noise": {
        "url": "http://localhost:9302",
        "name": "noise-service", 
        "version": "1.0.0",
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze"
    },
    "infrastructure": {
        "url": "http://localhost:9303",
        "name": "infrastructure-service",
        "version": "1.0.0", 
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze"
    },
    "business": {
        "url": "http://localhost:9304",
        "name": "business-service",
        "version": "1.0.0",
        "health_endpoint": "/health", 
        "analyze_endpoint": "/analyze"
    },
    "religious_events": {
        "url": "http://localhost:9305",
        "name": "religious-events-service",
        "version": "1.0.0",
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze"
    },
    "neighbor_dispute": {
        "url": "http://localhost:9306", 
        "name": "neighbor-dispute-service",
        "version": "1.0.0",
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze"
    },
    "environmental": {
        "url": "http://localhost:9307",
        "name": "environmental-service",
        "version": "1.0.0",
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze"
    }
}

# Initialize FastAPI app
app = FastAPI(
    title="CivicMind API Gateway",
    description="Central API Gateway for CivicMind microservices architecture",
    version=SERVICE_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "gateway",
            "description": "API Gateway operations"
        },
        {
            "name": "analysis", 
            "description": "Civic issue analysis routing"
        },
        {
            "name": "services",
            "description": "Service discovery and management"
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
service_health_cache = {}

@app.on_event("startup")
async def startup_event():
    """Initialize API Gateway on startup"""
    print("🌐 Starting CivicMind API Gateway")
    print("=" * 50)
    print(f"Version: {SERVICE_VERSION}")
    print(f"Port: {SERVICE_PORT}")
    print(f"Registered Services: {len(CIVIC_SERVICES)}")
    print("=" * 50)
    
    # Initial health check of all services
    await update_service_health_cache()
    
    print(f"🚀 API Gateway started successfully on port {SERVICE_PORT}")

async def update_service_health_cache():
    """Update health status cache for all services"""
    global service_health_cache
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, service_config in CIVIC_SERVICES.items():
            try:
                url = f"{service_config['url']}{service_config['health_endpoint']}"
                response = await client.get(url)
                
                service_health_cache[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_code": response.status_code,
                    "last_check": datetime.utcnow().isoformat() + "Z",
                    "url": service_config['url']
                }
            except Exception as e:
                service_health_cache[service_name] = {
                    "status": "unreachable",
                    "error": str(e),
                    "last_check": datetime.utcnow().isoformat() + "Z",
                    "url": service_config['url']
                }

def classify_issue(description: str) -> str:
    """
    Classify civic issue to determine which service should handle it.
    In production, this would use ML/AI for classification.
    """
    description_lower = description.lower()
    
    # Parking-related keywords
    if any(word in description_lower for word in [
        "park", "driveway", "block", "car", "vehicle", "permit", "meter"
    ]):
        return "parking"
    
    # Noise-related keywords
    elif any(word in description_lower for word in [
        "noise", "loud", "music", "bark", "construction", "sound"
    ]):
        return "noise"
    
    # Permits-related keywords
    elif any(word in description_lower for word in [
        "permit", "license", "build", "construction", "renovation", "addition"
    ]):
        return "permits"
    
    # Infrastructure keywords
    elif any(word in description_lower for word in [
        "road", "street", "pothole", "light", "water", "sewer", "utility"
    ]):
        return "infrastructure"
    
    # Business keywords
    elif any(word in description_lower for word in [
        "business", "commercial", "shop", "store", "restaurant"
    ]):
        return "business"
    
    # Religious/Cultural events
    elif any(word in description_lower for word in [
        "religious", "temple", "church", "mosque", "festival", "ceremony", "cultural"
    ]):
        return "religious_events"
    
    # Neighbor disputes
    elif any(word in description_lower for word in [
        "neighbor", "dispute", "fence", "property", "boundary", "conflict"
    ]):
        return "neighbor_dispute"
    
    # Environmental issues
    elif any(word in description_lower for word in [
        "environment", "pollution", "air", "water", "waste", "dumping", "recycle"
    ]):
        return "environmental"
    
    # Default to general infrastructure
    else:
        return "infrastructure"

@app.get("/", tags=["gateway"])
async def root():
    """API Gateway root endpoint"""
    uptime = round(time.time() - start_time, 2)
    
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "status": "running",
        "port": SERVICE_PORT,
        "architecture": "microservices",
        "uptime_seconds": uptime,
        "registered_services": len(CIVIC_SERVICES),
        "endpoints": {
            "analyze": "/api/v1/issues/analyze",
            "services": "/api/v1/services",
            "health": "/health",
            "docs": "/docs"
        },
        "description": "Central API Gateway routing requests to specialized civic services"
    }

@app.get("/health", tags=["gateway"])
async def health_check():
    """API Gateway health check"""
    uptime = round(time.time() - start_time, 2)
    
    # Count healthy services
    healthy_services = sum(1 for status in service_health_cache.values() 
                          if status.get("status") == "healthy")
    total_services = len(CIVIC_SERVICES)
    
    gateway_status = "healthy" if healthy_services > 0 else "degraded"
    
    return {
        "service": SERVICE_NAME,
        "status": gateway_status,
        "version": SERVICE_VERSION,
        "uptime_seconds": uptime,
        "downstream_services": {
            "total": total_services,
            "healthy": healthy_services,
            "unhealthy": total_services - healthy_services
        },
        "checks": {
            "gateway": {
                "status": "healthy",
                "details": "API Gateway operational"
            },
            "service_registry": {
                "status": "healthy" if total_services > 0 else "error",
                "details": f"{total_services} services registered"
            }
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/api/v1/services", tags=["services"])
async def get_services():
    """Get information about all registered services"""
    # Update health cache
    await update_service_health_cache()
    
    services_info = {}
    for service_name, service_config in CIVIC_SERVICES.items():
        health_info = service_health_cache.get(service_name, {"status": "unknown"})
        
        services_info[service_name] = {
            "name": service_config["name"],
            "version": service_config["version"],
            "url": service_config["url"],
            "health_status": health_info["status"],
            "last_health_check": health_info.get("last_check"),
            "endpoints": {
                "health": service_config["health_endpoint"],
                "analyze": service_config["analyze_endpoint"]
            }
        }
    
    return {
        "total_services": len(CIVIC_SERVICES),
        "services": services_info,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/api/v1/issues/analyze", tags=["analysis"])
async def analyze_civic_issue(request: Dict[str, Any]):
    """
    Analyze civic issue by routing to appropriate specialized service
    
    This endpoint:
    1. Classifies the issue type
    2. Routes to the appropriate specialized service
    3. Returns the analysis result with routing information
    """
    try:
        start_time_analysis = time.time()
        
        # Extract and validate request
        description = request.get("description", "")
        location = request.get("location", "")
        
        if not description:
            raise HTTPException(status_code=400, detail="Description is required")
        
        if len(description) < 10:
            raise HTTPException(status_code=400, detail="Description too short (minimum 10 characters)")
        
        # Classify issue to determine target service
        classified_service = classify_issue(description)
        
        print(f"🔍 Classifying issue: {description[:100]}...")
        print(f"🎯 Routing to: {classified_service}-service")
        
        # Check if target service is available
        if classified_service not in CIVIC_SERVICES:
            raise HTTPException(status_code=503, detail=f"Service {classified_service} not available")
        
        service_config = CIVIC_SERVICES[classified_service]
        service_health = service_health_cache.get(classified_service, {"status": "unknown"})
        
        if service_health.get("status") != "healthy":
            # Try to route to a fallback service or return error
            raise HTTPException(
                status_code=503, 
                detail=f"Service {classified_service} is {service_health.get('status', 'unavailable')}"
            )
        
        # Route request to specialized service
        async with httpx.AsyncClient(timeout=30.0) as client:
            service_url = f"{service_config['url']}{service_config['analyze_endpoint']}"
            
            response = await client.post(
                service_url,
                json=request,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"Service {classified_service} returned error: {response.status_code}"
                )
            
            service_response = response.json()
        
        processing_time = (time.time() - start_time_analysis) * 1000
        
        # Add gateway metadata to response
        gateway_response = {
            "gateway_info": {
                "service": SERVICE_NAME,
                "version": SERVICE_VERSION,
                "classification": classified_service,
                "routed_to": service_config["name"],
                "routing_time_ms": round(processing_time, 2)
            },
            "service_response": service_response,
            "total_processing_time_ms": round(processing_time, 2),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        print(f"✅ Request routed and completed in {processing_time:.0f}ms")
        return gateway_response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in API Gateway: {e}")
        raise HTTPException(status_code=500, detail=f"Gateway error: {str(e)}")

@app.get("/api/v1/services/{service_name}/health", tags=["services"])
async def check_service_health(service_name: str):
    """Check health of a specific service"""
    if service_name not in CIVIC_SERVICES:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    service_config = CIVIC_SERVICES[service_name]
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"{service_config['url']}{service_config['health_endpoint']}"
            response = await client.get(url)
            
            return {
                "service": service_name,
                "url": service_config["url"],
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "details": response.json() if response.status_code == 200 else None,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
    except Exception as e:
        return {
            "service": service_name,
            "url": service_config["url"],
            "status": "unreachable",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

@app.get("/metrics", tags=["gateway"])
async def get_metrics():
    """Gateway metrics for monitoring"""
    uptime = round(time.time() - start_time, 2)
    healthy_services = sum(1 for status in service_health_cache.values() 
                          if status.get("status") == "healthy")
    
    return {
        "gateway": {
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "uptime_seconds": uptime,
            "uptime_formatted": f"{uptime//3600:.0f}h {(uptime%3600)//60:.0f}m"
        },
        "services": {
            "total_registered": len(CIVIC_SERVICES),
            "healthy": healthy_services,
            "unhealthy": len(CIVIC_SERVICES) - healthy_services,
            "availability_percentage": round((healthy_services / len(CIVIC_SERVICES)) * 100, 1)
        },
        "requests": {
            "total": "N/A",  # Would implement request counting
            "success_rate": "N/A",  # Would implement success tracking
            "avg_response_time": "N/A"  # Would implement timing metrics
        }
    }

if __name__ == "__main__":
    print("🌐 CivicMind API Gateway")
    print("=" * 50)
    print(f"Version: {SERVICE_VERSION}")
    print(f"Port: {SERVICE_PORT}")
    print(f"Services: {len(CIVIC_SERVICES)} registered")
    print(f"Documentation: http://localhost:{SERVICE_PORT}/docs")
    print("=" * 50)
    
    # Run the gateway
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=SERVICE_PORT,
        reload=False,
        log_level="info"
    )
