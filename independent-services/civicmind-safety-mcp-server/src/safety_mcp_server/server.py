"""CivicMind Safety MCP Server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent


class SafetyMCPServer:
    def __init__(self):
        self.server = Server("safety-mcp-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            return [
                Resource(
                    uri="safety://inspections",
                    name="Safety Inspections",
                    description="Safety inspection schedules and records",
                    mimeType="application/json"
                ),
                Resource(
                    uri="safety://emergency_contacts",
                    name="Emergency Contacts",
                    description="Emergency service contact information",
                    mimeType="application/json"
                ),
                Resource(
                    uri="safety://safety_codes",
                    name="Safety Codes",
                    description="Safety regulations and codes",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            return f"Safety resource data for {uri.split('//')[-1]}"
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return [
                Tool(
                    name="schedule_inspection",
                    description="Schedule a safety inspection",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="report_hazard",
                    description="Report a safety hazard",
                    inputSchema={
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="find_emergency_info",
                    description="Find emergency information",
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
            result = f"Safety tool {name} executed with: {query}"
            return [TextContent(type="text", text=result)]


async def main():
    server = SafetyMCPServer()
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
