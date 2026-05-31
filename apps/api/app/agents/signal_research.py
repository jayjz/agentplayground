from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from app.agents.base import BaseAgent, AgentState
import structlog
import json
from typing import Dict, Any

logger = structlog.get_logger(__name__)

class SignalResearchAgent(BaseAgent):
    """Production-grade Signal Research Agent"""
    
    def __init__(self, model_name: str = "llama3.2:latest"):
        super().__init__(model_name)
        self.llm = ChatOllama(
            model=self.model_name,
            temperature=0.25,
            num_ctx=16384,
            format="json"
        )
    
    async def run(self, state: AgentState) -> AgentState:
        self.logger.info("Starting structured research", ticker=state.ticker)
        
        system_prompt = """You are a senior quantitative researcher at a multi-billion dollar hedge fund.
Be extremely critical, data-driven, and concise. Never hallucinate facts."""
        
        user_prompt = f'''
Analyze {state.ticker} for trading signals.

Hypothesis: {state.hypothesis or "None provided"}

Return valid JSON with this exact structure:
{{
  "technical_signals": "...", 
  "fundamental_catalysts": "...",
  "sentiment_summary": "...",
  "key_risks": "...",
  "conviction_score": 0.XX,
  "recommended_action": "buy|hold|sell|monitor",
  "summary": "..."
}}
'''
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            content = response.content.strip()
            
            # Try to parse JSON
            try:
                parsed = json.loads(content)
                state.analysis = parsed
                state.confidence = float(parsed.get("conviction_score", 0.5))
            except:
                state.analysis["raw"] = content
                state.confidence = 0.6
            
            state.raw_data["research_output"] = content
            state.status = "research_complete"
            
            self.logger.info("Research completed", ticker=state.ticker, confidence=state.confidence)
            
        except Exception as e:
            self.logger.error("Agent failed", ticker=state.ticker, error=str(e))
            state.status = "research_failed"
            state.analysis["error"] = str(e)
        
        return state
