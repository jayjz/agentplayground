# AgentPlayground

Production-grade monorepo for an agentic hedge-fund research copilot and market intelligence platform.

## Architecture

AgentPlayground is a local-first research platform that combines:
- Multi-agent workflows for signal research, event interpretation, and risk analysis
- Real-time market data ingestion and storage
- Paper trading infrastructure with human-in-the-loop approvals
- Vector embeddings for semantic search over research and filings

**Core Principles:**
- Paper trading by default - live trading requires explicit opt-in
- Immutable decision logs for auditability
- Human approval gates for all order proposals
- Local-first development with Docker Compose

## Tech Stack

**Backend:**
- Python 3.12, FastAPI, Pydantic v2
- LangGraph for agent orchestration
- LiteLLM for model routing
- PostgreSQL + pgvector, Redis, DuckDB, Polars
- SQLAlchemy 2.x, Alembic
- Prefect for workflows

**Frontend:**
- Next.js 14+ with TypeScript
- Tailwind CSS + shadcn/ui
- pnpm workspaces

**Infrastructure:**
- Docker Compose for local development
- GitHub Actions for CI
- OpenTelemetry for observability
- Structured JSON logging

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.12
- Node.js 20+ and pnpm
- Make

### Setup

1. Clone and install:
```bash
git clone <repo-url> agentplayground
cd agentplayground
cp .env.example .env
# Edit .env with your API keys
make install
```

2. Start infrastructure:
```bash
make setup-dev
```

3. Start development servers:
```bash
# Terminal 1 - API
cd apps/api
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Web
cd apps/web
pnpm dev
```

4. Access:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Web: http://localhost:3000
- Prefect: http://localhost:4200

## Project Structure

```
agentplayground/
├── apps/
│   ├── api/          # FastAPI backend
│   └── web/          # Next.js frontend
├── packages/
│   └── shared/       # Shared TypeScript/Python types
├── infra/            # Docker, DB init, observability
├── docs/             # Architecture and product docs
└── docker-compose.yml
```

## Development

### Common Commands

```bash
make lint          # Run all linters
make format        # Format code
make test          # Run tests
make docker-up     # Start services
make db-migrate    # Create migration (make db-migrate msg="description")
make db-upgrade    # Apply migrations
```

### Agent Development

Agents live in `apps/api/app/agents/` and use LangGraph for workflow orchestration:

```python
from app.agents.signal_research import SignalResearchAgent

agent = SignalResearchAgent()
result = await agent.research(ticker="AAPL", hypothesis="...")
```

### Adding Data Sources

1. Add provider in `apps/api/app/services/data_providers/`
2. Implement the `DataProvider` interface
3. Register in `app/services/data_providers/__init__.py`
4. Add credentials to `.env`

## Paper Trading

**IMPORTANT:** Live trading is disabled by default.

Paper trading simulates:
- Order execution with realistic slippage
- Portfolio tracking
- P&L calculation
- Risk checks

To propose a trade:
1. Agent generates candidate via `PortfolioAgent`
2. Candidate appears in dashboard for review
3. Human approves/rejects
4. If approved, executes in paper trading environment
5. All decisions logged immutably

## Documentation

- [Architecture](docs/architecture.md) - System design and data flows
- [Local Development](docs/local-development.md) - Detailed setup guide
- [API Overview](docs/api-overview.md) - REST and WebSocket APIs
- [Agent Workflows](docs/agent-workflows.md) - Agent design patterns
- [Data Model](docs/data-model.md) - Database schema
- [Security](docs/security.md) - Security model and secrets management

## Testing

```bash
# Backend
cd apps/api
pytest -v --cov=app

# Frontend
cd apps/web
pnpm test
pnpm test:e2e
```

## Deployment

See [docs/deployment.md](docs/deployment.md) for production deployment guides.

**Note:** This is research software. Do not use for live trading without:
1. Extensive testing
2. Risk management review
3. Legal/compliance approval
4. Explicitly enabling `LIVE_TRADING_ENABLED=true`

## License

Proprietary - All rights reserved

## Contributing

Internal project. See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.
