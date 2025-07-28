# 📚 CivicMind AI API Reference

Comprehensive API documentation for CivicMind AI's microservices platform including REST APIs, MCP protocol endpoints, and integration guides.

## 🌐 API Overview

CivicMind AI provides multiple API layers for different use cases:

- **🚪 API Gateway (Port 8300)** - Main entry point with intelligent routing
- **🎭 Orchestrator (Port 8000)** - Multi-service workflows and coordination
- **🏛️ Civic Services (8001-8008)** - Domain-specific REST APIs
- **🤖 MCP Agents (9300-9307)** - AI agent communication via Model Context Protocol

### Base URLs

| Environment | API Gateway | Orchestrator | Services | MCP Agents |
|-------------|-------------|--------------|----------|------------|
| **Development** | `http://localhost:8300` | `http://localhost:8000` | `http://localhost:800X` | `http://localhost:930X` |
| **Staging** | `https://api-staging.civicmind.ai` | `https://orchestrator-staging.civicmind.ai` | Internal mesh | Internal mesh |
| **Production** | `https://api.civicmind.ai` | Internal mesh | Internal mesh | Internal mesh |

### Authentication

```bash
# API Key Authentication (recommended for services)
curl -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     "http://localhost:8300/api/v1/..."

# Bearer Token Authentication (for user sessions)
curl -H "Authorization: Bearer your-jwt-token" \
     -H "Content-Type: application/json" \
     "http://localhost:8300/api/v1/..."
```

---

## 🚪 API Gateway Endpoints

### Issue Analysis and Routing

#### `POST /api/v1/issues/analyze`

Intelligently analyze citizen issues and route to appropriate services.

**Request:**
```json
{
  "query": "My neighbor parks blocking my driveway every night",
  "location": "Downtown District",
  "priority": "medium",
  "contact_info": {
    "email": "citizen@email.com",
    "phone": "555-0123"
  },
  "attachments": [
    {
      "type": "image",
      "url": "https://example.com/photo.jpg",
      "description": "Photo of blocked driveway"
    }
  ]
}
```

**Response:**
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
    "agent_analysis": "This appears to be a recurring parking violation...",
    "estimated_resolution_time": "3-5 business days",
    "relevant_regulations": [
      {
        "code": "PARK-101",
        "description": "Blocking driveways prohibited",
        "penalty": "$75 fine"
      }
    ]
  },
  "routing": {
    "selected_service": "parking-service",
    "mcp_agent": "parking-agent",
    "confidence_score": 0.95,
    "alternative_services": ["safety-service"]
  },
  "tracking": {
    "request_id": "REQ-20250115-001",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

#### `GET /api/v1/services/search`

Search available civic services and capabilities.

**Parameters:**
- `q` (string) - Search query
- `category` (string) - Service category filter
- `limit` (integer) - Maximum results (default: 10)

**Example:**
```bash
curl "http://localhost:8300/api/v1/services/search?q=building%20permit&category=permits"
```

**Response:**
```json
{
  "services": [
    {
      "name": "permits-service",
      "description": "Building permits, business licensing, and regulatory approvals",
      "categories": ["permits", "licensing", "building"],
      "capabilities": [
        "permit_applications",
        "requirement_analysis", 
        "status_tracking",
        "fee_calculation"
      ],
      "endpoint": "http://localhost:8002",
      "mcp_agent": "http://localhost:9301",
      "availability": "24/7",
      "average_response_time": "2.3s"
    }
  ],
  "suggestions": [
    "building permit application",
    "permit requirements",
    "permit status check",
    "permit fees"
  ],
  "total_results": 1,
  "search_time": "0.15s"
}
```

### Service Health and Status

#### `GET /health`

Check API Gateway health and connected services.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "orchestrator": "healthy",
    "parking-service": "healthy",
    "permits-service": "healthy",
    "noise-service": "degraded",
    "utilities-service": "healthy"
  },
  "mcp_agents": {
    "parking-agent": "connected",
    "permits-agent": "connected",
    "noise-agent": "reconnecting",
    "utilities-agent": "connected"
  },
  "performance": {
    "requests_per_minute": 150,
    "average_response_time": "1.2s",
    "error_rate": "0.1%"
  }
}
```

---

## 🎭 Orchestrator API

### Workflow Management

#### `POST /api/v1/workflows/{workflow_type}`

Start a multi-service workflow.

**Available Workflows:**
- `restaurant-opening` - Complete restaurant business setup
- `housing-development` - Residential development coordination
- `emergency-response` - Emergency service coordination
- `event-planning` - Community event permits and coordination

**Example - Restaurant Opening:**
```bash
curl -X POST "http://localhost:8000/api/v1/workflows/restaurant-opening" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Sample Bistro",
    "business_address": "789 Restaurant Row", 
    "owner_info": {
      "name": "John Smith",
      "phone": "555-0123",
      "email": "john@samplebistro.com"
    },
    "seating_capacity": 50,
    "serves_alcohol": true,
    "requires_renovation": true,
    "estimated_opening": "2025-06-01"
  }'
```

**Response:**
```json
{
  "workflow_id": "RESTO-20250115-143000",
  "status": "initiated",
  "estimated_completion": "8-12 weeks",
  "total_estimated_cost": 2150,
  "steps": [
    {
      "step": "business_license",
      "status": "pending",
      "estimated_duration": "1-2 weeks",
      "required_documents": ["Articles of incorporation", "Owner ID"]
    },
    {
      "step": "health_permit",
      "status": "waiting",
      "dependencies": ["business_license"],
      "estimated_duration": "2-3 weeks"
    }
  ],
  "next_actions": [
    "Submit business license application",
    "Schedule pre-opening health inspection"
  ]
}
```

#### `GET /api/v1/workflows/{workflow_id}/status`

Get workflow execution status and progress.

**Response:**
```json
{
  "workflow_id": "RESTO-20250115-143000",
  "status": "in_progress",
  "progress": 35,
  "started_at": "2025-01-15T14:30:00Z",
  "estimated_completion": "2025-03-15T00:00:00Z",
  "completed_steps": [
    {
      "step": "business_license",
      "completed_at": "2025-01-20T10:00:00Z",
      "result": {
        "license_id": "BL-2025-001",
        "status": "approved",
        "valid_until": "2026-01-20"
      }
    }
  ],
  "current_step": {
    "step": "health_permit",
    "status": "in_progress",
    "started_at": "2025-01-21T09:00:00Z",
    "estimated_completion": "2025-02-10T00:00:00Z"
  },
  "pending_steps": [
    "zoning_compliance",
    "fire_inspection",
    "liquor_license"
  ],
  "total_cost_incurred": 450,
  "remaining_estimated_cost": 1700
}
```

---

## 🏛️ Civic Service APIs

### Parking Service API (Port 8001)

#### `POST /api/v1/violations/report`

Report a parking violation.

**Request:**
```json
{
  "location": "123 Main St",
  "violation_type": "blocked_driveway",
  "license_plate": "ABC123",
  "description": "Vehicle blocking residential driveway",
  "reporter_contact": "citizen@email.com",
  "photos": [
    {
      "url": "https://example.com/photo1.jpg",
      "timestamp": "2025-01-15T10:30:00Z"
    }
  ],
  "priority": "medium"
}
```

**Response:**
```json
{
  "violation_id": "PV-2025-001234",
  "status": "submitted",
  "ticket_number": "PARK-789456",
  "estimated_response_time": "2-4 hours",
  "case_officer": {
    "name": "Officer Johnson",
    "badge_number": "P-1234",
    "contact": "parking@city.ai"
  },
  "next_steps": [
    "Officer will investigate within 2-4 hours",
    "You will receive email updates on case progress",
    "Citation will be issued if violation confirmed"
  ],
  "tracking_url": "https://city.ai/parking/track/PV-2025-001234"
}
```

#### `GET /api/v1/violations/{violation_id}/status`

Check violation report status.

**Response:**
```json
{
  "violation_id": "PV-2025-001234",
  "status": "resolved",
  "resolution": "citation_issued",
  "citation_number": "CITE-456789",
  "resolution_date": "2025-01-15T15:30:00Z",
  "details": {
    "officer_notes": "Violation confirmed. Citation issued to vehicle owner.",
    "citation_amount": 75,
    "due_date": "2025-02-14",
    "payment_options": ["online", "mail", "in_person"]
  },
  "timeline": [
    {
      "timestamp": "2025-01-15T10:30:00Z",
      "event": "violation_reported",
      "description": "Citizen reported blocked driveway"
    },
    {
      "timestamp": "2025-01-15T13:45:00Z", 
      "event": "officer_dispatched",
      "description": "Officer Johnson assigned to investigate"
    },
    {
      "timestamp": "2025-01-15T15:30:00Z",
      "event": "citation_issued",
      "description": "Violation confirmed, citation issued"
    }
  ]
}
```

### Permits Service API (Port 8002)

#### `POST /api/v1/permits/requirements`

Get permit requirements for a specific project.

**Request:**
```json
{
  "permit_type": "residential_deck",
  "property_address": "456 Oak Street",
  "project_description": "Deck addition to single-family home",
  "project_details": {
    "square_footage": 200,
    "height": "8 feet",
    "materials": ["pressure_treated_lumber", "composite_decking"]
  }
}
```

**Response:**
```json
{
  "permit_type": "residential_deck",
  "requirements": {
    "documents": [
      {
        "name": "Site Plan",
        "description": "Detailed drawing showing deck location relative to property lines",
        "required": true,
        "template_url": "https://city.ai/forms/site-plan-template.pdf"
      },
      {
        "name": "Structural Calculations", 
        "description": "Engineer-stamped calculations for deck support",
        "required": true,
        "professional_required": "Licensed Structural Engineer"
      }
    ],
    "inspections": [
      {
        "type": "foundation_inspection",
        "timing": "Before concrete pour",
        "estimated_duration": "30 minutes",
        "scheduling_notice": "24 hours"
      },
      {
        "type": "final_inspection",
        "timing": "Upon project completion",
        "estimated_duration": "45 minutes"
      }
    ],
    "fees": {
      "permit_fee": 150,
      "inspection_fees": 100,
      "total": 250,
      "payment_methods": ["credit_card", "check", "cash"]
    }
  },
  "timeline": {
    "estimated_approval_time": "2-3 weeks",
    "construction_window": "6 months from approval",
    "total_process_time": "3-4 weeks"
  },
  "regulations": [
    {
      "code": "BUILD-DECK-001",
      "description": "Residential deck setback requirements",
      "requirement": "Minimum 5 feet from property line"
    }
  ]
}
```

#### `POST /api/v1/permits/apply`

Submit a permit application.

**Request:**
```json
{
  "permit_type": "residential_deck",
  "applicant": {
    "name": "Jane Smith",
    "address": "456 Oak Street",
    "phone": "555-0456",
    "email": "jane@email.com",
    "property_owner": true
  },
  "project": {
    "description": "Deck addition to single-family home",
    "estimated_cost": 5000,
    "contractor": {
      "name": "ABC Construction",
      "license": "CONT-1234",
      "contact": "contractor@abc.com"
    }
  },
  "documents": [
    {
      "type": "site_plan",
      "file_url": "https://storage.example.com/site-plan.pdf"
    },
    {
      "type": "structural_calculations",
      "file_url": "https://storage.example.com/struct-calc.pdf"
    }
  ]
}
```

**Response:**
```json
{
  "application_id": "PERM-2025-5678",
  "status": "submitted",
  "submitted_at": "2025-01-15T11:00:00Z",
  "estimated_review_time": "2-3 weeks",
  "assigned_reviewer": {
    "name": "Building Inspector Mike",
    "email": "mike@city.ai",
    "phone": "555-CITY"
  },
  "fees": {
    "total_due": 250,
    "due_date": "2025-01-22T00:00:00Z",
    "payment_url": "https://city.ai/payments/PERM-2025-5678"
  },
  "next_steps": [
    "Pay permit fees within 7 days",
    "Await initial review by building department",
    "Address any review comments promptly"
  ],
  "tracking_url": "https://city.ai/permits/track/PERM-2025-5678"
}
```

---

## 🤖 MCP Agent Protocol

### Agent Communication

MCP (Model Context Protocol) agents provide AI-powered assistance for each civic domain. They expose resources, tools, and prompts through a standardized protocol.

#### List Available Resources

```bash
curl -X POST "http://localhost:9300/mcp/resources/list" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "resources": [
    {
      "uri": "parking://regulations",
      "name": "Parking Regulations Database",
      "description": "Complete parking rules and regulations",
      "mimeType": "application/json"
    },
    {
      "uri": "parking://violations",
      "name": "Violation Types and Penalties",
      "description": "All parking violation types with associated penalties",
      "mimeType": "application/json"
    }
  ]
}
```

#### List Available Tools

```bash
curl -X POST "http://localhost:9300/mcp/tools/list" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "tools": [
    {
      "name": "find_parking_regulations",
      "description": "Look up parking regulations for a specific location",
      "inputSchema": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "description": "Street address or location"
          },
          "violation_type": {
            "type": "string",
            "description": "Type of violation to check"
          }
        },
        "required": ["address"]
      }
    },
    {
      "name": "calculate_parking_fees",
      "description": "Calculate parking violation fees and penalties",
      "inputSchema": {
        "type": "object",
        "properties": {
          "violation_type": {
            "type": "string",
            "description": "Type of parking violation"
          },
          "repeat_offense": {
            "type": "boolean",
            "description": "Is this a repeat offense"
          }
        },
        "required": ["violation_type"]
      }
    }
  ]
}
```

#### Call Agent Tool

```bash
curl -X POST "http://localhost:9300/mcp/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "find_parking_regulations",
    "arguments": {
      "address": "123 Main St",
      "violation_type": "blocked_driveway"
    }
  }'
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "For 123 Main St (Downtown District):\n\n**Driveway Blocking Regulations:**\n- Municipal Code: PARK-101\n- Violation: Blocking any portion of a driveway\n- Fine: $75 for first offense, $150 for repeat\n- Enforcement: Active 24/7\n- Towing: Authorized after 1 hour\n\n**Reporting Process:**\n1. Document violation with photos\n2. Note license plate if visible\n3. File report through parking service\n4. Officer response within 2-4 hours\n\n**Legal Authority:**\nCity Municipal Code Section 10.64.050 - Stopping, standing, or parking prohibited in specified places."
    }
  ],
  "isError": false
}
```

---

## 🔐 Authentication & Authorization

### API Key Management

#### Get API Key
```bash
curl -X POST "http://localhost:8300/auth/api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "organization": "City of Springfield",
    "department": "Public Works",
    "contact_email": "admin@springfield.ai",
    "use_case": "Parking enforcement integration"
  }'
```

#### Validate API Key
```bash
curl -X GET "http://localhost:8300/auth/validate" \
  -H "X-API-Key: your-api-key"
```

### JWT Token Authentication

#### Login
```bash
curl -X POST "http://localhost:8300/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@city.ai",
    "password": "secure_password"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "user123",
    "email": "user@city.ai",
    "department": "Public Works",
    "permissions": ["parking:read", "parking:write", "permits:read"]
  }
}
```

---

## 📊 Rate Limits and Quotas

### Default Rate Limits

| Endpoint Type | Rate Limit | Burst Limit |
|---------------|------------|-------------|
| **Public APIs** | 100 req/min | 200 req/min |
| **Authenticated APIs** | 1000 req/min | 2000 req/min |
| **Workflow APIs** | 50 req/min | 100 req/min |
| **MCP Agents** | 500 req/min | 1000 req/min |

### Rate Limit Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642262400
X-RateLimit-Burst: 2000
```

### Handling Rate Limits

```python
import requests
import time

def api_call_with_retry(url, headers, data):
    while True:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 429:
            # Rate limited
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            continue
            
        return response
```

---

## 🔍 Error Handling

### Standard Error Response Format

```json
{
  "error": {
    "code": "PARKING_VIOLATION_NOT_FOUND",
    "message": "Violation with ID PV-2025-001234 not found",
    "details": {
      "violation_id": "PV-2025-001234",
      "searched_date_range": "2025-01-01 to 2025-01-15"
    },
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_abc123def456"
  }
}
```

### Common Error Codes

| HTTP Status | Error Code | Description | Resolution |
|-------------|------------|-------------|------------|
| **400** | `INVALID_REQUEST` | Malformed request data | Check request format and required fields |
| **401** | `UNAUTHORIZED` | Missing or invalid authentication | Provide valid API key or JWT token |
| **403** | `FORBIDDEN` | Insufficient permissions | Contact admin for permission upgrade |
| **404** | `NOT_FOUND` | Resource not found | Verify resource ID exists |
| **409** | `CONFLICT` | Resource conflict | Resolve conflicting state |
| **422** | `VALIDATION_ERROR` | Invalid input data | Fix validation errors in request |
| **429** | `RATE_LIMITED` | Too many requests | Implement rate limiting and retry logic |
| **500** | `INTERNAL_ERROR` | Server error | Report to support team |
| **503** | `SERVICE_UNAVAILABLE` | Service temporarily down | Check service status and retry |

---

## 🧪 Testing and Development

### Postman Collection

Import our Postman collection for easy API testing:

```bash
# Download collection
curl -o civicmind-api.postman_collection.json \
  https://raw.githubusercontent.com/rajathota/civicmind-ai/main/docs/postman/civicmind-api.postman_collection.json

# Import into Postman and set environment variables:
# - base_url: http://localhost:8300
# - api_key: your-api-key
```

### SDK and Libraries

#### Python SDK
```python
from civicmind_sdk import CivicMindClient

client = CivicMindClient(
    base_url="http://localhost:8300",
    api_key="your-api-key"
)

# Analyze issue
result = client.issues.analyze(
    query="Parking violation on Main Street",
    location="Downtown"
)

# Report violation  
violation = client.parking.report_violation(
    location="123 Main St",
    violation_type="blocked_driveway",
    description="Vehicle blocking driveway access"
)
```

#### JavaScript SDK
```javascript
import { CivicMindAPI } from '@civicmind/api-client';

const client = new CivicMindAPI({
  baseURL: 'http://localhost:8300',
  apiKey: 'your-api-key'
});

// Analyze issue
const result = await client.issues.analyze({
  query: 'Building permit question',
  location: 'Downtown District'
});

// Start workflow
const workflow = await client.workflows.start('restaurant-opening', {
  business_name: 'Test Restaurant',
  business_address: '123 Restaurant Row'
});
```

---

## 📈 Monitoring and Observability

### Metrics Endpoints

#### Gateway Metrics
```bash
curl "http://localhost:8300/metrics"
```

#### Service Health
```bash
curl "http://localhost:8300/api/v1/system/status"
```

**Response:**
```json
{
  "system": {
    "status": "healthy",
    "uptime": "5d 12h 30m",
    "version": "1.0.0"
  },
  "services": {
    "total": 8,
    "healthy": 7,
    "degraded": 1,
    "down": 0
  },
  "performance": {
    "requests_per_second": 25.3,
    "average_response_time": "1.2s",
    "error_rate": "0.1%",
    "success_rate": "99.9%"
  },
  "resources": {
    "cpu_usage": "45%",
    "memory_usage": "62%",
    "disk_usage": "23%"
  }
}
```

---

## 🌐 Webhooks and Events

### Webhook Registration

```bash
curl -X POST "http://localhost:8300/api/v1/webhooks" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "url": "https://your-app.com/webhooks/civicmind",
    "events": ["violation.created", "permit.approved", "workflow.completed"],
    "secret": "webhook-secret-key"
  }'
```

### Event Types

| Event | Description | Payload |
|-------|-------------|---------|
| `violation.created` | New parking violation reported | Violation details |
| `violation.resolved` | Violation case closed | Resolution details |
| `permit.submitted` | Permit application submitted | Application details |
| `permit.approved` | Permit application approved | Approval details |
| `workflow.started` | Multi-service workflow initiated | Workflow details |
| `workflow.completed` | Workflow finished | Completion summary |

### Webhook Payload Example

```json
{
  "event": "violation.created",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "violation_id": "PV-2025-001234",
    "type": "blocked_driveway",
    "location": "123 Main St",
    "status": "submitted",
    "reporter": "citizen@email.com"
  },
  "metadata": {
    "api_version": "v1",
    "source": "parking-service"
  }
}
```

---

This comprehensive API reference provides all the information needed to integrate with CivicMind AI's microservices platform. For additional support, consult the [Architecture Guide](architecture.md) or join our [GitHub Discussions](https://github.com/rajathota/civicmind-ai/discussions).
