from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.base import BaseAgent, AgentState
import structlog

logger = structlog.get_logger(__name__)

class PortfolioAgent(BaseAgent):
    """Portfolio recommendation agent"""
    
    async def run(self, state: AgentState) -> AgentState:
        self.logger.info("Starting portfolio recommendation", ticker=state.ticker)
        
        system_prompt = """You are a senior portfolio manager. Give clear, actionable portfolio advice."""
        
        user_prompt = f"""
Based on the research and risk analysis for {state.ticker}:
{state.analysis}

Recommend portfolio action. Return valid JSON:
{{
  "recommended_action": "buy|hold|sell|monitor",
  "position_size": "small|medium|large|none",
  "time_horizon": "short|medium|long",
  "rationale": "..."
}}
"""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            state.analysis["portfolio_recommendation"] = response.content
            state.status = "portfolio_complete"
        except Exception as e:
            logger.error("Portfolio agent failed", error=str(e))
            state.status = "portfolio_failed"
        
        return state