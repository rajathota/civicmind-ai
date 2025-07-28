"""
CivicMind Orchestrator Service
==============================

FastAPI service that orchestrates civic issue resolution workflows.
Coordinates between API services and MCP servers.

Port: 8100
Version: 1.0.0
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import uvicorn
from pydantic import BaseModel

from .workflows.civic_workflow import CivicWorkflowEngine
from .agents.agent_coordinator import AgentCoordinator

# Service configuration
SERVICE_NAME = "civicmind-orchestrator-service"
SERVICE_VERSION = "1.0.0"
SERVICE_PORT = 8100

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global components
workflow_engine: Optional[CivicWorkflowEngine] = None
agent_coordinator: Optional[AgentCoordinator] = None

# Create FastAPI app
app = FastAPI(
    title="CivicMind Orchestrator Service",
    description="Workflow orchestration for civic issue resolution",
    version=SERVICE_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CivicIssueRequest(BaseModel):
    """Request model for civic issue orchestration"""
    description: str
    location: Optional[str] = None
    citizen_info: Optional[Dict[str, Any]] = None
    priority: Optional[str] = "medium"
    issue_type: Optional[str] = None


class OrchestrationResponse(BaseModel):
    """Response model for orchestrated civic issue resolution"""
    workflow_id: str
    issue_classification: Dict[str, Any]
    assigned_services: List[str]
    mcp_agents_used: List[str]
    resolution_plan: Dict[str, Any]
    estimated_completion: str
    status: str


@app.on_event("startup")
async def startup_event():
    """Initialize the orchestrator service"""
    global workflow_engine, agent_coordinator
    
    try:
        logger.info(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}")
        
        # Initialize workflow engine
        workflow_engine = CivicWorkflowEngine()
        await workflow_engine.initialize()
        
        # Initialize agent coordinator  
        agent_coordinator = AgentCoordinator()
        await agent_coordinator.initialize()
        
        logger.info("Orchestrator service initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "status": "operational",
        "message": "CivicMind Orchestrator - Workflow Coordination Service",
        "capabilities": [
            "workflow_orchestration",
            "service_coordination", 
            "mcp_agent_management",
            "multi_step_resolution"
        ],
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        health_info = {
            "service": SERVICE_NAME,
            "status": "healthy",
            "version": SERVICE_VERSION,
            "timestamp": datetime.now().isoformat(),
            "components": {
                "workflow_engine": workflow_engine.get_status() if workflow_engine else "not_initialized",
                "agent_coordinator": agent_coordinator.get_status() if agent_coordinator else "not_initialized"
            }
        }
        
        return JSONResponse(status_code=200, content=health_info)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "service": SERVICE_NAME,
                "status": "unhealthy",
                "error": str(e)
            }
        )


@app.get("/workflows")
async def list_workflows():
    """List available workflow types"""
    if not workflow_engine:
        raise HTTPException(status_code=503, detail="Workflow engine not initialized")
    
    workflows = await workflow_engine.list_available_workflows()
    return {
        "available_workflows": workflows,
        "total_count": len(workflows)
    }


@app.get("/services")
async def list_services():
    """List available services and their status"""
    if not agent_coordinator:
        raise HTTPException(status_code=503, detail="Agent coordinator not initialized")
    
    services = await agent_coordinator.get_service_registry()
    return {
        "api_services": services.get("api_services", []),
        "mcp_servers": services.get("mcp_servers", []),
        "total_services": len(services.get("api_services", [])) + len(services.get("mcp_servers", []))
    }


@app.post("/orchestrate", response_model=OrchestrationResponse)
async def orchestrate_civic_issue(request: CivicIssueRequest):
    """
    Orchestrate the resolution of a civic issue.
    
    This endpoint coordinates the entire resolution process:
    1. Classifies the issue type
    2. Selects appropriate services and agents
    3. Creates resolution workflow
    4. Executes multi-step process
    """
    try:
        if not workflow_engine or not agent_coordinator:
            raise HTTPException(status_code=503, detail="Services not initialized")
        
        logger.info(f"Orchestrating civic issue: {request.description[:50]}...")
        
        # Step 1: Classify the issue
        classification = await workflow_engine.classify_issue(
            description=request.description,
            location=request.location,
            suggested_type=request.issue_type
        )
        
        # Step 2: Select appropriate services
        service_selection = await agent_coordinator.select_services(
            issue_type=classification["type"],
            priority=request.priority,
            location=request.location
        )
        
        # Step 3: Create resolution workflow
        workflow_plan = await workflow_engine.create_workflow(
            classification=classification,
            services=service_selection,
            citizen_info=request.citizen_info
        )
        
        # Step 4: Execute workflow
        execution_result = await workflow_engine.execute_workflow(
            workflow_plan=workflow_plan,
            issue_request=request.dict()
        )
        
        # Create response
        response = OrchestrationResponse(
            workflow_id=execution_result["workflow_id"],
            issue_classification=classification,
            assigned_services=service_selection["api_services"],
            mcp_agents_used=service_selection["mcp_servers"],
            resolution_plan=workflow_plan,
            estimated_completion=execution_result["estimated_completion"],
            status=execution_result["status"]
        )
        
        logger.info(f"Successfully orchestrated workflow {response.workflow_id}")
        return response
        
    except Exception as e:
        logger.error(f"Orchestration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Orchestration failed: {str(e)}")


@app.get("/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get the status of a specific workflow"""
    if not workflow_engine:
        raise HTTPException(status_code=503, detail="Workflow engine not initialized")
    
    try:
        status = await workflow_engine.get_workflow_status(workflow_id)
        return status
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get workflow status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/workflows/{workflow_id}/cancel")
async def cancel_workflow(workflow_id: str):
    """Cancel a running workflow"""
    if not workflow_engine:
        raise HTTPException(status_code=503, detail="Workflow engine not initialized")
    
    try:
        result = await workflow_engine.cancel_workflow(workflow_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to cancel workflow: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def main():
    """Main entry point for the orchestrator service"""
    logger.info(f"Starting {SERVICE_NAME} on port {SERVICE_PORT}")
    uvicorn.run(
        "orchestrator_service.main:app",
        host="0.0.0.0",
        port=SERVICE_PORT,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
