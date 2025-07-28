# 🚀 CivicMind AI Deployment Guide

Complete deployment documentation for CivicMind AI platform covering development, staging, and production environments.

## 📋 Table of Contents

1. [Environment Overview](#environment-overview)
2. [Prerequisites](#prerequisites)
3. [Development Deployment](#development-deployment)
4. [Staging Environment](#staging-environment)
5. [Production Deployment](#production-deployment)
6. [Docker Configurations](#docker-configurations)
7. [Kubernetes Deployment](#kubernetes-deployment)
8. [Monitoring & Observability](#monitoring--observability)
9. [Security Configuration](#security-configuration)
10. [Scaling Strategies](#scaling-strategies)
11. [Troubleshooting](#troubleshooting)

---

## 🌍 Environment Overview

CivicMind AI supports three deployment environments, each optimized for different use cases:

| Environment | Purpose | Characteristics | Resource Requirements |
|-------------|---------|-----------------|----------------------|
| **Development** | Local development, testing | Hot reload, debug mode, minimal security | 8GB RAM, 4 CPU cores |
| **Staging** | Pre-production testing, demos | Production-like config, test data | 16GB RAM, 8 CPU cores |
| **Production** | Live municipal deployment | High availability, security, monitoring | 32GB RAM, 16 CPU cores |

### Port Allocation Strategy

```
Development:  8000-8999 (Services), 9000-9999 (MCP Servers)
Staging:      18000-18999 (Services), 19000-19999 (MCP Servers)  
Production:   80/443 (Gateway), Internal mesh networking
```

---

## 📦 Prerequisites

### System Requirements

#### Minimum (Development)
- **OS**: Linux, macOS, or Windows with WSL2
- **RAM**: 8GB
- **Storage**: 20GB free space
- **CPU**: 4 cores
- **Network**: Internet access for dependencies

#### Recommended (Production)
- **OS**: Ubuntu 22.04 LTS or RHEL 8+
- **RAM**: 32GB+
- **Storage**: 100GB+ SSD with backup
- **CPU**: 16+ cores
- **Network**: Load balancer, CDN, monitoring

### Software Dependencies

```bash
# Core dependencies
Python 3.11+
Docker 24.0+
Docker Compose 2.20+
Git 2.40+

# Production additional
Kubernetes 1.28+
Helm 3.12+
nginx or Traefik
PostgreSQL 15+
Redis 7.0+
```

### Pre-Deployment Checklist

```bash
# 1. Verify Docker installation
docker --version
docker compose version

# 2. Check system resources
free -h
df -h
nproc

# 3. Verify Python version
python3 --version
pip --version

# 4. Test network connectivity
curl -I https://github.com
curl -I https://pypi.org
```

---

## 🛠️ Development Deployment

### Quick Start (Local Development)

```bash
# 1. Clone repository
git clone https://github.com/rajathota/civicmind-ai.git
cd civicmind-ai

# 2. Install shared library
cd shared-lib
pip install -e .
cd ..

# 3. Start core services individually (for development)
./scripts/start-dev.sh
```

### Development Script

```bash
#!/bin/bash
# File: scripts/start-dev.sh

set -e

echo "🚀 Starting CivicMind AI Development Environment"

# Set development environment variables
export ENVIRONMENT=development
export LOG_LEVEL=DEBUG
export RELOAD=true

# Start API Gateway
echo "Starting API Gateway on port 8300..."
cd independent-services/civicmind-api-gateway
python main.py &
GATEWAY_PID=$!
cd ../..

# Start Orchestrator
echo "Starting Orchestrator on port 8000..."
cd independent-services/civicmind-orchestrator-service
python main.py &
ORCHESTRATOR_PID=$!
cd ../..

# Start Parking Service
echo "Starting Parking Service on port 8001..."
cd independent-services/civicmind-parking-service
python main.py &
PARKING_PID=$!
cd ../..

# Start Parking MCP Server
echo "Starting Parking MCP Server on port 9300..."
cd independent-services/civicmind-parking-mcp-server
python main.py &
PARKING_MCP_PID=$!
cd ../..

# Start other MCP servers
echo "Starting remaining MCP servers..."
for service in permits noise utilities housing business safety environmental; do
    echo "Starting ${service} MCP server..."
    cd independent-services/civicmind-${service}-mcp-server
    python main.py &
    cd ../..
done

echo "✅ Development environment started!"
echo "🌐 API Gateway: http://localhost:8300"
echo "🎭 Orchestrator: http://localhost:8000"
echo "🚗 Parking Service: http://localhost:8001"

# Create cleanup function
cleanup() {
    echo "🧹 Cleaning up processes..."
    kill $GATEWAY_PID $ORCHESTRATOR_PID $PARKING_PID $PARKING_MCP_PID 2>/dev/null || true
    pkill -f "python main.py" 2>/dev/null || true
    echo "✅ Cleanup complete"
}

# Register cleanup function
trap cleanup EXIT

# Wait for user to stop
echo "Press Ctrl+C to stop all services"
wait
```

### Development Docker Compose

```yaml
# File: deployment/docker-compose.dev.yml
version: '3.8'

services:
  # API Gateway
  api-gateway:
    build: 
      context: ./independent-services/civicmind-api-gateway
      target: development
    ports:
      - "8300:8300"
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - RELOAD=true
      - ORCHESTRATOR_URL=http://orchestrator:8000
    volumes:
      - ./independent-services/civicmind-api-gateway:/app
      - ./shared-lib:/shared-lib
    depends_on:
      - orchestrator
    networks:
      - civicmind-dev
    restart: unless-stopped

  # Orchestrator Service
  orchestrator:
    build:
      context: ./independent-services/civicmind-orchestrator-service
      target: development
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - RELOAD=true
      - DATABASE_URL=sqlite:///./dev.db
    volumes:
      - ./independent-services/civicmind-orchestrator-service:/app
      - ./shared-lib:/shared-lib
    networks:
      - civicmind-dev
    restart: unless-stopped

  # Parking Service
  parking-service:
    build:
      context: ./independent-services/civicmind-parking-service
      target: development
    ports:
      - "8001:8001"
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - RELOAD=true
    volumes:
      - ./independent-services/civicmind-parking-service:/app
      - ./shared-lib:/shared-lib
    networks:
      - civicmind-dev
    restart: unless-stopped

  # Parking MCP Server
  parking-mcp:
    build:
      context: ./independent-services/civicmind-parking-mcp-server
      target: development
    ports:
      - "9300:9300"
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - PARKING_SERVICE_URL=http://parking-service:8001
    volumes:
      - ./independent-services/civicmind-parking-mcp-server:/app
      - ./shared-lib:/shared-lib
    networks:
      - civicmind-dev
    restart: unless-stopped

  # Development Database
  postgres-dev:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: civicmind_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data
      - ./sql/init-dev.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - civicmind-dev

  # Development Redis
  redis-dev:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - civicmind-dev

networks:
  civicmind-dev:
    driver: bridge

volumes:
  postgres_dev_data:
```

### Development Commands

```bash
# Start development environment
docker compose -f deployment/docker-compose.dev.yml up

# Start with rebuild
docker compose -f deployment/docker-compose.dev.yml up --build

# Start detached (background)
docker compose -f deployment/docker-compose.dev.yml up -d

# View logs
docker compose -f deployment/docker-compose.dev.yml logs -f api-gateway

# Stop environment
docker compose -f deployment/docker-compose.dev.yml down

# Reset environment (removes data)
docker compose -f deployment/docker-compose.dev.yml down -v
```

---

## 🧪 Staging Environment

### Staging Configuration

```yaml
# File: deployment/docker-compose.staging.yml
version: '3.8'

services:
  # Nginx Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./deployment/nginx/staging.conf:/etc/nginx/nginx.conf
      - ./deployment/ssl:/etc/ssl/certs
    depends_on:
      - api-gateway
    networks:
      - civicmind-staging
    restart: unless-stopped

  # API Gateway (Scaled)
  api-gateway:
    build:
      context: ./independent-services/civicmind-api-gateway
      target: production
    ports:
      - "18300:8300"
    environment:
      - ENVIRONMENT=staging
      - LOG_LEVEL=INFO
      - ORCHESTRATOR_URL=http://orchestrator:8000
      - DATABASE_URL=postgresql://staging_user:staging_password@postgres:5432/civicmind_staging
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
      - orchestrator
    networks:
      - civicmind-staging
    restart: unless-stopped
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

  # Orchestrator Service (Scaled)
  orchestrator:
    build:
      context: ./independent-services/civicmind-orchestrator-service
      target: production
    ports:
      - "18000:8000"
    environment:
      - ENVIRONMENT=staging
      - LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://staging_user:staging_password@postgres:5432/civicmind_staging
      - REDIS_URL=redis://redis:6379/1
    depends_on:
      - postgres
      - redis
    networks:
      - civicmind-staging
    restart: unless-stopped
    deploy:
      replicas: 2

  # All Service APIs (8001-8008)
  parking-service:
    build:
      context: ./independent-services/civicmind-parking-service
      target: production
    environment:
      - ENVIRONMENT=staging
      - DATABASE_URL=postgresql://staging_user:staging_password@postgres:5432/civicmind_staging
    networks:
      - civicmind-staging
    restart: unless-stopped

  permits-service:
    build:
      context: ./independent-services/civicmind-permits-service
      target: production
    environment:
      - ENVIRONMENT=staging
      - DATABASE_URL=postgresql://staging_user:staging_password@postgres:5432/civicmind_staging
    networks:
      - civicmind-staging
    restart: unless-stopped

  # All MCP Servers (9300-9307)
  parking-mcp:
    build:
      context: ./independent-services/civicmind-parking-mcp-server
      target: production
    environment:
      - ENVIRONMENT=staging
      - PARKING_SERVICE_URL=http://parking-service:8001
    networks:
      - civicmind-staging
    restart: unless-stopped

  permits-mcp:
    build:
      context: ./independent-services/civicmind-permits-mcp-server
      target: production
    environment:
      - ENVIRONMENT=staging
      - PERMITS_SERVICE_URL=http://permits-service:8002
    networks:
      - civicmind-staging
    restart: unless-stopped

  # Production-grade Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: civicmind_staging
      POSTGRES_USER: staging_user
      POSTGRES_PASSWORD: ${STAGING_DB_PASSWORD}
    volumes:
      - postgres_staging_data:/var/lib/postgresql/data
      - ./sql/init-staging.sql:/docker-entrypoint-initdb.d/init.sql
      - ./deployment/postgres/postgresql.staging.conf:/etc/postgresql/postgresql.conf
    networks:
      - civicmind-staging
    restart: unless-stopped

  # Redis for Caching
  redis:
    image: redis:7-alpine
    volumes:
      - redis_staging_data:/data
      - ./deployment/redis/redis.staging.conf:/usr/local/etc/redis/redis.conf
    networks:
      - civicmind-staging
    restart: unless-stopped

  # Monitoring Stack
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./deployment/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - civicmind-staging
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./deployment/grafana/dashboards:/etc/grafana/provisioning/dashboards
    networks:
      - civicmind-staging
    restart: unless-stopped

networks:
  civicmind-staging:
    driver: bridge

volumes:
  postgres_staging_data:
  redis_staging_data:
  prometheus_data:
  grafana_data:
```

### Staging Deployment Commands

```bash
# Deploy staging environment
docker compose -f deployment/docker-compose.staging.yml up -d

# Scale services
docker compose -f deployment/docker-compose.staging.yml up -d --scale api-gateway=3 --scale orchestrator=2

# Rolling update
docker compose -f deployment/docker-compose.staging.yml up -d --force-recreate api-gateway

# Monitor logs
docker compose -f deployment/docker-compose.staging.yml logs -f

# Health check
curl -f http://staging.civicmind.local/health
```

---

## 🏭 Production Deployment

### Production Architecture Overview

```mermaid
graph TB
    subgraph "Load Balancer Layer"
        LB[Load Balancer]
        CDN[CDN/Edge Cache]
    end
    
    subgraph "API Gateway Cluster"
        GW1[Gateway 1]
        GW2[Gateway 2] 
        GW3[Gateway 3]
    end
    
    subgraph "Service Mesh"
        ORCH1[Orchestrator 1]
        ORCH2[Orchestrator 2]
        
        subgraph "Service APIs"
            SVC1[Parking Service]
            SVC2[Permits Service]
            SVC3[Utilities Service]
            SVC4[Housing Service]
        end
        
        subgraph "MCP Servers"
            MCP1[Parking MCP]
            MCP2[Permits MCP]
            MCP3[Utilities MCP] 
            MCP4[Housing MCP]
        end
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL Cluster)]
        REDIS[(Redis Cluster)]
    end
    
    subgraph "Monitoring"
        PROM[Prometheus]
        GRAF[Grafana]
        ALERT[AlertManager]
    end
    
    CDN --> LB
    LB --> GW1
    LB --> GW2
    LB --> GW3
    
    GW1 --> ORCH1
    GW2 --> ORCH2
    
    ORCH1 --> SVC1
    ORCH1 --> SVC2
    ORCH2 --> SVC3
    ORCH2 --> SVC4
    
    SVC1 <--> MCP1
    SVC2 <--> MCP2
    SVC3 <--> MCP3
    SVC4 <--> MCP4
    
    SVC1 --> PG
    SVC2 --> PG
    SVC1 --> REDIS
    SVC2 --> REDIS
```

### Production Docker Compose

```yaml
# File: deployment/docker-compose.prod.yml
version: '3.8'

services:
  # Production Load Balancer
  traefik:
    image: traefik:v3.0
    command:
      - "--api.dashboard=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--providers.docker=true"
      - "--certificatesresolvers.letsencrypt.acme.email=${ACME_EMAIL}"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Traefik dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt_data:/letsencrypt
    networks:
      - civicmind-prod
    restart: unless-stopped

  # API Gateway Cluster
  api-gateway:
    image: civicmind/api-gateway:${VERSION}
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
      - DATABASE_URL=${PRODUCTION_DATABASE_URL}
      - REDIS_URL=${PRODUCTION_REDIS_URL}
      - JWT_SECRET=${JWT_SECRET}
      - RATE_LIMIT_ENABLED=true
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api-gateway.rule=Host(`api.civicmind.ai`)"
      - "traefik.http.routers.api-gateway.tls.certresolver=letsencrypt"
      - "traefik.http.services.api-gateway.loadbalancer.server.port=8300"
      - "traefik.http.middlewares.api-gateway-auth.basicauth.users=${API_GATEWAY_USERS}"
    depends_on:
      - postgres-primary
      - redis-cluster
    networks:
      - civicmind-prod
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

  # Orchestrator Cluster
  orchestrator:
    image: civicmind/orchestrator:${VERSION}
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
      - DATABASE_URL=${PRODUCTION_DATABASE_URL}
      - REDIS_URL=${PRODUCTION_REDIS_URL}
      - KAFKA_BROKERS=${KAFKA_BROKERS}
    networks:
      - civicmind-prod
    restart: unless-stopped
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 3G
          cpus: '1.5'

  # Production Database Cluster
  postgres-primary:
    image: postgres:15
    environment:
      POSTGRES_DB: civicmind_prod
      POSTGRES_USER: ${PROD_DB_USER}
      POSTGRES_PASSWORD: ${PROD_DB_PASSWORD}
      POSTGRES_REPLICATION_MODE: master
      POSTGRES_REPLICATION_USER: ${REPLICATION_USER}
      POSTGRES_REPLICATION_PASSWORD: ${REPLICATION_PASSWORD}
    volumes:
      - postgres_primary_data:/var/lib/postgresql/data
      - ./deployment/postgres/postgresql.prod.conf:/etc/postgresql/postgresql.conf
      - ./sql/init-prod.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - civicmind-prod
    restart: unless-stopped

  postgres-replica:
    image: postgres:15
    environment:
      POSTGRES_MASTER_SERVICE: postgres-primary
      POSTGRES_REPLICATION_MODE: slave
      POSTGRES_REPLICATION_USER: ${REPLICATION_USER}
      POSTGRES_REPLICATION_PASSWORD: ${REPLICATION_PASSWORD}
    depends_on:
      - postgres-primary
    networks:
      - civicmind-prod
    restart: unless-stopped

  # Redis Cluster
  redis-cluster:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf --cluster-enabled yes
    volumes:
      - redis_cluster_data:/data
      - ./deployment/redis/redis.prod.conf:/usr/local/etc/redis/redis.conf
    networks:
      - civicmind-prod
    restart: unless-stopped

  # Message Queue
  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: false
    depends_on:
      - zookeeper
    volumes:
      - kafka_data:/var/lib/kafka/data
    networks:
      - civicmind-prod
    restart: unless-stopped

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper_data:/var/lib/zookeeper/data
    networks:
      - civicmind-prod
    restart: unless-stopped

networks:
  civicmind-prod:
    driver: bridge

volumes:
  postgres_primary_data:
  redis_cluster_data:
  kafka_data:
  zookeeper_data:
  letsencrypt_data:
```

### Production Environment Variables

```bash
# File: deployment/.env.prod
# Database Configuration
PRODUCTION_DATABASE_URL=postgresql://prod_user:secure_password@postgres-primary:5432/civicmind_prod
PROD_DB_USER=prod_user
PROD_DB_PASSWORD=secure_password_here
REPLICATION_USER=repl_user
REPLICATION_PASSWORD=repl_password_here

# Redis Configuration
PRODUCTION_REDIS_URL=redis://redis-cluster:6379/0

# Application Configuration
VERSION=latest
JWT_SECRET=very_secure_jwt_secret_here
API_GATEWAY_USERS=admin:hashed_password_here

# SSL Configuration
ACME_EMAIL=admin@civicmind.ai

# Kafka Configuration
KAFKA_BROKERS=kafka:9092

# Monitoring
GRAFANA_PASSWORD=secure_grafana_password
PROMETHEUS_PASSWORD=secure_prometheus_password

# External Services
EXTERNAL_API_KEY=external_service_api_key
SMTP_PASSWORD=email_service_password
```

### Production Deployment Script

```bash
#!/bin/bash
# File: scripts/deploy-production.sh

set -e

echo "🏭 Starting CivicMind AI Production Deployment"

# Pre-deployment checks
echo "🔍 Running pre-deployment checks..."

# Check if all required environment variables are set
required_vars=(
    "PRODUCTION_DATABASE_URL"
    "PROD_DB_PASSWORD"
    "JWT_SECRET"
    "ACME_EMAIL"
)

for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "❌ Error: Environment variable $var is not set"
        exit 1
    fi
done

# Check system resources
echo "📊 Checking system resources..."
available_memory=$(free -m | awk 'NR==2{printf "%.0f", $7}')
if [[ $available_memory -lt 8000 ]]; then
    echo "⚠️  Warning: Available memory is ${available_memory}MB, recommended minimum is 8000MB"
fi

# Check disk space
available_disk=$(df -h / | awk 'NR==2{print $4}' | sed 's/G//')
if [[ ${available_disk%.*} -lt 50 ]]; then
    echo "⚠️  Warning: Available disk space is ${available_disk}GB, recommended minimum is 50GB"
fi

# Backup existing deployment
echo "💾 Creating backup of existing deployment..."
if docker compose -f deployment/docker-compose.prod.yml ps -q > /dev/null 2>&1; then
    docker compose -f deployment/docker-compose.prod.yml exec postgres-primary pg_dump -U $PROD_DB_USER civicmind_prod > backup-$(date +%Y%m%d-%H%M%S).sql
    echo "✅ Database backup created"
fi

# Pull latest images
echo "📥 Pulling latest images..."
docker compose -f deployment/docker-compose.prod.yml pull

# Deploy with rolling update
echo "🚀 Deploying production environment..."
docker compose -f deployment/docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health checks
echo "🏥 Running health checks..."
services=("api-gateway" "orchestrator" "postgres-primary" "redis-cluster")
for service in "${services[@]}"; do
    if ! docker compose -f deployment/docker-compose.prod.yml exec $service echo "Health check" > /dev/null 2>&1; then
        echo "❌ Health check failed for $service"
        exit 1
    fi
done

# API health check
if ! curl -f http://localhost/health > /dev/null 2>&1; then
    echo "❌ API health check failed"
    exit 1
fi

echo "✅ Production deployment completed successfully!"
echo "🌐 Access: https://api.civicmind.ai"
echo "📊 Monitoring: https://monitoring.civicmind.ai"
echo "📈 Grafana: https://grafana.civicmind.ai"

# Post-deployment tasks
echo "📋 Running post-deployment tasks..."

# Database migrations
echo "🗄️  Running database migrations..."
docker compose -f deployment/docker-compose.prod.yml exec api-gateway python -m alembic upgrade head

# Cache warming
echo "🔥 Warming up caches..."
curl -X POST http://localhost/admin/cache/warm > /dev/null 2>&1

# Send deployment notification
echo "📧 Sending deployment notification..."
curl -X POST "${SLACK_WEBHOOK_URL}" \
     -H 'Content-Type: application/json' \
     -d "{\"text\":\"✅ CivicMind AI production deployment completed successfully at $(date)\"}" > /dev/null 2>&1

echo "🎉 Deployment process completed!"
```

---

## ☸️ Kubernetes Deployment

### Kubernetes Namespace

```yaml
# File: deployment/kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: civicmind-prod
  labels:
    name: civicmind-prod
    environment: production
```

### ConfigMap

```yaml
# File: deployment/kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: civicmind-config
  namespace: civicmind-prod
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  RATE_LIMIT_ENABLED: "true"
  DATABASE_NAME: "civicmind_prod"
  REDIS_DB: "0"
```

### Secrets

```yaml
# File: deployment/kubernetes/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: civicmind-secrets
  namespace: civicmind-prod
type: Opaque
data:
  database-url: cG9zdGdyZXNxbCovL3VzZXI6cGFzc3dvcmRAaG9zdDo1NDMyL2RibmFtZQ==  # base64 encoded
  jwt-secret: anwtc2VjcmV0LWtleQ==  # base64 encoded
  redis-url: cmVkaXM6Ly9yZWRpcy1jbHVzdGVyOjYzNzkvMA==  # base64 encoded
```

### API Gateway Deployment

```yaml
# File: deployment/kubernetes/api-gateway-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: civicmind-prod
  labels:
    app: api-gateway
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
        version: v1
    spec:
      containers:
      - name: api-gateway
        image: civicmind/api-gateway:latest
        ports:
        - containerPort: 8300
        env:
        - name: ENVIRONMENT
          valueFrom:
            configMapKeyRef:
              name: civicmind-config
              key: ENVIRONMENT
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: civicmind-secrets
              key: database-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: civicmind-secrets
              key: jwt-secret
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8300
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8300
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: api-gateway-service
  namespace: civicmind-prod
spec:
  selector:
    app: api-gateway
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8300
  type: LoadBalancer
```

### Ingress Configuration

```yaml
# File: deployment/kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: civicmind-ingress
  namespace: civicmind-prod
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - api.civicmind.gov
    secretName: civicmind-tls
  rules:
  - host: api.civicmind.gov
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway-service
            port:
              number: 80
```

### PostgreSQL StatefulSet

```yaml
# File: deployment/kubernetes/postgres-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-primary
  namespace: civicmind-prod
spec:
  serviceName: postgres-primary-service
  replicas: 1
  selector:
    matchLabels:
      app: postgres-primary
  template:
    metadata:
      labels:
        app: postgres-primary
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: civicmind_prod
        - name: POSTGRES_USER
          value: prod_user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
      storageClassName: fast-ssd
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-primary-service
  namespace: civicmind-prod
spec:
  selector:
    app: postgres-primary
  ports:
  - port: 5432
    targetPort: 5432
  clusterIP: None
```

### Kubernetes Deployment Commands

```bash
# Create namespace
kubectl apply -f deployment/kubernetes/namespace.yaml

# Apply configurations
kubectl apply -f deployment/kubernetes/configmap.yaml
kubectl apply -f deployment/kubernetes/secrets.yaml

# Deploy database
kubectl apply -f deployment/kubernetes/postgres-statefulset.yaml

# Deploy application services
kubectl apply -f deployment/kubernetes/api-gateway-deployment.yaml
kubectl apply -f deployment/kubernetes/orchestrator-deployment.yaml

# Configure networking
kubectl apply -f deployment/kubernetes/ingress.yaml

# Check deployment status
kubectl get pods -n civicmind-prod
kubectl get services -n civicmind-prod

# Scale services
kubectl scale deployment api-gateway --replicas=5 -n civicmind-prod

# Rolling update
kubectl set image deployment/api-gateway api-gateway=civicmind/api-gateway:v2.0 -n civicmind-prod

# View logs
kubectl logs -f deployment/api-gateway -n civicmind-prod
```

---

## 📊 Monitoring & Observability

### Prometheus Configuration

```yaml
# File: deployment/monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "civicmind-rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'civicmind-api-gateway'
    static_configs:
      - targets: ['api-gateway:8300']
    metrics_path: /metrics
    scrape_interval: 10s

  - job_name: 'civicmind-orchestrator'
    static_configs:
      - targets: ['orchestrator:8000']
    metrics_path: /metrics

  - job_name: 'civicmind-services'
    static_configs:
      - targets: 
        - 'parking-service:8001'
        - 'permits-service:8002'
        - 'utilities-service:8003'
        - 'housing-service:8004'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "CivicMind AI Platform Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{job=\"civicmind-api-gateway\"}[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Response Times",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"civicmind-api-gateway\"}[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Service Health",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=~\"civicmind.*\"}",
            "legendFormat": "{{instance}}"
          }
        ]
      }
    ]
  }
}
```

### AlertManager Rules

```yaml
# File: deployment/monitoring/civicmind-rules.yml
groups:
- name: civicmind-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value }} errors per second"

  - alert: HighResponseTime
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High response time detected"
      description: "95th percentile response time is {{ $value }} seconds"

  - alert: DatabaseDown
    expr: up{job="postgres"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Database is down"
      description: "PostgreSQL database is not responding"

  - alert: LowDiskSpace
    expr: (node_filesystem_free_bytes / node_filesystem_size_bytes) * 100 < 20
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Low disk space"
      description: "Disk space is below 20%"
```

---

## 🔒 Security Configuration

### SSL/TLS Configuration

```nginx
# File: deployment/nginx/ssl.conf
server {
    listen 443 ssl http2;
    server_name api.civicmind.gov;

    ssl_certificate /etc/ssl/certs/civicmind.crt;
    ssl_certificate_key /etc/ssl/private/civicmind.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    
    location / {
        proxy_pass http://api-gateway:8300;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Rate limiting
        limit_req zone=api burst=20 nodelay;
        
        # Security
        proxy_hide_header X-Powered-By;
    }
}
```

### Environment Security

```bash
# File: deployment/security-checklist.sh
#!/bin/bash

echo "🔒 CivicMind AI Security Checklist"

# Check for default passwords
echo "🔍 Checking for default passwords..."
if grep -r "password" deployment/.env.prod | grep -q "default\|admin\|password"; then
    echo "❌ Default passwords found in environment files"
    exit 1
fi

# Check SSL certificates
echo "🔍 Checking SSL certificates..."
if ! openssl x509 -in deployment/ssl/civicmind.crt -text -noout > /dev/null 2>&1; then
    echo "❌ Invalid SSL certificate"
    exit 1
fi

# Check file permissions
echo "🔍 Checking file permissions..."
find deployment/ -name "*.key" -exec ls -la {} \; | awk '{if ($1 !~ /^-rw-------/) print "❌ Insecure key file permissions: " $9}'

# Check Docker security
echo "🔍 Checking Docker security..."
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy:latest image civicmind/api-gateway:latest

echo "✅ Security checklist completed"
```

---

## 📈 Scaling Strategies

### Horizontal Pod Autoscaler (Kubernetes)

```yaml
# File: deployment/kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway-hpa
  namespace: civicmind-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Load Testing Configuration

```python
# File: tests/load/locustfile.py
from locust import HttpUser, task, between

class CivicMindUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login and get authentication token"""
        self.token = self.login()
    
    def login(self):
        response = self.client.post("/auth/login", json={
            "username": "test_user",
            "password": "test_password"
        })
        return response.json().get("access_token")
    
    @task(3)
    def analyze_issue(self):
        """Test issue analysis endpoint"""
        self.client.post(
            "/api/v1/issues/analyze",
            json={"query": "My neighbor is parking in front of my driveway"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(2)
    def search_services(self):
        """Test service search"""
        self.client.get(
            "/api/v1/services/search",
            params={"q": "parking permits"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(1)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/health")

# Load testing commands:
# locust -f tests/load/locustfile.py --host=https://api.civicmind.gov
# locust -f tests/load/locustfile.py --host=https://api.civicmind.gov --users 100 --spawn-rate 10
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: Services Can't Connect to Database

```bash
# Diagnosis
docker compose -f deployment/docker-compose.prod.yml logs postgres-primary
docker compose -f deployment/docker-compose.prod.yml exec api-gateway ping postgres-primary

# Solutions
# 1. Check network connectivity
docker network ls
docker network inspect civicmind-prod

# 2. Verify environment variables
docker compose -f deployment/docker-compose.prod.yml exec api-gateway env | grep DATABASE

# 3. Reset database connections
docker compose -f deployment/docker-compose.prod.yml restart postgres-primary
```

#### Issue: High Memory Usage

```bash
# Diagnosis
docker stats
docker compose -f deployment/docker-compose.prod.yml exec api-gateway ps aux

# Solutions
# 1. Increase memory limits
# Edit docker-compose.prod.yml and increase memory limits

# 2. Optimize application configuration
# Reduce worker processes or adjust cache sizes

# 3. Scale horizontally
docker compose -f deployment/docker-compose.prod.yml up -d --scale api-gateway=5
```

#### Issue: SSL Certificate Problems

```bash
# Diagnosis
openssl x509 -in deployment/ssl/civicmind.crt -text -noout
curl -I https://api.civicmind.gov

# Solutions
# 1. Renew certificate
certbot renew --nginx

# 2. Update certificate in deployment
cp /etc/letsencrypt/live/api.civicmind.gov/fullchain.pem deployment/ssl/civicmind.crt
cp /etc/letsencrypt/live/api.civicmind.gov/privkey.pem deployment/ssl/civicmind.key

# 3. Restart services
docker compose -f deployment/docker-compose.prod.yml restart traefik
```

### Debugging Commands

```bash
# View all container logs
docker compose -f deployment/docker-compose.prod.yml logs -f

# Debug specific service
docker compose -f deployment/docker-compose.prod.yml exec api-gateway bash
docker compose -f deployment/docker-compose.prod.yml exec postgres-primary psql -U prod_user civicmind_prod

# Check resource usage
docker system df
docker system prune -a

# Network debugging
docker compose -f deployment/docker-compose.prod.yml exec api-gateway netstat -tlnp
docker compose -f deployment/docker-compose.prod.yml exec api-gateway nslookup postgres-primary

# Database debugging
docker compose -f deployment/docker-compose.prod.yml exec postgres-primary pg_stat_activity

# Performance monitoring
docker compose -f deployment/docker-compose.prod.yml exec api-gateway top
docker compose -f deployment/docker-compose.prod.yml exec redis-cluster redis-cli info memory
```

### Recovery Procedures

```bash
#!/bin/bash
# File: scripts/disaster-recovery.sh

echo "🚨 Starting disaster recovery procedure..."

# 1. Stop all services
docker compose -f deployment/docker-compose.prod.yml down

# 2. Restore database from backup
docker run --rm -v $(pwd)/backups:/backups postgres:15 \
    psql -h postgres-primary -U prod_user -d civicmind_prod < /backups/latest.sql

# 3. Clear Redis cache
docker compose -f deployment/docker-compose.prod.yml exec redis-cluster redis-cli FLUSHALL

# 4. Restart services with health checks
docker compose -f deployment/docker-compose.prod.yml up -d

# 5. Verify system health
sleep 60
curl -f https://api.civicmind.gov/health

echo "✅ Disaster recovery completed"
```

---

## ✅ Deployment Checklist

### Pre-Deployment

- [ ] Environment variables configured
- [ ] SSL certificates valid and installed
- [ ] Database migrations tested
- [ ] Security scan completed
- [ ] Load testing performed
- [ ] Backup procedures verified
- [ ] Monitoring configured
- [ ] DNS records configured

### During Deployment

- [ ] Rolling deployment strategy used
- [ ] Health checks passing
- [ ] Database connections verified
- [ ] Cache warming completed
- [ ] SSL/TLS working correctly
- [ ] Rate limiting active
- [ ] Monitoring data flowing

### Post-Deployment

- [ ] End-to-end tests passed
- [ ] Performance metrics normal
- [ ] Error rates within acceptable limits
- [ ] Alerts configured and tested
- [ ] Documentation updated
- [ ] Team notified
- [ ] Rollback plan ready

---

This comprehensive deployment guide covers all aspects of deploying CivicMind AI from development to production environments, ensuring reliable, secure, and scalable deployment of the platform.
