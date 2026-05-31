from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.base import BaseAgent, AgentState
from app.agents.signal_research import ResearchOutput  # reuse schema if you want
import structlog
from typing import Any

logger = structlog.get_logger(__name__)

class RiskAnalysisAgent(BaseAgent):
    """Critical risk analysis agent with LLM fallbacks"""
    
    async def run(self, state: AgentState) -> AgentState:
        self.logger.info("Starting risk analysis", ticker=state.ticker)
        
        system_prompt = """You are a senior risk manager at a multi-billion dollar hedge fund.
Be extremely conservative and identify real risks only."""
        
        user_prompt = f"""
Analyze risks for {state.ticker}.
Current research: {state.analysis}

Return valid JSON:
{{
  "key_risks": ["risk1", "risk2"],
  "risk_score": 0.XX,
  "mitigation_steps": ["step1", "step2"],
  "overall_risk_level": "low|medium|high"
}}
"""
        
        try:
            response = await self.llm.ainvoke([  # uses the fallback LLM from BaseAgent
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            # TODO: Add proper Pydantic parsing like in SignalResearchAgent
            state.analysis["risk_analysis"] = response.content
            state.risks.append({"ticker": state.ticker, "analysis": response.content})
            state.status = "risk_complete"
        except Exception as e:
            logger.error("Risk agent failed", error=str(e))
            state.status = "risk_failed"
        
        return state