from langgraph.graph import StateGraph, END
from app.agents.base import AgentState
from app.agents.signal_research import SignalResearchAgent
import structlog
from typing import Optional

logger = structlog.get_logger(__name__)

async def run_research_workflow(ticker: str, hypothesis: Optional[str] = None) -> AgentState:
    """Main research workflow using LangGraph"""
    
    initial_state = AgentState(
        task_id=f"research_{ticker}_{int(__import__('time').time())}",
        ticker=ticker.upper(),
        hypothesis=hypothesis
    )
    
    research_agent = SignalResearchAgent()
    
    workflow = StateGraph(AgentState)
    workflow.add_node("research", research_agent.run)
    workflow.set_entry_point("research")
    workflow.add_edge("research", END)
    
    app = workflow.compile()
    
    logger.info("Starting research workflow", ticker=ticker)
    
    try:
        result: AgentState = await app.ainvoke(initial_state)
        logger.info("Research workflow completed", ticker=ticker, status=result.status)
        return result
    except Exception as e:
        logger.error("Research workflow failed", ticker=ticker, error=str(e))
        initial_state.status = "failed"
        initial_state.analysis["error"] = str(e)
        return initial_state
