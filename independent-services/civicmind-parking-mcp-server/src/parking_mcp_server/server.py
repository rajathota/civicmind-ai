"""
CivicMind Parking MCP Server
============================

Model Context Protocol server for parking-related civic issues.
This server provides AI agent capabilities via the MCP protocol.

MCP Port: 3001
Version: 1.0.0
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializeResult
from mcp.types import (
    Resource, 
    Tool, 
    TextContent, 
    ImageContent, 
    EmbeddedResource
)
from pydantic import BaseModel

from .agents.parking_agent import ParkingMCPAgent
from .tools.parking_tools import (
    analyze_parking_issue,
    search_parking_regulations,
    find_parking_enforcement_contacts,
    generate_resolution_steps
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP Server configuration
MCP_SERVER_NAME = "civicmind-parking-mcp-server"
MCP_SERVER_VERSION = "1.0.0"
MCP_PORT = 3001

# Initialize the MCP server
app = FastMCP(MCP_SERVER_NAME)

# Global agent instance
parking_agent: Optional[ParkingMCPAgent] = None


class ParkingIssueRequest(BaseModel):
    """Request model for parking issue analysis"""
    description: str
    location: Optional[str] = None
    issue_type: Optional[str] = None
    priority: Optional[str] = "medium"
    context: Dict[str, Any] = {}


@app.list_resources()
async def list_resources() -> List[Resource]:
    """List available parking resources"""
    return [
        Resource(
            uri="parking://regulations/general",
            name="General Parking Regulations",
            description="Standard parking rules and regulations",
            mimeType="text/plain"
        ),
        Resource(
            uri="parking://enforcement/contacts",
            name="Parking Enforcement Contacts",
            description="Local parking enforcement contact information",
            mimeType="application/json"
        ),
        Resource(
            uri="parking://permits/info",
            name="Parking Permit Information",
            description="Information about parking permits and applications",
            mimeType="text/markdown"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read parking resource content"""
    if uri == "parking://regulations/general":
        return """
# General Parking Regulations

## Street Parking
- No parking within 15 feet of a fire hydrant
- No parking in front of driveways
- No parking during posted street cleaning times
- Maximum 72 hours in same spot

## Permit Parking
- Residential permits required in designated zones
- Visitor permits available for temporary parking
- Commercial permits for business vehicles

## Violations
- Blocking driveways: $75 fine
- Expired meters: $35 fine
- No permit in permit zone: $50 fine
- Fire hydrant blocking: $100 fine
"""
    elif uri == "parking://enforcement/contacts":
        return """
{
    "parking_enforcement": {
        "phone": "555-PARKING",
        "email": "parking@city.gov",
        "hours": "Monday-Friday 8AM-5PM"
    },
    "parking_violations": {
        "phone": "555-TICKETS",
        "email": "violations@city.gov", 
        "online": "https://city.gov/parking-tickets"
    },
    "permit_office": {
        "phone": "555-PERMITS",
        "email": "permits@city.gov",
        "address": "123 City Hall Plaza"
    }
}
"""
    elif uri == "parking://permits/info":
        return """
# Parking Permit Information

## Residential Permits
- Annual fee: $25
- Required documents: Proof of residence, vehicle registration
- Processing time: 5-7 business days

## Visitor Permits
- Daily rate: $5
- Maximum 14 days per month
- Available online or at City Hall

## Commercial Permits
- Monthly fee: $100
- Business license required
- Special zones available for delivery vehicles
"""
    else:
        raise ValueError(f"Unknown resource: {uri}")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available parking tools"""
    return [
        Tool(
            name="analyze_parking_issue",
            description="Analyze a parking issue and provide recommendations",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "location": {"type": "string"},
                    "issue_type": {"type": "string"},
                    "priority": {"type": "string"}
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="search_parking_regulations",
            description="Search for relevant parking regulations",
            inputSchema={
                "type": "object", 
                "properties": {
                    "query": {"type": "string"},
                    "location": {"type": "string"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="find_enforcement_contacts",
            description="Find relevant parking enforcement contacts",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_type": {"type": "string"},
                    "location": {"type": "string"}
                },
                "required": ["issue_type"]
            }
        ),
        Tool(
            name="generate_resolution_steps",
            description="Generate step-by-step resolution process",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_description": {"type": "string"},
                    "classification": {"type": "object"}
                },
                "required": ["issue_description"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute parking tools"""
    global parking_agent
    
    if not parking_agent:
        raise RuntimeError("Parking agent not initialized")
    
    try:
        if name == "analyze_parking_issue":
            result = await analyze_parking_issue(
                parking_agent,
                description=arguments["description"],
                location=arguments.get("location"),
                issue_type=arguments.get("issue_type"),
                priority=arguments.get("priority", "medium")
            )
        elif name == "search_parking_regulations":
            result = await search_parking_regulations(
                query=arguments["query"],
                location=arguments.get("location")
            )
        elif name == "find_enforcement_contacts":
            result = await find_parking_enforcement_contacts(
                issue_type=arguments["issue_type"],
                location=arguments.get("location")
            )
        elif name == "generate_resolution_steps":
            result = await generate_resolution_steps(
                issue_description=arguments["issue_description"],
                classification=arguments.get("classification", {})
            )
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        return [TextContent(type="text", text=str(result))]
    
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.on_initialize()
async def initialize() -> InitializeResult:
    """Initialize the MCP server"""
    global parking_agent
    
    logger.info(f"Initializing {MCP_SERVER_NAME} v{MCP_SERVER_VERSION}")
    
    try:
        # Initialize the parking agent
        parking_agent = ParkingMCPAgent()
        await parking_agent.initialize()
        
        logger.info("Parking MCP server initialized successfully")
        
        return InitializeResult(
            protocolVersion="2024-11-05",
            capabilities={
                "resources": {},
                "tools": {},
                "prompts": {}
            },
            serverInfo={
                "name": MCP_SERVER_NAME,
                "version": MCP_SERVER_VERSION
            }
        )
    
    except Exception as e:
        logger.error(f"Failed to initialize MCP server: {e}")
        raise


async def main():
    """Main entry point for the MCP server"""
    logger.info(f"Starting {MCP_SERVER_NAME} on port {MCP_PORT}")
    await app.run(port=MCP_PORT)


if __name__ == "__main__":
    asyncio.run(main())
