import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from chiron.agents.llm_client import LLMClient
from chiron.api.analysis_router import router as analysis_router
from chiron.api.ai_analysis_router import router as ai_analysis_router

logging.basicConfig(level=logging.INFO)
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.llm = LLMClient()
    logging.debug("LLMClient initialized")

    yield

    # ---- Shutdown (optional cleanup) ----
    # If you ever add a streaming client or DB connection, close it here
    logging.debug("Shutting down... LLMClient cleanup")

app = FastAPI(
    title="Chiron - HealthAtlas AI",
    version="0.1.0",
    lifespan=lifespan)

app.include_router(analysis_router, prefix="/api/v1/analyze")
app.include_router(ai_analysis_router, prefix="/api/v1/analyze")