"""
FastAPI Server for CivicMind AI Framework
=========================================

Main server application providing REST API for civic issue resolution.
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from civicmind.core.civic_orchestrator import (
    CivicOrchestrator, 
    CivicIssue, 
    IssueType, 
    Priority
)
from civicmind.core.agent_factory import AgentFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CivicMind AI API",
    description="AI-powered civic issue resolution platform",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
orchestrator: Optional[CivicOrchestrator] = None
agent_factory: Optional[AgentFactory] = None


class IssueRequest(BaseModel):
    """Request model for civic issues"""
    description: str
    location: Optional[str] = None
    citizen_info: Optional[Dict[str, Any]] = None
    priority: Optional[str] = "medium"


class IssueResponse(BaseModel):
    """Response model for civic issue analysis"""
    issue_id: str
    issue_type: str
    priority: str
    recommendations: list
    contacts: list
    documents: list
    next_steps: list
    resolution_path: str
    confidence: float
    timestamp: str


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    global orchestrator, agent_factory
    
    # Get API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error("OPENAI_API_KEY environment variable is required")
        raise RuntimeError("OPENAI_API_KEY environment variable is required")
    
    # Initialize components
    try:
        orchestrator = CivicOrchestrator(
            openai_api_key=openai_api_key,
            langsmith_api_key=os.getenv("LANGSMITH_API_KEY")
        )
        agent_factory = AgentFactory(openai_api_key=openai_api_key)
        logger.info("CivicMind AI framework initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize framework: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CivicMind AI Framework",
        "version": "0.1.0",
        "description": "AI-powered civic issue resolution platform"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "orchestrator": orchestrator is not None,
            "agent_factory": agent_factory is not None
        }
    }


@app.post("/api/v1/issues/analyze", response_model=IssueResponse)
async def analyze_issue(request: IssueRequest, background_tasks: BackgroundTasks):
    """
    Analyze a civic issue and provide recommendations
    """
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    try:
        # Create civic issue object
        issue = CivicIssue(
            id=f"issue_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=request.description,
            location=request.location,
            priority=Priority(request.priority.lower()) if request.priority else Priority.MEDIUM,
            citizen_info=request.citizen_info or {},
            timestamp=datetime.now()
        )
        
        # Process through orchestrator
        result = await orchestrator.process_issue(issue)
        
        # Format response
        response = IssueResponse(
            issue_id=result.issue.id,
            issue_type=result.issue.issue_type.value,
            priority=result.issue.priority.value,
            recommendations=result.recommendations,
            contacts=[contact.get("name", "") for contact in result.contacts],
            documents=result.documents,
            next_steps=result.next_steps,
            resolution_path=result.resolution_path,
            confidence=0.85,  # Default confidence
            timestamp=datetime.now().isoformat()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error analyzing issue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/agents")
async def list_agents():
    """List all available agent types"""
    if not agent_factory:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    agents = agent_factory.list_agents()
    return {
        "agents": list(agents.keys()),
        "count": len(agents)
    }


@app.post("/api/v1/agents/{agent_type}/analyze")
async def analyze_with_specific_agent(
    agent_type: str, 
    request: IssueRequest
):
    """
    Analyze an issue with a specific agent type
    """
    if not agent_factory:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    try:
        # Create and use specific agent
        agent = agent_factory.create_agent(agent_type)
        
        result = agent.analyze_issue(
            issue_description=request.description,
            location=request.location or "Unknown",
            context=request.citizen_info or {}
        )
        
        return {
            "agent_type": agent_type,
            "recommendations": result.recommendations,
            "contacts": result.contacts,
            "documents": result.documents,
            "next_steps": result.next_steps,
            "confidence": result.confidence,
            "community_first": result.community_first
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error with agent {agent_type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/locations/{location}/info")
async def get_location_info(location: str):
    """
    Get civic information for a specific location
    """
    # This would integrate with civic data APIs
    # For now, return placeholder data
    return {
        "location": location,
        "departments": [
            {"name": "Planning Department", "phone": "(555) 123-4567"},
            {"name": "Code Enforcement", "phone": "(555) 123-4568"},
            {"name": "Public Works", "phone": "(555) 123-4569"}
        ],
        "emergency_contacts": [
            {"name": "Police (Non-Emergency)", "phone": "(555) 123-4570"},
            {"name": "Fire Department", "phone": "(555) 123-4571"}
        ],
        "online_services": [
            {"name": "Permit Portal", "url": "https://example.gov/permits"},
            {"name": "311 Reporting", "url": "https://example.gov/311"}
        ]
    }


if __name__ == "__main__":
    # For development
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
