"""
CivicMind Utilities MCP Server
Water, electricity, gas, and utility service management
"""

import asyncio
import logging
from typing import Sequence
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("utilities_mcp_server")


class UtilitiesAgent:
    """Agent for handling utilities service requests"""
    
    async def get_resource_content(self, uri: str) -> str:
        """Get content for MCP resources"""
        resource_type = uri.split("//")[-1]
        
        resource_data = {
            "service_areas": "Utility service coverage areas and zones",
            "outage_reports": "Current and historical utility outages",
            "billing_info": "Utility billing information and rates"
        }
        
        return resource_data.get(resource_type, "Resource not found")


class UtilitiesTools:
    """Tools for utilities civic services"""
    
    async def execute_tool(self, name: str, arguments: dict) -> dict:
        """Execute a utilities tool"""
        query = arguments.get('query', '')
        
        if name == "report_outage":
            return {"result": f"Reported outage: {query}"}
        elif name == "schedule_service":
            return {"result": f"Scheduled service: {query}"}
        elif name == "check_availability":
            return {"result": f"Checked availability: {query}"}
        else:
            return {"error": f"Unknown tool: {name}"}


class UtilitiesMCPServer:
    """MCP Server for utilities civic services"""
    
    def __init__(self):
        self.server = Server("utilities-mcp-server")
        self.agent = UtilitiesAgent()
        self.tools_handler = UtilitiesTools()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP protocol handlers"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """List available utilities resources"""
            return [
                Resource(
                    uri="utilities://service_areas",
                    name="Service Areas",
                    description="Utility service coverage areas",
                    mimeType="application/json",
                ),
                Resource(
                    uri="utilities://outage_reports",
                    name="Outage Reports",
                    description="Current and historical outages",
                    mimeType="application/json",
                ),
                Resource(
                    uri="utilities://billing_info",
                    name="Billing Information",
                    description="Utility billing and rates",
                    mimeType="application/json",
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read utilities resource content"""
            return await self.agent.get_resource_content(uri)
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available utilities tools"""
            return [
                Tool(
                    name="report_outage",
                    description="Report a utility outage",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string", 
                                "description": "Outage details"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="schedule_service",
                    description="Schedule utility service",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string", 
                                "description": "Service request"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="check_availability",
                    description="Check service availability",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string", 
                                "description": "Location details"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, 
            arguments: dict | None = None
        ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Execute utilities tool"""
            if arguments is None:
                arguments = {}
            
            result = await self.tools_handler.execute_tool(name, arguments)
            return [TextContent(type="text", text=str(result))]


async def main():
    """Main server entry point"""
    server_instance = UtilitiesMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="utilities-mcp-server",
                server_version="1.0.0",
                capabilities={
                    "resources": {},
                    "tools": {},
                }
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
