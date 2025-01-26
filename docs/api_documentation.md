# CloudPioneer API Documentation

## Overview

The CloudPioneer API provides a comprehensive set of endpoints for integrating with our cloud resource optimization platform. This RESTful API supports both JSON and Protocol Buffers formats, with enterprise-grade security and scalability features.

## Base URL

```
https://api.cloudpioneer.com/v1
```

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

### Authentication

#### Login
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}
```

Response:
```json
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
```

Query Parameters:
- `page` (integer): Page number
- `per_page` (integer): Items per page
- `sort` (string): Sort field
- `order` (string): Sort order (asc/desc)
- `filter` (string): Filter criteria

Response:
```json
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

#### Get Resource Metrics
```http
GET /resources/{resource_id}/metrics
```

Query Parameters:
- `start_time` (ISO 8601)
- `end_time` (ISO 8601)
- `interval` (string): Aggregation interval
- `metrics` (array): List of metrics to retrieve

Response:
```json
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

### Team Management

#### List Team Members
```http
GET /teams/{team_id}/members
```

Response:
```json
{
    "members": [
        {
            "id": "usr_123",
            "email": "user@example.com",
            "role": "admin",
            "status": "active",
            "last_active": "2025-01-26T02:40:00Z"
        }
    ]
}
```

### Billing & Usage

#### Get Usage Report
```http
GET /billing/usage
```

Query Parameters:
- `start_date` (ISO 8601)
- `end_date` (ISO 8601)
- `granularity` (string): daily/weekly/monthly

Response:
```json
{
    "period": {
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-01-31T23:59:59Z"
    },
    "usage": {
        "compute_hours": 720,
        "storage_gb": 1000,
        "api_calls": 50000
    },
    "costs": {
        "compute": 150.00,
        "storage": 50.00,
        "api": 25.00,
        "total": 225.00
    }
}
```

### Webhooks

#### Register Webhook
```http
POST /webhooks
Content-Type: application/json

{
    "url": "https://example.com/webhook",
    "events": ["resource.created", "resource.updated"],
    "secret": "webhook_signing_secret"
}
```

Response:
```json
{
    "id": "webhook_123",
    "url": "https://example.com/webhook",
    "events": ["resource.created", "resource.updated"],
    "status": "active",
    "created_at": "2025-01-26T02:40:00Z"
}
```

## Error Handling

All errors follow a standard format:

```json
{
    "error": {
        "code": "invalid_request",
        "message": "The request was invalid",
        "details": {
            "field": "email",
            "reason": "must be a valid email address"
        }
    },
    "request_id": "req_123"
}
```

Common HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## SDKs & Libraries

Official SDKs are available for:
- Python: `pip install cloudpioneer`
- Node.js: `npm install cloudpioneer`
- Go: `go get github.com/cloudpioneer/go-sdk`
- Java: Available through Maven Central

## Best Practices

1. **Rate Limiting**
   - Implement exponential backoff
   - Cache responses when possible
   - Use bulk operations when available

2. **Authentication**
   - Rotate API keys regularly
   - Use separate keys for different environments
   - Never expose keys in client-side code

3. **Error Handling**
   - Always check error responses
   - Implement proper logging
   - Set up monitoring for API usage

4. **Performance**
   - Use compression for large requests
   - Implement request batching
   - Monitor API latency

## Support

For API support:
- Email: api-support@cloudpioneer.com
- Documentation: https://docs.cloudpioneer.com
- Status Page: https://status.cloudpioneer.com
