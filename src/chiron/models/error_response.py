from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    message: str
    status: int
    timestamp: datetime
    traceId: Optional[str] = None