# src/chiron/app.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from chiron.core.logging import configure_logging, get_logger
from chiron.core.errors import register_exception_handlers
from chiron.agents.llm_client import LLMClient

from chiron.api.v1.ai_analysis import router as ai_router
from chiron.api.v1.deterministic_analysis import router as det_router

load_dotenv()
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: initialize optional LLM client
    try:
        app.state.llm = LLMClient()  # will be disabled if no key
        logger.info("App startup: LLM client set (may be disabled)")
    except Exception as e:
        logger.exception("Failed to initialize LLM client: %s", e)
        app.state.llm = LLMClient(api_key=None)  # disabled client
    yield
    logger.info("App shutdown")


def create_app() -> FastAPI:
    app = FastAPI(title="Chiron - HealthAtlas AI", version="0.1.0", lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(det_router, prefix="/api/v1/analyze")
    app.include_router(ai_router, prefix="/api/v1/analyze")
    return app


app = create_app()
