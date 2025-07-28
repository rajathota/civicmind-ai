# CivicMind AI Framework - Quick Start Guide

## Overview

CivicMind AI is an open-source framework for building AI agents that help citizens resolve civic issues. The framework provides:

- **Multi-Agent System**: Specialized agents for different civic domains
- **Community-First Approach**: Prioritizes local resolution before legal escalation
- **Cultural Sensitivity**: Respects diverse community values and traditions
- **Self-Hosted Deployment**: Full control over your data and infrastructure

## Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Optional: LangSmith API key for debugging and observability

### Step 1: Clone and Setup

```bash
git clone <your-repo-url>
cd civicmind-framework
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Step 3: Run the Server

```bash
python server.py
```

The API will be available at `http://localhost:8000`

## Basic Usage

### Analyze a Civic Issue

```python
import requests

response = requests.post("http://localhost:8000/api/v1/issues/analyze", json={
    "description": "My neighbor's dog barks loudly every night from 11 PM to 2 AM",
    "location": "Folsom, CA",
    "priority": "medium"
})

result = response.json()
print(f"Issue Type: {result['issue_type']}")
print(f"Recommendations: {result['recommendations']}")
```

### Use Specific Agent

```python
response = requests.post("http://localhost:8000/api/v1/agents/noise/analyze", json={
    "description": "Construction noise at 6 AM on weekends",
    "location": "Sacramento, CA"
})
```

## Available Agents

- **Parking Agent**: Parking violations, permits, disputes
- **Noise Agent**: Noise complaints, sound ordinances
- **Permits Agent**: Building permits, licenses, events
- **Infrastructure Agent**: Roads, utilities, public works
- **Business Agent**: Home business licensing
- **Religious Events Agent**: Cultural and religious event planning
- **Neighbor Dispute Agent**: Interpersonal conflicts
- **Environmental Agent**: Pollution, waste, environmental issues

## Core Concepts

### Community-First Resolution

The framework prioritizes community-based solutions:

1. **Friendly Communication**: Encourage direct neighbor conversation
2. **Community Mediation**: Suggest local mediators or HOA involvement
3. **Educational Approach**: Explain rules and expectations
4. **Legal Escalation**: Only when community solutions fail

### Cultural Sensitivity

Inspired by Hindu philosophical principles:

- **Dharma**: Doing the right thing for the community
- **Ahimsa**: Non-harmful conflict resolution
- **Satsang**: Collective wisdom and shared knowledge
- **Seva**: Service to the community

### Agent Orchestration

The framework uses LangGraph for intelligent routing:

```
User Input → Classification → Context Analysis → Agent Routing → Recommendations
```

## API Endpoints

### Main Endpoints

- `POST /api/v1/issues/analyze` - Analyze any civic issue
- `GET /api/v1/agents` - List available agents
- `POST /api/v1/agents/{type}/analyze` - Use specific agent
- `GET /api/v1/locations/{location}/info` - Get location-specific info

### Health and Status

- `GET /` - Basic info
- `GET /health` - Health check

## Configuration

### Environment Variables

Key configuration options:

```env
OPENAI_API_KEY=your_key_here
LANGSMITH_API_KEY=optional_for_debugging
CIVICMIND_MODEL=gpt-4o
ENABLE_COMMUNITY_RESOLUTION=true
```

### Custom Agents

Create custom agents by extending `BaseCivicAgent`:

```python
from civicmind.agents.base_agent import BaseCivicAgent

class CustomAgent(BaseCivicAgent):
    def get_system_prompt(self) -> str:
        return "Your custom agent prompt..."
    
    def analyze_issue(self, issue_description, location, context):
        # Your custom logic
        pass
```

## Deployment

### Docker

```bash
docker build -t civicmind .
docker run -p 8000:8000 --env-file .env civicmind
```

### Kubernetes

```bash
kubectl apply -f deployment/kubernetes/
```

## Next Steps

1. **Customize Agents**: Modify existing agents for your specific locality
2. **Add Data Sources**: Integrate local government APIs
3. **Frontend Integration**: Build a web or mobile interface
4. **Extend Capabilities**: Add voice input, image processing, or multi-language support

## Support

- Documentation: `/docs` folder
- Issues: GitHub Issues
- Community: Join our discussions

## License

Apache 2.0 - See LICENSE file for details
