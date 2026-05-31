from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.agents.workflows.research_graph import run_research_workflow

router = APIRouter(prefix="/agents", tags=["agents"])


class ResearchRequest(BaseModel):
    ticker: str
    hypothesis: Optional[str] = None


class ResearchResponse(BaseModel):
    task_id: str
    ticker: str
    status: str
    confidence: float
    analysis: dict
    raw_data: dict


@router.post("/research/signal", response_model=ResearchResponse)
async def research_signal(request: ResearchRequest):
    """Run signal research agent workflow"""
    try:
        result = await run_research_workflow(
            ticker=request.ticker,
            hypothesis=request.hypothesis
        )
        
        return ResearchResponse(
            task_id=result.task_id,
            ticker=result.ticker,
            status=result.status,
            confidence=result.confidence,
            analysis=result.analysis,
            raw_data=result.raw_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))