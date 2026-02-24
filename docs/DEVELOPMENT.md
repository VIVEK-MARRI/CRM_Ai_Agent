# Development Guide

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

## Backend Development

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with local database and Redis settings
```

### 4. Start PostgreSQL (if local)
```bash
# Mac/Linux with Homebrew
brew services start postgresql

# Or use Docker
docker run -d \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=lead_scoring_db \
  -p 5432:5432 \
  postgres:15-alpine
```

### 5. Start Redis (if local)
```bash
# Mac/Linux with Homebrew
brew services start redis

# Or use Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### 6. Initialize Database
```bash
python -m seed_data.init_seed
```

### 7. Run Backend Server
```bash
python -m uvicorn app.main:app --reload --port 8000
```

Server runs on: http://localhost:8000

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Frontend Development

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

Frontend runs on: http://localhost:5173

### 3. Environment Variables
Create `.env.local`:
```
VITE_API_URL=http://localhost:8000/api
```

## Project File Structure

### Backend Files

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app factory
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py          # Route aggregation
│   │   ├── leads.py           # Lead endpoints
│   │   └── health.py          # Health check
│   ├── services/
│   │   ├── __init__.py
│   │   └── lead_service.py    # Lead business logic
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── scoring_engine.py  # Scoring algorithms
│   │   ├── explanation_engine.py
│   │   └── next_action_engine.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── lead.py            # SQLAlchemy models
│   │   └── schemas.py         # Pydantic schemas
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py        # Database setup
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration
│   │   └── logging.py         # Logging setup
│   └── __init__.py
├── seed_data/
│   ├── __init__.py
│   ├── leads.py               # Sample data
│   └── init_seed.py           # Seed script
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

### Frontend Files

```
frontend/
├── src/
│   ├── App.jsx                # Main app
│   ├── main.jsx               # Entry point
│   ├── index.css              # Global styles
│   ├── components/
│   │   ├── KPICard.jsx
│   │   ├── LeadTable.jsx
│   │   ├── ScoreLead.jsx
│   │   ├── ScoreCircle.jsx
│   │   ├── ScoreExplanationDrawer.jsx
│   │   └── AnalyticsOverview.jsx
│   ├── services/
│   │   └── api.js             # API client
│   ├── utils/
│   │   └── helpers.js         # Helper functions
│   └── styles/
│       └── globals.css
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── package.json
├── Dockerfile
└── .gitignore
```

## Common Development Tasks

### Add a New Lead Input Field

1. **Update backend schema** (`backend/app/models/schemas.py`):
```python
class LeadInput(BaseModel):
    # existing fields...
    new_field: bool = False
```

2. **Update database model** (`backend/app/models/lead.py`):
```python
class Lead(Base):
    # existing fields...
    new_field = Column(Boolean, default=False)
```

3. **Update scoring config** (`config/scoring_weights.yaml`):
```yaml
weights:
  new_field:
    weight: 20
    description: "Description of new field"
```

4. **Update frontend form** (`frontend/src/components/ScoreLead.jsx`):
```javascript
const [formData, setFormData] = useState({
  // existing fields...
  new_field: false,
})
```

### Modify Scoring Weights

Edit `config/scoring_weights.yaml`:
```yaml
weights:
  demo_requested:
    weight: 30  # Changed from 25
```

Restart backend - no code changes needed!

### Add New Component

1. Create `frontend/src/components/NewComponent.jsx`
2. Import in `frontend/src/App.jsx`
3. Use in appropriate tab/section

### Fix a Bug

1. Create feature branch: `git checkout -b fix/bug-name`
2. Reproduce the issue
3. Write test (if applicable)
4. Fix the bug
5. Run tests
6. Submit PR

## Debugging

### Backend
```python
# Add debug prints
from app.core.logging import logger
logger.debug(f"Debug info: {value}")

# Check database
import sqlite3
conn = sqlite3.connect('lead_scoring.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM leads")
```

### Frontend
- Use browser DevTools (F12)
- React Developer Tools extension
- Console logging with `console.log()`
- Network tab to inspect API calls

## Testing

### Backend
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_scoring_engine.py

# With coverage
pytest --cov=app tests/
```

### Frontend
```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

## Code Quality

### Backend
```bash
# Format code
black app/

# Linting
flake8 app/

# Type checking
mypy app/
```

### Frontend
```bash
# Format code
npx prettier --write src/

# Linting
npm run lint

# Type checking (TypeScript, if using)
```

## Performance Profiling

### Backend
```python
import cProfile
import pstats

pr = cProfile.Profile()
pr.enable()

# Your code here
result = service.score_lead(lead_data)

pr.disable()
ps = pstats.Stats(pr)
ps.print_stats()
```

### Frontend
Use Chrome DevTools Performance tab:
1. Open DevTools
2. Go to Performance tab
3. Record actions
4. Analyze flamegraph

## Database Troubleshooting

### Reset Database
```bash
# Delete all data
python -c "from app.db.database import SessionLocal, Lead; \
  db = SessionLocal(); \
  db.query(Lead).delete(); \
  db.commit()"

# Re-seed
python -m seed_data.init_seed
```

### View Database
```bash
# Using psql
psql postgresql://postgres:postgres@localhost/lead_scoring_db

# List leads
SELECT id, email, score, intent_level FROM leads ORDER BY score DESC;
```

## Deployment

### Local Docker
```bash
docker-compose up --build
```

### Production Considerations
See ARCHITECTURE.md → Deployment section

## Resources

- FastAPI: https://fastapi.tiangolo.com
- Pydantic: https://pydantic-settings.readthedocs.io
- SQLAlchemy: https://www.sqlalchemy.org
- React: https://react.dev
- Vite: https://vitejs.dev
- Recharts: https://recharts.org
- Framer Motion: https://www.framer.com/motion
- TailwindCSS: https://tailwindcss.com

## Support

Having issues? Check:
1. Environment variables are set
2. Ports are available (8000, 5173, 5432, 6379)
3. Database is running
4. Redis is running
5. Dependencies are installed
6. Logs for error messages
