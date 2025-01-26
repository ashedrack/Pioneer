# CloudPioneer Troubleshooting Guide

## Table of Contents
1. [Kafka and Zookeeper Issues](#kafka-and-zookeeper-issues)
2. [Monitoring Setup](#monitoring-setup)
3. [Performance Tuning](#performance-tuning)
4. [Common Issues and Solutions](#common-issues-and-solutions)
5. [Service Verification Process](#service-verification-process)

## Kafka and Zookeeper Issues

### Issue 1: Zookeeper Connection Length Errors
**Symptoms:**
```
WARN Close of session 0x0 (org.apache.zookeeper.server.NIOServerCnxn)
java.io.IOException: Len error 1195725856
```

**Solution Steps:**
1. Adjusted Zookeeper buffer size:
```yaml
ZOOKEEPER_JUTE_MAXBUFFER: 20971520  # 20MB
```

2. Added detailed Zookeeper logging:
```yaml
ZOOKEEPER_LOG4J_ROOT_LOGLEVEL: INFO
ZOOKEEPER_TOOLS_LOG4J_LOGLEVEL: INFO
KAFKA_OPTS: >-
  -Dzookeeper.slf4j.verbosity=DEBUG
  -Dlog4j.debug=true
```

3. Configured session timeouts:
```yaml
ZOOKEEPER_MAX_SESSION_TIMEOUT: 40000
ZOOKEEPER_MIN_SESSION_TIMEOUT: 4000
```

### Issue 2: Kafka Message Size Configuration
**Symptoms:**
- Large message transmission failures
- Connection closures

**Solution:**
1. Adjusted Kafka message sizes:
```yaml
KAFKA_MESSAGE_MAX_BYTES: 20971520        # 20MB
KAFKA_REPLICA_FETCH_MAX_BYTES: 20971520  # 20MB
KAFKA_MAX_REQUEST_SIZE: 20971520         # 20MB
```

2. Added network buffer configurations:
```yaml
KAFKA_SOCKET_REQUEST_MAX_BYTES: 20971520
KAFKA_SOCKET_SEND_BUFFER_BYTES: 20971520
KAFKA_SOCKET_RECEIVE_BUFFER_BYTES: 20971520
```

## Monitoring Setup

### Prometheus Configuration
1. Basic setup:
```yaml
prometheus:
  image: prom/prometheus:v2.30.3
  volumes:
    - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
```

2. Added scrape configurations:
```yaml
scrape_configs:
  - job_name: 'cloud-pioneer-api'
    static_configs:
      - targets: ['api:8000']
  - job_name: 'kafka'
    static_configs:
      - targets: ['kafka:9092']
```

### Grafana Setup
1. Basic configuration:
```yaml
grafana:
  image: grafana/grafana:8.2.0
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=cloudpioneer
```

2. Added plugins and provisioning:
```yaml
environment:
  - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource,grafana-piechart-panel
volumes:
  - ./config/grafana/provisioning:/etc/grafana/provisioning
```

## Performance Tuning

### Memory Allocation
1. Kafka memory settings:
```yaml
KAFKA_HEAP_OPTS: "-Xmx2G -Xms2G"
deploy:
  resources:
    limits:
      memory: 4G
    reservations:
      memory: 2G
```

2. Zookeeper memory settings:
```yaml
ZOOKEEPER_HEAP_OPTS: "-Xmx1G -Xms1G"
deploy:
  resources:
    limits:
      memory: 2G
    reservations:
      memory: 1G
```

### Network Configuration
1. Kafka network settings:
```yaml
KAFKA_NUM_NETWORK_THREADS: 3
KAFKA_NUM_IO_THREADS: 8
KAFKA_QUEUED_MAX_REQUESTS: 500
```

## Common Issues and Solutions

### Checking Service Health
1. Prometheus health check:
```bash
curl http://localhost:9090/-/healthy
```

2. API health check:
```bash
curl http://localhost:8000/health
```

### Restarting Services
1. Complete restart:
```bash
docker-compose down -v
docker-compose up --build
```

2. Individual service restart:
```bash
docker-compose restart <service-name>
```

### Log Access
1. View service logs:
```bash
docker-compose logs <service-name>
```

2. Follow logs in real-time:
```bash
docker-compose logs -f <service-name>
```

## Service Verification Process

### Step 1: Check Running Services
```bash
docker-compose ps
```

Expected output should show all services running:
```
NAME                           COMMAND                  SERVICE             STATUS              PORTS
pioneer-zookeeper-1           "/etc/confluent/dock…"   zookeeper           Up                 0.0.0.0:2181->2181/tcp, 0.0.0.0:2888->2888/tcp, 0.0.0.0:3888->3888/tcp
```

### Step 2: Verify Individual Service Health

#### 2.1 Prometheus Health Check
```bash
curl http://localhost:9090/-/healthy
```

Expected output:
```
HTTP/1.1 200 OK
Content-Length: 23
Content-Type: text/plain; charset=utf-8
Date: Sun, 26 Jan 2025 10:53:05 GMT

Prometheus is Healthy.
```

#### 2.2 Kafka Metrics Check
```bash
curl http://localhost:9092/metrics
```

Note: This command will fail with the following expected error as Kafka's metrics endpoint is internal:
```
curl : The underlying connection was closed: The connection was closed unexpectedly.
```

This is normal behavior as Kafka's metrics are exposed internally and should be accessed through Prometheus.

#### 2.3 API Health Check
```bash
curl http://localhost:8000/health
```

Expected output:
```json
{
    "status": "healthy"
}
```

### Step 3: Verify Service Status Summary

After running all checks, verify the following status:

#### Core Services
- ✅ API: Responding on port 8000
- ✅ Zookeeper: Running on ports 2181, 2888, 3888
- ✅ Kafka: Running (internal metrics)
- ✅ PostgreSQL: Connected via exporters

#### Monitoring Services
- ✅ Prometheus: Healthy on port 9090
- ✅ Grafana: Initialized
- ✅ Exporters: Connected and reporting

#### Configuration Status
- ✅ Buffer Sizes: Increased as per configuration
- ✅ Logging: Detailed logging enabled
- ✅ Resource Limits: Applied as configured

### Step 4: Access Service UIs

Verify access to the following endpoints:

1. Grafana Dashboard
   - URL: http://localhost:3000
   - Credentials: admin/cloudpioneer
   - Expected: Login page loads successfully

2. Prometheus UI
   - URL: http://localhost:9090
   - Expected: Targets page shows all services up

3. API Documentation
   - URL: http://localhost:8000/docs
   - Expected: Swagger UI loads successfully

4. Frontend Application
   - URL: http://localhost:3001
   - Expected: Application UI loads successfully

### Troubleshooting Common Verification Issues

1. **Service Not Responding**
   ```bash
   # Restart specific service
   docker-compose restart <service-name>
   
   # View service logs
   docker-compose logs -f <service-name>
   ```

2. **Port Conflicts**
   ```bash
   # Check for port usage
   netstat -ano | findstr "PORT_NUMBER"
   ```

3. **Container Health**
   ```bash
   # Check container health
   docker inspect <container_id> | findstr "Health"
   ```

## Verification Steps

### 1. Check All Services
```bash
docker-compose ps
```

### 2. Verify Connections
- Zookeeper: Port 2181
- Kafka: Port 9092
- API: Port 8000
- Grafana: Port 3000
- Prometheus: Port 9090

### 3. Monitor Metrics
1. Access Grafana:
   - URL: http://localhost:3000
   - Credentials: admin/cloudpioneer

2. Access Prometheus:
   - URL: http://localhost:9090
   - Verify targets are up

## Additional Resources
- Kafka Documentation: [Apache Kafka](https://kafka.apache.org/documentation/)
- Zookeeper Documentation: [Apache Zookeeper](https://zookeeper.apache.org/doc/current/)
- Prometheus Documentation: [Prometheus.io](https://prometheus.io/docs/introduction/overview/)
- Grafana Documentation: [Grafana Labs](https://grafana.com/docs/)
