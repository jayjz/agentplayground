# Local Development

## Prerequisites

- Docker Desktop or Docker Engine
- Python 3.12+
- Node.js 20+ and pnpm 8+
- Make
- Git

## Initial Setup

1. **Clone and configure:**
```bash
git clone <repo> agentplayground
cd agentplayground
cp .env.example .env
```

2. **Edit `.env`:**
Add at minimum:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- `ALPHA_VANTAGE_API_KEY` (optional, for market data)
- `SECRET_KEY` (generate with `openssl rand -hex 32`)

3. **Install dependencies:**
```bash
make install
```

This installs:
- Python dependencies via pip
- Node dependencies via pnpm
- Pre-commit hooks

4. **Start infrastructure:**
```bash
make setup-dev
```

This starts PostgreSQL, Redis, and Prefect, then runs migrations.

## Development Workflow

### Starting Services

**Option 1: Docker Compose (recommended for backend)**
```bash
make docker-up
```

**Option 2: Local services**
```bash
# Terminal 1: API
cd apps/api
uvicorn app.main:app --reload

# Terminal 2: Web
cd apps/web
pnpm dev

# Terminal 3: Worker (optional)
cd apps/api
python -m app.workers.main
```

### Database Migrations

Create a new migration after model changes:
```bash
make db-migrate msg="add signals table"
```

Apply migrations:
```bash
make db-upgrade
```

Revert last migration:
```bash
make db-downgrade
```

### Running Tests

```bash
# All tests
make test

# Backend only
cd apps/api && pytest -v

# Frontend only
cd apps/web && pnpm test

# With coverage
cd apps/api && pytest --cov=app --cov-report=html
```

### Code Quality

```bash
# Lint
make lint

# Format
make format

# Pre-commit (runs on git commit)
pre-commit run --all-files
```

## Project Structure

```
apps/api/
├── app/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── api/              # Route handlers
│   ├── core/             # Enums, exceptions, constants
│   ├── models/           # SQLAlchemy models
│   ├── services/         # Business logic
│   ├── agents/           # LangGraph agents
│   ├── workflows/        # Prefect flows
│   └── db/               # Database utilities
├── migrations/           # Alembic migrations
└── tests/                # Pytest tests

apps/web/
├── app/                  # Next.js app router
├── components/           # React components
├── lib/                  # Utilities and API client
└── public/               # Static assets
```

## Debugging

### API Logs
```bash
docker-compose logs -f api
```

### Database
```bash
# Connect to PostgreSQL
docker exec -it ap-postgres psql -U agentplayground -d agentplayground

# Check pgvector
\dx vector
```

### Redis
```bash
docker exec -it ap-redis redis-cli
```

## Common Issues

**Port already in use:**
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9
```

**Database connection failed:**
- Ensure Docker services are running: `docker-compose ps`
- Check `.env` DATABASE_URL matches docker-compose settings

**Migrations out of sync:**
```bash
make db-reset  # WARNING: Destroys all data
```

**pnpm install fails:**
```bash
# Clear cache
pnpm store prune
rm -rf node_modules apps/web/node_modules
pnpm install
```

## Environment Variables

See `.env.example` for full list. Key variables:

- `ENVIRONMENT`: development, staging, production
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR
- `PAPER_TRADING_ENABLED`: Must be true for development
- `LIVE_TRADING_ENABLED`: Keep false unless you know what you're doing

## Adding New Features

1. **Backend:**
   - Add models in `apps/api/app/models/`
   - Create migration: `make db-migrate msg="..."`
   - Add API routes in `apps/api/app/api/`
   - Add business logic in `apps/api/app/services/`

2. **Frontend:**
   - Add pages in `apps/web/app/`
   - Add components in `apps/web/components/`
   - Update API client in `apps/web/lib/api.ts`

3. **Agents:**
   - Create agent in `apps/api/app/agents/`
   - Define LangGraph workflow
   - Register in agent registry

## Data Ingestion

Initial market data load:
```bash
cd apps/api
python -m app.workflows.ingest_historical --tickers AAPL,MSFT,GOOGL --days 365
```

This is a manual step - production would use Prefect schedules.
