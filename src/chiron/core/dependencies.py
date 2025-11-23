from fastapi import Request

from chiron.agents.llm_client import LLMClient
from chiron.services.analysis_service import AnalysisService


def get_llm_client(request: Request) -> LLMClient:
    llm = getattr(request.app.state, "llm", None)
    if llm is None:
        # return disabled client (won't raise on creation)
        return LLMClient(api_key=None)
    return llm


def get_analysis_service() -> AnalysisService:
    # simple instantiation; replace with DI if it needs resources later
    return AnalysisService()
