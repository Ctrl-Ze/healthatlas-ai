from fastapi import Request
from chiron.agents.llm_client import LLMClient

def get_llm_client(request: Request) -> LLMClient:
    """
    Provides the shared LLMClient instance from app state.
    """
    llm = getattr(request.app.state, "llm", None)
    if not llm:
        raise RuntimeError("LLMClient is not initialized in app state")
    return llm