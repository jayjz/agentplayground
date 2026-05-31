from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from app.agents.base import BaseAgent, AgentState
import structlog
import os
import json
from typing import Optional

logger = structlog.get_logger(__name__)

class ResearchOutput(BaseModel):
    technical_signals: str
    fundamental_catalysts: str
    sentiment_summary: str
    key_risks: str
    conviction_score: float = Field(..., ge=0.0, le=1.0)
    recommended_action: str
    summary: str

class SignalResearchAgent(BaseAgent):
    """Production-grade Signal Research Agent with LLM fallbacks"""
    
    def __init__(self, model_name: str = "llama3.2:latest"):
        super().__init__(model_name)
        self.llm = self._get_llm_with_fallback(model_name)
        self.parser = PydanticOutputParser(pydantic_object=ResearchOutput)

    def _get_llm_with_fallback(self, model_name: str):
        # Primary: Ollama (local)
        try:
            return ChatOllama(
                model=model_name,
                temperature=0.2,
                num_ctx=16384,
                format="json"
            )
        except Exception as e:
            logger.warning("Ollama failed, trying OpenAI fallback", error=str(e))

        # Fallback: OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=api_key)
            except ImportError:
                logger.error("langchain-openai not installed")
            except Exception as e:
                logger.error("OpenAI fallback failed", error=str(e))

        raise RuntimeError("No LLM backend available. Run Ollama or install langchain-openai + set OPENAI_API_KEY")

    async def run(self, state: AgentState) -> AgentState:
        self.logger.info("Starting SignalResearchAgent", ticker=state.ticker)

        system_prompt = """You are a senior quantitative researcher at a multi-billion dollar hedge fund.
Be extremely critical, data-driven, concise, and never hallucinate."""

        user_prompt = f"""
Analyze {state.ticker} for trading signals.
Hypothesis: {state.hypothesis or "None provided"}

{self.parser.get_format_instructions()}

Return ONLY valid JSON. No extra text.
"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = await self.llm.ainvoke(messages)
            content = response.content.strip()

            parsed = self.parser.parse(content)
            state.analysis = parsed.model_dump()
            state.confidence = parsed.conviction_score
            state.status = "research_complete"
            state.raw_data["research_output"] = content

        except Exception as e:
            logger.error("SignalResearchAgent failed", ticker=state.ticker, error=str(e))
            state.status = "research_failed"
            state.analysis["error"] = str(e)

        return state