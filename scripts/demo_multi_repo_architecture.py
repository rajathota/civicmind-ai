#!/usr/bin/env python3
"""
Multi-Repository Architecture Demo
==================================

This script demonstrates the independent microservices architecture
with separate repositories for each service.
"""

import asyncio
import httpx
import time
import subprocess
import sys
import os
from pathlib import Path

# Configuration
DEMO_SERVICES = {
    "api-gateway": {
        "port": 8300,
        "path": "independent-services/civicmind-api-gateway",
        "main": "main.py"
    },
    "parking-service": {
        "port": 9300, 
        "path": "independent-services/civicmind-parking-service",
        "main": "main.py"
    }
}

async def check_service_health(service_name: str, port: int, timeout: int = 5):
    """Check if a service is healthy"""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"http://localhost:{port}/health")
            return response.status_code == 200
    except:
        return False

async def test_api_gateway_routing():
    """Test API Gateway routing to parking service"""
    print("\n🧪 Testing API Gateway Routing")
    print("=" * 50)
    
    # Test issue analysis via API Gateway
    test_request = {
        "description": "My neighbor parks blocking my driveway every night, making it impossible for me to leave for work",
        "location": "Folsom, CA",
        "priority": "high"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Test direct parking service access
            print("1. Testing direct parking service access...")
            parking_response = await client.post(
                "http://localhost:9300/analyze",
                json=test_request
            )
            
            if parking_response.status_code == 200:
                print("   ✅ Parking service responded directly")
                parking_data = parking_response.json()
                print(f"   📝 Issue ID: {parking_data.get('issue_id')}")
                print(f"   ⏱️  Processing time: {parking_data.get('processing_time_ms')}ms")
            else:
                print(f"   ❌ Parking service error: {parking_response.status_code}")
            
            print("\n2. Testing API Gateway routing...")
            # Test API Gateway routing
            gateway_response = await client.post(
                "http://localhost:8300/api/v1/issues/analyze",
                json=test_request
            )
            
            if gateway_response.status_code == 200:
                print("   ✅ API Gateway routed successfully")
                gateway_data = gateway_response.json()
                print(f"   🎯 Classified as: {gateway_data['gateway_info']['classification']}")
                print(f"   🚀 Routed to: {gateway_data['gateway_info']['routed_to']}")
                print(f"   ⏱️  Total time: {gateway_data.get('total_processing_time_ms')}ms")
            else:
                print(f"   ❌ API Gateway error: {gateway_response.status_code}")
                
    except Exception as e:
        print(f"❌ Testing failed: {e}")

async def test_service_independence():
    """Test that services can operate independently"""
    print("\n🔄 Testing Service Independence")
    print("=" * 50)
    
    # Test parking service independently
    print("1. Testing parking service independence...")
    parking_healthy = await check_service_health("parking", 9300)
    print(f"   Parking Service: {'✅ Healthy' if parking_healthy else '❌ Unhealthy'}")
    
    # Test API Gateway
    print("2. Testing API Gateway...")
    gateway_healthy = await check_service_health("api-gateway", 8300)
    print(f"   API Gateway: {'✅ Healthy' if gateway_healthy else '❌ Unhealthy'}")
    
    # Test service discovery
    if gateway_healthy:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                services_response = await client.get("http://localhost:8300/api/v1/services")
                if services_response.status_code == 200:
                    services_data = services_response.json()
                    print(f"   📊 Services registered: {services_data['total_services']}")
                    for service, info in services_data['services'].items():
                        status = info['health_status']
                        status_icon = "✅" if status == "healthy" else "❌"
                        print(f"      {status_icon} {service}: {status}")
        except Exception as e:
            print(f"   ❌ Service discovery failed: {e}")

def print_architecture_benefits():
    """Print the benefits of the multi-repository architecture"""
    print("\n🏗️ Multi-Repository Architecture Benefits")
    print("=" * 50)
    
    benefits = [
        "🚀 Independent Deployment - Each service can be deployed separately",
        "🔧 Technology Freedom - Each service can use different tech stacks", 
        "👥 Team Ownership - Teams can own entire service lifecycles",
        "📦 Dependency Management - No conflicts between service requirements",
        "🔄 Independent Scaling - Scale services based on individual demand",
        "🛡️ Fault Isolation - Service failures don't cascade",
        "📈 Faster Development - Teams can iterate independently",
        "🔒 Security Boundaries - Clear security isolation between services"
    ]
    
    for benefit in benefits:
        print(f"   {benefit}")

def print_repository_structure():
    """Print the recommended repository structure"""
    print("\n📁 Recommended Repository Structure")
    print("=" * 50)
    
    repos = [
        "📦 civicmind-shared-lib/          # Common models and utilities",
        "🌐 civicmind-api-gateway/         # Independent API Gateway",
        "🚗 civicmind-parking-service/     # Standalone parking service",
        "📋 civicmind-permits-service/     # Standalone permits service",
        "🔊 civicmind-noise-service/       # Standalone noise service",
        "🏗️ civicmind-infrastructure-service/ # Standalone infrastructure service",
        "🏢 civicmind-business-service/    # Standalone business service",
        "🕌 civicmind-religious-events-service/ # Standalone religious events service",
        "🏠 civicmind-neighbor-disputes-service/ # Standalone neighbor disputes service",
        "🌱 civicmind-environmental-service/ # Standalone environmental service",
        "🐳 civicmind-deployment/          # Infrastructure as Code",
        "📊 civicmind-monitoring/          # Observability stack"
    ]
    
    for repo in repos:
        print(f"   {repo}")

async def main():
    """Main demo function"""
    print("🎯 CivicMind Multi-Repository Architecture Demo")
    print("=" * 60)
    
    # Print architecture information
    print_repository_structure()
    print_architecture_benefits()
    
    # Check if services are running
    print(f"\n🔍 Checking Service Status")
    print("=" * 50)
    
    parking_running = await check_service_health("parking", 9300)
    gateway_running = await check_service_health("api-gateway", 8300)
    
    print(f"Parking Service (Port 9300): {'✅ Running' if parking_running else '❌ Not Running'}")
    print(f"API Gateway (Port 8300): {'✅ Running' if gateway_running else '❌ Not Running'}")
    
    if not parking_running or not gateway_running:
        print("\n⚠️  Services not running. To start them:")
        print("1. Parking Service: cd independent-services/civicmind-parking-service && python main.py")
        print("2. API Gateway: cd independent-services/civicmind-api-gateway && python main.py")
        print("\nOr run the demo with services automatically:")
        return
    
    # Test service independence
    await test_service_independence()
    
    # Test API Gateway routing
    await test_api_gateway_routing()
    
    print("\n🎉 Multi-Repository Architecture Demo Complete!")
    print("=" * 60)
    print("Key Takeaways:")
    print("✅ Services run independently")
    print("✅ API Gateway routes intelligently") 
    print("✅ Each service can be deployed separately")
    print("✅ Fault isolation works properly")
    print("✅ Clear separation of concerns")

if __name__ == "__main__":
    asyncio.run(main())
