"""
CivicMind Noise MCP Server
Noise complaints, ordinances, and sound regulations
"""

import asyncio
import logging
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("noise_mcp_server")

class NoiseAgent:
    """Agent for handling noise service requests"""
    
    async def get_resource_content(self, uri: str) -> str:
        """Get content for MCP resources"""
        resource_type = uri.split("//")[-1]
        
        resource_data = {
            "noise_ordinances": "City noise ordinances and regulations",
            "complaint_database": "Noise complaint records and tracking",
            "violation_records": "Noise violation history and enforcement"
        }
        
        return resource_data.get(resource_type, "Resource not found")

class NoiseTools:
    """Tools for noise civic services"""
    
    async def execute_tool(self, name: str, arguments: dict) -> dict:
        """Execute a noise tool"""
        if name == "file_complaint":
            return {"result": f"Filed noise complaint: {arguments.get('query', '')}"}
        elif name == "check_violations":
            return {"result": f"Checked violations for: {arguments.get('query', '')}"}
        elif name == "get_noise_limits":
            return {"result": f"Noise limits info: {arguments.get('query', '')}"}
        else:
            return {"error": f"Unknown tool: {name}"}

class NoiseMCPServer:
    """MCP Server for noise civic services"""
    
    def __init__(self):
        self.server = Server("noise-mcp-server")
        self.agent = NoiseAgent()
        self.tools_handler = NoiseTools()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP protocol handlers"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """List available noise resources"""
            return [
                Resource(
                    uri="noise://noise_ordinances",
                    name="Noise Ordinances",
                    description="City noise ordinances and regulations",
                    mimeType="application/json",
                ),
                Resource(
                    uri="noise://complaint_database",
                    name="Complaint Database",
                    description="Noise complaint records and tracking",
                    mimeType="application/json",
                ),
                Resource(
                    uri="noise://violation_records",
                    name="Violation Records",
                    description="Noise violation history and enforcement",
                    mimeType="application/json",
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read noise resource content"""
            return await self.agent.get_resource_content(uri)
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available noise tools"""
            return [
                Tool(
                    name="file_complaint",
                    description="File a noise complaint",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Complaint details"}
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="check_violations",
                    description="Check noise violations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Address or location"}
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_noise_limits",
                    description="Get noise limit information",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Zone or time details"}
                        },
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None = None) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Execute noise tool"""
            if arguments is None:
                arguments = {}
            
            result = await self.tools_handler.execute_tool(name, arguments)
            return [TextContent(type="text", text=str(result))]

async def main():
    """Main server entry point"""
    server_instance = NoiseMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="noise-mcp-server",
                server_version="1.0.0",
                capabilities={
                    "resources": {},
                    "tools": {},
                }
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
