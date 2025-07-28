"""CivicMind Housing MCP Server"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent

class HousingMCPServer:
    def __init__(self):
        self.server = Server("housing-mcp-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            return [
                Resource(uri="housing://programs", name="Housing Programs", 
                        description="Available housing assistance programs", 
                        mimeType="application/json"),
                Resource(uri="housing://assistance", name="Rental Assistance", 
                        description="Rental assistance programs", 
                        mimeType="application/json"),
                Resource(uri="housing://codes", name="Housing Codes", 
                        description="Housing code regulations", 
                        mimeType="application/json")
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            return f"Housing resource data for {uri.split('//')[-1]}"
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return [
                Tool(name="find_assistance", description="Find housing assistance",
                     inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
                Tool(name="check_eligibility", description="Check program eligibility",
                     inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
                Tool(name="report_violations", description="Report housing violations",
                     inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]})
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict = None):
            if arguments is None: arguments = {}
            result = f"Housing tool {name} executed with: {arguments.get('query', '')}"
            return [TextContent(type="text", text=result)]

async def main():
    server = HousingMCPServer()
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
