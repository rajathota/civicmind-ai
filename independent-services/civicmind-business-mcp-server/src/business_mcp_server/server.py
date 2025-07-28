"""CivicMind Business MCP Server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent


class BusinessMCPServer:
    def __init__(self):
        self.server = Server("business-mcp-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            return [
                Resource(
                    uri="business://registry",
                    name="Business Registry",
                    description="Business registration database",
                    mimeType="application/json"
                ),
                Resource(
                    uri="business://incentives",
                    name="Development Incentives",
                    description="Business development incentive programs",
                    mimeType="application/json"
                ),
                Resource(
                    uri="business://zones",
                    name="Commercial Zones",
                    description="Commercial zoning information",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            return f"Business resource data for {uri.split('//')[-1]}"
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return [
                Tool(
                    name="register_business",
                    description="Register a new business",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="find_incentives",
                    description="Find business incentives",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="check_zoning",
                    description="Check commercial zoning",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict = None):
            if arguments is None:
                arguments = {}
            query = arguments.get('query', '')
            result = f"Business tool {name} executed with: {query}"
            return [TextContent(type="text", text=result)]


async def main():
    server = BusinessMCPServer()
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
