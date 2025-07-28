# 💡 CivicMind AI Examples & Tutorials

Comprehensive examples demonstrating CivicMind AI's **microservices architecture** and how to build AI-powered civic solutions.

## 📋 Table of Contents

1. [🚀 Quick Start Examples](#-quick-start-examples)
2. [🏗️ Building Your First Agent](#️-building-your-first-agent)
3. [🔌 Service Integration Examples](#-service-integration-examples)
4. [🌐 API Gateway Usage](#-api-gateway-usage)
5. [🎭 Orchestrator Workflows](#-orchestrator-workflows)
6. [🤖 MCP Agent Development](#-mcp-agent-development)
7. [🚢 Deployment Examples](#-deployment-examples)
8. [🔧 Advanced Integration Patterns](#-advanced-integration-patterns)

---

## 🚀 Quick Start Examples

### Basic Citizen Request via API Gateway

The API Gateway (Port 8300) intelligently routes requests to appropriate services:

```bash
# Submit a parking violation issue
curl -X POST "http://localhost:8300/api/v1/issues/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "My neighbor parks blocking my driveway every night",
    "citizen_id": "12345",
    "location": "123 Main St, Anytown",
    "contact_info": {
      "email": "citizen@example.com",
      "phone": "+1-555-0123"
    }
  }'
```

**Response:**
```json
{
  "service": "parking-service",
  "confidence": 0.95,
  "response": {
    "issue_type": "parking_violation",
    "violation_code": "PV-001",
    "suggested_actions": [
      "Contact parking enforcement at 311",
      "Document violations with photos and timestamps",
      "File a formal complaint through the parking service"
    ],
    "estimated_response_time": "24-48 hours",
    "case_number": "PK-2024-001234"
  }
}
```

### Multi-Service Complex Request

```bash
# Business permit requiring multiple departments
curl -X POST "http://localhost:8300/api/v1/issues/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I want to open a food truck business downtown",
    "business_type": "mobile_food_vendor",
    "location": "Downtown Business District"
  }'
```

**Response (Orchestrated):**
```json
{
  "services": ["business-service", "permits-service", "safety-service"],
  "workflow_id": "WF-2024-001",
  "combined_response": {
    "required_permits": [
      {
        "type": "business_license",
        "department": "Business Services",
        "estimated_cost": "$150",
        "processing_time": "5-7 business days"
      },
      {
        "type": "mobile_vendor_permit",
        "department": "Permits & Licensing",
        "estimated_cost": "$300",
        "processing_time": "10-14 business days"
      },
      {
        "type": "health_permit",
        "department": "Public Safety",
        "estimated_cost": "$75",
        "processing_time": "3-5 business days"
      }
    ],
    "total_estimated_cost": "$525",
    "next_steps": [
      "Apply for business license first",
      "Schedule health inspection",
      "Submit mobile vendor application with approved locations"
    ]
  }
}
```

## 🏗️ Building Your First Agent

### Step 1: Create MCP Server Structure

```python
# File: my-custom-mcp-server/main.py
"""
Custom Transportation MCP Server
Handles public transit, ride-share, and traffic issues
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent

# Import shared models
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared-lib'))

from civicmind_common.models.base_models import CivicRequest, CivicResponse
from civicmind_common.utils.logging import setup_logging
from civicmind_common.clients.openai_client import OpenAIClient

class TransportationMCPServer:
    def __init__(self):
        self.server = Server("transportation-mcp-server")
        self.openai_client = OpenAIClient()
        self.logger = setup_logging("transportation-mcp")
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources():
            """List available transportation resources"""
            return [
                Resource(
                    uri="transportation://routes",
                    name="Public Transit Routes",
                    description="Real-time bus and train route information",
                    mimeType="application/json"
                ),
                Resource(
                    uri="transportation://schedules",
                    name="Transit Schedules", 
                    description="Schedule information for all public transit",
                    mimeType="application/json"
                ),
                Resource(
                    uri="transportation://traffic",
                    name="Traffic Conditions",
                    description="Current traffic conditions and road closures",
                    mimeType="application/json"
                ),
                Resource(
                    uri="transportation://parking",
                    name="Public Parking",
                    description="Available public parking spaces and rates",
                    mimeType="application/json"
                )
            ]
        
        @self.server.list_tools()
        async def handle_list_tools():
            """List available transportation tools"""
            return [
                Tool(
                    name="find_route",
                    description="Find optimal public transit route between two locations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "from": {"type": "string", "description": "Origin location"},
                            "to": {"type": "string", "description": "Destination location"},
                            "departure_time": {"type": "string", "description": "Preferred departure time (optional)"},
                            "transport_mode": {
                                "type": "string", 
                                "enum": ["bus", "train", "mixed", "walking"],
                                "description": "Preferred transportation mode"
                            },
                            "accessibility": {"type": "boolean", "description": "Require wheelchair accessibility"}
                        },
                        "required": ["from", "to"]
                    }
                ),
                Tool(
                    name="report_transit_issue",
                    description="Report issues with public transportation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "route": {"type": "string", "description": "Route identifier (e.g., 'Bus 42', 'Blue Line')"},
                            "issue_type": {
                                "type": "string",
                                "enum": ["delay", "breakdown", "overcrowding", "safety", "cleanliness"],
                                "description": "Type of issue to report"
                            },
                            "description": {"type": "string", "description": "Detailed description of the issue"},
                            "location": {"type": "string", "description": "Location where issue occurred"},
                            "severity": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "description": "Severity level of the issue"
                            }
                        },
                        "required": ["route", "issue_type", "description"]
                    }
                ),
                Tool(
                    name="check_service_alerts",
                    description="Check current service alerts and disruptions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "route": {"type": "string", "description": "Specific route to check (optional)"},
                            "area": {"type": "string", "description": "Geographic area to check (optional)"}
                        }
                    }
                ),
                Tool(
                    name="find_parking",
                    description="Find available parking near a location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "Location to find parking near"},
                            "duration": {"type": "string", "description": "Expected parking duration"},
                            "max_cost": {"type": "number", "description": "Maximum acceptable cost per hour"}
                        },
                        "required": ["location"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            """Handle tool execution"""
            self.logger.info(f"Tool called: {name} with args: {arguments}")
            
            try:
                if name == "find_route":
                    return await self._find_route(arguments)
                elif name == "report_transit_issue":
                    return await self._report_transit_issue(arguments)
                elif name == "check_service_alerts":
                    return await self._check_service_alerts(arguments)
                elif name == "find_parking":
                    return await self._find_parking(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
                    
            except Exception as e:
                self.logger.error(f"Error executing tool {name}: {str(e)}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _find_route(self, args: Dict[str, Any]) -> List[TextContent]:
        """Find optimal transit route"""
        from_loc = args.get("from")
        to_loc = args.get("to")
        departure_time = args.get("departure_time", "now")
        transport_mode = args.get("transport_mode", "mixed")
        accessibility = args.get("accessibility", False)
        
        # Simulate route finding logic
        route_options = [
            {
                "route_id": "RT-001",
                "description": f"Bus 42 from {from_loc} to Metro Station, then Blue Line to {to_loc}",
                "total_time": "35 minutes",
                "cost": "$3.50",
                "transfers": 1,
                "walking_distance": "0.3 miles",
                "accessibility": True,
                "steps": [
                    f"Walk to bus stop near {from_loc} (2 min)",
                    "Take Bus 42 towards Downtown (15 min)",
                    "Transfer to Blue Line at Metro Station (3 min)",
                    f"Take Blue Line to {to_loc} (12 min)",
                    f"Walk to destination (3 min)"
                ]
            },
            {
                "route_id": "RT-002", 
                "description": f"Direct Bus 15 from {from_loc} to {to_loc}",
                "total_time": "45 minutes",
                "cost": "$2.25",
                "transfers": 0,
                "walking_distance": "0.2 miles",
                "accessibility": True,
                "steps": [
                    f"Walk to bus stop near {from_loc} (3 min)",
                    f"Take Bus 15 direct to {to_loc} (38 min)",
                    f"Walk to destination (4 min)"
                ]
            }
        ]
        
        # Filter by accessibility if required
        if accessibility:
            route_options = [r for r in route_options if r["accessibility"]]
        
        response = {
            "query": f"Route from {from_loc} to {to_loc}",
            "departure_time": departure_time,
            "route_options": route_options,
            "recommendation": route_options[0]["route_id"] if route_options else None,
            "timestamp": datetime.now().isoformat()
        }
        
        return [TextContent(type="text", text=str(response))]
    
    async def _report_transit_issue(self, args: Dict[str, Any]) -> List[TextContent]:
        """Report a transit issue"""
        route = args.get("route")
        issue_type = args.get("issue_type")
        description = args.get("description")
        location = args.get("location", "Unknown")
        severity = args.get("severity", "medium")
        
        # Generate issue ticket
        ticket_id = f"TR-{datetime.now().strftime('%Y%m%d')}-{hash(description) % 10000:04d}"
        
        response = {
            "ticket_id": ticket_id,
            "route": route,
            "issue_type": issue_type,
            "description": description,
            "location": location,
            "severity": severity,
            "status": "submitted",
            "estimated_resolution": "24-48 hours" if severity in ["low", "medium"] else "2-4 hours",
            "contact_info": "Transit Authority: 311 or transit-support@city.ai",
            "timestamp": datetime.now().isoformat()
        }
        
        return [TextContent(type="text", text=str(response))]
    
    async def _check_service_alerts(self, args: Dict[str, Any]) -> List[TextContent]:
        """Check current service alerts"""
        route = args.get("route")
        area = args.get("area")
        
        # Simulate service alerts
        alerts = [
            {
                "alert_id": "SA-001",
                "route": "Blue Line",
                "type": "delay",
                "severity": "medium",
                "description": "15-minute delays due to signal maintenance",
                "affected_stations": ["Downtown", "City Center", "University"],
                "start_time": "2024-01-15T08:00:00",
                "estimated_end": "2024-01-15T17:00:00"
            },
            {
                "alert_id": "SA-002", 
                "route": "Bus 42",
                "type": "detour",
                "severity": "low",
                "description": "Temporary route change due to street construction",
                "affected_stops": ["Main St & 5th", "Downtown Plaza"],
                "start_time": "2024-01-15T06:00:00",
                "estimated_end": "2024-01-20T18:00:00"
            }
        ]
        
        # Filter alerts if specific route/area requested
        if route:
            alerts = [a for a in alerts if route.lower() in a["route"].lower()]
        if area:
            alerts = [a for a in alerts if area.lower() in str(a.get("affected_stations", [])).lower()]
        
        response = {
            "active_alerts": len(alerts),
            "alerts": alerts,
            "last_updated": datetime.now().isoformat()
        }
        
        return [TextContent(type="text", text=str(response))]
    
    async def _find_parking(self, args: Dict[str, Any]) -> List[TextContent]:
        """Find available parking"""
        location = args.get("location")
        duration = args.get("duration", "2 hours")
        max_cost = args.get("max_cost", 10.0)
        
        # Simulate parking options
        parking_options = [
            {
                "garage_id": "PG-001",
                "name": "City Center Garage",
                "address": f"Near {location}",
                "distance": "0.1 miles",
                "hourly_rate": 3.50,
                "available_spaces": 45,
                "features": ["covered", "ev_charging", "accessible"],
                "hours": "24/7"
            },
            {
                "garage_id": "PG-002",
                "name": "Main Street Parking",
                "address": f"2 blocks from {location}",
                "distance": "0.3 miles",
                "hourly_rate": 2.00,
                "available_spaces": 12,
                "features": ["street_level", "accessible"],
                "hours": "6 AM - 10 PM"
            }
        ]
        
        # Filter by max cost
        parking_options = [p for p in parking_options if p["hourly_rate"] <= max_cost]
        
        response = {
            "location": location,
            "duration": duration,
            "parking_options": parking_options,
            "recommendation": parking_options[0]["garage_id"] if parking_options else None,
            "timestamp": datetime.now().isoformat()
        }
        
        return [TextContent(type="text", text=str(response))]

# Server startup
async def main():
    """Start the Transportation MCP Server"""
    logging.basicConfig(level=logging.INFO)
    
    server = TransportationMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Create Service Integration

```python
# File: transportation-api-service/main.py
"""
Transportation API Service
Provides REST API endpoints for transportation data
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared-lib'))

from civicmind_common.models.base_models import CivicRequest, CivicResponse
from civicmind_common.utils.health_checks import HealthChecker

app = FastAPI(
    title="Transportation API Service",
    description="Transportation civic services API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP client configuration
MCP_SERVER_URL = "http://localhost:9308"  # Transportation MCP server

@app.post("/analyze")
async def analyze_transportation_issue(request: CivicRequest):
    """Analyze transportation-related civic issues"""
    try:
        # Forward request to MCP server
        async with httpx.AsyncClient() as client:
            mcp_response = await client.post(
                f"{MCP_SERVER_URL}/analyze",
                json=request.dict()
            )
            mcp_data = mcp_response.json()
        
        # Process and return response
        return CivicResponse(
            service="transportation-service",
            confidence=0.90,
            response=mcp_data,
            timestamp=request.timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/routes")
async def get_routes(origin: str, destination: str):
    """Get transit routes between two locations"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MCP_SERVER_URL}/tools/call",
                json={
                    "tool": "find_route",
                    "arguments": {
                        "from": origin,
                        "to": destination
                    }
                }
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/issues")
async def report_issue(
    route: str,
    issue_type: str,
    description: str,
    location: str = None,
    severity: str = "medium"
):
    """Report a transportation issue"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MCP_SERVER_URL}/tools/call",
                json={
                    "tool": "report_transit_issue",
                    "arguments": {
                        "route": route,
                        "issue_type": issue_type,
                        "description": description,
                        "location": location,
                        "severity": severity
                    }
                }
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "transportation-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
```

### Step 3: Register with API Gateway

```python
# File: Update API Gateway configuration
# Add to independent-services/civicmind-api-gateway/main.py

CIVIC_SERVICES.update({
    "transportation": {
        "url": "http://localhost:8009",
        "mcp_server": "http://localhost:9308", 
        "name": "transportation-service",
        "version": "1.0.0",
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze",
        "keywords": ["transport", "transit", "bus", "train", "traffic", "parking", "route"]
    }
})
```

### Step 4: Create Docker Configuration

```dockerfile
# File: transportation-mcp-server/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy shared library
COPY ../shared-lib /app/shared-lib
RUN cd /app/shared-lib && pip install -e .

# Copy MCP server code
COPY . .

EXPOSE 9308

CMD ["python", "main.py"]
```

```yaml
# File: docker-compose.transportation.yml
version: '3.8'

services:
  transportation-api:
    build: ./transportation-api-service
    ports:
      - "8009:8009"
    environment:
      - MCP_SERVER_URL=http://transportation-mcp:9308
    depends_on:
      - transportation-mcp
    networks:
      - civicmind-network

  transportation-mcp:
    build: ./transportation-mcp-server
    ports:
      - "9308:9308"
    environment:
      - LOG_LEVEL=INFO
    networks:
      - civicmind-network

networks:
  civicmind-network:
    external: true
```

## 🔌 Service Integration Examples

### Direct API Service Usage

```bash
# Test transportation service directly
curl -X POST "http://localhost:8009/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Bus 42 is always late on my commute",
    "citizen_id": "67890",
    "timestamp": "2024-01-15T09:30:00Z"
  }'
```

### MCP Server Direct Communication

```python
import asyncio
import json
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test MCP server directly"""
    
    # Connect to MCP server
    async with stdio_client() as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools])
            
            # Call find_route tool
            result = await session.call_tool(
                "find_route",
                {
                    "from": "Downtown Library",
                    "to": "University Campus",
                    "transport_mode": "mixed",
                    "accessibility": True
                }
            )
            
            print("Route result:", result)

# Run the test
asyncio.run(test_mcp_server())
```

## 🌐 API Gateway Usage

### Complex Multi-Service Requests

```python
# Example: Business requiring multiple approvals
business_request = {
    "query": "I want to open a restaurant with outdoor seating and live music",
    "business_type": "restaurant",
    "features": ["outdoor_seating", "live_entertainment"],
    "location": "Downtown Arts District",
    "citizen_id": "12345"
}

# The API Gateway will coordinate between:
# 1. Business Service - business license
# 2. Permits Service - food service permit, outdoor seating permit
# 3. Noise Service - entertainment permit for live music
# 4. Safety Service - fire safety inspection
```

### Request Routing Logic

```python
# API Gateway routing algorithm
def route_request(query: str, context: dict) -> List[str]:
    """
    Intelligent routing based on query analysis
    """
    keywords = extract_keywords(query.lower())
    services = []
    
    routing_rules = {
        'parking': ['park', 'vehicle', 'ticket', 'violation', 'meter'],
        'permits': ['permit', 'license', 'application', 'building'],
        'noise': ['noise', 'loud', 'music', 'complaint', 'disturbance'],
        'utilities': ['power', 'water', 'outage', 'billing', 'utility'],
        'housing': ['housing', 'rent', 'landlord', 'property', 'apartment'],
        'business': ['business', 'commercial', 'shop', 'store', 'entrepreneur'],
        'safety': ['safety', 'fire', 'emergency', 'hazard', 'inspection'],
        'environmental': ['environment', 'pollution', 'recycling', 'green']
    }
    
    for service, service_keywords in routing_rules.items():
        if any(keyword in keywords for keyword in service_keywords):
            services.append(service)
    
    return services
```

## 🎭 Orchestrator Workflows

### Complex Workflow Example

```python
# File: orchestrator workflow example
class BusinessLicenseWorkflow:
    """
    Multi-step workflow for business license applications
    """
    
    async def execute(self, request: BusinessLicenseRequest):
        workflow_id = f"BL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        steps = [
            self.validate_business_info,
            self.check_zoning_compliance,
            self.verify_tax_requirements,
            self.schedule_inspections,
            self.process_permits,
            self.generate_license
        ]
        
        results = {}
        for step in steps:
            try:
                result = await step(request, results)
                results[step.__name__] = result
                
                # Log step completion
                await self.log_workflow_step(workflow_id, step.__name__, "completed")
                
            except Exception as e:
                await self.log_workflow_step(workflow_id, step.__name__, "failed", str(e))
                return WorkflowResult(
                    workflow_id=workflow_id,
                    status="failed",
                    failed_step=step.__name__,
                    error=str(e)
                )
        
        return WorkflowResult(
            workflow_id=workflow_id,
            status="completed",
            results=results
        )
    
    async def validate_business_info(self, request: BusinessLicenseRequest, context: dict):
        """Step 1: Validate business information"""
        # Call business service for validation
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://business-service:8006/validate",
                json=request.business_info
            )
            return response.json()
    
    async def check_zoning_compliance(self, request: BusinessLicenseRequest, context: dict):
        """Step 2: Check zoning compliance"""
        # Call permits service for zoning check
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://permits-service:8002/zoning/check",
                json={
                    "address": request.business_address,
                    "business_type": request.business_type
                }
            )
            return response.json()
```

## 🤖 MCP Agent Development

### Advanced Agent Features

```python
class AdvancedCivicAgent:
    """
    Advanced MCP agent with context awareness and learning capabilities
    """
    
    def __init__(self):
        self.context_memory = {}
        self.interaction_history = []
        
    async def handle_complex_query(self, query: str, context: dict):
        """
        Handle complex multi-domain queries
        """
        # Parse query for multiple intents
        intents = await self.extract_intents(query)
        
        # Coordinate with multiple services
        responses = []
        for intent in intents:
            service_response = await self.call_service(intent.service, intent.query)
            responses.append(service_response)
        
        # Synthesize comprehensive response
        return await self.synthesize_response(responses, context)
    
    async def extract_intents(self, query: str) -> List[Intent]:
        """Use AI to extract multiple intents from complex queries"""
        prompt = f"""
        Analyze this civic query and extract all distinct intents:
        Query: "{query}"
        
        Identify which civic services are needed and what specific information 
        or actions are required for each.
        """
        
        response = await self.openai_client.complete(prompt)
        return self.parse_intents(response)
    
    async def learn_from_interaction(self, query: str, response: str, feedback: dict):
        """
        Learn from citizen interactions to improve future responses
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "feedback": feedback,
            "satisfaction_score": feedback.get("rating", 0)
        }
        
        self.interaction_history.append(interaction)
        
        # Update context memory for similar queries
        keywords = self.extract_keywords(query)
        for keyword in keywords:
            if keyword not in self.context_memory:
                self.context_memory[keyword] = []
            self.context_memory[keyword].append(interaction)
```

## 🚢 Deployment Examples

### Kubernetes Deployment

```yaml
# File: k8s/transportation-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: transportation-api
  labels:
    app: transportation-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: transportation-api
  template:
    metadata:
      labels:
        app: transportation-api
    spec:
      containers:
      - name: transportation-api
        image: civicmind/transportation-api:1.0.0
        ports:
        - containerPort: 8009
        env:
        - name: MCP_SERVER_URL
          value: "http://transportation-mcp:9308"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8009
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8009
          initialDelaySeconds: 30
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: transportation-api
spec:
  selector:
    app: transportation-api
  ports:
  - protocol: TCP
    port: 8009
    targetPort: 8009
  type: ClusterIP

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: transportation-mcp
  labels:
    app: transportation-mcp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: transportation-mcp
  template:
    metadata:
      labels:
        app: transportation-mcp
    spec:
      containers:
      - name: transportation-mcp
        image: civicmind/transportation-mcp:1.0.0
        ports:
        - containerPort: 9308
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-credentials
              key: openai-key
```

### Production Docker Compose

```yaml
# File: docker-compose.prod.yml
version: '3.8'

services:
  # Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - api-gateway
    restart: unless-stopped

  # API Gateway (Multiple instances)
  api-gateway:
    build: ./independent-services/civicmind-api-gateway
    deploy:
      replicas: 3
    environment:
      - ENV=production
      - LOG_LEVEL=INFO
      - RATE_LIMIT=1000
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  # Orchestrator Service
  orchestrator:
    build: ./independent-services/civicmind-orchestrator-service
    deploy:
      replicas: 2
    environment:
      - ENV=production
      - DATABASE_URL=postgresql://user:pass@postgres:5432/civicmind
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # All Civic Services
  parking-service:
    build: ./independent-services/civicmind-parking-service
    deploy:
      replicas: 2
    environment:
      - MCP_SERVER_URL=http://parking-mcp:9300
    restart: unless-stopped

  parking-mcp:
    build: ./independent-services/civicmind-parking-mcp-server
    deploy:
      replicas: 2
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped

  # Infrastructure
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: civicmind
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Monitoring
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  grafana_data:

networks:
  default:
    name: civicmind-network
```

## 🔧 Advanced Integration Patterns

### Event-Driven Architecture

```python
# Event-driven communication between services
class CivicEventBus:
    """
    Event bus for inter-service communication
    """
    
    def __init__(self):
        self.subscribers = {}
        
    def subscribe(self, event_type: str, handler: callable):
        """Subscribe to events"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    async def publish(self, event: CivicEvent):
        """Publish event to subscribers"""
        if event.type in self.subscribers:
            for handler in self.subscribers[event.type]:
                await handler(event)

# Example usage
event_bus = CivicEventBus()

# Subscribe to permit approval events
@event_bus.subscribe("permit_approved")
async def handle_permit_approval(event: CivicEvent):
    """Notify other services when permit is approved"""
    if event.data.get("permit_type") == "business":
        # Trigger business license workflow
        await business_service.initiate_license_process(event.data)

# Publish event from permits service
await event_bus.publish(CivicEvent(
    type="permit_approved",
    source="permits-service",
    data={"permit_id": "BP-2024-001", "permit_type": "business"}
))
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    """
    Circuit breaker for service resilience
    """
    
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        """Call function with circuit breaker protection"""
        
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            
            raise e

# Usage
parking_service_breaker = CircuitBreaker()

async def call_parking_service(request):
    return await parking_service_breaker.call(
        httpx.post,
        "http://parking-service:8001/analyze",
        json=request
    )
```

### Saga Pattern for Distributed Transactions

```python
class BusinessLicenseSaga:
    """
    Saga pattern for business license workflow
    """
    
    def __init__(self):
        self.steps = [
            ("create_application", "cancel_application"),
            ("validate_zoning", "revert_zoning"),
            ("process_payment", "refund_payment"),
            ("schedule_inspection", "cancel_inspection"),
            ("issue_license", "revoke_license")
        ]
    
    async def execute(self, application_data):
        """Execute saga with compensation"""
        completed_steps = []
        
        try:
            for step, compensation in self.steps:
                result = await self.execute_step(step, application_data)
                completed_steps.append((step, compensation, result))
                
                # Update application with step result
                application_data.update(result)
            
            return {"status": "success", "license_id": application_data["license_id"]}
            
        except Exception as e:
            # Compensate completed steps in reverse order
            await self.compensate(completed_steps)
            return {"status": "failed", "error": str(e)}
    
    async def compensate(self, completed_steps):
        """Compensate completed steps"""
        for step, compensation, result in reversed(completed_steps):
            try:
                await self.execute_step(compensation, result)
            except Exception as e:
                # Log compensation failure
                logger.error(f"Compensation failed for {step}: {e}")
```

---

These examples demonstrate the power and flexibility of CivicMind AI's microservices architecture. Each service is independent, scalable, and can be developed and deployed separately while still working together to provide comprehensive civic services.
    "location": "Folsom, CA",
    "priority": "high"
  }'
```

The API Gateway will:
1. Analyze the request content
2. Route to **Parking Agent (Port 9300)**
3. Return comprehensive response with routing information

---

## 🚗 **Parking Issues (Port 9300)**

### **Example 1: Neighbor Blocking Driveway**

**Via API Gateway (Recommended):**
```bash
curl -X POST http://localhost:8300/api/v1/issues/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My neighbor parks blocking my driveway every night, making it impossible for me to leave for work in the morning",
    "location": "Folsom, CA",
    "priority": "high",
    "citizen_info": {
      "name": "John Smith",
      "address": "123 Oak Street",
      "phone": "(916) 555-0123"
    }
  }'
```

**Direct Agent Access:**
```bash
curl -X POST http://localhost:9300/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Neighbor blocking driveway nightly",
    "location": "Folsom, CA",
    "context": {"priority": "high"}
  }'
```

**CivicMind Response:**
```json
{
  "issue_id": "parking-001-20250728",
  "classification": {
    "type": "parking",
    "subtype": "driveway_blocking",
    "confidence": 0.95,
    "agent": "parking"
  },
  "community_first_approach": true,
  "recommendations": [
    "Start with a friendly, non-confrontational conversation with your neighbor",
    "Check if there are legitimate parking challenges in your neighborhood",
    "Verify your driveway boundaries and local parking regulations",
    "Document the issue with photos showing dates and times"
  ],
  "step_by_step_resolution": [
    {
      "step": 1,
      "action": "Community Conversation",
      "description": "Approach your neighbor politely to discuss the issue",
      "script": "Hi [Neighbor's name], I hope you're doing well. I wanted to talk about the parking situation. I've noticed your car has been parked in a way that blocks my driveway, and it's making it difficult for me to get to work on time. Is there anything we can work out together?"
    },
    {
      "step": 2,
      "action": "Seek Understanding",
      "description": "Try to understand if there are underlying issues",
      "considerations": ["Limited street parking", "Multiple cars per household", "Recent changes in neighborhood"]
    },
    {
      "step": 3,
      "action": "Collaborative Solution",
      "description": "Work together to find a mutually beneficial solution",
      "options": ["Alternate parking schedules", "Identify additional parking spaces", "Share information about permit parking"]
    }
  ],
  "escalation_path": [
    {
      "level": "Community",
      "actions": ["HOA mediation", "Neighborhood association", "Community meeting"]
    },
    {
      "level": "Municipal",
      "actions": ["Parking enforcement contact", "City parking regulations", "Formal complaint process"]
    }
  ],
  "contacts": [
    {
      "name": "Folsom Parking Enforcement",
      "phone": "(916) 355-7200",
      "email": "parking@folsom.ca.us",
      "hours": "Monday-Friday 8:00 AM - 5:00 PM"
    },
    {
      "name": "Folsom Code Enforcement",
      "phone": "(916) 355-7285",
      "email": "codeenforcement@folsom.ca.us"
    }
  ],
  "documents": [
    {
      "title": "Folsom Municipal Code - Parking Regulations",
      "url": "https://folsom.ca.us/parking-regulations",
      "relevance": "Legal requirements for driveway access"
    },
    {
      "title": "Neighbor Communication Template",
      "type": "generated",
      "content": "A friendly letter template for discussing parking issues"
    }
  ],
  "cultural_considerations": {
    "note": "Consider cultural differences in communication styles and conflict resolution preferences",
    "suggestions": ["Use respectful, non-confrontational language", "Consider involving community elders if appropriate", "Respect different approaches to problem-solving"]
  }
}
```

### **Example 2: Residential Parking Permit**

**Scenario**: Need information about getting a residential parking permit.

```python
import requests

response = requests.post("http://localhost:8000/api/v1/agents/parking/analyze", json={
    "description": "Our street has become overcrowded with commuter parking. How can we get residential parking permits?",
    "location": "Sacramento, CA",
    "issue_type": "permits"
})

print(response.json())
```

**Response includes:**
- Eligibility requirements for residential parking permits
- Application process and required documents
- Cost and renewal information
- Community petition process
- Timeline for implementation

result = response.json()
print(f"Issue Type: {result['issue_type']}")
print(f"Next Steps: {result['next_steps']}")
```

### Example 2: Urgent Safety Issue

```python
response = requests.post("http://localhost:8000/api/v1/issues/analyze", json={
    "description": "Street light is out at a busy intersection causing safety concerns",
    "location": "Sacramento, CA",
    "priority": "urgent",
    "citizen_info": {
        "contact_preference": "phone",
        "follow_up": True
    }
})
```

## Parking Issues

### Example 3: Neighbor Parking Dispute

```python
# Use the parking specialist agent
response = requests.post("http://localhost:8000/api/v1/agents/parking/analyze", json={
    "description": "My neighbor consistently parks in front of my driveway, blocking my access. This happens 3-4 times per week, usually overnight.",
    "location": "Folsom, CA",
    "citizen_info": {
        "previous_attempts": "Talked to neighbor once, no change",
        "urgency": "affects daily routine"
    }
})

result = response.json()
# Expected response includes community-first approaches
print("Community Resolution Steps:")
for step in result['next_steps']:
    print(f"- {step}")
```

### Example 4: Commercial Vehicle Parking

```python
response = requests.post("http://localhost:8000/api/v1/agents/parking/analyze", json={
    "description": "Large commercial trucks park on residential street overnight, violating neighborhood parking rules",
    "location": "Davis, CA"
})
```

## Noise Complaints

### Example 5: Dog Barking Issue

```python
response = requests.post("http://localhost:8000/api/v1/agents/noise/analyze", json={
    "description": "Neighbor's dog barks loudly every night from 11 PM to 2 AM, affecting my family's sleep",
    "location": "Roseville, CA",
    "citizen_info": {
        "duration": "ongoing for 3 weeks",
        "impact": "affecting children's sleep and school performance"
    }
})

# Framework prioritizes community resolution
result = response.json()
print("Recommended Approach:", result['community_first'])
```

### Example 6: Construction Noise

```python
response = requests.post("http://localhost:8000/api/v1/agents/noise/analyze", json={
    "description": "Construction work starts at 6 AM on weekends with heavy machinery",
    "location": "Elk Grove, CA"
})
```

## Permit Applications

### Example 7: Home Addition Permit

```python
response = requests.post("http://localhost:8000/api/v1/agents/permits/analyze", json={
    "description": "I want to build a small shed in my backyard, 10x12 feet, for storage",
    "location": "Folsom, CA",
    "citizen_info": {
        "property_type": "single family home",
        "hoa": "yes"
    }
})

# Get specific permit requirements
result = response.json()
print("Required Documents:")
for doc in result['documents']:
    print(f"- {doc}")
```

### Example 8: Event Permit for Cultural Celebration

```python
response = requests.post("http://localhost:8000/api/v1/agents/religious_events/analyze", json={
    "description": "Planning a Diwali celebration in the community park with 100+ attendees, music, and food vendors",
    "location": "Fremont, CA",
    "citizen_info": {
        "event_date": "2024-11-01",
        "expected_attendees": 120,
        "activities": ["music", "food", "cultural performances"]
    }
})
```

## Infrastructure Problems

### Example 9: Water Drainage Issue

```python
response = requests.post("http://localhost:8000/api/v1/agents/infrastructure/analyze", json={
    "description": "Water accumulates in front of my house after every rain, creating a breeding ground for mosquitoes",
    "location": "San Jose, CA",
    "citizen_info": {
        "problem_frequency": "every rainfall",
        "health_concerns": "mosquito breeding"
    }
})
```

### Example 10: Broken Streetlight

```python
response = requests.post("http://localhost:8000/api/v1/agents/infrastructure/analyze", json={
    "description": "Streetlight at the corner of Main St and Oak Ave has been out for 2 weeks",
    "location": "Palo Alto, CA"
})
```

## Home Business Licensing

### Example 11: Home Daycare Setup

```python
response = requests.post("http://localhost:8000/api/v1/agents/home_business/analyze", json={
    "description": "I want to start a small home daycare for 6 children in my residence",
    "location": "Concord, CA",
    "citizen_info": {
        "business_type": "childcare",
        "capacity": 6,
        "home_modifications": "fence installation planned"
    }
})
```

### Example 12: Home-Based Catering

```python
response = requests.post("http://localhost:8000/api/v1/agents/home_business/analyze", json={
    "description": "Starting a small catering business from my home kitchen",
    "location": "Livermore, CA"
})
```

## Religious and Cultural Events

### Example 13: Temple Festival Planning

```python
response = requests.post("http://localhost:8000/api/v1/agents/religious_events/analyze", json={
    "description": "Planning annual Ganesh Chaturthi procession from temple to nearby lake for visarjan ceremony",
    "location": "Fremont, CA",
    "citizen_info": {
        "participants": 200,
        "route_length": "2 miles",
        "requires_road_closure": True,
        "cultural_significance": "important Hindu festival"
    }
})

# Framework understands cultural sensitivity
result = response.json()
print("Cultural Considerations:", result.get('cultural_guidance', []))
```

### Example 14: Community Iftar Event

```python
response = requests.post("http://localhost:8000/api/v1/agents/religious_events/analyze", json={
    "description": "Organizing community Iftar dinner in park during Ramadan for 150 people",
    "location": "San Francisco, CA"
})
```

## Neighbor Disputes

### Example 15: Property Line Dispute

```python
response = requests.post("http://localhost:8000/api/v1/agents/neighbor_dispute/analyze", json={
    "description": "Neighbor built a fence that appears to encroach 2 feet onto my property",
    "location": "Oakland, CA",
    "citizen_info": {
        "survey_available": False,
        "fence_height": "6 feet",
        "communication_attempts": "one informal conversation"
    }
})

# Emphasizes mediation before legal action
result = response.json()
print("Mediation Options:", result.get('mediation_resources', []))
```

### Example 16: Tree Overhang Issue

```python
response = requests.post("http://localhost:8000/api/v1/agents/neighbor_dispute/analyze", json={
    "description": "Neighbor's tree branches hang over my property, dropping leaves and blocking sunlight",
    "location": "Berkeley, CA"
})
```

## Environmental Concerns

### Example 17: Illegal Dumping

```python
response = requests.post("http://localhost:8000/api/v1/agents/environmental/analyze", json={
    "description": "Someone is repeatedly dumping construction debris in the empty lot next to my house",
    "location": "Stockton, CA",
    "citizen_info": {
        "frequency": "weekly",
        "debris_type": "construction materials",
        "safety_concern": "attracts rodents"
    }
})
```

### Example 18: Air Quality Complaint

```python
response = requests.post("http://localhost:8000/api/v1/agents/environmental/analyze", json={
    "description": "Strong chemical smell coming from nearby business, causing headaches and respiratory issues",
    "location": "Richmond, CA"
})
```

## Custom Agent Usage

### Example 19: Creating Location-Specific Agent

```python
from civicmind.agents.base_agent import BaseCivicAgent

class FolsomSpecificAgent(BaseCivicAgent):
    def get_system_prompt(self):
        return """
        You are a specialized agent for Folsom, CA civic issues.
        
        Key Folsom contacts:
        - City Hall: (916) 355-7400
        - Code Enforcement: (916) 355-7424
        - Public Works: (916) 355-7420
        
        Folsom-specific considerations:
        - Historic district preservation rules
        - Folsom Lake proximity regulations
        - American River Parkway guidelines
        """
    
    def analyze_issue(self, issue_description, location, context):
        # Custom Folsom-specific logic
        pass

# Register the custom agent
from civicmind.core.agent_factory import AgentFactory
factory = AgentFactory(openai_api_key="your-key")
factory.register_agent("folsom_specific", FolsomSpecificAgent)
```

### Example 20: Batch Processing Multiple Issues

```python
import asyncio
import aiohttp

async def process_multiple_issues():
    issues = [
        {
            "description": "Pothole on Main Street",
            "location": "Folsom, CA",
            "priority": "medium"
        },
        {
            "description": "Broken streetlight",
            "location": "Folsom, CA", 
            "priority": "high"
        },
        {
            "description": "Noise complaint about neighbor",
            "location": "Folsom, CA",
            "priority": "low"
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for issue in issues:
            task = session.post(
                "http://localhost:8000/api/v1/issues/analyze",
                json=issue
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        for i, response in enumerate(responses):
            result = await response.json()
            print(f"Issue {i+1}: {result['issue_type']}")

# Run batch processing
asyncio.run(process_multiple_issues())
```

## Integration Examples

### Example 21: Webhook Integration

```python
from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/webhook/seeclickfix")
async def handle_seeclickfix_webhook(request: Request):
    """Handle incoming issues from SeeClickFix"""
    data = await request.json()
    
    # Transform SeeClickFix data to CivicMind format
    civic_issue = {
        "description": data.get("description"),
        "location": f"{data.get('lat')}, {data.get('lng')}",
        "priority": "medium",
        "citizen_info": {
            "source": "seeclickfix",
            "external_id": data.get("id")
        }
    }
    
    # Process with CivicMind
    response = requests.post(
        "http://localhost:8000/api/v1/issues/analyze",
        json=civic_issue
    )
    
    return {"status": "processed", "civicmind_response": response.json()}
```

### Example 22: Mobile App Integration

```javascript
// React Native example
import React, { useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';

const CivicIssueForm = () => {
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [result, setResult] = useState(null);

  const submitIssue = async () => {
    try {
      const response = await fetch('http://your-server:8000/api/v1/issues/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description,
          location,
          priority: 'medium'
        }),
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error submitting issue:', error);
    }
  };

  return (
    <View>
      <TextInput
        placeholder="Describe your civic issue..."
        value={description}
        onChangeText={setDescription}
        multiline
      />
      <TextInput
        placeholder="Location"
        value={location}
        onChangeText={setLocation}
      />
      <Button title="Get Help" onPress={submitIssue} />
      
      {result && (
        <View>
          <Text>Issue Type: {result.issue_type}</Text>
          <Text>Next Steps:</Text>
          {result.next_steps.map((step, index) => (
            <Text key={index}>• {step}</Text>
          ))}
        </View>
      )}
    </View>
  );
};
```

These examples demonstrate the flexibility and community-first approach of the CivicMind AI framework. The system consistently prioritizes diplomatic resolution and cultural sensitivity while providing clear, actionable guidance for citizens.
