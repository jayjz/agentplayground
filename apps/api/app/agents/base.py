from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger(__name__)


class AgentState(BaseModel):
    """Shared state across all agents"""
    task_id: str
    ticker: str
    hypothesis: Optional[str] = None
    raw_data: Dict[str, Any] = {}
    analysis: Dict[str, Any] = {}
    confidence: float = 0.0
    evidence: list[Dict[str, Any]] = []
    risks: list[Dict[str, Any]] = []
    next_steps: list[str] = []
    human_approval_needed: bool = True
    status: str = "initialized"


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, model_name: str = "llama3.2:latest"):
        self.model_name = model_name
        self.logger = logger.bind(agent=self.__class__.__name__)
    
    @abstractmethod
    async def run(self, state: AgentState) -> AgentState:
        pass
