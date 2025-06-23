# Deployment Guide

This guide provides comprehensive instructions for deploying the AI-Backed Community Legal Aid Assistant across different environments and platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [NodeOps Deployment](#nodeops-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Production Considerations](#production-considerations)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 2GB
- Storage: 10GB
- Network: Internet connection for LLM API calls

**Recommended Requirements:**
- CPU: 4 cores
- RAM: 4GB
- Storage: 20GB
- Network: High-speed internet connection

### Software Dependencies

**Required:**
- Docker 20.10+
- Docker Compose 2.0+
- Git

**Optional:**
- Kubernetes 1.20+ (for NodeOps/K8s deployment)
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### External Services

**Required:**
- OpenAI API key (or local LLM setup)

**Optional:**
- PostgreSQL database (for production)
- Redis (for caching and rate limiting)
- Email service (for notifications)

## Environment Configuration

### Environment Variables

Create a `.env` file based on `.env.production`:

```bash
# Copy the template
cp .env.production .env

# Edit with your values
nano .env
```

### Critical Settings

**Security (Required):**
```bash
SECRET_KEY=your-super-secure-secret-key-here
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Database (Production):**
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/legal_aid_db
```

**Application:**
```bash
DEBUG=false
DEFAULT_JURISDICTION=US
DOMAIN_NAME=your-domain.com
```

### Configuration Validation

Validate your configuration:

```bash
# Check environment file
./deploy.sh validate-config

# Test database connection
docker-compose exec backend python -c "from app.core.database import engine; print('Database OK' if engine else 'Database Error')"

# Test LLM connection
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"description": "test issue"}'
```

## Local Development

### Quick Start

```bash
# Clone repository
git clone <repository-url>
cd legal-aid-assistant

# Start development environment
./deploy.sh dev

# Access application
open http://localhost:3000
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend/legal-aid-frontend
npm install
npm run dev
```

### Development Tools

**API Testing:**
```bash
# Install HTTPie
pip install httpie

# Test endpoints
http POST localhost:8000/api/analyze description="test issue"
```

**Database Management:**
```bash
# View database
sqlite3 backend/legal_aid.db ".tables"

# Reset database
rm backend/legal_aid.db
python backend/init_db.py
```

## Docker Deployment

### Single-Host Deployment

**Development:**
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Production:**
```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### Docker Swarm

**Initialize Swarm:**
```bash
docker swarm init
```

**Deploy Stack:**
```bash
# Deploy to swarm
docker stack deploy -c docker-compose.prod.yml legal-aid

# Check services
docker service ls
docker service logs legal-aid_backend
```

**Update Services:**
```bash
# Update backend
docker service update --image legal-aid-backend:v2 legal-aid_backend

# Scale frontend
docker service scale legal-aid_frontend=3
```

### Health Checks

```bash
# Check container health
docker-compose ps

# Manual health check
curl http://localhost:8000/api/health
curl http://localhost:3000/health
```

## NodeOps Deployment

### Prerequisites

1. NodeOps account and CLI
2. Kubernetes cluster access
3. Container registry access

### Preparation

**Build and Push Images:**
```bash
# Build images
docker build -t your-registry/legal-aid-backend:v1 ./backend
docker build -t your-registry/legal-aid-frontend:v1 ./frontend/legal-aid-frontend

# Push to registry
docker push your-registry/legal-aid-backend:v1
docker push your-registry/legal-aid-frontend:v1
```

**Update Deployment Configuration:**
```yaml
# Edit nodeops-deployment.yaml
spec:
  containers:
  - name: backend
    image: your-registry/legal-aid-backend:v1
```

### Deployment Steps

**1. Create Secrets:**
```bash
kubectl create secret generic legal-aid-secrets \
  --from-literal=OPENAI_API_KEY=your-api-key \
  --from-literal=SECRET_KEY=your-secret-key
```

**2. Deploy Application:**
```bash
kubectl apply -f nodeops-deployment.yaml
```

**3. Verify Deployment:**
```bash
# Check pods
kubectl get pods -l app=legal-aid-backend

# Check services
kubectl get services

# View logs
kubectl logs -l app=legal-aid-backend
```

**4. Access Application:**
```bash
# Get external IP
kubectl get service legal-aid-frontend-service

# Port forward for testing
kubectl port-forward service/legal-aid-frontend-service 8080:80
```

### NodeOps Template Creation

**Create Template Manifest:**
```yaml
apiVersion: nodeops.io/v1
kind: Template
metadata:
  name: legal-aid-assistant
  version: "1.0.0"
spec:
  description: "AI-Backed Community Legal Aid Assistant"
  category: "Legal Tech"
  parameters:
    - name: OPENAI_API_KEY
      description: "OpenAI API Key for LLM integration"
      required: true
      type: secret
    - name: DOMAIN_NAME
      description: "Domain name for the application"
      required: false
      default: "legal-aid.example.com"
  resources:
    - nodeops-deployment.yaml
```

## Cloud Platforms

### AWS Deployment

**Using ECS:**
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name legal-aid-cluster

# Create task definition
aws ecs register-task-definition --cli-input-json file://aws-task-definition.json

# Create service
aws ecs create-service \
  --cluster legal-aid-cluster \
  --service-name legal-aid-service \
  --task-definition legal-aid-task \
  --desired-count 2
```

**Using EKS:**
```bash
# Create EKS cluster
eksctl create cluster --name legal-aid-cluster --region us-west-2

# Deploy application
kubectl apply -f nodeops-deployment.yaml
```

### Google Cloud Platform

**Using Cloud Run:**
```bash
# Deploy backend
gcloud run deploy legal-aid-backend \
  --image gcr.io/your-project/legal-aid-backend:v1 \
  --platform managed \
  --region us-central1

# Deploy frontend
gcloud run deploy legal-aid-frontend \
  --image gcr.io/your-project/legal-aid-frontend:v1 \
  --platform managed \
  --region us-central1
```

**Using GKE:**
```bash
# Create GKE cluster
gcloud container clusters create legal-aid-cluster \
  --zone us-central1-a \
  --num-nodes 3

# Deploy application
kubectl apply -f nodeops-deployment.yaml
```

### Azure Deployment

**Using Container Instances:**
```bash
# Create resource group
az group create --name legal-aid-rg --location eastus

# Deploy containers
az container create \
  --resource-group legal-aid-rg \
  --name legal-aid-backend \
  --image your-registry/legal-aid-backend:v1 \
  --ports 8000
```

**Using AKS:**
```bash
# Create AKS cluster
az aks create \
  --resource-group legal-aid-rg \
  --name legal-aid-cluster \
  --node-count 3

# Deploy application
kubectl apply -f nodeops-deployment.yaml
```

## Production Considerations

### Security

**SSL/TLS Configuration:**
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/legal-aid.crt;
    ssl_certificate_key /etc/ssl/private/legal-aid.key;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
}
```

**Environment Security:**
```bash
# Use secrets management
kubectl create secret generic legal-aid-secrets \
  --from-literal=OPENAI_API_KEY="$(cat openai-key.txt)"

# Restrict network access
kubectl apply -f network-policies.yaml
```

### Database

**PostgreSQL Setup:**
```bash
# Create database
createdb legal_aid_db

# Run migrations
python backend/init_db.py

# Backup strategy
pg_dump legal_aid_db > backup_$(date +%Y%m%d).sql
```

**Database Optimization:**
```sql
-- Create indexes for performance
CREATE INDEX idx_legal_issues_category ON legal_issues(category);
CREATE INDEX idx_legal_issues_created_at ON legal_issues(created_at);
CREATE INDEX idx_legal_advice_issue_id ON legal_advice(issue_id);
```

### Scaling

**Horizontal Scaling:**
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: legal-aid-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: legal-aid-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Load Balancing:**
```yaml
# Service configuration
apiVersion: v1
kind: Service
metadata:
  name: legal-aid-backend-service
spec:
  type: LoadBalancer
  selector:
    app: legal-aid-backend
  ports:
  - port: 80
    targetPort: 8000
```

### Performance Optimization

**Caching:**
```python
# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**CDN Configuration:**
```yaml
# CloudFront distribution
Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
        - DomainName: !GetAtt LoadBalancer.DNSName
          Id: legal-aid-origin
          CustomOriginConfig:
            HTTPPort: 80
            OriginProtocolPolicy: http-only
```

## Monitoring and Maintenance

### Health Monitoring

**Kubernetes Probes:**
```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /api/health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

**External Monitoring:**
```bash
# Uptime monitoring
curl -f https://your-domain.com/api/health || echo "Service down"

# Performance monitoring
curl -w "@curl-format.txt" -o /dev/null -s https://your-domain.com/
```

### Logging

**Centralized Logging:**
```yaml
# Fluentd configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*legal-aid*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      format json
    </source>
```

**Log Analysis:**
```bash
# View application logs
kubectl logs -l app=legal-aid-backend --tail=100

# Search for errors
kubectl logs -l app=legal-aid-backend | grep ERROR

# Export logs
kubectl logs -l app=legal-aid-backend > application.log
```

### Backup and Recovery

**Database Backup:**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
kubectl exec -it postgres-pod -- pg_dump legal_aid_db > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://legal-aid-backups/
```

**Application Backup:**
```bash
# Backup generated documents
kubectl cp legal-aid-backend-pod:/app/generated_documents ./backup/documents/

# Backup configuration
kubectl get configmap legal-aid-config -o yaml > config-backup.yaml
```

### Updates and Rollbacks

**Rolling Updates:**
```bash
# Update backend image
kubectl set image deployment/legal-aid-backend backend=legal-aid-backend:v2

# Check rollout status
kubectl rollout status deployment/legal-aid-backend

# Rollback if needed
kubectl rollout undo deployment/legal-aid-backend
```

**Blue-Green Deployment:**
```bash
# Deploy new version
kubectl apply -f deployment-v2.yaml

# Switch traffic
kubectl patch service legal-aid-backend-service -p '{"spec":{"selector":{"version":"v2"}}}'

# Remove old version
kubectl delete deployment legal-aid-backend-v1
```

## Troubleshooting

### Common Issues

**Container Won't Start:**
```bash
# Check pod status
kubectl describe pod legal-aid-backend-pod

# View container logs
kubectl logs legal-aid-backend-pod -c backend

# Check resource limits
kubectl top pods
```

**Database Connection Issues:**
```bash
# Test database connectivity
kubectl exec -it legal-aid-backend-pod -- python -c "
from app.core.database import engine
try:
    engine.execute('SELECT 1')
    print('Database OK')
except Exception as e:
    print(f'Database Error: {e}')
"
```

**LLM API Issues:**
```bash
# Test OpenAI API
curl -X POST https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"test"}]}'
```

**Performance Issues:**
```bash
# Check resource usage
kubectl top pods
kubectl top nodes

# Analyze slow queries
kubectl exec -it postgres-pod -- psql legal_aid_db -c "
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
"
```

### Debug Mode

**Enable Debug Logging:**
```bash
# Update environment
kubectl set env deployment/legal-aid-backend DEBUG=true LOG_LEVEL=DEBUG

# View detailed logs
kubectl logs -f legal-aid-backend-pod
```

**Local Debugging:**
```bash
# Run backend in debug mode
cd backend
DEBUG=true uvicorn main:app --reload --log-level debug

# Run frontend in debug mode
cd frontend/legal-aid-frontend
npm run dev
```

### Support Resources

**Documentation:**
- [API Reference](api.md)
- [Configuration Guide](configuration.md)
- [Security Best Practices](security.md)

**Community:**
- GitHub Issues: Report bugs and request features
- Discord: Real-time community support
- Stack Overflow: Tag questions with `legal-aid-assistant`

**Professional Support:**
- Email: support@legal-aid-assistant.com
- Enterprise Support: Available for production deployments
- Custom Development: Available for specialized requirements

---

For additional deployment assistance, please refer to the platform-specific documentation or contact our support team.

