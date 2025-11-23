import json
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid
from .logging import get_logger
from chiron.models.error_response import ErrorResponse

logger = get_logger(__name__)

class AIUnavailableError(Exception):
    pass

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        trace_id = request.headers.get("x-trace-id") or str(uuid.uuid4())
        logger.exception("Unhandled exception (trace=%s): %s", trace_id, exc)
        payload = ErrorResponse(
            error=exc.__class__.__name__,
            message=str(exc),
            status=500,
            timestamp=datetime.utcnow(),
            traceId=trace_id
        )
        return JSONResponse(
            status_code=500,
            content=json.loads(payload.model_dump_json())
)
