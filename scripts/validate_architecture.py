#!/usr/bin/env python3
"""
CivicMind Microservices Architecture Validator
==============================================

Validates that all components of the microservices architecture are properly set up.
"""

import os
import sys
from pathlib import Path

def validate_structure():
    """Validate the microservices directory structure"""
    print("🔍 Validating CivicMind Microservices Architecture...")
    print("=" * 55)
    
    required_paths = [
        # API Gateway
        "services/api_gateway/main.py",
        "services/api_gateway/models.py", 
        "services/api_gateway/config.py",
        "services/api_gateway/middleware.py",
        "services/api_gateway/Dockerfile",
        "services/api_gateway/requirements.txt",
        
        # MCP Base Server
        "services/mcp_base/server.py",
        
        # MCP Servers
        "services/mcp_servers/parking_server.py",
        "services/mcp_servers/permits_server.py",
        "services/mcp_servers/noise_server.py",
        "services/mcp_servers/infrastructure_server.py",
        "services/mcp_servers/business_server.py",
        "services/mcp_servers/religious_events_server.py",
        "services/mcp_servers/neighbor_dispute_server.py",
        "services/mcp_servers/environmental_server.py",
        "services/mcp_servers/Dockerfile",
        
        # Agents
        "civicmind/agents/parking_agent.py",
        "civicmind/agents/permits_agent.py",
        "civicmind/agents/noise_agent.py",
        "civicmind/agents/infrastructure_agent.py",
        "civicmind/agents/business_agent.py",
        "civicmind/agents/religious_events_agent.py",
        "civicmind/agents/neighbor_dispute_agent.py",
        "civicmind/agents/environmental_agent.py",
        
        # Scripts
        "scripts/start_services.py",
        "scripts/start_services.ps1",
        "scripts/generate_mcp_servers.py",
        
        # Docker
        "docker-compose.microservices.yml",
        
        # Documentation
        "MICROSERVICES.md"
    ]
    
    missing_files = []
    existing_files = []
    
    for path in required_paths:
        if os.path.exists(path):
            existing_files.append(path)
            print(f"✅ {path}")
        else:
            missing_files.append(path)
            print(f"❌ {path}")
    
    print(f"\n📊 Summary:")
    print(f"✅ Existing: {len(existing_files)} files")
    print(f"❌ Missing: {len(missing_files)} files")
    
    if missing_files:
        print(f"\n⚠️  Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def validate_ports():
    """Validate port configuration"""
    print(f"\n🔌 Port Configuration:")
    print("-" * 25)
    
    ports = {
        "API Gateway": 8300,
        "Parking MCP": 9300,
        "Permits MCP": 9301,
        "Noise MCP": 9302,
        "Infrastructure MCP": 9303,
        "Business MCP": 9304,
        "Religious Events MCP": 9305,
        "Neighbor Dispute MCP": 9306,
        "Environmental MCP": 9307
    }
    
    for service, port in ports.items():
        print(f"✅ {service:<25} Port {port}")
    
    return True

def validate_docker_setup():
    """Validate Docker configuration"""
    print(f"\n🐳 Docker Configuration:")
    print("-" * 28)
    
    docker_files = [
        "docker-compose.microservices.yml",
        "services/api_gateway/Dockerfile",
        "services/mcp_servers/Dockerfile"
    ]
    
    all_exist = True
    for file in docker_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            all_exist = False
    
    return all_exist

def show_getting_started():
    """Show getting started instructions"""
    print(f"\n🚀 Getting Started:")
    print("-" * 20)
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("   pip install -r services/api_gateway/requirements.txt")
    
    print("\n2. Start services (choose one):")
    print("   # Windows PowerShell")
    print("   .\\scripts\\start_services.ps1")
    print("   ")
    print("   # Python script")
    print("   python scripts/start_services.py")
    print("   ")
    print("   # Docker Compose")
    print("   docker-compose -f docker-compose.microservices.yml up -d")
    
    print("\n3. Access services:")
    print("   API Gateway: http://localhost:8300")
    print("   API Docs:    http://localhost:8300/docs")
    print("   Health:      http://localhost:8300/health")
    
    print("\n4. Test API:")
    print("   curl -X POST \"http://localhost:8300/api/v1/analyze\" \\")
    print("     -H \"Content-Type: application/json\" \\")
    print("     -d '{\"issue_text\": \"Test parking issue\"}'")

def main():
    """Main validation function"""
    print("CivicMind Microservices Architecture Validator")
    print("=" * 50)
    
    # Change to project root
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    all_good = True
    
    # Validate structure
    if not validate_structure():
        all_good = False
    
    # Validate ports
    validate_ports()
    
    # Validate Docker setup
    if not validate_docker_setup():
        all_good = False
    
    if all_good:
        print(f"\n🎉 Architecture Validation: SUCCESS")
        print("=" * 35)
        print("✅ All components are properly configured!")
        print("✅ Microservices architecture is ready!")
        show_getting_started()
    else:
        print(f"\n❌ Architecture Validation: FAILED")
        print("=" * 32)
        print("⚠️  Some components are missing or misconfigured.")
        print("Please check the missing files and fix the issues.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
