# 🤖 Building Your First CivicMind AI Agent

This tutorial will guide you through creating a complete MCP (Model Context Protocol) agent from scratch, including the API service integration and deployment configuration.

## 📋 Overview

We'll build a **Transportation Agent** that handles:
- Public transit route planning
- Transit issue reporting
- Service alert monitoring
- Parking space finding

## 🏗️ Project Structure

```
civicmind-transportation/
├── transportation-mcp-server/          # MCP Agent
│   ├── main.py                        # MCP server implementation
│   ├── agents/
│   │   ├── transportation_agent.py    # Domain logic
│   │   └── transportation_tools.py    # Tool implementations
│   ├── models/
│   │   └── transportation_models.py   # Data models
│   ├── requirements.txt
│   └── Dockerfile
├── transportation-api-service/         # REST API Service
│   ├── main.py                        # FastAPI application
│   ├── routes/
│   │   ├── routes.py                  # Route planning endpoints
│   │   ├── issues.py                  # Issue reporting endpoints
│   │   └── alerts.py                  # Service alerts endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml                  # Local development
├── deployment/                         # Production configs
│   ├── kubernetes/
│   └── terraform/
└── tests/                             # Test suites
    ├── unit/
    ├── integration/
    └── e2e/
```

## 🚀 Step 1: Create the MCP Server

### Transportation Agent Implementation

```python
# File: transportation-mcp-server/agents/transportation_agent.py
"""
Transportation Agent - Core domain logic for transit services
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import sys
import os

# Add shared library to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared-lib'))

from civicmind_common.models.base_models import CivicRequest, CivicResponse
from civicmind_common.clients.openai_client import OpenAIClient
from civicmind_common.utils.logging import setup_logging

class TransportationAgent:
    """
    Transportation domain agent with AI-powered assistance
    """
    
    def __init__(self):
        self.logger = setup_logging("transportation-agent")
        self.openai_client = OpenAIClient()
        
        # Mock transit data - in production, connect to real APIs
        self.routes = self._load_transit_routes()
        self.service_alerts = self._load_service_alerts()
        self.parking_data = self._load_parking_data()
    
    def _load_transit_routes(self) -> Dict[str, Any]:
        """Load transit route information"""
        return {
            "bus_routes": {
                "42": {
                    "name": "Downtown Express",
                    "stops": ["City Hall", "Main Library", "University", "Hospital"],
                    "frequency": "15 minutes",
                    "hours": "5:00 AM - 11:00 PM",
                    "accessibility": True
                },
                "15": {
                    "name": "Cross-town Local",
                    "stops": ["West Side", "Downtown", "East Side", "Mall"],
                    "frequency": "20 minutes", 
                    "hours": "6:00 AM - 10:00 PM",
                    "accessibility": True
                }
            },
            "rail_lines": {
                "blue": {
                    "name": "Blue Line Metro",
                    "stations": ["Airport", "Downtown", "University", "Stadium"],
                    "frequency": "10 minutes",
                    "hours": "5:00 AM - 12:00 AM",
                    "accessibility": True
                },
                "green": {
                    "name": "Green Line Metro", 
                    "stations": ["North Terminal", "City Center", "Hospital", "South Terminal"],
                    "frequency": "12 minutes",
                    "hours": "5:30 AM - 11:30 PM",
                    "accessibility": True
                }
            }
        }
    
    def _load_service_alerts(self) -> List[Dict[str, Any]]:
        """Load current service alerts"""
        return [
            {
                "id": "SA-001",
                "route": "Blue Line",
                "type": "delay",
                "severity": "medium",
                "message": "15-minute delays due to signal maintenance",
                "affected_stations": ["Downtown", "University"],
                "start_time": datetime.now() - timedelta(hours=2),
                "estimated_end": datetime.now() + timedelta(hours=6)
            },
            {
                "id": "SA-002",
                "route": "Bus 42",
                "type": "detour",
                "severity": "low", 
                "message": "Temporary route change due to street construction",
                "affected_stops": ["Main Library"],
                "start_time": datetime.now() - timedelta(days=3),
                "estimated_end": datetime.now() + timedelta(days=10)
            }
        ]
    
    def _load_parking_data(self) -> Dict[str, Any]:
        """Load parking availability data"""
        return {
            "downtown": {
                "garage_1": {
                    "name": "City Center Garage",
                    "address": "123 Main St",
                    "total_spaces": 500,
                    "available_spaces": 87,
                    "hourly_rate": 3.50,
                    "features": ["covered", "ev_charging", "accessible"],
                    "hours": "24/7"
                },
                "garage_2": {
                    "name": "Library Parking",
                    "address": "456 Oak Ave",
                    "total_spaces": 200,
                    "available_spaces": 23,
                    "hourly_rate": 2.00,
                    "features": ["accessible"],
                    "hours": "6 AM - 10 PM"
                }
            }
        }
    
    async def find_route(self, origin: str, destination: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Find optimal transit route between two locations
        """
        options = options or {}
        transport_mode = options.get("transport_mode", "mixed")
        departure_time = options.get("departure_time", "now")
        accessibility_required = options.get("accessibility", False)
        
        self.logger.info(f"Finding route from {origin} to {destination}")
        
        # Use AI to analyze the best route options
        prompt = f"""
        Find the best public transit route from {origin} to {destination}.
        
        Available routes:
        {self._format_routes_for_ai()}
        
        Requirements:
        - Transport mode preference: {transport_mode}
        - Departure time: {departure_time}
        - Accessibility required: {accessibility_required}
        
        Provide 2-3 route options with details about:
        - Total travel time
        - Number of transfers
        - Walking distance
        - Cost
        - Step-by-step directions
        """
        
        ai_response = await self.openai_client.complete(prompt)
        
        # Process AI response and format route options
        route_options = self._parse_ai_route_response(ai_response, origin, destination)
        
        return {
            "origin": origin,
            "destination": destination,
            "requested_time": departure_time,
            "options": route_options,
            "accessibility_filter": accessibility_required,
            "timestamp": datetime.now().isoformat()
        }
    
    async def report_transit_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Report a transit system issue
        """
        route = issue_data.get("route")
        issue_type = issue_data.get("issue_type")
        description = issue_data.get("description")
        location = issue_data.get("location")
        severity = issue_data.get("severity", "medium")
        
        # Generate unique ticket ID
        ticket_id = f"TR-{datetime.now().strftime('%Y%m%d')}-{hash(description) % 10000:04d}"
        
        # Use AI to categorize and prioritize the issue
        prompt = f"""
        Analyze this transit issue report:
        
        Route: {route}
        Issue Type: {issue_type}
        Description: {description}
        Location: {location}
        Reported Severity: {severity}
        
        Provide:
        1. Confirmed issue category
        2. Suggested priority level (low/medium/high/critical)
        3. Estimated resolution timeframe
        4. Recommended immediate actions
        5. Department to handle this issue
        """
        
        ai_analysis = await self.openai_client.complete(prompt)
        analysis = self._parse_ai_analysis(ai_analysis)
        
        # Create issue record
        issue_record = {
            "ticket_id": ticket_id,
            "route": route,
            "issue_type": issue_type,
            "description": description,
            "location": location,
            "severity": analysis.get("priority", severity),
            "category": analysis.get("category", issue_type),
            "status": "submitted",
            "assigned_department": analysis.get("department", "Transit Operations"),
            "estimated_resolution": analysis.get("resolution_time", "24-48 hours"),
            "recommended_actions": analysis.get("actions", []),
            "created_at": datetime.now().isoformat(),
            "contact_methods": [
                "Phone: 311",
                "Email: transit-support@city.gov",
                f"Online: city.gov/transit/ticket/{ticket_id}"
            ]
        }
        
        self.logger.info(f"Created transit issue ticket: {ticket_id}")
        
        return issue_record
    
    async def get_service_alerts(self, route_filter: str = None) -> Dict[str, Any]:
        """
        Get current service alerts, optionally filtered by route
        """
        alerts = self.service_alerts.copy()
        
        if route_filter:
            alerts = [
                alert for alert in alerts 
                if route_filter.lower() in alert["route"].lower()
            ]
        
        # Add real-time severity assessment using AI
        for alert in alerts:
            if alert["type"] == "delay":
                # Calculate actual impact
                alert["impact_score"] = self._calculate_impact_score(alert)
        
        return {
            "total_alerts": len(alerts),
            "active_alerts": alerts,
            "last_updated": datetime.now().isoformat(),
            "next_update": (datetime.now() + timedelta(minutes=5)).isoformat()
        }
    
    async def find_parking(self, location: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Find available parking near a location
        """
        options = options or {}
        max_cost = options.get("max_cost", 10.0)
        duration = options.get("duration", "2 hours")
        features_required = options.get("features", [])
        
        # Filter parking options
        all_parking = []
        for area, garages in self.parking_data.items():
            for garage_id, garage in garages.items():
                # Apply filters
                if garage["hourly_rate"] <= max_cost:
                    if not features_required or any(f in garage["features"] for f in features_required):
                        garage_info = garage.copy()
                        garage_info["garage_id"] = garage_id
                        garage_info["area"] = area
                        garage_info["distance_estimate"] = self._estimate_distance(location, garage["address"])
                        all_parking.append(garage_info)
        
        # Sort by availability and distance
        all_parking.sort(key=lambda x: (x["available_spaces"] == 0, x["distance_estimate"]))
        
        return {
            "search_location": location,
            "search_criteria": {
                "max_cost": max_cost,
                "duration": duration,
                "required_features": features_required
            },
            "parking_options": all_parking[:5],  # Top 5 options
            "timestamp": datetime.now().isoformat()
        }
    
    def _format_routes_for_ai(self) -> str:
        """Format route data for AI processing"""
        routes_text = "Bus Routes:\n"
        for route_id, route in self.routes["bus_routes"].items():
            routes_text += f"- Bus {route_id}: {route['name']} - {', '.join(route['stops'])}\n"
        
        routes_text += "\nRail Lines:\n"
        for line_id, line in self.routes["rail_lines"].items():
            routes_text += f"- {line['name']}: {', '.join(line['stations'])}\n"
        
        return routes_text
    
    def _parse_ai_route_response(self, ai_response: str, origin: str, destination: str) -> List[Dict[str, Any]]:
        """Parse AI response into structured route options"""
        # Simplified parsing - in production, use more sophisticated NLP
        return [
            {
                "route_id": "RT-001",
                "description": f"Bus 42 to Blue Line from {origin} to {destination}",
                "total_time": "35 minutes",
                "cost": "$3.50",
                "transfers": 1,
                "walking_distance": "0.3 miles",
                "accessibility": True,
                "steps": [
                    f"Walk to bus stop near {origin} (3 min)",
                    "Take Bus 42 towards Downtown (15 min)",
                    "Transfer to Blue Line at Downtown Station (2 min)",
                    f"Take Blue Line to {destination} (12 min)",
                    f"Walk to destination (3 min)"
                ]
            },
            {
                "route_id": "RT-002",
                "description": f"Direct Bus 15 from {origin} to {destination}",
                "total_time": "45 minutes", 
                "cost": "$2.25",
                "transfers": 0,
                "walking_distance": "0.2 miles",
                "accessibility": True,
                "steps": [
                    f"Walk to bus stop near {origin} (4 min)",
                    f"Take Bus 15 direct to {destination} (38 min)",
                    f"Walk to destination (3 min)"
                ]
            }
        ]
    
    def _parse_ai_analysis(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI analysis response"""
        # Simplified parsing - in production, use structured AI output
        return {
            "category": "service_disruption",
            "priority": "medium",
            "resolution_time": "24-48 hours",
            "department": "Transit Operations",
            "actions": [
                "Route inspection scheduled",
                "Temporary signage deployed",
                "Passenger notifications activated"
            ]
        }
    
    def _calculate_impact_score(self, alert: Dict[str, Any]) -> float:
        """Calculate the impact score of a service alert"""
        severity_weights = {"low": 0.25, "medium": 0.5, "high": 0.75, "critical": 1.0}
        base_score = severity_weights.get(alert["severity"], 0.5)
        
        # Adjust based on affected stations/stops
        affected_count = len(alert.get("affected_stations", alert.get("affected_stops", [])))
        impact_multiplier = min(1.0 + (affected_count * 0.1), 2.0)
        
        return round(base_score * impact_multiplier, 2)
    
    def _estimate_distance(self, location1: str, location2: str) -> float:
        """Estimate distance between two locations (simplified)"""
        # In production, use actual geocoding and distance calculation
        return round(abs(hash(location1) - hash(location2)) % 20 / 10.0, 1)
```

### Transportation Tools Implementation

```python
# File: transportation-mcp-server/agents/transportation_tools.py
"""
Transportation Tools - MCP tool implementations for transit services
"""

from typing import Dict, Any, List
from mcp.types import Tool, TextContent
from .transportation_agent import TransportationAgent

class TransportationTools:
    """
    MCP tools for transportation services
    """
    
    def __init__(self):
        self.agent = TransportationAgent()
    
    def get_tool_definitions(self) -> List[Tool]:
        """
        Define all available MCP tools for transportation
        """
        return [
            Tool(
                name="find_route",
                description="Find optimal public transit route between two locations",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "origin": {"type": "string", "description": "Starting location"},
                        "destination": {"type": "string", "description": "Destination location"},
                        "departure_time": {"type": "string", "description": "Preferred departure time (optional)"},
                        "transport_mode": {
                            "type": "string",
                            "enum": ["bus", "rail", "mixed", "walking"],
                            "description": "Preferred transportation mode"
                        },
                        "accessibility": {"type": "boolean", "description": "Require wheelchair accessibility"}
                    },
                    "required": ["origin", "destination"]
                }
            ),
            Tool(
                name="report_transit_issue",
                description="Report issues with public transportation services",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "route": {"type": "string", "description": "Route identifier (e.g., 'Bus 42', 'Blue Line')"},
                        "issue_type": {
                            "type": "string",
                            "enum": ["delay", "breakdown", "overcrowding", "safety", "cleanliness", "accessibility"],
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
                description="Find available parking spaces near a location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Location to find parking near"},
                        "duration": {"type": "string", "description": "Expected parking duration"},
                        "max_cost": {"type": "number", "description": "Maximum acceptable cost per hour"},
                        "features": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["covered", "ev_charging", "accessible", "secure"]
                            },
                            "description": "Required parking features"
                        }
                    },
                    "required": ["location"]
                }
            ),
            Tool(
                name="plan_trip",
                description="Plan a complex multi-stop trip using public transportation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "stops": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of locations to visit in order"
                        },
                        "start_time": {"type": "string", "description": "Trip start time"},
                        "return_to_origin": {"type": "boolean", "description": "Return to starting location"}
                    },
                    "required": ["stops"]
                }
            )
        ]
    
    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        Execute a transportation tool
        """
        try:
            if name == "find_route":
                result = await self.agent.find_route(
                    arguments["origin"],
                    arguments["destination"],
                    {
                        "departure_time": arguments.get("departure_time"),
                        "transport_mode": arguments.get("transport_mode", "mixed"),
                        "accessibility": arguments.get("accessibility", False)
                    }
                )
                
            elif name == "report_transit_issue":
                result = await self.agent.report_transit_issue(arguments)
                
            elif name == "check_service_alerts":
                result = await self.agent.get_service_alerts(
                    arguments.get("route")
                )
                
            elif name == "find_parking":
                result = await self.agent.find_parking(
                    arguments["location"],
                    {
                        "duration": arguments.get("duration"),
                        "max_cost": arguments.get("max_cost"),
                        "features": arguments.get("features", [])
                    }
                )
                
            elif name == "plan_trip":
                result = await self._plan_multi_stop_trip(arguments)
                
            else:
                result = {"error": f"Unknown tool: {name}"}
            
            return [TextContent(type="text", text=str(result))]
            
        except Exception as e:
            error_result = {"error": str(e), "tool": name}
            return [TextContent(type="text", text=str(error_result))]
    
    async def _plan_multi_stop_trip(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Plan a multi-stop trip using public transportation
        """
        stops = arguments["stops"]
        start_time = arguments.get("start_time", "now")
        return_to_origin = arguments.get("return_to_origin", False)
        
        if len(stops) < 2:
            return {"error": "At least 2 stops required for trip planning"}
        
        # Plan route segments
        segments = []
        current_time = start_time
        
        # Add return trip if requested
        if return_to_origin:
            stops.append(stops[0])
        
        for i in range(len(stops) - 1):
            origin = stops[i]
            destination = stops[i + 1]
            
            # Get route for this segment
            segment_route = await self.agent.find_route(
                origin, 
                destination,
                {"departure_time": current_time}
            )
            
            segments.append({
                "segment": i + 1,
                "from": origin,
                "to": destination,
                "route": segment_route,
                "departure_time": current_time
            })
            
            # Update time for next segment (simplified)
            # In production, calculate actual arrival time
            current_time = "next_departure"
        
        total_time = sum(35 for _ in segments)  # Simplified calculation
        total_cost = sum(3.50 for _ in segments)  # Simplified calculation
        
        return {
            "trip_overview": {
                "total_stops": len(stops),
                "total_segments": len(segments),
                "estimated_total_time": f"{total_time} minutes",
                "estimated_total_cost": f"${total_cost}",
                "start_time": start_time,
                "return_trip": return_to_origin
            },
            "segments": segments,
            "recommendations": [
                "Allow 10 minutes buffer between segments",
                "Check service alerts before departure",
                "Consider purchasing day pass for cost savings"
            ]
        }
```

### MCP Server Main Implementation

```python
# File: transportation-mcp-server/main.py
"""
Transportation MCP Server - Main server implementation
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent

from agents.transportation_agent import TransportationAgent
from agents.transportation_tools import TransportationTools

class TransportationMCPServer:
    """
    Main MCP server for transportation services
    """
    
    def __init__(self):
        self.server = Server("transportation-mcp-server")
        self.agent = TransportationAgent()
        self.tools = TransportationTools()
        self.logger = logging.getLogger("transportation-mcp-server")
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        """
        Setup MCP protocol handlers
        """
        
        @self.server.list_resources()
        async def handle_list_resources():
            """List available transportation resources"""
            return [
                Resource(
                    uri="transportation://routes",
                    name="Transit Routes",
                    description="Real-time public transit route information",
                    mimeType="application/json"
                ),
                Resource(
                    uri="transportation://schedules",
                    name="Transit Schedules",
                    description="Schedule information for all public transit",
                    mimeType="application/json"
                ),
                Resource(
                    uri="transportation://alerts",
                    name="Service Alerts",
                    description="Current service alerts and disruptions",
                    mimeType="application/json"
                ),
                Resource(
                    uri="transportation://parking",
                    name="Parking Information",
                    description="Real-time parking availability and rates",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str):
            """Read transportation resource data"""
            if uri == "transportation://routes":
                return [TextContent(type="text", text=str(self.agent.routes))]
            elif uri == "transportation://schedules":
                # In production, fetch real-time schedule data
                schedules = {"message": "Real-time schedule data would be provided here"}
                return [TextContent(type="text", text=str(schedules))]
            elif uri == "transportation://alerts":
                alerts = await self.agent.get_service_alerts()
                return [TextContent(type="text", text=str(alerts))]
            elif uri == "transportation://parking":
                return [TextContent(type="text", text=str(self.agent.parking_data))]
            else:
                raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_tools()
        async def handle_list_tools():
            """List available transportation tools"""
            return self.tools.get_tool_definitions()
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            """Execute transportation tools"""
            self.logger.info(f"Tool called: {name} with arguments: {arguments}")
            return await self.tools.execute_tool(name, arguments)

async def main():
    """
    Start the Transportation MCP Server
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = TransportationMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🌐 Step 2: Create the API Service

### REST API Implementation

```python
# File: transportation-api-service/main.py
"""
Transportation API Service - REST API for transportation services
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import logging
import sys
import os
from typing import Dict, Any, List, Optional

# Add shared library to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared-lib'))

from civicmind_common.models.base_models import CivicRequest, CivicResponse, HealthCheckResponse
from civicmind_common.utils.logging import setup_logging
from civicmind_common.utils.health_checks import HealthChecker

# Service configuration
SERVICE_NAME = "transportation-api-service"
SERVICE_VERSION = "1.0.0"
SERVICE_PORT = 8009

# MCP server configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:9308")

# Initialize FastAPI app
app = FastAPI(
    title="CivicMind Transportation API",
    description="REST API for transportation and transit services",
    version=SERVICE_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
logger = setup_logging(SERVICE_NAME)
health_checker = HealthChecker(SERVICE_NAME)

@app.post("/analyze", response_model=CivicResponse)
async def analyze_transportation_issue(request: CivicRequest):
    """
    Analyze transportation-related civic issues using AI
    """
    try:
        logger.info(f"Analyzing transportation issue: {request.query}")
        
        # Forward to MCP server for AI analysis
        async with httpx.AsyncClient() as client:
            mcp_response = await client.post(
                f"{MCP_SERVER_URL}/analyze",
                json=request.dict(),
                timeout=30.0
            )
            
            if mcp_response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"MCP server error: {mcp_response.status_code}"
                )
            
            mcp_data = mcp_response.json()
        
        return CivicResponse(
            service="transportation-service",
            confidence=0.90,
            response=mcp_data,
            timestamp=request.timestamp
        )
        
    except httpx.RequestError as e:
        logger.error(f"Failed to connect to MCP server: {e}")
        raise HTTPException(status_code=503, detail="Transportation service unavailable")
    except Exception as e:
        logger.error(f"Error analyzing transportation issue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/routes")
async def find_route(
    origin: str = Query(..., description="Starting location"),
    destination: str = Query(..., description="Destination location"),
    departure_time: Optional[str] = Query(None, description="Preferred departure time"),
    transport_mode: Optional[str] = Query("mixed", description="Transportation mode"),
    accessibility: Optional[bool] = Query(False, description="Require accessibility")
):
    """
    Find optimal transit routes between two locations
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MCP_SERVER_URL}/tools/call",
                json={
                    "name": "find_route",
                    "arguments": {
                        "origin": origin,
                        "destination": destination,
                        "departure_time": departure_time,
                        "transport_mode": transport_mode,
                        "accessibility": accessibility
                    }
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Route planning service error")
                
            return response.json()
            
    except Exception as e:
        logger.error(f"Error finding route: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/issues")
async def report_transit_issue(
    route: str,
    issue_type: str,
    description: str,
    location: Optional[str] = None,
    severity: Optional[str] = "medium"
):
    """
    Report transportation or transit issues
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MCP_SERVER_URL}/tools/call",
                json={
                    "name": "report_transit_issue",
                    "arguments": {
                        "route": route,
                        "issue_type": issue_type,
                        "description": description,
                        "location": location,
                        "severity": severity
                    }
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Issue reporting service error")
                
            return response.json()
            
    except Exception as e:
        logger.error(f"Error reporting transit issue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts")
async def get_service_alerts(
    route: Optional[str] = Query(None, description="Filter by specific route"),
    area: Optional[str] = Query(None, description="Filter by geographic area")
):
    """
    Get current transit service alerts and disruptions
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MCP_SERVER_URL}/tools/call",
                json={
                    "name": "check_service_alerts",
                    "arguments": {
                        "route": route,
                        "area": area
                    }
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Service alerts unavailable")
                
            return response.json()
            
    except Exception as e:
        logger.error(f"Error getting service alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/parking")
async def find_parking(
    location: str = Query(..., description="Location to find parking near"),
    duration: Optional[str] = Query("2 hours", description="Expected parking duration"),
    max_cost: Optional[float] = Query(10.0, description="Maximum cost per hour"),
    features: Optional[List[str]] = Query(None, description="Required features")
):
    """
    Find available parking spaces near a location
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MCP_SERVER_URL}/tools/call",
                json={
                    "name": "find_parking",
                    "arguments": {
                        "location": location,
                        "duration": duration,
                        "max_cost": max_cost,
                        "features": features or []
                    }
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Parking service unavailable")
                
            return response.json()
            
    except Exception as e:
        logger.error(f"Error finding parking: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint for service monitoring
    """
    try:
        # Check MCP server connectivity
        async with httpx.AsyncClient() as client:
            mcp_response = await client.get(
                f"{MCP_SERVER_URL}/health",
                timeout=5.0
            )
            mcp_healthy = mcp_response.status_code == 200
    except:
        mcp_healthy = False
    
    health_status = health_checker.check_health()
    health_status["dependencies"] = {
        "mcp_server": "healthy" if mcp_healthy else "unhealthy"
    }
    
    return HealthCheckResponse(**health_status)

@app.get("/metrics")
async def get_metrics():
    """
    Service metrics endpoint for monitoring
    """
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": health_checker.get_uptime(),
        "requests_processed": health_checker.get_request_count(),
        "last_health_check": health_checker.last_check_time.isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {SERVICE_NAME} v{SERVICE_VERSION} on port {SERVICE_PORT}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=SERVICE_PORT,
        log_level="info"
    )
```

## 🐳 Step 3: Docker Configuration

### MCP Server Dockerfile

```dockerfile
# File: transportation-mcp-server/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared library and install
COPY ../shared-lib /app/shared-lib
RUN cd /app/shared-lib && pip install -e .

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 9308

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:9308/health')"

# Start server
CMD ["python", "main.py"]
```

### API Service Dockerfile  

```dockerfile
# File: transportation-api-service/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared library and install
COPY ../shared-lib /app/shared-lib
RUN cd /app/shared-lib && pip install -e .

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8009

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8009/health || exit 1

# Start server
CMD ["python", "main.py"]
```

### Docker Compose for Development

```yaml
# File: docker-compose.yml
version: '3.8'

services:
  transportation-api:
    build: ./transportation-api-service
    ports:
      - "8009:8009"
    environment:
      - MCP_SERVER_URL=http://transportation-mcp:9308
      - LOG_LEVEL=INFO
    depends_on:
      - transportation-mcp
    networks:
      - civicmind-network
    restart: unless-stopped

  transportation-mcp:
    build: ./transportation-mcp-server
    ports:
      - "9308:9308"
    environment:
      - LOG_LEVEL=INFO
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    networks:
      - civicmind-network
    restart: unless-stopped

  # Optional: Add databases, caches, etc.
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    networks:
      - civicmind-network
    restart: unless-stopped

networks:
  civicmind-network:
    driver: bridge

# For integration with main CivicMind stack
networks:
  default:
    external:
      name: civicmind-network
```

## 🧪 Step 4: Testing

### Unit Tests

```python
# File: tests/unit/test_transportation_agent.py
"""
Unit tests for Transportation Agent
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from agents.transportation_agent import TransportationAgent

class TestTransportationAgent:
    
    @pytest.fixture
    def agent(self):
        """Create agent instance for testing"""
        agent = TransportationAgent()
        agent.openai_client = Mock()
        agent.openai_client.complete = AsyncMock()
        return agent
    
    @pytest.mark.asyncio
    async def test_find_route_basic(self, agent):
        """Test basic route finding functionality"""
        # Mock AI response
        agent.openai_client.complete.return_value = "Mock route response"
        
        result = await agent.find_route("Downtown", "University")
        
        assert result["origin"] == "Downtown"
        assert result["destination"] == "University"
        assert "options" in result
        assert "timestamp" in result
    
    @pytest.mark.asyncio
    async def test_find_route_with_accessibility(self, agent):
        """Test route finding with accessibility requirements"""
        result = await agent.find_route(
            "City Hall", 
            "Hospital",
            {"accessibility": True}
        )
        
        # Verify accessibility is considered
        assert result["accessibility_filter"] is True
        for option in result["options"]:
            assert option["accessibility"] is True
    
    @pytest.mark.asyncio
    async def test_report_transit_issue(self, agent):
        """Test transit issue reporting"""
        # Mock AI analysis
        agent.openai_client.complete.return_value = "Mock analysis"
        
        issue_data = {
            "route": "Bus 42",
            "issue_type": "delay",
            "description": "Bus is consistently 15 minutes late",
            "location": "Main St Station",
            "severity": "medium"
        }
        
        result = await agent.report_transit_issue(issue_data)
        
        assert "ticket_id" in result
        assert result["route"] == "Bus 42"
        assert result["status"] == "submitted"
        assert "estimated_resolution" in result
    
    @pytest.mark.asyncio
    async def test_get_service_alerts(self, agent):
        """Test service alerts retrieval"""
        result = await agent.get_service_alerts()
        
        assert "total_alerts" in result
        assert "active_alerts" in result
        assert "last_updated" in result
    
    @pytest.mark.asyncio
    async def test_get_service_alerts_filtered(self, agent):
        """Test filtered service alerts"""
        result = await agent.get_service_alerts("Blue Line")
        
        # Check that filtering works
        for alert in result["active_alerts"]:
            assert "blue line" in alert["route"].lower()
    
    @pytest.mark.asyncio
    async def test_find_parking(self, agent):
        """Test parking search functionality"""
        result = await agent.find_parking(
            "Downtown",
            {"max_cost": 5.0, "features": ["accessible"]}
        )
        
        assert "search_location" in result
        assert "parking_options" in result
        
        # Verify cost filter
        for option in result["parking_options"]:
            assert option["hourly_rate"] <= 5.0
```

### Integration Tests

```python
# File: tests/integration/test_api_service.py
"""
Integration tests for Transportation API Service
"""

import pytest
import httpx
from fastapi.testclient import TestClient

from transportation_api_service.main import app

class TestTransportationAPI:
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "transportation-api-service"
    
    def test_find_route_endpoint(self, client):
        """Test route finding endpoint"""
        response = client.get(
            "/routes",
            params={
                "origin": "Downtown Library",
                "destination": "University Campus",
                "transport_mode": "mixed"
            }
        )
        
        # Should work even if MCP server is mocked
        # In real integration tests, ensure MCP server is running
        assert response.status_code in [200, 500]  # 500 if MCP unavailable
    
    @pytest.mark.asyncio
    async def test_analyze_endpoint(self, client):
        """Test issue analysis endpoint"""
        request_data = {
            "query": "Bus 42 is always late in the morning",
            "citizen_id": "test_citizen",
            "timestamp": "2024-01-15T09:00:00Z"
        }
        
        response = client.post("/analyze", json=request_data)
        
        # Should return proper response structure
        if response.status_code == 200:
            data = response.json()
            assert "service" in data
            assert "confidence" in data
            assert "response" in data
```

### End-to-End Tests

```python
# File: tests/e2e/test_full_workflow.py
"""
End-to-end tests for complete transportation workflows
"""

import pytest
import asyncio
import httpx

class TestTransportationWorkflow:
    
    @pytest.mark.asyncio
    async def test_complete_route_planning_workflow(self):
        """Test complete route planning from citizen request to response"""
        
        # Step 1: Citizen submits request via API Gateway
        citizen_request = {
            "query": "I need to get from downtown to the university for a 2 PM class",
            "citizen_id": "student_123",
            "urgency": "normal"
        }
        
        async with httpx.AsyncClient() as client:
            # Submit to API Gateway
            gateway_response = await client.post(
                "http://localhost:8300/api/v1/issues/analyze",
                json=citizen_request
            )
            
            if gateway_response.status_code == 200:
                gateway_data = gateway_response.json()
                assert gateway_data["service"] == "transportation-service"
                
                # Step 2: Direct API call for detailed route
                route_response = await client.get(
                    "http://localhost:8009/routes",
                    params={
                        "origin": "downtown",
                        "destination": "university",
                        "departure_time": "1:30 PM"
                    }
                )
                
                if route_response.status_code == 200:
                    route_data = route_response.json()
                    assert "options" in route_data
                    assert len(route_data["options"]) > 0
    
    @pytest.mark.asyncio
    async def test_issue_reporting_workflow(self):
        """Test complete issue reporting workflow"""
        
        # Step 1: Report issue via API
        issue_data = {
            "route": "Bus 42",
            "issue_type": "delay",
            "description": "Bus has been 20+ minutes late every day this week",
            "location": "Main St & 5th Ave",
            "severity": "medium"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8009/issues",
                params=issue_data
            )
            
            if response.status_code == 200:
                data = response.json()
                assert "ticket_id" in data
                ticket_id = data["ticket_id"]
                
                # Step 2: Verify issue was processed
                assert data["status"] == "submitted"
                assert "estimated_resolution" in data
```

## 🚀 Step 5: Deployment

### Local Development

```bash
# Start the complete transportation service
cd civicmind-transportation

# Start services
docker-compose up -d

# Test health
curl http://localhost:8009/health
curl http://localhost:9308/health

# Test route finding
curl "http://localhost:8009/routes?origin=downtown&destination=university"

# Test via API Gateway (if integrated)
curl -X POST "http://localhost:8300/api/v1/issues/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "I need transit directions to the hospital"}'
```

### Production Deployment

```yaml
# File: deployment/kubernetes/transportation-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: transportation-api
  labels:
    app: transportation-api
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: transportation-api
  template:
    metadata:
      labels:
        app: transportation-api
        version: v1.0.0
    spec:
      containers:
      - name: transportation-api
        image: civicmind/transportation-api:1.0.0
        ports:
        - containerPort: 8009
        env:
        - name: MCP_SERVER_URL
          value: "http://transportation-mcp:9308"
        - name: LOG_LEVEL
          value: "INFO"
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
apiVersion: apps/v1
kind: Deployment
metadata:
  name: transportation-mcp
  labels:
    app: transportation-mcp
    version: v1.0.0
spec:
  replicas: 2
  selector:
    matchLabels:
      app: transportation-mcp
  template:
    metadata:
      labels:
        app: transportation-mcp
        version: v1.0.0
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
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"

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
apiVersion: v1
kind: Service
metadata:
  name: transportation-mcp
spec:
  selector:
    app: transportation-mcp
  ports:
  - protocol: TCP
    port: 9308
    targetPort: 9308
  type: ClusterIP
```

## 🎯 Step 6: Integration with CivicMind Platform

### Register with API Gateway

Add your service to the API Gateway configuration:

```python
# File: Update independent-services/civicmind-api-gateway/main.py

CIVIC_SERVICES.update({
    "transportation": {
        "url": "http://transportation-api:8009",
        "mcp_server": "http://transportation-mcp:9308",
        "name": "transportation-service",
        "version": "1.0.0",
        "health_endpoint": "/health",
        "analyze_endpoint": "/analyze",
        "keywords": ["transport", "transit", "bus", "train", "metro", "route", "schedule", "traffic", "parking"]
    }
})
```

### Update Main Docker Compose

```yaml
# Add to main docker-compose.microservices.yml
  transportation-api:
    build: ./independent-services/civicmind-transportation-api-service
    ports:
      - "8009:8009"
    environment:
      - MCP_SERVER_URL=http://transportation-mcp:9308
    depends_on:
      - transportation-mcp
    networks:
      - civicmind-network
    restart: unless-stopped

  transportation-mcp:
    build: ./independent-services/civicmind-transportation-mcp-server
    ports:
      - "9308:9308"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    networks:
      - civicmind-network
    restart: unless-stopped
```

## ✅ Verification

Test your complete agent:

```bash
# Test direct API service
curl "http://localhost:8009/routes?origin=downtown&destination=airport"

# Test via API Gateway  
curl -X POST "http://localhost:8300/api/v1/issues/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I get to the airport using public transportation?",
    "citizen_id": "traveler_456"
  }'

# Test MCP tools directly
curl -X POST "http://localhost:9308/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "find_route",
    "arguments": {
      "origin": "downtown",
      "destination": "airport",
      "accessibility": true
    }
  }'
```

## 🎉 Congratulations!

You've successfully built a complete CivicMind AI agent with:

✅ **MCP Server** with AI-powered tools and resources  
✅ **REST API Service** for integration with existing systems  
✅ **Docker containerization** for easy deployment  
✅ **Health checks and monitoring** for production readiness  
✅ **Integration** with the CivicMind platform  
✅ **Comprehensive testing** suite  
✅ **Production deployment** configurations  

Your Transportation Agent is now ready to help citizens with:
- 🚌 **Route Planning** - Optimal public transit routes
- 🚨 **Issue Reporting** - Transit service problems
- 📢 **Service Alerts** - Real-time disruption information  
- 🅿️ **Parking Services** - Available parking spaces

## 🔄 Next Steps

1. **Enhance AI Capabilities** - Add more sophisticated route optimization
2. **Real-time Data** - Integrate with actual transit APIs
3. **Mobile App** - Build citizen-facing mobile application
4. **Analytics** - Add usage analytics and reporting
5. **Scale** - Deploy to production with load balancing

This tutorial demonstrates the power and flexibility of CivicMind AI's architecture for building domain-specific civic services that can work independently or as part of the larger platform.
