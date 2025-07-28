# 🚀 CivicMind AI Quick Start Guide

Get CivicMind AI running in minutes with this comprehensive quick start guide covering development setup, first API calls, and essential workflows.

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
- **RAM**: 8GB minimum, 16GB recommended for full platform
- **Storage**: 10GB free space for development, 50GB+ for production
- **CPU**: 4+ cores recommended for optimal performance

### Software Dependencies
- **Python 3.11+** - [Download from python.org](https://python.org/downloads/)
- **Docker Desktop** - [Get Docker](https://docker.com/get-started)
- **Git** - [Install Git](https://git-scm.com/downloads)
- **curl** or **Postman** - For API testing

### Optional Tools
- **VS Code** with Python extension for development
- **kubectl** for Kubernetes deployment
- **Docker Compose** (included with Docker Desktop)

---

## ⚡ 5-Minute Setup

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/rajathota/civicmind-ai.git
cd civicmind-ai

# 2. Start all services with Docker Compose
docker compose -f deployment/docker-compose.dev.yml up -d

# 3. Wait for services to start (about 2-3 minutes)
docker compose -f deployment/docker-compose.dev.yml logs -f api-gateway
```

### Option 2: Manual Service Startup

```bash
# 1. Clone and setup
git clone https://github.com/rajathota/civicmind-ai.git
cd civicmind-ai

# 2. Install shared library
cd shared-lib
pip install -e .
cd ..

# 3. Start development services
./scripts/start-dev.sh
```

---

## 🏥 Health Check

Verify all services are running:

```bash
# Check API Gateway (main entry point)
curl -f http://localhost:8300/health
# Expected: {"status": "healthy", "timestamp": "2025-01-15T10:30:00Z"}

# Check Orchestrator
curl -f http://localhost:8000/health
# Expected: {"status": "healthy", "services": 8, "agents": 8}

# Check Parking Service
curl -f http://localhost:8001/health
# Expected: {"status": "healthy", "service": "parking", "mcp_agent": "connected"}
```

### Service Status Dashboard

| Service | Port | Status Check | Expected Response |
|---------|------|--------------|-------------------|
| **API Gateway** | 8300 | `curl localhost:8300/health` | `{"status": "healthy"}` |
| **Orchestrator** | 8000 | `curl localhost:8000/health` | `{"status": "healthy"}` |
| **Parking Service** | 8001 | `curl localhost:8001/health` | `{"status": "healthy"}` |
| **Parking MCP** | 9300 | `curl localhost:9300/health` | `{"status": "ready"}` |

---

## 🎯 First API Calls

### 1. Analyze a Citizen Issue

```bash
curl -X POST "http://localhost:8300/api/v1/issues/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "My neighbor parks blocking my driveway every night",
    "location": "Downtown District",
    "priority": "medium"
  }'
```

**Expected Response:**
```json
{
  "service": "parking-service",
  "confidence": 0.95,
  "response": {
    "issue_type": "parking_violation",
    "suggested_actions": [
      "Contact parking enforcement",
      "Document violations with photos",
      "File formal complaint"
    ],
    "next_steps": "File complaint through parking service",
    "agent_analysis": "This appears to be a recurring parking violation that blocks vehicle access. The issue falls under parking enforcement jurisdiction.",
    "estimated_resolution_time": "3-5 business days"
  },
  "routing": {
    "selected_service": "parking-service",
    "mcp_agent": "parking-agent",
    "confidence_score": 0.95
  }
}
```

### 2. Search Available Services

```bash
curl -X GET "http://localhost:8300/api/v1/services/search?q=building permit"
```

**Expected Response:**
```json
{
  "services": [
    {
      "name": "permits-service",
      "description": "Building permits, business licensing, and regulatory approvals",
      "capabilities": ["permit_applications", "requirement_analysis", "status_tracking"],
      "endpoint": "http://localhost:8002",
      "mcp_agent": "http://localhost:9301"
    }
  ],
  "suggestions": [
    "building permit application",
    "permit requirements",
    "permit status check"
  ]
}
```

### 3. Direct Service Interaction

```bash
# Call parking service directly
curl -X POST "http://localhost:8001/api/v1/violations/report" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "123 Main St",
    "violation_type": "blocked_driveway",
    "description": "Vehicle blocking residential driveway",
    "reporter_contact": "citizen@email.com"
  }'
```

### 4. MCP Agent Direct Communication

```bash
# List available tools from parking MCP agent
curl -X POST "http://localhost:9300/mcp/tools/list" \
  -H "Content-Type: application/json"

# Use a specific tool
curl -X POST "http://localhost:9300/mcp/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "find_parking_regulations",
    "arguments": {
      "address": "123 Main St",
      "violation_type": "blocked_driveway"
    }
  }'
```

---

## 🛠️ Development Workflow

### Project Structure Overview

```
civicmind-ai/
├── 🏗️ independent-services/          # All microservices
│   ├── 🚪 civicmind-api-gateway/     # Main entry point (Port 8300)
│   ├── 🎭 civicmind-orchestrator-service/  # Workflow coordinator
│   ├── 🚗 civicmind-parking-service/       # Parking domain API
│   └── 🤖 civicmind-*-mcp-server/          # AI agents (Ports 9300-9307)
├── 📚 shared-lib/                     # Common utilities
├── 🚢 deployment/                    # Docker & K8s configs
└── 📖 docs/                          # Documentation
```

### Adding a New Service

1. **Create service directory:**
```bash
mkdir independent-services/civicmind-transportation-service
cd independent-services/civicmind-transportation-service
```

2. **Use shared library template:**
```python
# main.py
from fastapi import FastAPI
from civicmind_common.models import BaseModel
from civicmind_common.database import get_db_connection
from civicmind_common.auth import require_auth

app = FastAPI(title="Transportation Service")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "transportation"}
```

3. **Register with API Gateway:**
```python
# In API Gateway configuration
REGISTERED_SERVICES = {
    "transportation": {
        "url": "http://transportation-service:8009",
        "mcp_server": "http://transportation-mcp:9308",
        "keywords": ["transportation", "transit", "routes", "public_transport"]
    }
}
```

### Debugging Common Issues

#### Service Discovery Issues
```bash
# Check Docker networks
docker network ls
docker network inspect civicmind-dev

# Verify service registration
curl http://localhost:8300/api/v1/services/list
```

#### Database Connection Problems
```bash
# Check shared library installation
cd shared-lib && pip install -e . --upgrade

# Verify database connection
docker compose -f deployment/docker-compose.dev.yml exec postgres psql -U dev_user -d civicmind_dev
```

#### MCP Agent Communication
```bash
# Test MCP agent directly
curl -X POST "http://localhost:9300/mcp/ping"

# Check agent logs
docker compose -f deployment/docker-compose.dev.yml logs parking-mcp
```

---

## 📱 Testing the Platform

### Unit Testing

```bash
# Run all unit tests
pytest tests/unit/ -v

# Test specific service
pytest tests/unit/test_parking_service.py -v

# Run with coverage
pytest tests/unit/ --cov=civicmind_common --cov-report=html
```

### Integration Testing

```bash
# Full integration test suite
pytest tests/integration/ -v

# Test API Gateway routing
pytest tests/integration/test_gateway_routing.py -v

# Test MCP agent communication
pytest tests/integration/test_mcp_agents.py -v
```

### End-to-End Testing

```bash
# Complete workflow tests
pytest tests/e2e/ -v

# Test citizen journey
pytest tests/e2e/test_citizen_workflows.py::test_parking_complaint_workflow -v
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load/locustfile.py --host=http://localhost:8300

# Test specific endpoints
locust -f tests/load/test_gateway_performance.py --users 100 --spawn-rate 10
```

---

## 🌐 Common Use Cases

### 1. Parking Violation Workflow

```bash
# Step 1: Analyze the issue
curl -X POST "http://localhost:8300/api/v1/issues/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "Car parked in handicap spot without permit"}'

# Step 2: File the violation report
curl -X POST "http://localhost:8001/api/v1/violations/report" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "City Hall Parking Lot",
    "violation_type": "handicap_violation",
    "license_plate": "ABC123",
    "description": "Vehicle parked in handicap space without visible permit"
  }'

# Step 3: Track the complaint
curl -X GET "http://localhost:8001/api/v1/violations/12345/status"
```

### 2. Building Permit Inquiry

```bash
# Get permit requirements
curl -X POST "http://localhost:8300/api/v1/issues/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "I need to build a deck on my house"}'

# Check specific requirements
curl -X POST "http://localhost:8002/api/v1/permits/requirements" \
  -H "Content-Type: application/json" \
  -d '{
    "permit_type": "residential_deck",
    "property_address": "456 Oak Street",
    "project_description": "Deck addition to single-family home"
  }'
```

### 3. Multi-Service Workflow

```bash
# Start a complex workflow (restaurant opening)
curl -X POST "http://localhost:8000/api/v1/workflows/restaurant-opening" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Sample Bistro",
    "business_address": "789 Restaurant Row",
    "owner_info": {"name": "John Smith", "phone": "555-0123"},
    "seating_capacity": 50,
    "serves_alcohol": true
  }'

# Check workflow progress
curl -X GET "http://localhost:8000/api/v1/workflows/RESTO-20250115-143000/status"
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Core Configuration
ENVIRONMENT=development
LOG_LEVEL=DEBUG
RELOAD=true

# Database Configuration
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/civicmind_dev

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# API Gateway Configuration
GATEWAY_PORT=8300
GATEWAY_HOST=0.0.0.0

# Service Discovery
ORCHESTRATOR_URL=http://localhost:8000
PARKING_SERVICE_URL=http://localhost:8001
PERMITS_SERVICE_URL=http://localhost:8002

# MCP Servers
PARKING_MCP_URL=http://localhost:9300
PERMITS_MCP_URL=http://localhost:9301

# External APIs (Optional)
OPENAI_API_KEY=your_openai_key_here
GOOGLE_MAPS_API_KEY=your_maps_key_here
```

### Docker Compose Customization

Edit `deployment/docker-compose.dev.yml` for custom ports or configurations:

```yaml
services:
  api-gateway:
    ports:
      - "8300:8300"  # Change external port if needed
    environment:
      - CUSTOM_SETTING=value
    volumes:
      - ./custom-config:/app/config  # Mount custom configs
```

---

## 🚀 Next Steps

### Explore Documentation
- **[Architecture Guide](architecture.md)** - Deep dive into system design
- **[Building Agents](examples/building-an-agent.md)** - Create custom MCP agents
- **[Deployment Guide](deployment.md)** - Production deployment strategies
- **[API Reference](api-reference.md)** - Complete API documentation

### Development Tasks
1. **Add a new civic service** following the service template
2. **Create a custom MCP agent** for your specific use case
3. **Integrate with external APIs** using the shared library
4. **Deploy to staging environment** using Docker Compose

### Community Engagement
- **Star the repository** to show support
- **Join discussions** on GitHub for feature requests
- **Contribute** by fixing bugs or adding new features
- **Share feedback** on your implementation experience

---

## 🆘 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using port 8300
lsof -i :8300  # macOS/Linux
netstat -ano | findstr :8300  # Windows

# Use different ports in docker-compose.dev.yml
```

#### Service Won't Start
```bash
# Check logs
docker compose -f deployment/docker-compose.dev.yml logs api-gateway

# Restart specific service
docker compose -f deployment/docker-compose.dev.yml restart api-gateway
```

#### Database Connection Issues
```bash
# Reset database
docker compose -f deployment/docker-compose.dev.yml down -v
docker compose -f deployment/docker-compose.dev.yml up -d postgres

# Check connection
docker compose -f deployment/docker-compose.dev.yml exec postgres psql -U dev_user -d civicmind_dev -c "SELECT 1;"
```

### Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/rajathota/civicmind-ai/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/rajathota/civicmind-ai/discussions)
- **Documentation**: [Browse complete docs](https://github.com/rajathota/civicmind-ai/tree/main/docs)

---

🎉 **Congratulations!** You now have CivicMind AI running locally. Start building intelligent civic solutions that make government services more accessible and efficient for everyone.
