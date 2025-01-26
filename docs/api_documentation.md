# CloudPioneer API Documentation

## Overview

The CloudPioneer API provides a comprehensive set of endpoints for integrating with our cloud resource optimization platform. This RESTful API supports both JSON and Protocol Buffers formats, with enterprise-grade security and scalability features.

## Base URLs

- Local Development: `http://localhost:8000`
- Production: `https://api.cloudpioneer.com/v1`

## Authentication

All API requests require authentication using either an API key or OAuth 2.0 tokens.

### API Key Authentication
```http
Authorization: Bearer YOUR_API_KEY
```

### OAuth 2.0
```http
Authorization: Bearer YOUR_OAUTH_TOKEN
```

## Rate Limiting

- Free tier: 1000 requests/hour
- Professional tier: 10,000 requests/hour
- Enterprise tier: Custom limits

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1516131012
```

## Endpoints

### Health Check

#### Check API Health
```http
GET /health

Response:
{
    "status": "healthy"
}
```

### Authentication

#### Login
```http
POST /auth/login
Content-Type: application/json

Request:
{
    "email": "user@example.com",
    "password": "secure_password"
}

Response:
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

### Resource Management

#### List Resources
```http
GET /resources

Query Parameters:
- page (integer): Page number
- per_page (integer): Items per page
- sort (string): Sort field
- order (string): Sort order (asc/desc)
- filter (string): Filter criteria

Response:
{
    "items": [
        {
            "id": "res_123",
            "name": "production-server",
            "type": "instance",
            "status": "running",
            "metrics": {
                "cpu_usage": 45.2,
                "memory_usage": 2048576,
                "disk_usage": 80.5
            },
            "cost": {
                "hourly": 0.125,
                "monthly_estimated": 90.00
            },
            "tags": {
                "environment": "production",
                "team": "backend"
            }
        }
    ],
    "total": 100,
    "page": 1,
    "per_page": 10
}
```

### Metrics & Monitoring

#### Get Resource Metrics
```http
GET /resources/{resource_id}/metrics

Query Parameters:
- start_time (ISO 8601)
- end_time (ISO 8601)
- interval (string): Aggregation interval
- metrics (array): List of metrics to retrieve

Response:
{
    "resource_id": "res_123",
    "interval": "5m",
    "metrics": {
        "cpu_usage": [
            {
                "timestamp": "2025-01-26T02:40:00Z",
                "value": 45.2
            }
        ],
        "memory_usage": [
            {
                "timestamp": "2025-01-26T02:40:00Z",
                "value": 2048576
            }
        ]
    }
}
```

#### Get Kafka Metrics
```http
GET /kafka/metrics

Response:
{
    "broker_id": 1,
    "metrics": {
        "messages_in_per_sec": 1000,
        "bytes_in_per_sec": 50000,
        "bytes_out_per_sec": 100000,
        "active_controller_count": 1,
        "offline_partitions_count": 0,
        "under_replicated_partitions": 0
    }
}
```

#### Get System Metrics
```http
GET /system/metrics

Response:
{
    "cpu": {
        "usage_percent": 45.2,
        "load_average": [1.5, 1.2, 0.9]
    },
    "memory": {
        "total": 8589934592,
        "used": 4294967296,
        "free": 4294967296,
        "usage_percent": 50.0
    },
    "disk": {
        "total": 107374182400,
        "used": 53687091200,
        "free": 53687091200,
        "usage_percent": 50.0
    }
}
```

### Event Streaming

#### Create Event Stream
```http
POST /events/stream
Content-Type: application/json

Request:
{
    "topic": "resource_metrics",
    "filters": {
        "resource_types": ["instance", "database"],
        "metrics": ["cpu", "memory"],
        "min_interval": "1m"
    }
}

Response:
{
    "stream_id": "stream_123",
    "websocket_url": "ws://api.cloudpioneer.com/v1/events/stream_123",
    "token": "ws_token_123"
}
```

#### WebSocket Event Format
```json
{
    "event_type": "metric_update",
    "timestamp": "2025-01-26T02:40:00Z",
    "resource_id": "res_123",
    "data": {
        "cpu_usage": 45.2,
        "memory_usage": 2048576
    }
}
```

### Error Responses

#### Standard Error Format
```json
{
    "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "The requested resource was not found",
        "details": {
            "resource_id": "res_123"
        }
    },
    "request_id": "req_abc123"
}
```

## Best Practices

### Rate Limiting
1. Implement exponential backoff
2. Cache responses when possible
3. Use bulk operations when available

### Error Handling
1. Always check error responses
2. Implement proper retry logic
3. Log failed requests with request_id

### Security
1. Never log or expose API keys
2. Use HTTPS for all requests
3. Implement proper token rotation

## Monitoring Integration

### Prometheus Metrics
Available at: `http://localhost:9090/metrics`

Common metrics:
```
# API Request Rate
http_requests_total{method="GET", endpoint="/resources"}

# Response Time
http_request_duration_seconds{method="GET", endpoint="/resources"}

# Error Rate
http_requests_errors_total{method="GET", endpoint="/resources"}
```

### Grafana Integration
1. Add Prometheus as data source:
   - URL: `http://prometheus:9090`
   - Access: Server (default)

2. Import provided dashboards:
   - API Performance Dashboard (ID: 12345)
   - Resource Metrics Dashboard (ID: 12346)
   - System Metrics Dashboard (ID: 12347)

## WebSocket Connections

### Connection Example
```javascript
const ws = new WebSocket('ws://api.cloudpioneer.com/v1/events/stream_123');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

### Heartbeat
- Server sends ping every 30 seconds
- Client must respond with pong within 10 seconds
- Connection closed if no pong received

## Changelog

### v1.1.0 (2025-01-26)
- Added system metrics endpoints
- Enhanced Kafka monitoring
- Added WebSocket support for real-time updates
- Improved error handling and logging
