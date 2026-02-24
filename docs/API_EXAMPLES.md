# API Usage Examples

## 1. Score a Single Lead

```bash
curl -X POST http://localhost:8000/api/score-lead \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@company.com",
    "name": "John Doe",
    "company": "Acme Corporation",
    "demo_requested": true,
    "registration": true,
    "enquiry_call_whatsapp": false,
    "enquiry_date": "2024-02-20T10:00:00Z",
    "pricing_compared": true,
    "lead_through_events": false,
    "lead_through_call": true,
    "lead_through_referral": false
  }'
```

## 2. List All Leads (with pagination)

```bash
curl -X GET "http://localhost:8000/api/leads?skip=0&limit=20&sort_by=score" \
  -H "Content-Type: application/json"
```

## 3. Filter Leads by Intent

```bash
curl -X GET "http://localhost:8000/api/leads?intent_filter=High&sort_by=score" \
  -H "Content-Type: application/json"
```

## 4. Get Single Lead Details

```bash
curl -X GET "http://localhost:8000/api/leads/1" \
  -H "Content-Type: application/json"
```

## 5. Get Analytics Overview

```bash
curl -X GET "http://localhost:8000/api/analytics" \
  -H "Content-Type: application/json"
```

## 6. Health Check

```bash
curl -X GET "http://localhost:8000/health" \
  -H "Content-Type: application/json"
```

## 7. Python Example

```python
import requests

base_url = "http://localhost:8000/api"

# Score a lead
lead_data = {
    "email": "alice@example.com",
    "name": "Alice Smith",
    "company": "Tech Corp",
    "demo_requested": True,
    "registration": True,
    "enquiry_call_whatsapp": True,
    "enquiry_date": "2024-02-22T09:30:00Z",
    "pricing_compared": True,
    "lead_through_events": True,
    "lead_through_call": False,
    "lead_through_referral": True
}

response = requests.post(f"{base_url}/score-lead", json=lead_data)
result = response.json()

print(f"Lead Score: {result['score']}")
print(f"Intent Level: {result['intent_level']}")
print(f"Recommended Action: {result['recommended_action']}")
```

## 8. JavaScript Example

```javascript
const BASE_URL = 'http://localhost:8000/api'

const leadData = {
  email: 'bob@example.com',
  name: 'Bob Johnson',
  company: 'StartUp Inc',
  demo_requested: true,
  registration: false,
  enquiry_call_whatsapp: true,
  enquiry_date: new Date().toISOString(),
  pricing_compared: false,
  lead_through_events: true,
  lead_through_call: true,
  lead_through_referral: false
}

fetch(`${BASE_URL}/score-lead`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(leadData)
})
.then(r => r.json())
.then(result => {
  console.log(`Score: ${result.score}`)
  console.log(`Intent: ${result.intent_level}`)
  console.log(`Action: ${result.recommended_action}`)
})
```

## Response Format

All responses follow this structure:

```json
{
  "id": 1,
  "email": "john@example.com",
  "name": "John Doe",
  "company": "Company Inc",
  "score": 78.5,
  "intent_level": "High",
  "confidence": 85.2,
  "recommended_action": "Direct sales call within 24 hrs",
  "created_at": "2024-02-20T10:00:00Z",
  "updated_at": "2024-02-20T10:00:00Z",
  "explanation": {
    "score": 78.5,
    "intent_level": "High",
    "feature_contributions": [
      {
        "feature": "demo_requested",
        "impact": 32.5,
        "reason": "Lead requested a product demo"
      }
    ],
    "confidence": 85.2,
    "recommended_action": "Direct sales call within 24 hrs"
  }
}
```

## Error Response

```json
{
  "detail": "Error message here"
}
```

## Status Codes

- 200: Success
- 400: Bad request (validation error)
- 404: Resource not found
- 500: Server error

## Rate Limiting (Future)

Implement with:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/score-lead")
@limiter.limit("100/minute")
def score_lead(...):
    ...
```
