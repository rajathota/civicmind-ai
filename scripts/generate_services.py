"""
Service Generation Script
========================

Rapidly create all remaining CivicMind services using templates.
"""

import os
import shutil
from pathlib import Path

# Service definitions
SERVICES = [
    {
        "name": "permits",
        "port": 3002,
        "api_port": 8002,
        "description": "Permit applications and approvals",
        "capabilities": [
            "permit_application_guidance",
            "document_verification",
            "approval_process_tracking",
            "fee_calculation",
            "community_input_collection"
        ]
    },
    {
        "name": "noise",
        "port": 3003, 
        "api_port": 8003,
        "description": "Noise complaints and mediation",
        "capabilities": [
            "noise_level_assessment",
            "neighbor_mediation",
            "ordinance_enforcement",
            "pattern_recognition",
            "community_quiet_hours"
        ]
    },
    {
        "name": "utilities",
        "port": 3004,
        "api_port": 8004,
        "description": "Utility services and infrastructure",
        "capabilities": [
            "service_outage_reporting",
            "utility_billing_disputes",
            "service_connection_requests",
            "infrastructure_maintenance",
            "emergency_response_coordination"
        ]
    },
    {
        "name": "housing",
        "port": 3005,
        "api_port": 8005,
        "description": "Housing issues and tenant rights",
        "capabilities": [
            "tenant_rights_guidance",
            "housing_code_violations",
            "rent_dispute_mediation",
            "habitability_assessments",
            "affordable_housing_assistance"
        ]
    },
    {
        "name": "business",
        "port": 3006,
        "api_port": 8006,
        "description": "Business licensing and operations",
        "capabilities": [
            "business_license_applications",
            "zoning_compliance_checks",
            "operational_permits",
            "neighbor_business_disputes",
            "economic_development_guidance"
        ]
    },
    {
        "name": "safety",
        "port": 3007,
        "api_port": 8007,
        "description": "Public safety and emergency services",
        "capabilities": [
            "safety_hazard_reporting",
            "emergency_response_coordination",
            "community_watch_programs",
            "traffic_safety_analysis",
            "incident_documentation"
        ]
    },
    {
        "name": "environmental",
        "port": 3008,
        "api_port": 8008,
        "description": "Environmental issues and sustainability",
        "capabilities": [
            "environmental_impact_assessment",
            "pollution_reporting",
            "sustainability_initiatives",
            "waste_management_issues",
            "green_space_advocacy"
        ]
    }
]

def create_mcp_server(service_info):
    """Create MCP server for a service"""
    name = service_info["name"]
    port = service_info["port"]
    description = service_info["description"]
    capabilities = service_info["capabilities"]
    
    base_dir = f"civicmind-{name}-mcp-server"
    
    print(f"Creating MCP server: {base_dir}")
    
    # Create directory structure
    os.makedirs(f"{base_dir}/src/{name}_mcp_server/agents", exist_ok=True)
    os.makedirs(f"{base_dir}/src/{name}_mcp_server/tools", exist_ok=True)
    os.makedirs(f"{base_dir}/tests", exist_ok=True)
    
    # Create package init files
    with open(f"{base_dir}/src/{name}_mcp_server/__init__.py", "w") as f:
        f.write(f'"""\nCivicMind {name.title()} MCP Server Package\n"""\n\n')
        f.write(f'__version__ = "1.0.0"\n')
        f.write(f'__author__ = "CivicMind AI Team"\n')
        f.write(f'__email__ = "team@civicmind.ai"\n')
    
    with open(f"{base_dir}/src/{name}_mcp_server/agents/__init__.py", "w") as f:
        f.write(f'from .{name}_agent import {name.title()}MCPAgent\n\n')
        f.write(f'__all__ = ["{name.title()}MCPAgent"]\n')
    
    with open(f"{base_dir}/src/{name}_mcp_server/tools/__init__.py", "w") as f:
        f.write(f'from .{name}_tools import (\n')
        f.write(f'    analyze_{name}_issue,\n')
        f.write(f'    search_{name}_regulations,\n')
        f.write(f'    find_{name}_contacts,\n')
        f.write(f'    generate_{name}_resolution_steps\n')
        f.write(f')\n\n')
        f.write(f'__all__ = [\n')
        f.write(f'    "analyze_{name}_issue",\n')
        f.write(f'    "search_{name}_regulations",\n')
        f.write(f'    "find_{name}_contacts",\n')
        f.write(f'    "generate_{name}_resolution_steps"\n')
        f.write(f']\n')

def create_api_service(service_info):
    """Create API service for a service"""
    name = service_info["name"]
    api_port = service_info["api_port"]
    description = service_info["description"]
    capabilities = service_info["capabilities"]
    
    base_dir = f"civicmind-{name}-api-service"
    
    print(f"Creating API service: {base_dir}")
    
    # Create directory structure
    os.makedirs(f"{base_dir}/src/{name}_service/agents", exist_ok=True)
    os.makedirs(f"{base_dir}/src/{name}_service/models", exist_ok=True)
    os.makedirs(f"{base_dir}/src/{name}_service/services", exist_ok=True)
    os.makedirs(f"{base_dir}/src/{name}_service/config", exist_ok=True)
    os.makedirs(f"{base_dir}/src/{name}_service/utils", exist_ok=True)
    os.makedirs(f"{base_dir}/tests", exist_ok=True)
    os.makedirs(f"{base_dir}/deployment", exist_ok=True)
    os.makedirs(f"{base_dir}/docs", exist_ok=True)
    os.makedirs(f"{base_dir}/.github/workflows", exist_ok=True)

if __name__ == "__main__":
    # Change to independent-services directory
    os.chdir(".")
    
    for service in SERVICES:
        create_mcp_server(service)
        create_api_service(service)
    
    print("All services created successfully!")
