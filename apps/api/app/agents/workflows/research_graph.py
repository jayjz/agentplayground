from langgraph.graph import StateGraph, END
from app.agents.base import AgentState
from app.agents.signal_research import SignalResearchAgent
from app.agents.risk_analysis import RiskAnalysisAgent
from app.agents.portfolio_agent import PortfolioAgent
import structlog
from typing import Optional

logger = structlog.get_logger(__name__)

async def run_research_workflow(ticker: str, hypothesis: Optional[str] = None) -> AgentState:
    """Multi-agent supervisor workflow"""
    
    initial_state = AgentState(
        task_id=f"research_{ticker}_{int(__import__('time').time())}",
        ticker=ticker.upper(),
        hypothesis=hypothesis
    )
    
    research_agent = SignalResearchAgent()
    risk_agent = RiskAnalysisAgent()
    portfolio_agent = PortfolioAgent()
    
    workflow = StateGraph(AgentState)
    
    workflow.add_node("research", research_agent.run)
    workflow.add_node("risk", risk_agent.run)
    workflow.add_node("portfolio", portfolio_agent.run)
    
    # Sequential flow for now (can be made parallel later)
    workflow.set_entry_point("research")
    workflow.add_edge("research", "risk")
    workflow.add_edge("risk", "portfolio")
    workflow.add_edge("portfolio", END)
    
    app = workflow.compile()
    
    logger.info("Starting multi-agent research workflow", ticker=ticker)
    
    try:
        result: AgentState = await app.ainvoke(initial_state)
        return result
    except Exception as e:
        logger.error("Workflow failed", error=str(e))
        initial_state.status = "failed"
        initial_state.analysis["error"] = str(e)
        return initial_state