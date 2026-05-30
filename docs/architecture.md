# Architecture

## System Overview

AgentPlayground is a local-first agentic research platform for hedge-fund style quantitative research and paper trading.

### Core Components

1. **Data Layer**
   - PostgreSQL + pgvector for transactional data and embeddings
   - Redis for caching and job queues
   - DuckDB for local analytical workloads
   - Polars for high-performance data processing

2. **API Layer (FastAPI)**
   - REST endpoints for CRUD operations
   - WebSocket for real-time updates
   - Background workers for data ingestion
   - Agent orchestration via LangGraph

3. **Agent System**
   - Signal Research Agent: Generates trading hypotheses
   - Event Interpretation Agent: Analyzes news/events
   - Regime Agent: Identifies market regimes
   - Relative Value Agent: Finds mispricings
   - Risk Narrative Agent: Explains risk exposures

4. **Portfolio Management**
   - Candidate generation from signals
   - Scoring and ranking
   - Constraint checking
   - Paper trading execution
   - Human approval gates

5. **Frontend (Next.js)**
   - Real-time dashboard
   - Signal explorer
   - Event feed
   - Trade review interface
   - Backtest visualization

### Data Flow

```
Market Data → Ingestion Workers → PostgreSQL
                                      ↓
News/Events → Event Agent → Signal Research Agent → Candidates
                                      ↓
                                 Portfolio Engine → Human Review → Paper Trading
                                      ↓
                                 Audit Log (Immutable)
```

### Agent Workflow (LangGraph)

Each agent follows a ReAct pattern:
1. Observe: Gather context and data
2. Think: Analyze and form hypothesis
3. Act: Query tools or generate output
4. Reflect: Evaluate confidence and next steps

Agents communicate via shared state in PostgreSQL and Redis.

### Security Model

- All secrets in environment variables
- No hardcoded credentials
- API authentication via JWT
- Row-level security in PostgreSQL
- Immutable audit logs
- Paper trading by default (live trading requires explicit config)

### Scalability Considerations

- Stateless API servers (horizontal scaling)
- Redis for distributed locking
- PostgreSQL connection pooling
- DuckDB for analytical queries (avoids OLTP contention)
- Prefect for workflow orchestration
