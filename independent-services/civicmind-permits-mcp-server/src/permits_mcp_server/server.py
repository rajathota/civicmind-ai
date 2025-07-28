"""
CivicMind Permits MCP Server
============================

Model Context Protocol server for permit-related civic issues.
This server provides AI agent capabilities for permit applications and approvals.

MCP Port: 3002
Version: 1.0.0
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializeResult
from mcp.types import Resource, Tool, TextContent
from pydantic import BaseModel

from .agents.permits_agent import PermitsMCPAgent
from .tools.permits_tools import (
    analyze_permit_application,
    search_permit_requirements,
    find_permit_office_contacts,
    generate_application_steps
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP Server configuration
MCP_SERVER_NAME = "civicmind-permits-mcp-server"
MCP_SERVER_VERSION = "1.0.0"
MCP_PORT = 3002

# Initialize the MCP server
app = FastMCP(MCP_SERVER_NAME)

# Global agent instance
permits_agent: Optional[PermitsMCPAgent] = None


class PermitApplicationRequest(BaseModel):
    """Request model for permit application analysis"""
    permit_type: str
    description: str
    location: Optional[str] = None
    property_type: Optional[str] = None
    project_scope: Optional[str] = None
    context: Dict[str, Any] = {}


@app.list_resources()
async def list_resources() -> List[Resource]:
    """List available permit resources"""
    return [
        Resource(
            uri="permits://requirements/building",
            name="Building Permit Requirements",
            description="Requirements for building permits and construction",
            mimeType="text/plain"
        ),
        Resource(
            uri="permits://requirements/business",
            name="Business License Requirements", 
            description="Business licensing and operational permits",
            mimeType="text/plain"
        ),
        Resource(
            uri="permits://contacts/office",
            name="Permit Office Contacts",
            description="Local permit office contact information",
            mimeType="application/json"
        ),
        Resource(
            uri="permits://fees/schedule",
            name="Permit Fee Schedule",
            description="Current permit fees and payment information",
            mimeType="text/markdown"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read permit resource content"""
    if uri == "permits://requirements/building":
        return """
# Building Permit Requirements

## Residential Construction
- Structural changes requiring permits
- Electrical work permits
- Plumbing modification permits
- HVAC installation permits

## Commercial Construction
- New construction permits
- Renovation permits
- Change of use permits
- Accessibility compliance

## Required Documents
- Property survey
- Construction plans
- Engineering reports (if applicable)
- Contractor licenses
- Insurance documentation

## Timeline
- Plan review: 2-4 weeks
- Inspection scheduling: 5-7 business days
- Final approval: 1-2 weeks after completion
"""
    elif uri == "permits://requirements/business":
        return """
# Business License Requirements

## Basic Business License
- Business registration
- Tax identification number
- Zoning compliance verification
- Insurance requirements

## Specialized Permits
- Food service permits
- Liquor licenses
- Professional service licenses
- Home business permits

## Application Process
- Submit application with required documents
- Pay applicable fees
- Schedule zoning inspection (if required)
- Await approval notification
"""
    elif uri == "permits://contacts/office":
        return """
{
    "building_permits": {
        "name": "Building Permit Office",
        "phone": "555-PERMITS",
        "email": "building@city.gov",
        "address": "456 City Hall Plaza",
        "hours": "Monday-Friday 8AM-4PM"
    },
    "business_licenses": {
        "name": "Business License Office",
        "phone": "555-BUSINESS",
        "email": "business@city.gov",
        "address": "456 City Hall Plaza",
        "hours": "Monday-Friday 9AM-3PM"
    },
    "zoning_department": {
        "name": "Zoning Department",
        "phone": "555-ZONING",
        "email": "zoning@city.gov",
        "address": "789 Planning Building"
    }
}
"""
    elif uri == "permits://fees/schedule":
        return """
# Permit Fee Schedule

## Building Permits
- Residential addition: $150 + $10 per $1000 construction value
- Deck/patio: $75 base fee
- Electrical work: $50 base fee
- Plumbing work: $50 base fee

## Business Licenses
- Basic business license: $100 annual fee
- Home business license: $50 annual fee
- Food service permit: $200 annual fee
- Liquor license: $500 annual fee

## Additional Fees
- Plan review fee: $75
- Inspection fees: $50 per inspection
- Re-inspection fee: $75
- Expedited review: 50% surcharge
"""
    else:
        raise ValueError(f"Unknown resource: {uri}")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available permit tools"""
    return [
        Tool(
            name="analyze_permit_application",
            description="Analyze permit application requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "permit_type": {"type": "string"},
                    "description": {"type": "string"},
                    "location": {"type": "string"},
                    "project_scope": {"type": "string"}
                },
                "required": ["permit_type", "description"]
            }
        ),
        Tool(
            name="search_permit_requirements",
            description="Search for specific permit requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "permit_type": {"type": "string"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="find_permit_contacts",
            description="Find relevant permit office contacts",
            inputSchema={
                "type": "object",
                "properties": {
                    "permit_type": {"type": "string"},
                    "location": {"type": "string"}
                },
                "required": ["permit_type"]
            }
        ),
        Tool(
            name="generate_application_steps",
            description="Generate step-by-step application process",
            inputSchema={
                "type": "object",
                "properties": {
                    "permit_type": {"type": "string"},
                    "project_description": {"type": "string"}
                },
                "required": ["permit_type"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute permit tools"""
    global permits_agent
    
    if not permits_agent:
        raise RuntimeError("Permits agent not initialized")
    
    try:
        if name == "analyze_permit_application":
            result = await analyze_permit_application(
                permits_agent,
                permit_type=arguments["permit_type"],
                description=arguments["description"],
                location=arguments.get("location"),
                project_scope=arguments.get("project_scope")
            )
        elif name == "search_permit_requirements":
            result = await search_permit_requirements(
                query=arguments["query"],
                permit_type=arguments.get("permit_type")
            )
        elif name == "find_permit_contacts":
            result = await find_permit_office_contacts(
                permit_type=arguments["permit_type"],
                location=arguments.get("location")
            )
        elif name == "generate_application_steps":
            result = await generate_application_steps(
                permit_type=arguments["permit_type"],
                project_description=arguments.get("project_description", "")
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
    global permits_agent
    
    logger.info(f"Initializing {MCP_SERVER_NAME} v{MCP_SERVER_VERSION}")
    
    try:
        # Initialize the permits agent
        permits_agent = PermitsMCPAgent()
        await permits_agent.initialize()
        
        logger.info("Permits MCP server initialized successfully")
        
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
