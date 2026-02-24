# Lead Scoring Agent

A production-ready AI-powered Lead Scoring Assistant integrating with CRM systems. This system provides intelligent lead qualification, scoring explanations, and next-best-action recommendations.

## Features

✨ **Core Capabilities**
- 🎯 Intelligent lead scoring (0–100 scale)
- 📊 Feature-level contribution analysis
- 🚀 Next best action recommendations
- 📈 Real-time analytics dashboard
- 🔄 Deterministic & explainable scores

🏗️ **Architecture**
- Modular, scalable design
- Layered architecture (API → Service → Engines)
- Config-driven weights (YAML-based)
- Production-ready with Docker
- PostgreSQL + Redis integration

🎨 **User Interface**
- Modern React dashboard with Vite
- Real-time lead management
- Score visualization with animations
- Responsive design with TailwindCSS
- Micro-interactions with Framer Motion

## Project Structure

```
lead-scoring-agent/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes & endpoints
│   │   ├── services/         # Business logic layer
│   │   ├── engines/          # Scoring engines
│   │   ├── models/           # Pydantic & SQLAlchemy models
│   │   ├── core/             # Configuration & logging
│   │   ├── db/               # Database setup
│   │   └── main.py           # FastAPI app factory
│   ├── seed_data/            # Sample leads
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API client
│   │   ├── utils/            # Helper functions
│   │   ├── styles/           # CSS
│   │   └── App.jsx           # Main app
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
├── config/
│   └── scoring_weights.yaml  # Scoring configuration
└── docker-compose.yml
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Or: Python 3.11+, Node.js 18+, PostgreSQL 15, Redis 7

### Option 1: Docker Compose (Recommended)

```bash
cd lead-scoring-agent
docker-compose up
```

This will start:
- Backend API: http://localhost:8000
- Frontend: http://localhost:5173
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Option 2: Local Development

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy .env.example to .env and configure
cp .env.example .env

# Initialize database
python -m seed_data.init_seed

# Run server
python -m uvicorn app.main:app --reload
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

## API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### Score a Lead
```http
POST /score-lead

Request:
{
  "email": "john@example.com",
  "name": "John Doe",
  "company": "Company Inc",
  "demo_requested": true,
  "registration": true,
  "enquiry_call_whatsapp": false,
  "enquiry_date": "2024-02-20T10:00:00",
  "pricing_compared": true,
  "lead_through_events": false,
  "lead_through_call": true,
  "lead_through_referral": false
}

Response:
{
  "id": 1,
  "score": 78.5,
  "intent_level": "High",
  "confidence": 85.2,
  "recommended_action": "Direct sales call within 24 hrs",
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

#### List Leads
```http
GET /leads?skip=0&limit=20&sort_by=score&intent_filter=High

Response:
{
  "leads": [...],
  "total": 100,
  "skip": 0,
  "limit": 20
}
```

#### Get Analytics
```http
GET /analytics

Response:
{
  "total_leads": 100,
  "average_score": 65.5,
  "high_intent_count": 25,
  "high_intent_percentage": 25.0,
  "conversion_forecast": 0.45,
  "source_breakdown": {
    "demo_requested": 35,
    "registration": 42,
    "referral": 18
  }
}
```

## Scoring Engine

### How It Works

1. **Feature-Based Scoring**: Each engagement signal has a weight
2. **Recency Decay**: Recent enquiries score higher
3. **Normalization**: Final score scaled to 0–100
4. **Deterministic**: Same input always produces same output

### Configuration

Edit `config/scoring_weights.yaml` to adjust:
- Feature weights
- Recency decay parameters
- Intent thresholds
- Conversion probabilities
- Recommended actions

### Score Interpretation

| Score | Intent | Action | Probability |
|-------|--------|--------|-------------|
| 80-100 | High | Direct sales call | 70-90% |
| 60-79 | Medium | Email + Follow-up | 40-70% |
| 40-59 | Medium | Nurture campaign | 20-40% |
| 0-39 | Low | Drip marketing | <20% |

## Input Features

- **demo_requested** (boolean): Lead requested product demo
- **registration** (boolean): Lead completed registration
- **enquiry_call_whatsapp** (boolean): Contact via call/WhatsApp
- **enquiry_date** (datetime): Date of enquiry
- **pricing_compared** (boolean): Lead reviewed pricing
- **lead_through_events** (boolean): Lead from events
- **lead_through_call** (boolean): Warm lead from direct call
- **lead_through_referral** (boolean): Referred lead

## Database

### Schema

**Leads Table**
```sql
- id (Primary Key)
- email (Unique, Indexed)
- name
- company
- score (Indexed)
- intent_level (Indexed)
- confidence
- recommended_action
- feature_contributions (JSON)
- created_at (Indexed)
- updated_at
```

### Migrations

Migrations run automatically on startup via SQLAlchemy.

## Development

### Adding New Features

1. **New Scoring Signal**: Add to `config/scoring_weights.yaml` and update `LeadInput` schema
2. **New Engine**: Extend `engines/` with new logic module
3. **New API Endpoint**: Add to `api/leads.py` with documentation
4. **New Component**: Create in `frontend/src/components/`

### Testing

```bash
# Backend
cd backend
pytest  # (add tests/)

# Frontend
cd frontend
npm test  # (add tests/)
```

## Performance

- **Response Time**: < 200ms for scoring
- **Concurrency**: 4 workers x uvicorn
- **Caching**: Redis for recent scores
- **Database**: Indexed queries on score, intent_level, created_at

## Security

Production considerations:
- Add JWT authentication
- Enable HTTPS/TLS
- Restrict CORS origins
- Add rate limiting
- Encrypt sensitive data
- Use environment-specific configs

## Monitoring & Logging

- Structured JSON logging enabled
- Log level configurable via `LOG_LEVEL` env var
- Health check endpoint: `GET /health`
- Metrics endpoint ready for integration

## Deployment

### Docker Production Build

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Environment Variables

```env
ENV=production
DEBUG=false
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://host:6379/0
LOG_LEVEL=INFO
```

## Contributing

1. Follow the layered architecture pattern
2. Add docstrings to all functions
3. Use type hints
4. Add tests for new features
5. Update documentation

## License

MIT License - See LICENSE file

## Support

For issues and questions, create a GitHub issue or contact the development team.
