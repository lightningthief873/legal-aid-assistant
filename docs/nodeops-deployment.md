# NodeOps Deployment Guide

## AI-Backed Community Legal Aid Assistant - NodeOps Template

This guide provides step-by-step instructions for deploying the AI-Backed Community Legal Aid Assistant on the NodeOps platform as a containerized template.

## Overview

The AI-Backed Community Legal Aid Assistant is a production-ready containerized application that provides:

- **AI-powered legal analysis** using LLM technology
- **Document generation** for legal notices and complaints
- **Resource lookup** for local legal aid organizations
- **Modern web interface** with responsive design
- **Scalable architecture** ready for production deployment

## Template Structure

```
legal-aid-assistant/
├── backend/                 # FastAPI backend service
│   ├── app/                # Application code
│   ├── Dockerfile          # Backend container configuration
│   ├── requirements.txt    # Python dependencies
│   └── init_db.py         # Database initialization
├── frontend/               # React frontend application
│   └── legal-aid-frontend/
│       ├── src/           # React source code
│       ├── Dockerfile     # Frontend container configuration
│       └── nginx.conf     # Nginx configuration
├── docker-compose.yml     # Local development setup
├── docker-compose.prod.yml # Production deployment
├── nodeops-deployment.yaml # NodeOps Kubernetes manifests
├── deploy.sh              # Deployment automation script
├── .env.production        # Environment configuration template
└── docs/                  # Comprehensive documentation
```

## Prerequisites

### NodeOps Platform Requirements

- NodeOps account with container deployment access
- Kubernetes cluster (managed by NodeOps)
- Container registry access
- Domain name (optional, for custom domains)

### External Dependencies

- **OpenAI API Key** (required for LLM functionality)
  - Get from: https://platform.openai.com/
  - Alternative: Local LLM setup (Ollama, etc.)

### Resource Requirements

**Minimum:**
- 2 CPU cores
- 4GB RAM
- 10GB storage

**Recommended:**
- 4 CPU cores
- 8GB RAM
- 20GB storage

## Quick Deployment

### 1. Prepare Configuration

```bash
# Clone the template
git clone <repository-url>
cd legal-aid-assistant

# Configure environment
cp .env.production .env
nano .env  # Edit with your settings
```

**Critical Settings:**
```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key-here
SECRET_KEY=your-super-secure-secret-key

# Optional
DOMAIN_NAME=your-domain.com
DEFAULT_JURISDICTION=US
```

### 2. Build and Push Images

```bash
# Build images
docker build -t your-registry/legal-aid-backend:v1 ./backend
docker build -t your-registry/legal-aid-frontend:v1 ./frontend/legal-aid-frontend

# Push to NodeOps registry
docker push your-registry/legal-aid-backend:v1
docker push your-registry/legal-aid-frontend:v1
```

### 3. Deploy to NodeOps

```bash
# Update image references in deployment manifest
sed -i 's|legal-aid-backend:latest|your-registry/legal-aid-backend:v1|g' nodeops-deployment.yaml
sed -i 's|legal-aid-frontend:latest|your-registry/legal-aid-frontend:v1|g' nodeops-deployment.yaml

# Create secrets
kubectl create secret generic legal-aid-secrets \
  --from-literal=OPENAI_API_KEY="your-api-key" \
  --from-literal=SECRET_KEY="your-secret-key"

# Deploy application
kubectl apply -f nodeops-deployment.yaml

# Check deployment status
kubectl get pods -l app=legal-aid-backend
kubectl get services
```

### 4. Access Application

```bash
# Get external IP
kubectl get service legal-aid-frontend-service

# Or use port forwarding for testing
kubectl port-forward service/legal-aid-frontend-service 8080:80
```

## Detailed Deployment Steps

### Step 1: Environment Setup

**Create Environment File:**
```bash
cp .env.production .env
```

**Configure Required Variables:**
```bash
# AI/LLM Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Security
SECRET_KEY=your-super-secure-secret-key-change-this

# Application
DEBUG=false
DEFAULT_JURISDICTION=US

# Database (SQLite for simple deployments)
DATABASE_URL=sqlite:///./legal_aid.db

# Optional: PostgreSQL for production
# DATABASE_URL=postgresql://user:password@postgres:5432/legal_aid_db
```

### Step 2: Container Registry Setup

**Option A: Use NodeOps Registry**
```bash
# Login to NodeOps registry
docker login registry.nodeops.io

# Tag images
docker tag legal-aid-backend:latest registry.nodeops.io/your-org/legal-aid-backend:v1
docker tag legal-aid-frontend:latest registry.nodeops.io/your-org/legal-aid-frontend:v1

# Push images
docker push registry.nodeops.io/your-org/legal-aid-backend:v1
docker push registry.nodeops.io/your-org/legal-aid-frontend:v1
```

**Option B: Use External Registry (Docker Hub, etc.)**
```bash
# Build and push to Docker Hub
docker build -t your-dockerhub-username/legal-aid-backend:v1 ./backend
docker build -t your-dockerhub-username/legal-aid-frontend:v1 ./frontend/legal-aid-frontend

docker push your-dockerhub-username/legal-aid-backend:v1
docker push your-dockerhub-username/legal-aid-frontend:v1
```

### Step 3: Kubernetes Deployment

**Create Namespace (Optional):**
```bash
kubectl create namespace legal-aid
kubectl config set-context --current --namespace=legal-aid
```

**Create Secrets:**
```bash
kubectl create secret generic legal-aid-secrets \
  --from-literal=OPENAI_API_KEY="your-openai-api-key" \
  --from-literal=SECRET_KEY="your-secret-key" \
  --from-literal=DATABASE_URL="sqlite:///./legal_aid.db"
```

**Deploy Application:**
```bash
# Update image references in nodeops-deployment.yaml
# Then deploy
kubectl apply -f nodeops-deployment.yaml
```

**Verify Deployment:**
```bash
# Check pods
kubectl get pods
kubectl describe pod legal-aid-backend-xxx

# Check services
kubectl get services
kubectl describe service legal-aid-frontend-service

# Check logs
kubectl logs -l app=legal-aid-backend
kubectl logs -l app=legal-aid-frontend
```

### Step 4: Domain and SSL Setup

**Configure Ingress (if using custom domain):**
```yaml
# Update nodeops-deployment.yaml ingress section
spec:
  tls:
  - hosts:
    - your-domain.com
    secretName: legal-aid-tls
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: legal-aid-frontend-service
            port:
              number: 80
```

**SSL Certificate (Let's Encrypt):**
```bash
# Install cert-manager (if not available)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

## NodeOps Template Configuration

### Template Manifest

Create `nodeops-template.yaml`:

```yaml
apiVersion: nodeops.io/v1
kind: Template
metadata:
  name: legal-aid-assistant
  version: "1.0.0"
  description: "AI-Backed Community Legal Aid Assistant"
  category: "Legal Tech"
  tags:
    - "ai"
    - "legal"
    - "community"
    - "fastapi"
    - "react"
spec:
  parameters:
    - name: OPENAI_API_KEY
      description: "OpenAI API Key for LLM integration"
      type: secret
      required: true
    - name: SECRET_KEY
      description: "Secret key for application security"
      type: secret
      required: true
      generate: true
    - name: DOMAIN_NAME
      description: "Domain name for the application"
      type: string
      required: false
      default: "legal-aid.example.com"
    - name: DEFAULT_JURISDICTION
      description: "Default legal jurisdiction"
      type: string
      required: false
      default: "US"
    - name: REPLICAS
      description: "Number of replicas for each service"
      type: integer
      required: false
      default: 2
  resources:
    - nodeops-deployment.yaml
  documentation:
    - README.md
    - docs/api.md
    - docs/deployment.md
```

### Template Deployment

```bash
# Submit template to NodeOps
nodeops template create -f nodeops-template.yaml

# Deploy from template
nodeops template deploy legal-aid-assistant \
  --set OPENAI_API_KEY="your-api-key" \
  --set DOMAIN_NAME="your-domain.com"
```

## Scaling and Production Considerations

### Horizontal Pod Autoscaling

```yaml
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
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Database Considerations

**For Production, Consider PostgreSQL:**

```yaml
# Add to nodeops-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: legal_aid_db
        - name: POSTGRES_USER
          value: legal_aid_user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
```

### Monitoring and Logging

**Add Monitoring:**
```yaml
# Prometheus monitoring
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: legal-aid-monitor
spec:
  selector:
    matchLabels:
      app: legal-aid-backend
  endpoints:
  - port: http
    path: /metrics
```

**Centralized Logging:**
```yaml
# Fluentd sidecar for log collection
- name: fluentd
  image: fluent/fluentd:v1.16
  volumeMounts:
  - name: varlog
    mountPath: /var/log
  - name: fluentd-config
    mountPath: /fluentd/etc
```

## Troubleshooting

### Common Issues

**1. Pods Not Starting:**
```bash
# Check pod status
kubectl describe pod legal-aid-backend-xxx

# Common causes:
# - Image pull errors (check registry access)
# - Resource limits (check node capacity)
# - Configuration errors (check secrets/configmaps)
```

**2. Service Not Accessible:**
```bash
# Check service endpoints
kubectl get endpoints legal-aid-frontend-service

# Check ingress
kubectl describe ingress legal-aid-ingress

# Test internal connectivity
kubectl exec -it legal-aid-backend-pod -- curl http://legal-aid-frontend-service
```

**3. Database Connection Issues:**
```bash
# Check database pod
kubectl logs postgres-pod

# Test connection from backend
kubectl exec -it legal-aid-backend-pod -- python -c "
from app.core.database import engine
print('Database OK' if engine else 'Database Error')
"
```

**4. LLM API Issues:**
```bash
# Check API key configuration
kubectl get secret legal-aid-secrets -o yaml

# Test API connectivity
kubectl exec -it legal-aid-backend-pod -- python -c "
import openai
openai.api_key = 'your-key'
print(openai.Model.list())
"
```

### Performance Optimization

**1. Resource Tuning:**
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

**2. Caching:**
```yaml
# Add Redis for caching
- name: redis
  image: redis:7-alpine
  ports:
  - containerPort: 6379
```

**3. CDN Integration:**
```yaml
# Configure CDN for static assets
annotations:
  nginx.ingress.kubernetes.io/configuration-snippet: |
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
      expires 1y;
      add_header Cache-Control "public, immutable";
    }
```

## Security Best Practices

### 1. Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: legal-aid-network-policy
spec:
  podSelector:
    matchLabels:
      app: legal-aid-backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: legal-aid-frontend
    ports:
    - protocol: TCP
      port: 8000
```

### 2. Pod Security Standards

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: backend
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

### 3. Secret Management

```bash
# Use external secret management
kubectl apply -f - <<EOF
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
EOF
```

## Maintenance and Updates

### Rolling Updates

```bash
# Update backend image
kubectl set image deployment/legal-aid-backend backend=legal-aid-backend:v2

# Monitor rollout
kubectl rollout status deployment/legal-aid-backend

# Rollback if needed
kubectl rollout undo deployment/legal-aid-backend
```

### Backup Strategy

```bash
# Database backup
kubectl exec postgres-pod -- pg_dump legal_aid_db > backup.sql

# Configuration backup
kubectl get configmap legal-aid-config -o yaml > config-backup.yaml
kubectl get secret legal-aid-secrets -o yaml > secrets-backup.yaml
```

### Health Monitoring

```bash
# Set up health checks
curl -f http://your-domain.com/api/health

# Monitor metrics
kubectl top pods
kubectl top nodes
```

## Support and Resources

### Documentation
- [Complete README](../README.md)
- [API Documentation](../docs/api.md)
- [Contributing Guide](../CONTRIBUTING.md)

### Community
- GitHub Issues: Report bugs and request features
- Discord: Real-time community support
- Email: support@legal-aid-assistant.com

### Professional Support
- Enterprise deployment assistance
- Custom development services
- Training and consultation

---

## Template Checklist

Before deploying to NodeOps, ensure:

- [ ] Environment variables configured
- [ ] Container images built and pushed
- [ ] Secrets created in Kubernetes
- [ ] Domain name configured (if applicable)
- [ ] SSL certificates set up
- [ ] Resource limits appropriate for your cluster
- [ ] Monitoring and logging configured
- [ ] Backup strategy in place
- [ ] Health checks passing
- [ ] Documentation reviewed

## Quick Start Commands

```bash
# 1. Configure environment
cp .env.production .env && nano .env

# 2. Build and push images
docker build -t your-registry/legal-aid-backend:v1 ./backend
docker build -t your-registry/legal-aid-frontend:v1 ./frontend/legal-aid-frontend
docker push your-registry/legal-aid-backend:v1
docker push your-registry/legal-aid-frontend:v1

# 3. Create secrets
kubectl create secret generic legal-aid-secrets \
  --from-literal=OPENAI_API_KEY="your-api-key" \
  --from-literal=SECRET_KEY="your-secret-key"

# 4. Deploy
kubectl apply -f nodeops-deployment.yaml

# 5. Check status
kubectl get pods,services,ingress
```

Your AI-Backed Community Legal Aid Assistant is now ready for production deployment on NodeOps!

