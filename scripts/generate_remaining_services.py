#!/usr/bin/env python3
"""
Generate all remaining civic service implementations (MCP servers and API services)
"""

import os
from pathlib import Path

# Service configurations
SERVICES = {
    "permits": {
        "description": "Building permits, business licenses, and regulatory compliance",
        "resources": ["building_permits", "business_licenses", "fee_schedules"],
        "tools": ["analyze_application", "search_requirements", "find_contacts"]
    },
    "noise": {
        "description": "Noise complaints, ordinances, and sound regulations",
        "resources": ["noise_ordinances", "complaint_database", "violation_records"],
        "tools": ["file_complaint", "check_violations", "get_noise_limits"]
    },
    "utilities": {
        "description": "Water, electricity, gas, and utility service management",
        "resources": ["service_areas", "outage_reports", "billing_info"],
        "tools": ["report_outage", "schedule_service", "check_availability"]
    },
    "housing": {
        "description": "Affordable housing, rental assistance, and housing codes",
        "resources": ["housing_programs", "rental_assistance", "housing_codes"],
        "tools": ["find_assistance", "check_eligibility", "report_violations"]
    },
    "business": {
        "description": "Business registration, development incentives, and commercial permits",
        "resources": ["business_registry", "development_incentives", "commercial_zones"],
        "tools": ["register_business", "find_incentives", "check_zoning"]
    },
    "safety": {
        "description": "Public safety, emergency services, and safety inspections",
        "resources": ["safety_inspections", "emergency_contacts", "safety_codes"],
        "tools": ["schedule_inspection", "report_hazard", "find_emergency_info"]
    },
    "environmental": {
        "description": "Environmental regulations, sustainability programs, and waste management",
        "resources": ["environmental_regulations", "sustainability_programs", "waste_schedules"],
        "tools": ["check_regulations", "find_programs", "schedule_pickup"]
    }
}

def create_mcp_server(service_name, config):
    """Create MCP server files for a service"""
    base_path = Path(f"independent-services/civicmind-{service_name}-mcp-server")
    
    # Create server.py
    server_content = f'''"""
CivicMind {service_name.title()} MCP Server
{config["description"]}
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

from .agents.{service_name}_agent import {service_name.title()}Agent
from .tools.{service_name}_tools import {service_name.title()}Tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("{service_name}_mcp_server")

class {service_name.title()}MCPServer:
    """MCP Server for {service_name} civic services"""
    
    def __init__(self):
        self.server = Server("{service_name}-mcp-server")
        self.agent = {service_name.title()}Agent()
        self.tools_handler = {service_name.title()}Tools()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP protocol handlers"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """List available {service_name} resources"""
            return [
{self._generate_resource_list(config["resources"])}
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read {service_name} resource content"""
            return await self.agent.get_resource_content(uri)
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available {service_name} tools"""
            return [
{self._generate_tool_list(config["tools"])}
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None = None) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Execute {service_name} tool"""
            if arguments is None:
                arguments = {{}}
            
            result = await self.tools_handler.execute_tool(name, arguments)
            return [TextContent(type="text", text=str(result))]

    def _generate_resource_list(self, resources):
        """Generate resource list code"""
        resource_items = []
        for resource in resources:
            resource_items.append(f'''                Resource(
                    uri="{service_name}://{resource}",
                    name="{resource.replace('_', ' ').title()}",
                    description="{resource.replace('_', ' ')} information and data",
                    mimeType="application/json",
                )''')
        return ',\\n'.join(resource_items)

    def _generate_tool_list(self, tools):
        """Generate tool list code"""
        tool_items = []
        for tool in tools:
            tool_items.append(f'''                Tool(
                    name="{tool}",
                    description="{tool.replace('_', ' ').title()} for {service_name} services",
                    inputSchema={{
                        "type": "object",
                        "properties": {{
                            "query": {{"type": "string", "description": "Query or request details"}}
                        }},
                        "required": ["query"]
                    }}
                )''')
        return ',\\n'.join(tool_items)

async def main():
    """Main server entry point"""
    server_instance = {service_name.title()}MCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="{service_name}-mcp-server",
                server_version="1.0.0",
                capabilities={{
                    "resources": {{}},
                    "tools": {{}},
                }}
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
'''

    # Create agent file
    agent_content = f'''"""
{service_name.title()} Agent for CivicMind
"""

from typing import Dict, Any, Optional
from civicmind_common.agents.base_agent import BaseAgent
from civicmind_common.models.civic_models import CitizenRequest, ServiceResponse

class {service_name.title()}Agent(BaseAgent):
    """Agent for handling {service_name} civic services"""
    
    def __init__(self):
        super().__init__(service_type="{service_name}")
        self.service_description = "{config['description']}"
    
    async def process_request(self, request: CitizenRequest) -> ServiceResponse:
        """Process {service_name} service request"""
        try:
            # Extract request details
            query = request.query
            citizen_id = request.citizen_id
            
            # Process based on request type
            if "application" in query.lower():
                return await self._handle_application(query, citizen_id)
            elif "status" in query.lower():
                return await self._check_status(query, citizen_id)
            elif "information" in query.lower():
                return await self._provide_information(query)
            else:
                return await self._general_assistance(query, citizen_id)
                
        except Exception as e:
            self.logger.error(f"Error processing {service_name} request: {{e}}")
            return ServiceResponse(
                success=False,
                message="Sorry, I encountered an error processing your request.",
                data={{"error": str(e)}}
            )
    
    async def _handle_application(self, query: str, citizen_id: str) -> ServiceResponse:
        """Handle application-related requests"""
        return ServiceResponse(
            success=True,
            message=f"I'll help you with your {service_name} application.",
            data={{
                "next_steps": "Application process information",
                "required_documents": "Document requirements",
                "estimated_timeline": "Processing timeline"
            }}
        )
    
    async def _check_status(self, query: str, citizen_id: str) -> ServiceResponse:
        """Check status of existing applications or services"""
        return ServiceResponse(
            success=True,
            message=f"Here's the status of your {service_name} request.",
            data={{
                "status": "In review",
                "last_updated": "Recent update",
                "next_action": "Required action"
            }}
        )
    
    async def _provide_information(self, query: str) -> ServiceResponse:
        """Provide general information about {service_name} services"""
        return ServiceResponse(
            success=True,
            message=f"Here's information about {service_name} services.",
            data={{
                "overview": "Service overview",
                "requirements": "General requirements",
                "contacts": "Relevant contacts"
            }}
        )
    
    async def _general_assistance(self, query: str, citizen_id: str) -> ServiceResponse:
        """Provide general assistance"""
        return ServiceResponse(
            success=True,
            message=f"I'm here to help with {service_name} services.",
            data={{
                "assistance_type": "General help",
                "available_services": ["Service 1", "Service 2", "Service 3"],
                "contact_info": "Contact information"
            }}
        )
    
    async def get_resource_content(self, uri: str) -> str:
        """Get content for MCP resources"""
        resource_type = uri.split("//")[-1]
        
        # Mock resource content - in production, this would fetch real data
        resource_data = {{
            f"{resource}": f"{{resource.replace('_', ' ').title()}} data and information"
            for resource in {config['resources']}
        }}
        
        return resource_data.get(resource_type, "Resource not found")
'''

    # Create tools file
    tools_content = f'''"""
{service_name.title()} Tools for CivicMind MCP Server
"""

from typing import Dict, Any
import logging

logger = logging.getLogger("{service_name}_tools")

class {service_name.title()}Tools:
    """Tools for {service_name} civic services"""
    
    def __init__(self):
        self.available_tools = {config['tools']}
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a {service_name} tool"""
        try:
            if tool_name not in self.available_tools:
                return {{"error": f"Tool {{tool_name}} not found"}}
            
            # Route to appropriate tool method
            method_name = f"_{{tool_name}}"
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                return await method(arguments)
            else:
                return {{"error": f"Tool implementation {{tool_name}} not found"}}
                
        except Exception as e:
            logger.error(f"Error executing tool {{tool_name}}: {{e}}")
            return {{"error": f"Tool execution failed: {{str(e)}}"}}
'''

    # Add tool methods
    for tool in config['tools']:
        tools_content += f'''
    
    async def _{tool}(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute {tool.replace('_', ' ')} tool"""
        query = arguments.get("query", "")
        
        # Mock implementation - replace with actual logic
        return {{
            "tool": "{tool}",
            "query": query,
            "result": "Tool execution result for {tool.replace('_', ' ')}",
            "status": "success"
        }}'''

    # Write files
    os.makedirs(base_path / "src" / f"{service_name}_mcp_server", exist_ok=True)
    os.makedirs(base_path / "src" / f"{service_name}_mcp_server" / "agents", exist_ok=True)
    os.makedirs(base_path / "src" / f"{service_name}_mcp_server" / "tools", exist_ok=True)
    
    # Write server.py
    with open(base_path / "src" / f"{service_name}_mcp_server" / "server.py", "w") as f:
        f.write(server_content)
    
    # Write agent file
    with open(base_path / "src" / f"{service_name}_mcp_server" / "agents" / f"{service_name}_agent.py", "w") as f:
        f.write(agent_content)
    
    # Write tools file
    with open(base_path / "src" / f"{service_name}_mcp_server" / "tools" / f"{service_name}_tools.py", "w") as f:
        f.write(tools_content)
    
    # Write __init__.py files
    init_content = f'"""CivicMind {service_name.title()} MCP Server"""\\n__version__ = "1.0.0"'
    with open(base_path / "src" / f"{service_name}_mcp_server" / "__init__.py", "w") as f:
        f.write(init_content)
    
    with open(base_path / "src" / f"{service_name}_mcp_server" / "agents" / "__init__.py", "w") as f:
        f.write("")
    
    with open(base_path / "src" / f"{service_name}_mcp_server" / "tools" / "__init__.py", "w") as f:
        f.write("")

def main():
    """Generate all service files"""
    for service_name, config in SERVICES.items():
        print(f"Creating MCP server for {service_name}...")
        create_mcp_server(service_name, config)
        print(f"✅ {service_name} MCP server created")
    
    print(f"\\n🎉 All {len(SERVICES)} MCP servers created successfully!")

if __name__ == "__main__":
    main()
