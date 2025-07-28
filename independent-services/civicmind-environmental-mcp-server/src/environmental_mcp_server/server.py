"""CivicMind Environmental MCP Server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent


class EnvironmentalMCPServer:
    def __init__(self):
        self.server = Server("environmental-mcp-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            return [
                Resource(
                    uri="environmental://regulations",
                    name="Environmental Regulations",
                    description="Environmental laws and regulations",
                    mimeType="application/json"
                ),
                Resource(
                    uri="environmental://sustainability_programs",
                    name="Sustainability Programs",
                    description="City sustainability initiatives",
                    mimeType="application/json"
                ),
                Resource(
                    uri="environmental://waste_schedules",
                    name="Waste Schedules",
                    description="Waste collection schedules",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            return f"Environmental resource data for {uri.split('//')[-1]}"
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return [
                Tool(
                    name="check_regulations",
                    description="Check environmental regulations",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="find_programs",
                    description="Find sustainability programs",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="schedule_pickup",
                    description="Schedule waste pickup",
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
            result = f"Environmental tool {name} executed with: {query}"
            return [TextContent(type="text", text=result)]


async def main():
    server = EnvironmentalMCPServer()
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
