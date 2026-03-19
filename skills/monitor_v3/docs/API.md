# Agent Monitor v3 - API Documentation

## Base URL

```
http://localhost:8080/api/v1
```

---

## Authentication

```bash
# Header
Authorization: Bearer <api_key>
```

---

## Endpoints

### Health

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "3.0.0"
}
```

---

### Agents

#### List Agents

```
GET /api/v1/agents
```

Response:
```json
{
  "agents": [
    {
      "id": "agent-001",
      "name": "Main Agent",
      "status": "running",
      "health_score": 85
    }
  ]
}
```

#### Get Agent Details

```
GET /api/v1/agents/{agent_id}
```

Response:
```json
{
  "id": "agent-001",
  "name": "Main Agent",
  "status": "running",
  "health_score": 85,
  "cost_daily": 12.50,
  "latency_avg": 1500,
  "error_rate": 0.02
}
```

---

### Metrics

#### Get Metrics

```
GET /api/v1/agents/{agent_id}/metrics
```

Query Parameters:
- `period`: daily, weekly, monthly (default: daily)

Response:
```json
{
  "agent_id": "agent-001",
  "period": "daily",
  "metrics": {
    "requests": 150,
    "errors": 3,
    "cost": 12.50,
    "latency_avg": 1500,
    "latency_p95": 3000
  }
}
```

---

### Costs

#### Get Cost Breakdown

```
GET /api/v1/agents/{agent_id}/costs
```

Query Parameters:
- `period`: daily, weekly, monthly

Response:
```json
{
  "agent_id": "agent-001",
  "period": "daily",
  "total_cost": 12.50,
  "by_model": {
    "gpt-4o": {"cost": 8.00, "requests": 50},
    "claude-3": {"cost": 4.50, "requests": 100}
  },
  "by_task": {
    "task-001": {"cost": 5.00, "requests": 20},
    "task-002": {"cost": 7.50, "requests": 30}
  }
}
```

---

### Alerts

#### Get Alerts

```
GET /api/v1/alerts
```

Query Parameters:
- `agent_id`: Filter by agent
- `level`: critical, warning, info
- `limit`: Max results (default: 100)

Response:
```json
{
  "alerts": [
    {
      "id": "alert-001",
      "agent_id": "agent-001",
      "level": "warning",
      "title": "HighLatency",
      "message": "P95 latency > 5s",
      "timestamp": "2026-03-19T12:00:00Z"
    }
  ]
}
```

#### Create Alert Rule

```
POST /api/v1/alerts/rules
```

Body:
```json
{
  "name": "high_cost",
  "condition": "cost > 10.0",
  "level": "warning",
  "channels": ["slack", "email"]
}
```

---

### RBAC

#### Get Users

```
GET /api/v1/users
```

#### Create User

```
POST /api/v1/users
```

Body:
```json
{
  "username": "john",
  "role": "viewer",
  "projects": ["project-001"]
}
```

---

### Trends

#### Get Trend Data

```
GET /api/v1/trends
```

Query Parameters:
- `agent_id`: Filter by agent
- `metric`: health_score, cost, latency
- `days`: Number of days (default: 7)

Response:
```json
{
  "metric": "health_score",
  "days": 7,
  "data": [
    {"date": "2026-03-13", "value": 85},
    {"date": "2026-03-14", "value": 82},
    {"date": "2026-03-15", "value": 88}
  ]
}
```

---

## Python Client Example

```python
import requests

class AgentMonitorClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get_agents(self):
        return requests.get(f"{self.base_url}/api/v1/agents", headers=self.headers).json()
    
    def get_metrics(self, agent_id: str, period: str = "daily"):
        return requests.get(
            f"{self.base_url}/api/v1/agents/{agent_id}/metrics",
            params={"period": period},
            headers=self.headers
        ).json()
    
    def get_costs(self, agent_id: str, period: str = "daily"):
        return requests.get(
            f"{self.base_url}/api/v1/agents/{agent_id}/costs",
            params={"period": period},
            headers=self.headers
        ).json()


# Usage
client = AgentMonitorClient("http://localhost:8080", "your-api-key")
agents = client.get_agents()
metrics = client.get_metrics("agent-001")
```

---

## Error Responses

```json
{
  "error": "NotFound",
  "message": "Agent not found",
  "code": 404
}
```

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |
