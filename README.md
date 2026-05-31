# AgentPlayground

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green.svg)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

**Agentic hedge-fund research copilot and market intelligence platform.** Multi-agent system for signal research, event interpretation, and risk analysis with real-time market data, paper trading infrastructure, and human-in-the-loop approvals.

<p align="center">
  <img src="docs/screenshots/dashboard.png" alt="AgentPlayground Dashboard" width="800">
  <br>
  <em>Dashboard, agent workflows, and paper trading interface - screenshots coming soon</em>
</p>

## Overview

AgentPlayground is a local-first research platform that orchestrates specialized AI agents to:

- **Research signals** across market data, news, and filings
- **Interpret events** with contextual understanding and cross-referencing  
- **Analyze risk** through multi-factor models and scenario testing
- **Propose trades** with full reasoning traces and human approval gates
- **Learn continuously** from outcomes and feedback

Built for quantitative researchers and systematic traders who need transparent, auditable AI assistance—not black-box predictions.

## ✨ Key Features

- **Multi-Agent Workflows** - Specialized agents (research, risk, portfolio) coordinated via LangGraph
- **Real-Time Data** - Live market feeds, news ingestion, and SEC filing monitoring
- **Paper Trading First** - All strategies validated in simulation before any live consideration
- **Human-in-the-Loop** - Explicit approval required for all order proposals with full audit trail
- **Local-First Architecture** - Docker Compose stack runs entirely on your infrastructure
- **Vector Intelligence** - Semantic search across research notes, filings, and market commentary

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Frontend                         │
│  Dashboard • Research Workspace • Paper Trading • Analytics │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST + WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Agents    │  │  Workflows   │  │   Data Layer    │   │
│  │  (LangGraph)│  │  (Prefect)   │  │  PG + Redis +   │   │
│  │             │  │              │  │  DuckDB + Qdrant│   │
│  └─────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow:**
Market Data → Ingestion → Vector DB → Agents → Research → Portfolio Agent → Human Review → Paper Trading → Analytics

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Node.js 20+ and pnpm
- Make

### Installation

```bash
# Clone repository
git clone https://github.com/jayjz/agentplayground.git
cd agentplayground

# Configure environment
cp .env.example .env
# Add your API keys to .env

# Install dependencies
make install

# Start infrastructure
make setup-dev
# Starts: PostgreSQL, Redis, Qdrant, Prefect
```

### Development Servers

```bash
# Terminal 1 - API (http://localhost:8000)
cd apps/api
uvicorn app.main:app --reload

# Terminal 2 - Web UI (http://localhost:3000)
cd apps/web
pnpm dev

# Terminal 3 - Prefect UI (http://localhost:4200)
prefect server start
```

### First Steps

1. **Access the dashboard** at http://localhost:3000
2. **Configure data sources** in Settings → API Keys
3. **Run initial ingestion**: `make ingest-historical SYMBOLS=AAPL,MSFT,GOOGL`
4. **Start research agent**: Navigate to Research → New Hypothesis
5. **Review paper trades** in Portfolio → Proposals (requires human approval)

## 📁 Project Structure

```
agentplayground/
├── apps/
│   ├── api/                 # FastAPI backend + agents
│   │   ├── app/
│   │   │   ├── agents/      # LangGraph agent implementations
│   │   │   ├── api/         # REST endpoints
│   │   │   ├── core/        # Config, logging, security
│   │   │   ├── models/      # SQLAlchemy models
│   │   │   ├── services/    # Business logic
│   │   │   └── workflows/   # Prefect flows
│   │   └── tests/
│   └── web/                 # Next.js 14 frontend
│       ├── app/             # App router pages
│       ├── components/      # React components
│       └── lib/             # API client, utils
├── packages/
│   └── shared/              # Shared TypeScript types
├── infra/
│   ├── docker/              # Dockerfiles
│   ├── postgres/            # DB initialization
│   └── observability/       # OpenTelemetry config
└── docs/                    # Architecture docs
```

## 🤖 Agent Workflows

### Signal Research Agent
Analyzes market data, news, and filings to identify potential opportunities:
```python
from app.agents import SignalResearchAgent

agent = SignalResearchAgent()
result = await agent.research(
    ticker="AAPL",
    hypothesis="Services revenue acceleration",
    lookback_days=90
)
# Returns: evidence, confidence score, related signals
```

### Risk Analysis Agent
Multi-factor risk assessment and scenario modeling:
```python
agent = RiskAnalysisAgent()
risk_profile = await agent.analyze_portfolio(
    positions=[...],
    scenarios=["rate_hike", "earnings_miss", "sector_rotation"]
)
```

### Portfolio Agent
Generates trade proposals with full reasoning traces:
```python
agent = PortfolioAgent()
proposal = await agent.propose_trade(
    signal=result,
    risk_profile=risk_profile,
    max_position_size=0.05
)
# Requires human approval before execution
```

## 💼 Paper Trading

**Safety First:** Live trading is disabled by default and requires explicit opt-in via `LIVE_TRADING_ENABLED=true`.

**Paper Trading Features:**
- Realistic order execution with configurable slippage models
- Portfolio-level risk checks and position limits
- Full audit trail of all decisions and approvals
- Performance attribution and P&L tracking
- Integration with research notes and signal provenance

**Approval Workflow:**
1. Agent generates proposal with reasoning trace
2. Appears in dashboard with risk metrics
3. Human reviews and approves/rejects
4. If approved: executes in paper environment
5. Outcome logged for agent learning

## 🛠️ Development

### Common Commands

```bash
make lint              # Ruff + ESLint
make format            # Auto-format all code
make test              # Pytest + Vitest
make test-e2e          # Playwright E2E tests
make docker-up         # Start all services
make db-migrate        # Create migration
make db-upgrade        # Apply migrations
```

### Adding a Data Provider

```python
# apps/api/app/services/data_providers/my_provider.py
from .base import DataProvider

class MyProvider(DataProvider):
    async def fetch_quotes(self, symbols: list[str]) -> list[Quote]:
        # Implementation
        pass
```

Register in `__init__.py` and add credentials to `.env`.

## 📊 Monitoring & Observability

- **Logs:** Structured JSON logs in `logs/` (rotated daily)
- **Metrics:** OpenTelemetry traces sent to configured backend
- **Health:** `/health` endpoint for each service
- **Prefect UI:** http://localhost:4200 for workflow monitoring

## 🧪 Testing

```bash
# Backend with coverage
cd apps/api
pytest -v --cov=app --cov-report=html

# Frontend
cd apps/web
pnpm test        # Unit tests
pnpm test:e2e    # E2E with Playwright
```

## 📚 Documentation

- [Architecture Deep Dive](docs/architecture.md) - System design and data flows
- [Local Development](docs/local-development.md) - Detailed setup and troubleshooting  
- [API Reference](docs/api-overview.md) - REST and WebSocket APIs
- [Agent Development](docs/agent-workflows.md) - Building custom agents
- [Data Model](docs/data-model.md) - Database schema and relationships
- [Deployment Guide](docs/deployment.md) - Production deployment

## ⚠️ Important Disclaimers

**Research Software:** This is a research and educational platform, not a production trading system.

**Do NOT use for live trading without:**
- Extensive backtesting and validation
- Professional risk management review
- Legal and compliance approval
- Understanding that past performance doesn't guarantee future results
- Explicitly setting `LIVE_TRADING_ENABLED=true` (disabled by default)

**No Financial Advice:** All outputs are for research purposes only. Not investment advice.

## 📄 License

Proprietary - All rights reserved. See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Internal project. See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and architecture decision records (ADRs).

---

**Built for systematic traders who want AI assistance without black boxes.** Every decision is explainable, every trade is auditable, and humans stay in control.
