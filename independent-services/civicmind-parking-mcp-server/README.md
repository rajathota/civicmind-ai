# CivicMind Parking MCP Server

**Model Context Protocol server for parking-related civic issues**

[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-blue)](https://modelcontextprotocol.io/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview

The CivicMind Parking MCP Server provides AI agent capabilities for parking issue analysis via the Model Context Protocol (MCP). This server specializes in intelligent analysis of parking violations, permit guidance, and community-first resolution strategies.

## Features

- **🤖 AI Agent Integration**: MCP-compliant server for LLM integration
- **🚗 Parking Expertise**: Specialized knowledge of parking regulations and enforcement
- **🤝 Community-First**: Prioritizes neighbor-to-neighbor resolution when appropriate
- **📋 Comprehensive Analysis**: Classification, recommendations, and step-by-step guidance
- **🔗 Resource Access**: Parking regulations, enforcement contacts, and permit information

## MCP Protocol Support

This server implements the Model Context Protocol for seamless integration with:
- Claude Desktop
- Custom MCP clients
- LLM applications
- AI agent frameworks

### MCP Capabilities

- **Resources**: Access to parking regulations and contact information
- **Tools**: Parking issue analysis, regulation search, contact finding
- **Prompts**: Structured prompts for parking issue resolution

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/civicmind-ai/civicmind-parking-mcp-server.git
cd civicmind-parking-mcp-server

# Install dependencies
pip install -e .

# Run the MCP server
parking-mcp-server
```

### MCP Client Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "civicmind-parking": {
      "command": "parking-mcp-server",
      "args": [],
      "env": {
        "MCP_PORT": "3001"
      }
    }
  }
}
```

## MCP Resources

### Available Resources

- `parking://regulations/general` - General parking regulations
- `parking://enforcement/contacts` - Enforcement contact information  
- `parking://permits/info` - Parking permit information

### Example Resource Access

```python
# Read parking regulations
content = await mcp_client.read_resource("parking://regulations/general")
```

## MCP Tools

### analyze_parking_issue

Analyze a parking issue and provide recommendations.

```json
{
  "name": "analyze_parking_issue",
  "arguments": {
    "description": "My neighbor parks blocking my driveway every night",
    "location": "123 Main Street", 
    "priority": "high"
  }
}
```

### search_parking_regulations

Search for relevant parking regulations.

```json
{
  "name": "search_parking_regulations",
  "arguments": {
    "query": "driveway blocking",
    "location": "Downtown"
  }
}
```

### find_enforcement_contacts

Find relevant parking enforcement contacts.

```json
{
  "name": "find_enforcement_contacts",
  "arguments": {
    "issue_type": "driveway_blocking",
    "location": "Residential District"
  }
}
```

### generate_resolution_steps

Generate step-by-step resolution process.

```json
{
  "name": "generate_resolution_steps", 
  "arguments": {
    "issue_description": "Car parked in front of fire hydrant",
    "classification": {"type": "fire_hydrant", "severity": "high"}
  }
}
```

## Configuration

### Environment Variables

```bash
# MCP Server Configuration
MCP_PORT=3001
MCP_SERVER_NAME=civicmind-parking-mcp-server

# Logging
LOG_LEVEL=INFO
DEBUG=false
```

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black src/ tests/
ruff check src/ tests/

# Type checking  
mypy src/
```

### Project Structure

```
civicmind-parking-mcp-server/
├── src/parking_mcp_server/           # Main server package
│   ├── server.py                     # MCP server implementation
│   ├── agents/                       # AI agents
│   │   └── parking_agent.py          # Parking analysis agent
│   └── tools/                        # MCP tools
│       └── parking_tools.py          # Tool implementations
├── tests/                            # Test suite
├── pyproject.toml                    # Package configuration
└── README.md                         # This file
```

## MCP Integration Examples

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "parking": {
      "command": "parking-mcp-server"
    }
  }
}
```

### Custom MCP Client

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_parking_server():
    server_params = StdioServerParameters(
        command="parking-mcp-server"
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the server
            await session.initialize()
            
            # Use parking analysis tool
            result = await session.call_tool(
                "analyze_parking_issue",
                {
                    "description": "Driveway blocked by neighbor",
                    "location": "Main Street"
                }
            )
            
            print(result)

asyncio.run(use_parking_server())
```

## Community-First Approach

This MCP server implements a community-first resolution strategy:

1. **🤝 Neighbor Communication**: Encourages direct, respectful conversation
2. **📝 Documentation**: Provides guidance on proper issue documentation
3. **🏢 Building Management**: Involves property management when appropriate
4. **👮 Enforcement**: Escalates to official enforcement only when necessary

## API Reference

### ParkingMCPAgent

The core agent class that handles parking issue analysis.

#### Methods

- `analyze_issue()` - Comprehensive parking issue analysis
- `get_capabilities()` - List agent capabilities  
- `get_info()` - Agent information and status

### Tool Functions

- `analyze_parking_issue()` - Main analysis tool
- `search_parking_regulations()` - Regulation search
- `find_parking_enforcement_contacts()` - Contact lookup
- `generate_resolution_steps()` - Step generation

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`) 
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **MCP Documentation**: [Model Context Protocol](https://modelcontextprotocol.io/)
- **Issues**: [GitHub Issues](https://github.com/civicmind-ai/civicmind-parking-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/civicmind-ai/civicmind-parking-mcp-server/discussions)

---

**Part of the CivicMind AI Platform** - Building community-first civic solutions with AI agent integration.
