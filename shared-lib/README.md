# CivicMind Common Library

Shared models, utilities, and base classes for CivicMind microservices architecture.

## Overview

This library provides common functionality used across all CivicMind services:

- **Base Models**: Standard request/response models
- **Agent Models**: AI agent-specific data structures  
- **Authentication**: JWT handling and security utilities
- **Health Checks**: Service health monitoring
- **Logging**: Structured logging for microservices
- **OpenAI Client**: Shared OpenAI integration

## Installation

```bash
pip install civicmind-common
```

## Usage

```python
from civicmind_common import CivicRequest, CivicResponse
from civicmind_common.utils.logging import setup_logging
from civicmind_common.utils.health_checks import HealthChecker

# Setup logging
logger = setup_logging("parking-service")

# Create health checker
health = HealthChecker("parking-service")
status = health.get_health_status()
```

## Development

```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black civicmind_common/

# Type checking
mypy civicmind_common/
```

## License

Apache 2.0 - See LICENSE file for details.
