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

## Error Handling

### Error Responses

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

### HTTP Status Codes

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

- Rate limit: 1000 requests per minute
- Rate limit header: X-RateLimit-Limit
- Remaining requests: X-RateLimit-Remaining
- Reset time: X-RateLimit-Reset

## Webhooks

### Configure Webhook

```http
POST /webhooks/configure
```

**Request Body:**
```json
{
  "url": "string",
  "events": ["resource.created", "action.scheduled"],
  "secret": "string"
}
```

### Webhook Payload Example

```json
{
  "event_type": "action.scheduled",
  "timestamp": "2025-01-24T12:00:00Z",
  "data": {
    "resource_id": "string",
    "action": "string",
    "scheduled_time": "datetime"
  }
}
```

## SDK Examples

### Python

```python
from cloudpioneer import CloudPioneerClient

client = CloudPioneerClient(api_key='your_api_key')

# Get resource metrics
metrics = client.get_resource_metrics(
    resource_id='i-1234567890abcdef0',
    metric_type='cpu'
)

# Schedule action
schedule = client.schedule_action(
    resource_id='i-1234567890abcdef0',
    action='shutdown',
    scheduled_time='2025-01-25T00:00:00Z'
)
```

### JavaScript

```javascript
const CloudPioneer = require('cloudpioneer');

const client = new CloudPioneer('your_api_key');

// Get cost analysis
client.getCostAnalysis({
  startDate: '2025-01-01',
  endDate: '2025-01-24',
  groupBy: 'service'
})
.then(costs => console.log(costs))
.catch(error => console.error(error));
```

## Best Practices

1. **Rate Limiting**
   - Implement exponential backoff
   - Cache responses when possible
   - Use bulk operations

2. **Error Handling**
   - Handle all error cases
   - Log error responses
   - Implement retry logic

3. **Security**
   - Rotate API keys regularly
   - Use HTTPS only
   - Validate webhook signatures

## Support

For API support:
1. Check API documentation
2. Review error messages
3. Contact API support team

## Changelog

### v1.0.0 (2025-01-24)
- Initial API release
- Basic resource management
- Cost analytics
- AI insights
