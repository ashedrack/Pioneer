# CloudPioneer API Documentation

## Overview

The CloudPioneer API provides programmatic access to cloud resource optimization features. This RESTful API allows you to monitor resources, manage schedules, and access AI insights.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API requests require authentication using JWT tokens.

```http
Authorization: Bearer <your_token>
```

## Endpoints

### Resource Management

#### Get Resource Metrics

```http
GET /resources/metrics
```

Retrieve current resource metrics.

**Parameters:**
```json
{
  "resource_id": "string",
  "metric_type": "string",
  "start_time": "datetime",
  "end_time": "datetime"
}
```

**Response:**
```json
{
  "resource_id": "i-1234567890abcdef0",
  "metrics": {
    "cpu_usage": 45.5,
    "memory_usage": 78.2,
    "disk_usage": 62.1,
    "network_usage": 25.8
  },
  "timestamp": "2025-01-24T12:00:00Z"
}
```

#### Schedule Resource Action

```http
POST /resources/schedule
```

Schedule a resource management action.

**Request Body:**
```json
{
  "resource_id": "string",
  "action": "string",
  "scheduled_time": "datetime",
  "parameters": {
    "key": "value"
  }
}
```

**Response:**
```json
{
  "schedule_id": "string",
  "status": "scheduled",
  "details": {
    "resource_id": "string",
    "action": "string",
    "scheduled_time": "datetime"
  }
}
```

### Cost Analytics

#### Get Cost Analysis

```http
GET /resources/costs
```

Retrieve cost analysis data.

**Parameters:**
```json
{
  "start_date": "date",
  "end_date": "date",
  "group_by": "string"
}
```

**Response:**
```json
{
  "total_cost": 1234.56,
  "breakdown": {
    "compute": 567.89,
    "storage": 234.56,
    "network": 432.10
  },
  "trends": [
    {
      "date": "2025-01-24",
      "cost": 123.45
    }
  ]
}
```

### AI Insights

#### Get Predictions

```http
GET /resources/predictions
```

Get resource usage predictions.

**Parameters:**
```json
{
  "resource_id": "string",
  "prediction_window": "integer"
}
```

**Response:**
```json
{
  "resource_id": "string",
  "predictions": [
    {
      "timestamp": "datetime",
      "cpu_usage": 45.5,
      "memory_usage": 78.2,
      "confidence": 0.95
    }
  ]
}
```

#### Get Optimization Recommendations

```http
GET /resources/recommendations
```

Get AI-powered optimization recommendations.

**Response:**
```json
{
  "recommendations": [
    {
      "resource_id": "string",
      "action": "string",
      "expected_savings": 123.45,
      "confidence": 0.92,
      "reasoning": "string"
    }
  ]
}
```

### Schedule Management

#### Create Schedule

```http
POST /schedules
```

Create a new resource optimization schedule.

**Request Body:**
```json
{
  "resource_id": "string",
  "schedule_type": "start|stop|resize",
  "cron_expression": "0 0 * * *",
  "timezone": "UTC",
  "action_params": {
    "instance_type": "t3.micro",
    "target_state": "running"
  }
}
```

**Response:**
```json
{
  "schedule_id": "sch_123456",
  "status": "active",
  "created_at": "2025-01-25T17:26:44Z"
}
```

#### List Schedules

```http
GET /schedules
```

List all active schedules.

**Parameters:**
```json
{
  "resource_id": "string",
  "status": "active|inactive",
  "page": 1,
  "per_page": 10
}
```

### AI Insights

#### Get Optimization Recommendations

```http
GET /insights/recommendations
```

Get AI-powered optimization recommendations.

**Parameters:**
```json
{
  "resource_id": "string",
  "recommendation_type": "cost|performance|security",
  "time_range": "7d|30d|90d"
}
```

## Error Handling

The API uses conventional HTTP response codes to indicate the success or failure of requests:

- `200 OK`: Request succeeded
- `201 Created`: Resource was successfully created
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Authentication succeeded but insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

Error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error context"
    }
  }
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- 1000 requests per hour per API key
- 100 requests per minute per IP address

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1706201204
```

When the rate limit is exceeded, the API will respond with a 429 status code.

## Pagination

List endpoints support pagination using the following query parameters:

- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)

Response includes pagination metadata:
```json
{
  "data": [...],
  "metadata": {
    "current_page": 1,
    "per_page": 10,
    "total_pages": 5,
    "total_items": 42
  }
}
```

## SDKs and Tools

- Python SDK: [GitHub Repository](https://github.com/cloudpioneer/python-sdk)
- JavaScript SDK: [GitHub Repository](https://github.com/cloudpioneer/js-sdk)
- CLI Tool: [GitHub Repository](https://github.com/cloudpioneer/cli)

## Support

For API support, please contact:
- Email: api-support@cloudpioneer.com
- Documentation: https://docs.cloudpioneer.com
- Status Page: https://status.cloudpioneer.com

## Changelog

### v1.0.0 (2025-01-24)
- Initial API release
- Basic resource management
- Cost analytics
- AI insights

### v1.1.0 (2025-01-25)
- Added schedule management endpoints
- Improved error handling and rate limiting documentation
- Added pagination support for list endpoints
