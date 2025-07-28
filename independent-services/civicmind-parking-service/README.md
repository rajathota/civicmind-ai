# CivicMind Parking Service

**Independent microservice for parking-related civic issues**

[![CI/CD](https://github.com/civicmind-ai/civicmind-parking-service/workflows/Parking%20Service%20CI/CD/badge.svg)](https://github.com/civicmind-ai/civicmind-parking-service/actions)
[![codecov](https://codecov.io/gh/civicmind-ai/civicmind-parking-service/branch/main/graph/badge.svg)](https://codecov.io/gh/civicmind-ai/civicmind-parking-service)

## Overview

The CivicMind Parking Service is a standalone microservice that specializes in analyzing and providing solutions for parking-related civic issues. Built with community-first principles, it offers intelligent analysis and actionable recommendations for parking problems in urban environments.

## Features

- **Intelligent Analysis**: AI-powered analysis of parking issues
- **Community-First Solutions**: Recommendations prioritizing community needs
- **RESTful API**: Clean, well-documented REST endpoints
- **Health Monitoring**: Built-in health checks and metrics
- **Docker Support**: Containerized for easy deployment
- **Production Ready**: Comprehensive logging, error handling, and monitoring

## API Endpoints

### Core Endpoints

- `GET /` - Service information and status
- `GET /health` - Health check for monitoring
- `GET /info` - Detailed service information
- `GET /metrics` - Service metrics and uptime
- `POST /analyze` - Analyze parking issues

### Documentation

- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/civicmind-ai/civicmind-parking-service.git
cd civicmind-parking-service

# Run with docker-compose
docker-compose up --build

# Service available at http://localhost:8001
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run the service
parking-service

# Or with Python directly
python -m parking_service.main
```

### Example Usage

```bash
# Analyze a parking issue
curl -X POST http://localhost:9300/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My neighbor parks blocking my driveway every night",
    "location": "Folsom, CA",
    "context": {"priority": "high"}
  }'
```

### Response Format

```json
{
  "issue_id": "parking-1690502400",
  "service_info": {
    "service": "parking-service",
    "version": "1.0.0",
    "agent_type": "parking",
    "port": 9300
  },
  "analysis": {
    "classification": {
      "type": "parking",
      "confidence": 0.95,
      "subtype": "driveway_blocking"
    },
    "recommendations": [...],
    "next_steps": [...],
    "community_first_approach": true,
    "contacts": [...]
  },
  "processing_time_ms": 45.2,
  "timestamp": "2025-07-28T10:30:00Z",
  "status": "completed"
}
```

## Architecture Benefits

### Independent Deployment
- Deploy parking service without affecting other civic services
- Scale based on parking-specific demand
- Independent release cycles

### Technology Freedom
- Choose optimal tech stack for parking domain
- Upgrade dependencies independently
- Customize for parking-specific requirements

### Team Ownership
- Parking team owns entire service lifecycle
- Clear boundaries and responsibilities
- Faster development and iteration

## Configuration

### Environment Variables

```bash
# Service configuration
PARKING_SERVICE_PORT=9300
PARKING_SERVICE_HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# External dependencies
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://...
```

### Health Checks

The service provides comprehensive health checks:

```bash
curl http://localhost:9300/health
```

Returns:
- Service status and uptime
- Agent initialization status
- Memory usage checks
- External dependency status

## Development

### Local Setup

```bash
# Clone the parking service repository
git clone https://github.com/civicmind/parking-service.git
cd parking-service

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with auto-reload
uvicorn main:app --reload --port 9300
```

### Testing

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Load testing
artillery run load-test.yml
```

## Monitoring

### Metrics Endpoint

```bash
curl http://localhost:9300/metrics
```

Provides:
- Service uptime
- Request counts
- Error rates
- Response times
- Agent status

### Logging

Structured JSON logs for easy parsing:

```json
{
  "timestamp": "2025-07-28T10:30:00Z",
  "service": "parking-service",
  "level": "INFO",
  "message": "Analysis completed",
  "processing_time_ms": 45.2,
  "issue_type": "driveway_blocking"
}
```

## Deployment

### Production Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  parking-service:
    image: civicmind/parking-service:latest
    ports:
      - "9300:9300"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9300/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: parking-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: parking-service
  template:
    metadata:
      labels:
        app: parking-service
    spec:
      containers:
      - name: parking-service
        image: civicmind/parking-service:latest
        ports:
        - containerPort: 9300
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: civicmind-secrets
              key: openai-api-key
```

## Contributing

1. Fork the parking service repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

Apache 2.0 - See LICENSE file for details.

## Support

- **Issues**: GitHub Issues
- **Documentation**: Service docs at `/docs`
- **Team**: parking-team@civicmind.ai
