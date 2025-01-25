# CloudPioneer Deployment Guide

## Deployment Options

### 1. Local Development Environment

#### Prerequisites
- Docker Desktop
- Python 3.9+
- Node.js 16+
- Git

#### Setup Steps
```bash
# Clone repository
git clone https://github.com/yourusername/cloud-pioneer.git
cd cloud-pioneer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Start services
docker-compose up --build
```

### 2. Production Environment (AWS)

#### Infrastructure Setup (Terraform)
```hcl
# main.tf
provider "aws" {
  region = "us-west-2"
}

module "vpc" {
  source = "./modules/vpc"
  # VPC configuration
}

module "eks" {
  source = "./modules/eks"
  # EKS configuration
}

module "rds" {
  source = "./modules/rds"
  # RDS configuration
}

module "elasticache" {
  source = "./modules/elasticache"
  # Redis configuration
}
```

#### Kubernetes Deployment
```yaml
# kubernetes/production/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudpioneer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cloudpioneer
  template:
    metadata:
      labels:
        app: cloudpioneer
    spec:
      containers:
      - name: api
        image: cloudpioneer/api:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

#### Deployment Steps
1. Set up infrastructure:
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

2. Configure Kubernetes:
   ```bash
   aws eks update-kubeconfig --name cloudpioneer-cluster
   kubectl apply -f kubernetes/production/
   ```

3. Deploy applications:
   ```bash
   # Build and push Docker images
   docker build -t cloudpioneer/api:latest .
   docker push cloudpioneer/api:latest

   # Deploy to Kubernetes
   kubectl apply -f kubernetes/production/deployment.yaml
   ```

### 3. Production Environment (GCP)

#### Infrastructure Setup (Terraform)
```hcl
# main.tf
provider "google" {
  project = "cloudpioneer"
  region  = "us-central1"
}

module "gke" {
  source = "./modules/gke"
  # GKE configuration
}

module "cloud_sql" {
  source = "./modules/cloud_sql"
  # Cloud SQL configuration
}

module "memorystore" {
  source = "./modules/memorystore"
  # Redis configuration
}
```

#### Deployment Steps
1. Set up GCP project:
   ```bash
   gcloud init
   gcloud auth application-default login
   ```

2. Deploy infrastructure:
   ```bash
   cd terraform/gcp
   terraform init
   terraform apply
   ```

3. Configure GKE:
   ```bash
   gcloud container clusters get-credentials cloudpioneer-cluster
   kubectl apply -f kubernetes/gcp/
   ```

### 4. Production Environment (Azure)

#### Infrastructure Setup (Terraform)
```hcl
# main.tf
provider "azurerm" {
  features {}
}

module "aks" {
  source = "./modules/aks"
  # AKS configuration
}

module "postgresql" {
  source = "./modules/postgresql"
  # PostgreSQL configuration
}

module "redis" {
  source = "./modules/redis"
  # Redis configuration
}
```

#### Deployment Steps
1. Set up Azure CLI:
   ```bash
   az login
   az account set --subscription "Your-Subscription"
   ```

2. Deploy infrastructure:
   ```bash
   cd terraform/azure
   terraform init
   terraform apply
   ```

3. Configure AKS:
   ```bash
   az aks get-credentials --resource-group cloudpioneer --name cloudpioneer-cluster
   kubectl apply -f kubernetes/azure/
   ```

### 5. Hybrid Cloud Environment

#### Prerequisites
- Multi-cloud CLI tools
- VPN or Direct Connect setup
- Kubernetes federation configuration

#### Deployment Steps
1. Set up network connectivity:
   ```bash
   # Configure VPN/Direct Connect
   ./scripts/setup_network_connectivity.sh

   # Configure DNS
   ./scripts/setup_dns.sh
   ```

2. Deploy core services:
   ```bash
   # Deploy central management plane
   kubectl apply -f kubernetes/management/

   # Deploy agents
   ./scripts/deploy_agents.sh
   ```

3. Configure federation:
   ```bash
   # Set up Kubernetes federation
   kubefed init cloudpioneer --host-cluster-context=primary-context

   # Join clusters
   kubefed join aws --cluster-context=aws-context
   kubefed join gcp --cluster-context=gcp-context
   kubefed join azure --cluster-context=azure-context
   ```

## Environment-Specific Configurations

### Development
```yaml
# config/development.yaml
database:
  host: localhost
  port: 5432
  ssl: false

kafka:
  bootstrap_servers: localhost:9092
  auto_create_topics: true

redis:
  host: localhost
  port: 6379
```

### Staging
```yaml
# config/staging.yaml
database:
  host: staging-db.internal
  port: 5432
  ssl: true

kafka:
  bootstrap_servers: kafka-staging:9092
  auto_create_topics: false

redis:
  host: redis-staging
  port: 6379
```

### Production
```yaml
# config/production.yaml
database:
  host: ${DB_HOST}
  port: 5432
  ssl: true
  connection_pool: 20

kafka:
  bootstrap_servers: ${KAFKA_SERVERS}
  auto_create_topics: false
  replication_factor: 3

redis:
  host: ${REDIS_HOST}
  port: 6379
  cluster_mode: true
```

## Monitoring Setup

### Prometheus Configuration
```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
```

### Grafana Setup
```bash
# Deploy Grafana
kubectl apply -f monitoring/grafana/

# Import dashboards
kubectl apply -f monitoring/dashboards/
```

## Security Configurations

### TLS Setup
```bash
# Generate certificates
./scripts/generate_certs.sh

# Configure TLS
kubectl create secret tls cloudpioneer-tls --cert=tls.crt --key=tls.key
```

### Network Policies
```yaml
# kubernetes/network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
```
