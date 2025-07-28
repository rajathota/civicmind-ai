# 🚀 CivicMind AI Deployment Guide

Comprehensive guide for deploying CivicMind AI in various environments, from development to production.

## 🏗️ Deployment Architecture Options

### **🏠 Self-Hosted (Recommended)**

**Benefits:**
- 🔒 Complete data sovereignty
- 💰 Cost-effective for small deployments
- 🎨 Fully customizable for local needs
- 📊 Direct control over analytics

**Ideal for:**
- Local governments
- Small to medium cities
- Privacy-conscious organizations
- Development and testing

```mermaid
graph TB
    A[🌐 Load Balancer] --> B[🚪 API Gateway]
    B --> C[🧠 CivicMind Core]
    C --> D[🗄️ PostgreSQL]
    C --> E[⚡ Redis Cache]
    C --> F[📊 Vector Store]
    
    G[🔐 SSL/TLS] --> A
    H[📈 Monitoring] --> C
    I[📱 Mobile Apps] --> A
    J[💻 Web Interface] --> A
```

### **☁️ Cloud-Native**

**Benefits:**
- 📈 Auto-scaling capabilities
- 🌍 Multi-region deployment
- 🛡️ Enterprise security features
- 🔧 Managed services integration

**Ideal for:**
- Large metropolitan areas
- Multi-city deployments
- High-availability requirements
- Enterprise integrations

```mermaid
graph TB
    subgraph "☁️ Cloud Provider"
        A[🌐 API Gateway] --> B[⚖️ Load Balancer]
        B --> C[🤖 Agent Pods]
        C --> D[🗄️ Managed DB]
        C --> E[📊 Vector Service]
        
        F[📈 Auto Scaling] --> C
        G[🔍 Monitoring] --> C
        H[🛡️ Security] --> A
    end
```

## 🐳 Docker Deployment

### **Single Container (Development)**

Perfect for development and testing:

```bash
# Build the container
docker build -t civicmind-ai .

# Run with environment variables
docker run -d \
  --name civicmind \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  -e CIVICMIND_PORT=8000 \
  -v $(pwd)/data:/app/data \
  civicmind-ai
```

### **Docker Compose (Recommended)**

Complete multi-service deployment:

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Main CivicMind API service
  civicmind-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
      - DATABASE_URL=postgresql://civicmind:password@postgres:5432/civicmind
      - REDIS_URL=redis://redis:6379
      - VECTOR_STORE_TYPE=chroma
      - VECTOR_STORE_PATH=/app/data/vectorstore
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL database
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=civicmind
      - POSTGRES_USER=civicmind
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U civicmind"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Nginx reverse proxy (optional)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - civicmind-api
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

**Deployment commands:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale the API service
docker-compose up -d --scale civicmind-api=3

# Stop all services
docker-compose down

# Complete cleanup
docker-compose down -v
```

## ☸️ Kubernetes Deployment

### **Basic Kubernetes Manifests**

**Namespace:**
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: civicmind
```

**ConfigMap:**
```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: civicmind-config
  namespace: civicmind
data:
  CIVICMIND_HOST: "0.0.0.0"
  CIVICMIND_PORT: "8000"
  VECTOR_STORE_TYPE: "chroma"
  VECTOR_STORE_PATH: "/app/data/vectorstore"
  DATABASE_URL: "postgresql://civicmind:password@postgres-service:5432/civicmind"
  REDIS_URL: "redis://redis-service:6379"
```

**Secret:**
```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: civicmind-secrets
  namespace: civicmind
type: Opaque
data:
  OPENAI_API_KEY: <base64-encoded-api-key>
  SECRET_KEY: <base64-encoded-secret-key>
```

**Deployment:**
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: civicmind-api
  namespace: civicmind
spec:
  replicas: 3
  selector:
    matchLabels:
      app: civicmind-api
  template:
    metadata:
      labels:
        app: civicmind-api
    spec:
      containers:
      - name: civicmind-api
        image: civicmind-ai:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: civicmind-config
        - secretRef:
            name: civicmind-secrets
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
        - name: logs-volume
          mountPath: /app/logs
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: civicmind-data-pvc
      - name: logs-volume
        persistentVolumeClaim:
          claimName: civicmind-logs-pvc
```

**Service:**
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: civicmind-api-service
  namespace: civicmind
spec:
  selector:
    app: civicmind-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

**Ingress:**
```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: civicmind-ingress
  namespace: civicmind
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - civicmind.yourdomain.com
    secretName: civicmind-tls
  rules:
  - host: civicmind.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: civicmind-api-service
            port:
              number: 80
```

**Deploy to Kubernetes:**
```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n civicmind

# View logs
kubectl logs -f deployment/civicmind-api -n civicmind

# Scale deployment
kubectl scale deployment civicmind-api --replicas=5 -n civicmind
```

## 🔧 Production Configuration

### **Environment Variables for Production**

```bash
# AI Configuration
OPENAI_API_KEY=your_production_api_key
CIVICMIND_MODEL=gpt-4o
CIVICMIND_TEMPERATURE=0.1

# Server Configuration
CIVICMIND_HOST=0.0.0.0
CIVICMIND_PORT=8000
CIVICMIND_RELOAD=false

# Database Configuration
DATABASE_URL=postgresql://username:password@db-host:5432/civicmind
REDIS_URL=redis://redis-host:6379

# Vector Store Configuration
VECTOR_STORE_TYPE=chroma
VECTOR_STORE_PATH=/app/data/vectorstore

# Security
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_ORIGINS=["https://yourdomain.com"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/civicmind.log

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_MONITORING=true
ENABLE_RATE_LIMITING=true

# Performance
WORKERS=4
MAX_CONNECTIONS=1000
TIMEOUT=60
```

### **Database Setup**

**PostgreSQL Setup:**
```sql
-- Create database and user
CREATE DATABASE civicmind;
CREATE USER civicmind WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE civicmind TO civicmind;

-- Create tables (auto-created by application)
-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
```

**Redis Configuration:**
```redis
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### **Nginx Configuration**

```nginx
# nginx.conf
upstream civicmind_backend {
    server civicmind-api:8000;
    # Add more servers for load balancing
    # server civicmind-api-2:8000;
    # server civicmind-api-3:8000;
}

server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    location / {
        proxy_pass http://civicmind_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://civicmind_backend/health;
        access_log off;
    }

    # Static files (if any)
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 📊 Monitoring and Observability

### **Health Checks**

The application provides several health check endpoints:

```bash
# Basic health check
curl https://yourdomain.com/health

# Detailed system status
curl https://yourdomain.com/api/v1/system/status

# Agent availability
curl https://yourdomain.com/api/v1/agents/health
```

### **Logging Configuration**

```python
# logging_config.py
import logging
import logging.handlers
from pathlib import Path

def setup_logging():
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                'logs/civicmind.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("civicmind").setLevel(logging.DEBUG)
```

### **Metrics Collection**

**Prometheus Configuration:**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'civicmind'
    static_configs:
      - targets: ['civicmind-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s
```

**Grafana Dashboard:**
```json
{
  "dashboard": {
    "title": "CivicMind AI Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

## 🔄 CI/CD Pipeline

### **GitHub Actions Workflow**

```yaml
# .github/workflows/deploy.yml
name: Deploy CivicMind AI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: pytest
    
    - name: Run linting
      run: |
        flake8 civicmind/
        black --check civicmind/
        mypy civicmind/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t civicmind-ai:${{ github.sha }} .
        docker tag civicmind-ai:${{ github.sha }} civicmind-ai:latest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push civicmind-ai:${{ github.sha }}
        docker push civicmind-ai:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        # Your deployment script here
        kubectl set image deployment/civicmind-api civicmind-api=civicmind-ai:${{ github.sha }}
        kubectl rollout status deployment/civicmind-api
```

## 🔒 Security Best Practices

### **API Security**

1. **Rate Limiting**: Implement request rate limiting
2. **Authentication**: Use JWT tokens for API access
3. **HTTPS Only**: Force SSL/TLS encryption
4. **Input Validation**: Sanitize all user inputs
5. **CORS Configuration**: Restrict cross-origin requests

### **Infrastructure Security**

1. **Network Segmentation**: Isolate services in VPCs/subnets
2. **Firewall Rules**: Restrict unnecessary ports
3. **Regular Updates**: Keep all dependencies updated
4. **Backup Strategy**: Regular encrypted backups
5. **Access Control**: Implement least-privilege access

### **Data Protection**

1. **Encryption at Rest**: Encrypt database and file storage
2. **Encryption in Transit**: Use TLS for all communications
3. **Data Retention**: Implement automatic data expiry
4. **Privacy Compliance**: GDPR/CCPA compliance measures
5. **Audit Logging**: Log all data access and changes

## 🚀 Scaling Strategies

### **Horizontal Scaling**

```bash
# Docker Compose scaling
docker-compose up -d --scale civicmind-api=5

# Kubernetes scaling
kubectl scale deployment civicmind-api --replicas=10
```

### **Vertical Scaling**

```yaml
# Increase resource limits
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### **Database Scaling**

1. **Read Replicas**: Separate read and write operations
2. **Connection Pooling**: Use PgBouncer for PostgreSQL
3. **Caching**: Implement Redis caching strategy
4. **Partitioning**: Partition large tables by date/location

## 📈 Performance Optimization

### **Application Level**

1. **Async Processing**: Use background tasks for heavy operations
2. **Caching**: Cache agent responses and API calls
3. **Connection Pooling**: Reuse database connections
4. **Compression**: Enable gzip compression
5. **CDN**: Use CDN for static assets

### **Database Optimization**

1. **Indexing**: Create appropriate database indexes
2. **Query Optimization**: Optimize slow queries
3. **Connection Limits**: Set appropriate connection limits
4. **Maintenance**: Regular VACUUM and ANALYZE

### **Infrastructure Optimization**

1. **Load Balancing**: Distribute traffic across instances
2. **Auto-scaling**: Automatic scaling based on metrics
3. **Resource Monitoring**: Monitor CPU, memory, and disk usage
4. **Network Optimization**: Optimize network latency

---

This deployment guide covers everything from simple development setups to enterprise-grade production deployments. Choose the deployment method that best fits your organization's needs and security requirements.
