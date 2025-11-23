import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from chiron.core.dependencies import get_analysis_service
from chiron.models.blood_tests import BloodTestItem, BloodTestRequest
from chiron.services.analysis_service import AnalysisService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/blood-test/deterministic",
    tags=["analysis"],
    response_model=dict
)
async def analyze_blood_tests_deterministic(
    request: Request,
    req: BloodTestRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service)
):

    trace_id = request.headers.get("X-Trace-Id", "no-trace-id")

    if not req.tests:
        raise HTTPException(status_code=400, detail="At least one test is required")

    tests_list = [t.model_dump() for t in req.tests]
    rule_output = analysis_service.analyze(tests_list)

    logger.info(f"[traceId={trace_id}] Deterministic analysis completed")

    return {
        "traceId": trace_id,
        "user_id": req.user_id,
        **rule_output
    }
