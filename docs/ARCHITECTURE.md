# Comprehensive Architecture Documentation

## System Overview

The Lead Scoring Agent is an enterprise-ready system for intelligent lead qualification, powered by AI-driven scoring and explainability.

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer (React)                    │
│  Dashboard | Lead Scoring Form | Lead Management | Analytics │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      └──→ HTTP/REST API
                      │
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                       │
│  POST /score-lead  |  GET /leads  |  GET/analytics          │
└──────────────────┬────────────────────────────────────────┬──┘
                   │                                         │
       ┌───────────┴─────────────────┐                       │
       │                             │                       │
┌──────▼──────────────────┐ ┌────────▼──────────────────┐   │
│  Services Layer         │ │  Data Layer              │   │
│  - LeadService          │ │  - SQLAlchemy ORM       │   │
│  - Orchestration        │ │  - PostgreSQL DB        │   │
│  - Business Logic       │ │  - Redis Cache          │   │
└──────┬────────────────┬─┘ └────────────────────────┬──┘   │
       │                │                            │       │
   ┌───▼────┬──────┬───▼──┐                          │       │
   │         │      │      │                          │       │
   ▼         ▼      ▼      ▼                          │       │
┌─────┐ ┌──────┐ ┌────┐ ┌────────┐                  │       │
│Score│ │Expl.│ │Next│ │ Config │                   │       │
│Eng. │ │ Eng.│ │Act.│ │ Loader │                   │       │
└─────┘ └──────┘ └────┘ └────────┘                  │       │
                                                    │       │
└─────────────────────────────────────────────────────┘
```

## Layered Architecture

### 1. API Layer (`app/api/`)

**Responsibility**: Route definition, request validation, response formatting

**Components**:
- `leads.py`: Lead management endpoints
- `health.py`: Health check endpoint
- `router.py`: Router aggregation

**Pattern**: Each endpoint delegates to service layer

```python
# Example: Score Lead Endpoint
@router.post("/score-lead", response_model=dict)
def score_lead(lead_data: LeadInput, db: Session = Depends(get_db)):
    service = LeadService(db)
    result = service.score_lead(lead_data)
    return result
```

### 2. Service Layer (`app/services/`)

**Responsibility**: Business logic orchestration, database operations

**Components**:
- `lead_service.py`: Lead CRUD and scoring pipeline

**Key Methods**:
- `score_lead()`: Full scoring pipeline
- `get_lead()`: Single lead retrieval
- `list_leads()`: Pagination and filtering
- `get_analytics()`: Aggregated metrics

**Pattern**: Services use engines and repositories

```python
def score_lead(self, lead_data: LeadInput):
    # 1. Score using engine
    scoring_result = self.scoring_engine.score(lead_dict)
    
    # 2. Explain using engine
    explanation = self.explanation_engine.explain_score(...)
    
    # 3. Get action using engine
    action = self.action_engine.get_action(score)
    
    # 4. Persist to database
    db.add(lead_model)
    db.commit()
    
    # 5. Return results
    return response
```

### 3. Engines Layer (`app/engines/`)

**Responsibility**: Pure algorithmic logic, deterministic operations

**Components**:

#### A. Scoring Engine
```python
class ConfigDrivenScoringEngine(ScoringStrategy):
    def score(self, lead_data) -> Dict:
        # 1. Read weights from YAML config
        # 2. Calculate weighted base scores
        # 3. Calculate recency score
        # 4. Normalize to 0-100
        # 5. Return score with contributions
```

**Algorithm**:
```
1. For each feature:
   if feature is true:
       score += weight[feature]
   
2. Recency Score = max(0, (15 - days_since_enquiry) / 15 * 10)
   
3. Final Score = min(100, (total_score / total_weights) * 100)
```

#### B. Explanation Engine
```python
class ExplanationEngine:
    def explain_score(self, score, contributions):
        # 1. Classify intent level
        # 2. Calculate confidence
        # 3. Format contributions
        # 4. Generate summary
```

**Confidence Calculation**:
```
Confidence = (
    data_completeness * 0.3 +
    signal_recency * 0.4 +
    signal_diversity * 0.3
) * 100
```

#### C. Next Action Engine
```python
class NextActionEngine:
    def get_action(self, score):
        # 1. Determine score bracket
        # 2. Lookup action configuration
        # 3. Calculate conversion probability
        # 4. Generate rationale
```

**Score to Action Mapping**:
```
80-100: Immediate → Direct sales call (70-90%)
60-79:  High      → Pricing + Follow-up (40-70%)
40-59:  Medium    → Nurture (20-40%)
<40:    Low       → Drip marketing (<20%)
```

### 4. Data Layer (`app/db/` + `app/models/`)

**Responsibility**: Data persistence and schema definition

**Components**:
- `database.py`: Connection, session management
- `models/lead.py`: SQLAlchemy ORM model
- `models/schemas.py`: Pydantic validation schemas

**Database Schema**:
```sql
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    score FLOAT DEFAULT 0.0,
    intent_level VARCHAR(50) DEFAULT 'Low',
    confidence FLOAT DEFAULT 0.0,
    feature_contributions TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_score ON leads(score);
CREATE INDEX idx_intent_level ON leads(intent_level);
CREATE INDEX idx_created_at ON leads(created_at);
```

## Configuration System

### Config-Driven Approach

```yaml
# config/scoring_weights.yaml
version: "1.0"

weights:
  demo_requested:
    weight: 25
    description: "Lead requested a product demo"
  
  registration:
    weight: 15
    description: "Lead completed registration"
  # ... more weights

recency:
  days_decay: 15
  max_score: 10

intent_thresholds:
  high: 80
  medium: 60
  low: 40

conversion_probabilities:
  score_80_100:
    probability: 0.75
    urgency: "Immediate"
  # ... more brackets

recommended_actions:
  score_80_100:
    urgency: "Immediate"
    action: "Direct sales call within 24 hrs"
  # ... more actions
```

**Benefits**:
- No code changes for weight updates
- Easy A/B testing
- Audit trail via version control

## Data Flow

### Lead Scoring Flow

```
User Input (React Form)
         ↓
API Validation (Pydantic)
         ↓
LeadService.score_lead()
    ↓ ↓ ↓
    └────────────────────┐
    │                    │
ScoringEngine        ConfigLoader
    │                    │
    └────Contributions───┘
                ↓
        ExplanationEngine
                ↓
        NextActionEngine
                ↓
        Persist to DB
                ↓
    Return Results → Frontend
```

### Analytics Flow

```
GET /analytics
         ↓
LeadService.get_analytics()
         ↓
Database Aggregation
  - COUNT(total_leads)
  - AVG(score)
  - COUNT WHERE intent_level='High'
  - Distribution analysis
         ↓
    Format Response
         ↓
    Return JSON → Frontend Charts
```

## Frontend Architecture

### Component Hierarchy

```
App.jsx (main container)
    ├── Header
    ├── Navigation (Tab selector)
    └── Main Content
        ├── Dashboard Tab
        │   ├── KPICard (4x)
        │   └── AnalyticsOverview
        │       ├── PieChart (Intent Distribution)
        │       └── BarChart (Source Breakdown)
        │
        ├── ScoreLead Tab
        │   ├── Form (left)
        │   └── Results (right)
        │       ├── ScoreCircle
        │       └── Contributions
        │
        └── Leads Tab
            ├── LeadTable
            └── ScoreExplanationDrawer
```

### State Management

```
App Component (Root)
├── leads: []
├── analytics: {}
├── loading: boolean
├── activeTab: 'dashboard' | 'score' | 'leads'
├── page: number
└── totalLeads: number
```

### Key Components

**KPICard**: Displays metrics with icons and trends

**ScoreCircle**: Animated circular progress meter

**LeadTable**: 
- Sortable columns
- Pagination
- Inline score display

**ScoreLead**:
- Input form with validation
- Real-time results
- Contribution visualization

**AnalyticsOverview**:
- Recharts integration
- Pie & bar charts
- Source breakdown

## Performance Considerations

### Backend
- **Scoring**: < 200ms (config-driven, no ML)
- **Database**: Indexed queries on score, intent_level, created_at
- **Caching**: Redis for recently scored leads
- **Concurrency**: 4 uvicorn workers
- **Connection Pool**: 10 connections with 20 overflow

### Frontend
- **Code Splitting**: Vite automatic chunks
- **Animations**: Framer Motion with GPU acceleration
- **API Calls**: Debounced search, pagination
- **Asset Size**: TailwindCSS purged CSS

## Scalability

### Horizontal Scaling

```
┌─────────────────┐
│  Load Balancer  │
└────────┬────────┘
    ┌────┴────┬────────┬────────┐
    │         │        │        │
┌───▼── ┌────▼─┐ ┌────▼─┐ ┌───▼───┐
│App 1  │ App 2│ │ App 3│ │ App 4 │
└───┬── └───┬──┘ └──┬───┘ └───┬───┘
    │       │       │       │
    └───────┴───┬───┴───────┘
            ┌───▼─────┐
            │PostgreSQL   │ (Read Replica)
            └──────────┘
            
            └───────────┐
            ┌───────────▼──┐
            │ Redis Cluster │
            └───────────────┘
```

### Database Optimization

- Indexed queries
- Connection pooling
- Query caching via Redis
- Batch operations

## Security

### Input Validation
- Pydantic models enforce types
- Email validation
- Required field checks

### Output Sanitization
- JSON response formatting
- No sensitive data leakage
- Structured error responses

### Future Enhancements
- JWT authentication
- Rate limiting
- SSL/TLS encryption
- CORS policy enforcement
- Audit logging

## Extension Points

### Adding New Features

**1. New Scoring Signal**:
```python
# 1. Update config
weights:
  new_signal: 
    weight: 20

# 2. Update LeadInput schema
class LeadInput(BaseModel):
    new_signal: bool = False

# 3. Engine automatically uses it
```

**2. New Engine Type**:
```python
# Extend ScoringStrategy
class MLScoringEngine(ScoringStrategy):
    def score(self, lead_data):
        # ML model logic
        pass

# Update config to switch engines
```

**3. New API Endpoint**:
```python
@router.get("/custom-endpoint")
def custom_endpoint(db: Session = Depends(get_db)):
    service = LeadService(db)
    # Logic here
    return result
```

## Testing Strategy

```
Unit Tests:
├── Engine tests (scoring logic)
├── Schema tests (validation)
└── Helper tests (utilities)

Integration Tests:
├── API endpoint tests
├── Database operation tests
└── Service layer tests

E2E Tests:
├── Lead scoring flow
├── Lead listing and filtering
└── Analytics calculation
```

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] SSL/TLS certificates installed
- [ ] Backup strategy configured
- [ ] Monitoring alerts set up
- [ ] Load balancer configured
- [ ] CDN setup for frontend
- [ ] Email notifications configured
- [ ] Rate limiting enabled
- [ ] Audit logging active
- [ ] Performance baseline established
- [ ] Disaster recovery plan documented
