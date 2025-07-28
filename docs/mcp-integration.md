# 🔌 MCP Integration Guide

Model Context Protocol (MCP) enables AI assistants to directly interact with CivicMind AI's microservices platform, providing natural language access to all civic services through standardized AI agent communication.

## 🌟 Overview

MCP (Model Context Protocol) is an open standard that enables AI assistants like Claude to communicate with external services through a standardized interface. CivicMind AI implements dedicated MCP servers for each civic domain, creating seamless AI-powered civic service interactions.

### 🎯 What MCP Enables

- **Natural Language Queries**: "Check my parking violations" → Automated API calls
- **Cross-Service Intelligence**: AI agents coordinate between multiple civic domains
- **Real-Time Integration**: Direct connection to live civic service APIs
- **Standardized Protocol**: Universal AI assistant compatibility

## 🏗️ MCP Server Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Assistant  │    │   MCP Client    │    │   MCP Server    │
│  (Claude/GPT)   │ ◄─►│    (Bridge)     │ ◄─►│  (CivicMind)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                               ┌─────────────────┐
                                               │ Microservices   │
                                               │ (8 Civic APIs)  │
                                               └─────────────────┘
```

### 🚀 Available MCP Servers

Each civic domain runs its own intelligent MCP server with specialized AI capabilities:

| Domain | Port | URL | Capabilities |
|--------|------|-----|-------------|
| **🚗 Parking** | 9300 | `http://localhost:9300` | Violation reports, citation lookup, payment processing, space finding |
| **🏗️ Permits** | 9301 | `http://localhost:9301` | Application analysis, requirement lookup, status tracking, fee calculation |
| **🔊 Noise** | 9302 | `http://localhost:9302` | Complaint filing, ordinance lookup, enforcement tracking |
| **🚨 Safety** | 9303 | `http://localhost:9303` | Emergency coordination, incident reporting, resource dispatch |
| **💧 Utilities** | 9304 | `http://localhost:9304` | Service requests, outage reporting, billing inquiries |
| **🚌 Transportation** | 9305 | `http://localhost:9305` | Traffic management, transit info, road maintenance |
| **🏡 Zoning** | 9306 | `http://localhost:9306` | Compliance checks, land use guidance, variance applications |
| **🌱 Environmental** | 9307 | `http://localhost:9307` | Waste management, environmental reporting, sustainability programs |

---

## 🛠️ Installation and Setup

### Local Development Setup

1. **Start Complete CivicMind Platform**
   ```bash
   # Start all microservices and MCP servers
   docker-compose up -d
   
   # Verify MCP servers are running
   curl http://localhost:9300/health  # Parking MCP
   curl http://localhost:9301/health  # Permits MCP
   curl http://localhost:9302/health  # Noise MCP
   
   # Check all MCP servers at once
   for i in {0..7}; do
     echo "Checking MCP Server $((9300 + i))..."
     curl -s http://localhost:$((9300 + i))/health | jq '.status'
   done
   ```

2. **Configure Claude Desktop Integration**
   
   Add to your Claude Desktop configuration (`~/.claude/config.json`):
   ```json
   {
     "mcpServers": {
       "civicmind-parking": {
         "command": "mcp-client",
         "args": ["--url", "http://localhost:9300"],
         "description": "Parking violations, citations, and space management"
       },
       "civicmind-permits": {
         "command": "mcp-client", 
         "args": ["--url", "http://localhost:9301"],
         "description": "Building permits and licensing services"
       },
       "civicmind-safety": {
         "command": "mcp-client",
         "args": ["--url", "http://localhost:9303"],
         "description": "Public safety and emergency services"
       }
     }
   }
   ```

3. **VS Code MCP Extension Setup**
   ```json
   // settings.json
   {
     "mcp.servers": [
       {
         "name": "CivicMind Parking",
         "url": "http://localhost:9300",
         "autoConnect": true
       },
       {
         "name": "CivicMind Permits", 
         "url": "http://localhost:9301",
         "autoConnect": true
       }
     ]
   }
   ```

### Production Deployment

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  # MCP Server Cluster
  parking-mcp:
    image: civicmind/parking-mcp:latest
    ports:
      - "9300:9300"
    environment:
      - API_GATEWAY_URL=http://api-gateway:8300
      - PARKING_SERVICE_URL=http://parking-service:8001
      - MCP_PORT=9300
      - LOG_LEVEL=info
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9300/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - civicmind-network

  permits-mcp:
    image: civicmind/permits-mcp:latest
    ports:
      - "9301:9301"
    environment:
      - API_GATEWAY_URL=http://api-gateway:8300
      - PERMITS_SERVICE_URL=http://permits-service:8002
      - MCP_PORT=9301
    networks:
      - civicmind-network

  # Load balancer for MCP traffic
  mcp-loadbalancer:
    image: nginx:alpine
    ports:
      - "9000:80"
    volumes:
      - ./nginx-mcp.conf:/etc/nginx/nginx.conf
    depends_on:
      - parking-mcp
      - permits-mcp
    networks:
      - civicmind-network
```

---

## 📡 MCP Protocol Communication

### Basic MCP Flow

1. **Initialize Connection**
   ```json
   {
     "jsonrpc": "2.0",
     "method": "initialize",
     "params": {
       "protocolVersion": "2024-11-05",
       "clientInfo": {
         "name": "Claude Desktop",
         "version": "3.5.0"
       },
       "capabilities": {
         "roots": {"listChanged": true},
         "sampling": {}
       }
     },
     "id": 1
   }
   ```

2. **List Available Resources**
   ```json
   {
     "jsonrpc": "2.0",
     "method": "resources/list",
     "id": 2
   }
   ```

3. **Discover Tools**
   ```json
   {
     "jsonrpc": "2.0", 
     "method": "tools/list",
     "id": 3
   }
   ```

4. **Execute Tool**
   ```json
   {
     "jsonrpc": "2.0",
     "method": "tools/call",
     "params": {
       "name": "check_parking_violations",
       "arguments": {
         "license_plate": "ABC123",
         "include_payment_options": true
       }
     },
     "id": 4
   }
   ```

---

## 🚗 Parking MCP Server

### Available Tools

#### `check_violations`
Look up parking violations by license plate.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "license_plate": {"type": "string", "description": "License plate number"},
    "include_payment_options": {"type": "boolean", "default": true},
    "date_range": {"type": "string", "description": "Optional date range (e.g., '30d', '2024-01')"}
  },
  "required": ["license_plate"]
}
```

**Example Call:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "check_violations",
    "arguments": {
      "license_plate": "ABC123",
      "include_payment_options": true
    }
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "**Parking Violations for License Plate ABC123**\n\n🅿️ **Outstanding Violations: 2**\n\n1. **Violation #VIO-2025-001234**\n   - Type: Expired Meter\n   - Location: 123 Main St, Zone A\n   - Date: January 10, 2025\n   - Fine: $25.00\n   - Due: February 9, 2025\n   - Status: ⚠️ Unpaid\n\n2. **Violation #VIO-2025-001456**\n   - Type: Blocked Driveway  \n   - Location: 456 Oak Ave\n   - Date: January 12, 2025\n   - Fine: $75.00\n   - Due: February 11, 2025\n   - Status: ⚠️ Unpaid\n\n💰 **Total Outstanding: $100.00**\n\n**Payment Options:**\n- 🌐 Online: https://city.ai/parking/pay\n- 📞 Phone: (555) 123-PARK\n- 🏢 In Person: City Hall, Room 101\n\n⏰ **Pay by due date to avoid late fees!**"
      }
    ],
    "isError": false
  },
  "id": 1
}
```

#### `find_parking`
Find available parking spaces near a location.

**Example Usage:**
```json
{
  "name": "find_parking",
  "arguments": {
    "location": "Downtown City Hall",
    "duration": "2 hours",
    "parking_type": "street"
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text", 
      "text": "🅿️ **Parking Options Near Downtown City Hall**\n\n**Street Parking (2-hour limit):**\n1. 📍 Main St (100 block) - $2.00/hour\n   - 🚶 0.1 miles away\n   - ✅ 8 spaces available\n   - ⏰ Enforced 8am-6pm\n\n2. 📍 1st Avenue - $1.50/hour  \n   - 🚶 0.2 miles away\n   - ✅ 12 spaces available\n   - ⏰ 2-hour limit\n\n**Nearby Garages:**\n3. 🏢 City Center Garage - $5.00 flat rate\n   - 🚶 0.3 miles away\n   - ✅ 45 spaces available\n   - ⏰ No time limit\n\n💡 **Recommendation:** Main St parking is closest and most economical for your 2-hour needs."
    }
  ],
  "isError": false
}
```

#### `report_violation`
Report a parking violation with photo evidence.

#### `make_payment`
Process payment for outstanding violations.

---

## 🏗️ Permits MCP Server

### Available Tools

#### `analyze_application`
Analyze permit application requirements and provide guidance.

**Example Call:**
```json
{
  "name": "analyze_application",
  "arguments": {
    "permit_type": "residential_deck",
    "project_description": "Adding 400 sq ft deck to back of house",
    "property_address": "123 Oak Street",
    "estimated_cost": 8000
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "🏗️ **Residential Deck Permit Analysis**\n\n**Project Overview:**\n- Type: Deck Addition (400 sq ft)\n- Location: 123 Oak Street\n- Estimated Cost: $8,000\n\n✅ **Permit Requirements Met:**\n- Size under 500 sq ft threshold\n- Residential property zoning compatible\n- Standard setback requirements apply\n\n📋 **Required Documents:**\n1. 📐 Site plan showing deck location\n2. 🏗️ Structural drawings with dimensions\n3. ⚡ Electrical plans (if adding outlets/lighting)\n4. 🏠 Property survey (if close to setbacks)\n\n💰 **Estimated Fees:**\n- Permit Fee: $150\n- Plan Review: $75\n- Inspections: $100\n- **Total: $325**\n\n⏱️ **Timeline:**\n- Application Review: 2-3 weeks\n- Construction Period: 6 months from approval\n\n📞 **Next Steps:**\n1. Submit application with required documents\n2. Pay fees within 7 days\n3. Schedule foundation inspection before building\n\n💡 **Tip:** Consider hiring a licensed contractor for structural calculations."
    }
  ],
  "isError": false
}
```

#### `check_requirements`
Get specific requirements for any permit type.

#### `submit_application`
Submit permit application with document upload.

#### `track_status`
Track permit application progress and next steps.

---

## 🔧 Custom MCP Client Development

### Python MCP Client

```python
import asyncio
import json
import aiohttp
from typing import Dict, List, Optional

class CivicMindMCPClient:
    def __init__(self, base_url: str = "http://localhost", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = None
        self.servers = {
            "parking": 9300,
            "permits": 9301, 
            "noise": 9302,
            "safety": 9303,
            "utilities": 9304,
            "transportation": 9305,
            "zoning": 9306,
            "environmental": 9307
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def initialize_server(self, domain: str) -> Dict:
        """Initialize MCP connection to a specific domain server"""
        port = self.servers.get(domain)
        if not port:
            raise ValueError(f"Unknown domain: {domain}")
        
        url = f"{self.base_url}:{port}/mcp"
        payload = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {
                    "name": "CivicMind Python Client",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        async with self.session.post(url, json=payload, headers=headers) as response:
            result = await response.json()
            return result
    
    async def list_tools(self, domain: str) -> List[Dict]:
        """List available tools for a domain"""
        port = self.servers[domain]
        url = f"{self.base_url}:{port}/mcp"
        
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2
        }
        
        async with self.session.post(url, json=payload) as response:
            result = await response.json()
            return result.get("result", {}).get("tools", [])
    
    async def call_tool(self, domain: str, tool_name: str, arguments: Dict) -> Dict:
        """Call a specific tool on a domain server"""
        port = self.servers[domain]
        url = f"{self.base_url}:{port}/mcp"
        
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": 3
        }
        
        async with self.session.post(url, json=payload) as response:
            result = await response.json()
            if "error" in result:
                raise Exception(f"MCP Error: {result['error']}")
            return result.get("result", {})

# Usage Examples
async def parking_example():
    async with CivicMindMCPClient() as client:
        # Initialize parking server
        await client.initialize_server("parking")
        
        # Check violations
        violations = await client.call_tool("parking", "check_violations", {
            "license_plate": "ABC123",
            "include_payment_options": True
        })
        
        print("Violations:", violations["content"][0]["text"])
        
        # Find parking
        parking = await client.call_tool("parking", "find_parking", {
            "location": "Downtown",
            "duration": "2 hours"
        })
        
        print("Parking options:", parking["content"][0]["text"])

async def permits_example():
    async with CivicMindMCPClient() as client:
        # Initialize permits server
        await client.initialize_server("permits")
        
        # Analyze application
        analysis = await client.call_tool("permits", "analyze_application", {
            "permit_type": "building_permit",
            "project_description": "Adding a garage to residential property",
            "property_address": "123 Main Street",
            "estimated_cost": 15000
        })
        
        print("Permit analysis:", analysis["content"][0]["text"])
        
        # Check requirements
        requirements = await client.call_tool("permits", "check_requirements", {
            "permit_type": "building_permit",
            "project_scope": "garage_addition"
        })
        
        print("Requirements:", requirements["content"][0]["text"])

# Run examples
if __name__ == "__main__":
    asyncio.run(parking_example())
    asyncio.run(permits_example())
```

### JavaScript/TypeScript MCP Client

```typescript
import axios, { AxiosInstance } from 'axios';

interface MCPResponse {
  jsonrpc: string;
  result?: {
    content: Array<{
      type: string;
      text: string;
    }>;
    isError: boolean;
  };
  error?: {
    code: number;
    message: string;
  };
  id: number;
}

class CivicMindMCPClient {
  private baseUrl: string;
  private apiKey?: string;
  private client: AxiosInstance;
  
  private servers = {
    parking: 9300,
    permits: 9301,
    noise: 9302,
    safety: 9303,
    utilities: 9304,
    transportation: 9305,
    zoning: 9306,
    environmental: 9307
  };

  constructor(baseUrl: string = 'http://localhost', apiKey?: string) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
    this.client = axios.create({
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        ...(apiKey && { 'X-API-Key': apiKey })
      }
    });
  }

  async initializeServer(domain: keyof typeof this.servers): Promise<MCPResponse> {
    const port = this.servers[domain];
    const url = `${this.baseUrl}:${port}/mcp`;
    
    const payload = {
      jsonrpc: '2.0',
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        clientInfo: {
          name: 'CivicMind JS Client',
          version: '1.0.0'
        }
      },
      id: 1
    };
    
    const response = await this.client.post(url, payload);
    return response.data;
  }

  async listTools(domain: keyof typeof this.servers): Promise<any[]> {
    const port = this.servers[domain];
    const url = `${this.baseUrl}:${port}/mcp`;
    
    const payload = {
      jsonrpc: '2.0',
      method: 'tools/list',
      id: 2
    };
    
    const response = await this.client.post(url, payload);
    return response.data.result?.tools || [];
  }

  async callTool(
    domain: keyof typeof this.servers,
    toolName: string,
    arguments: Record<string, any>
  ): Promise<MCPResponse> {
    const port = this.servers[domain];
    const url = `${this.baseUrl}:${port}/mcp`;
    
    const payload = {
      jsonrpc: '2.0',
      method: 'tools/call',
      params: {
        name: toolName,
        arguments
      },
      id: 3
    };
    
    const response = await this.client.post(url, payload);
    const result = response.data;
    
    if (result.error) {
      throw new Error(`MCP Error: ${result.error.message}`);
    }
    
    return result;
  }

  // Convenience methods for common operations
  async checkParkingViolations(licensePlate: string): Promise<string> {
    await this.initializeServer('parking');
    const result = await this.callTool('parking', 'check_violations', {
      license_plate: licensePlate,
      include_payment_options: true
    });
    return result.result?.content[0]?.text || '';
  }

  async findParking(location: string, duration: string = '2 hours'): Promise<string> {
    await this.initializeServer('parking');
    const result = await this.callTool('parking', 'find_parking', {
      location,
      duration
    });
    return result.result?.content[0]?.text || '';
  }

  async analyzePermit(
    permitType: string,
    projectDescription: string,
    propertyAddress: string,
    estimatedCost?: number
  ): Promise<string> {
    await this.initializeServer('permits');
    const result = await this.callTool('permits', 'analyze_application', {
      permit_type: permitType,
      project_description: projectDescription,
      property_address: propertyAddress,
      ...(estimatedCost && { estimated_cost: estimatedCost })
    });
    return result.result?.content[0]?.text || '';
  }
}

// Usage Examples
async function main() {
  const client = new CivicMindMCPClient();
  
  try {
    // Check parking violations
    const violations = await client.checkParkingViolations('ABC123');
    console.log('Violations:', violations);
    
    // Find parking
    const parking = await client.findParking('Downtown City Hall', '3 hours');
    console.log('Parking:', parking);
    
    // Analyze permit
    const permitAnalysis = await client.analyzePermit(
      'residential_deck',
      'Adding 200 sq ft deck with stairs',
      '456 Oak Street',
      6000
    );
    console.log('Permit Analysis:', permitAnalysis);
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
```

---

## 🧪 Testing MCP Integration

### Automated Testing Suite

```python
import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch

class TestCivicMindMCP:
    @pytest.fixture
    async def mcp_client(self):
        client = CivicMindMCPClient("http://localhost")
        async with client:
            yield client

    @pytest.mark.asyncio
    async def test_parking_violations_check(self, mcp_client):
        """Test parking violations lookup"""
        result = await mcp_client.call_tool("parking", "check_violations", {
            "license_plate": "TEST123"
        })
        
        assert result is not None
        assert "content" in result
        assert len(result["content"]) > 0
        assert "violations" in result["content"][0]["text"].lower()

    @pytest.mark.asyncio
    async def test_permits_requirements(self, mcp_client):
        """Test permit requirements lookup"""
        result = await mcp_client.call_tool("permits", "check_requirements", {
            "permit_type": "building_permit",
            "project_scope": "garage_addition"
        })
        
        assert result is not None
        assert "requirements" in result["content"][0]["text"].lower()

    @pytest.mark.asyncio
    async def test_all_servers_health(self):
        """Test that all MCP servers are healthy"""
        client = CivicMindMCPClient()
        
        for domain in client.servers:
            port = client.servers[domain]
            # Test health endpoint
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://localhost:{port}/health") as response:
                    assert response.status == 200
                    health_data = await response.json()
                    assert health_data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_error_handling(self, mcp_client):
        """Test proper error handling for invalid requests"""
        with pytest.raises(Exception) as exc_info:
            await mcp_client.call_tool("parking", "invalid_tool", {})
        
        assert "error" in str(exc_info.value).lower()

    @pytest.mark.parametrize("domain,tool,args", [
        ("parking", "check_violations", {"license_plate": "ABC123"}),
        ("permits", "check_requirements", {"permit_type": "building_permit"}),
        ("noise", "file_complaint", {"location": "123 Main St", "noise_type": "loud_music"}),
        ("utilities", "report_outage", {"service_type": "water", "address": "456 Oak Ave"}),
    ])
    @pytest.mark.asyncio
    async def test_cross_domain_tools(self, mcp_client, domain, tool, args):
        """Test tools across different domains"""
        result = await mcp_client.call_tool(domain, tool, args)
        assert result is not None
        assert "content" in result

# Load Testing
async def load_test_mcp_servers(concurrent_requests=50, total_requests=1000):
    """Load test MCP servers with concurrent requests"""
    import time
    
    async def make_request(client, domain, tool, args):
        try:
            start_time = time.time()
            result = await client.call_tool(domain, tool, args)
            response_time = time.time() - start_time
            return {"success": True, "response_time": response_time}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    client = CivicMindMCPClient()
    async with client:
        tasks = []
        for _ in range(total_requests):
            # Rotate through different domains and tools
            domain = "parking"
            tool = "check_violations"
            args = {"license_plate": f"TEST{_ % 1000:03d}"}
            
            task = make_request(client, domain, tool, args)
            tasks.append(task)
            
            # Limit concurrent requests
            if len(tasks) >= concurrent_requests:
                results = await asyncio.gather(*tasks)
                tasks = []
                
                # Analyze results
                successful = sum(1 for r in results if r["success"])
                avg_response_time = sum(r.get("response_time", 0) for r in results if r["success"]) / max(successful, 1)
                
                print(f"Batch complete: {successful}/{len(results)} successful, avg response time: {avg_response_time:.3f}s")
        
        # Process remaining tasks
        if tasks:
            results = await asyncio.gather(*tasks)
            successful = sum(1 for r in results if r["success"])
            print(f"Final batch: {successful}/{len(results)} successful")

# Run load test
if __name__ == "__main__":
    asyncio.run(load_test_mcp_servers())
```

### Manual Testing with curl

```bash
#!/bin/bash
# test-mcp-servers.sh

echo "🧪 Testing CivicMind MCP Servers..."

# Test all server health endpoints
for i in {0..7}; do
  port=$((9300 + i))
  echo "Checking MCP server on port $port..."
  curl -s http://localhost:$port/health | jq '.status' || echo "❌ Server on port $port is down"
done

# Test MCP protocol on parking server
echo "🚗 Testing Parking MCP Server..."
curl -X POST http://localhost:9300/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }' | jq '.result.tools[].name'

# Test violation check
echo "🎫 Testing violation check..."
curl -X POST http://localhost:9300/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "check_violations",
      "arguments": {"license_plate": "TEST123"}
    },
    "id": 2
  }' | jq '.result.content[0].text'

# Test permits server
echo "🏗️ Testing Permits MCP Server..."
curl -X POST http://localhost:9301/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "check_requirements", 
      "arguments": {
        "permit_type": "building_permit",
        "project_scope": "deck_addition"
      }
    },
    "id": 3
  }' | jq '.result.content[0].text'

echo "✅ MCP testing complete!"
```

---

## 🔒 Security and Production Considerations

### Authentication and Authorization

```python
class SecureMCPClient(CivicMindMCPClient):
    def __init__(self, base_url: str, api_key: str, user_token: Optional[str] = None):
        super().__init__(base_url, api_key)
        self.user_token = user_token
        
    async def call_tool(self, domain: str, tool_name: str, arguments: Dict) -> Dict:
        """Enhanced tool calling with security context"""
        # Add user context and permissions
        enhanced_args = {
            **arguments,
            "_user_context": {
                "token": self.user_token,
                "domain": domain,
                "requested_tool": tool_name,
                "timestamp": time.time()
            }
        }
        
        return await super().call_tool(domain, tool_name, enhanced_args)

# Rate limiting and circuit breaker
from circuitbreaker import circuit
import asyncio

class ResilientMCPClient(SecureMCPClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate_limiter = asyncio.Semaphore(10)  # Max 10 concurrent requests
        
    @circuit(failure_threshold=5, recovery_timeout=30)
    async def call_tool_with_resilience(self, domain: str, tool_name: str, arguments: Dict) -> Dict:
        """Tool calling with circuit breaker and rate limiting"""
        async with self.rate_limiter:
            return await self.call_tool(domain, tool_name, arguments)
```

### Monitoring and Observability

```python
from prometheus_client import Counter, Histogram, Gauge
import logging

# Metrics
mcp_requests_total = Counter('mcp_requests_total', 'Total MCP requests', ['domain', 'tool', 'status'])
mcp_request_duration = Histogram('mcp_request_duration_seconds', 'MCP request duration', ['domain', 'tool'])
mcp_active_connections = Gauge('mcp_active_connections', 'Active MCP connections', ['domain'])

class MonitoredMCPClient(ResilientMCPClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        
    async def call_tool(self, domain: str, tool_name: str, arguments: Dict) -> Dict:
        """Instrumented tool calling with metrics and logging"""
        start_time = time.time()
        
        try:
            self.logger.info(f"Calling MCP tool {domain}.{tool_name}", extra={
                "domain": domain,
                "tool": tool_name,
                "args": arguments
            })
            
            result = await super().call_tool(domain, tool_name, arguments)
            
            # Record success metrics
            mcp_requests_total.labels(domain=domain, tool=tool_name, status='success').inc()
            
            return result
            
        except Exception as e:
            # Record error metrics
            mcp_requests_total.labels(domain=domain, tool=tool_name, status='error').inc()
            
            self.logger.error(f"MCP tool call failed: {domain}.{tool_name}", extra={
                "domain": domain,
                "tool": tool_name,
                "error": str(e)
            })
            raise
            
        finally:
            # Record timing
            duration = time.time() - start_time
            mcp_request_duration.labels(domain=domain, tool=tool_name).observe(duration)
```

---

## 🚀 Advanced Integration Patterns

### Multi-Domain Workflows

```python
class CivicWorkflowOrchestrator:
    def __init__(self, mcp_client: CivicMindMCPClient):
        self.client = mcp_client
        
    async def restaurant_opening_workflow(self, business_info: Dict) -> Dict:
        """Orchestrate restaurant opening across multiple domains"""
        workflow_results = {}
        
        # Step 1: Check zoning compliance
        zoning_check = await self.client.call_tool("zoning", "check_compliance", {
            "property_address": business_info["address"],
            "business_type": "restaurant",
            "seating_capacity": business_info["seating_capacity"]
        })
        workflow_results["zoning"] = zoning_check
        
        # Step 2: Analyze permit requirements
        permit_analysis = await self.client.call_tool("permits", "analyze_application", {
            "permit_type": "business_license",
            "business_type": "restaurant",
            "serves_alcohol": business_info.get("serves_alcohol", False)
        })
        workflow_results["permits"] = permit_analysis
        
        # Step 3: Check parking requirements
        parking_analysis = await self.client.call_tool("parking", "analyze_requirements", {
            "business_address": business_info["address"],
            "seating_capacity": business_info["seating_capacity"],
            "peak_hours": business_info.get("peak_hours", "6pm-10pm")
        })
        workflow_results["parking"] = parking_analysis
        
        # Step 4: Safety inspection scheduling
        safety_requirements = await self.client.call_tool("safety", "get_requirements", {
            "business_type": "restaurant",
            "capacity": business_info["seating_capacity"]
        })
        workflow_results["safety"] = safety_requirements
        
        return {
            "workflow_id": f"restaurant-{int(time.time())}",
            "status": "analysis_complete",
            "results": workflow_results,
            "next_steps": self._generate_next_steps(workflow_results)
        }
    
    def _generate_next_steps(self, results: Dict) -> List[str]:
        """Generate prioritized next steps based on workflow results"""
        steps = []
        
        # Parse results and create action items
        for domain, result in results.items():
            content = result.get("content", [{}])[0].get("text", "")
            if "required" in content.lower():
                steps.append(f"Complete {domain} requirements")
        
        return steps

# Usage
async def main():
    async with CivicMindMCPClient() as client:
        orchestrator = CivicWorkflowOrchestrator(client)
        
        business_info = {
            "name": "Joe's Pizza",
            "address": "123 Main Street",
            "seating_capacity": 40,
            "serves_alcohol": True,
            "estimated_opening": "2025-06-01"
        }
        
        workflow_result = await orchestrator.restaurant_opening_workflow(business_info)
        print(json.dumps(workflow_result, indent=2))
```

### Real-Time Event Streaming

```python
import asyncio
import websockets
import json

class MCPEventStreamer:
    def __init__(self, mcp_client: CivicMindMCPClient):
        self.client = mcp_client
        self.subscribers = {}
        
    async def subscribe_to_events(self, domain: str, event_types: List[str], callback):
        """Subscribe to real-time events from MCP servers"""
        if domain not in self.subscribers:
            self.subscribers[domain] = []
        
        self.subscribers[domain].append({
            "event_types": event_types,
            "callback": callback
        })
        
        # Start event listener for this domain
        await self._start_event_listener(domain)
    
    async def _start_event_listener(self, domain: str):
        """Start WebSocket connection to MCP server for events"""
        port = self.client.servers[domain]
        uri = f"ws://localhost:{port}/events"
        
        try:
            async with websockets.connect(uri) as websocket:
                # Subscribe to events
                await websocket.send(json.dumps({
                    "action": "subscribe",
                    "events": ["violation.created", "permit.submitted", "complaint.filed"]
                }))
                
                # Listen for events
                async for message in websocket:
                    event_data = json.loads(message)
                    await self._handle_event(domain, event_data)
                    
        except Exception as e:
            print(f"Event listener error for {domain}: {e}")
    
    async def _handle_event(self, domain: str, event_data: Dict):
        """Handle incoming events and notify subscribers"""
        event_type = event_data.get("type")
        
        for subscriber in self.subscribers.get(domain, []):
            if event_type in subscriber["event_types"]:
                await subscriber["callback"](domain, event_data)

# Usage
async def main():
    async with CivicMindMCPClient() as client:
        streamer = MCPEventStreamer(client)
        
        # Subscribe to parking violations
        async def handle_parking_event(domain, event):
            if event["type"] == "violation.created":
                print(f"🚨 New parking violation: {event['data']['violation_id']}")
                
                # Auto-response: Check if repeat offender
                result = await client.call_tool("parking", "check_violations", {
                    "license_plate": event["data"]["license_plate"]
                })
                print(f"Violation history: {result['content'][0]['text']}")
        
        await streamer.subscribe_to_events("parking", ["violation.created"], handle_parking_event)
        
        # Keep running
        await asyncio.sleep(3600)  # Run for 1 hour
```

---

This comprehensive MCP integration guide enables developers to build powerful AI applications that leverage CivicMind AI's complete microservices platform through standardized Model Context Protocol communication. The MCP layer provides natural language access to all civic services while maintaining security, scalability, and real-time capabilities.
