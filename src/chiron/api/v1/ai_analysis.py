import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from chiron.models.blood_tests import BloodTestRequest
from chiron.models.error_response import ErrorResponse
from chiron.services.analysis_service import AnalysisService
from chiron.core.dependencies import get_llm_client, get_analysis_service
from chiron.agents.llm_client import AIUnavailableError, LLMClient

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/blood-test/ai",
    tags=["analysis"],
    response_model=dict,
    responses={503: {"model": ErrorResponse}}
)
async def analyze_blood_tests_ai(
    request: Request,
    req: BloodTestRequest,
    llm: LLMClient = Depends(get_llm_client),
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """
    Deterministic analysis + JSON-mode OpenAI summary.
    """

    trace_id = request.headers.get("X-Trace-Id", "no-trace-id")

    if not req.tests:
        raise HTTPException(status_code=400, detail="At least one test is required")

    tests_list = [t.model_dump() for t in req.tests]

    rule_output = analysis_service.analyze(tests_list)

    response_payload = {
        "traceId": trace_id,
        "user_id": req.user_id,
        "summary": {
            "abnormal_count": rule_output["analysis"]["abnormal_count"],
            "risk_level": rule_output["analysis"]["risk_level"],
            "critical_findings": rule_output["warnings"][:5],
        },
        "results": rule_output["results"],
        "facts": rule_output["facts"],
        "ai_summary": None,
        "lifestyle_suggestions": []
    }

    try:
        ai_out = await llm.summarize_with_lifestyle(
            warnings=rule_output["warnings"],
            tests=tests_list,
            profile=None
        )

        response_payload["ai_summary"] = ai_out.get("ai_summary")
        response_payload["lifestyle_suggestions"] = ai_out.get("lifestyle_suggestions", [])

        logger.info(f"[traceId={trace_id}] AI summary generated successfully")

    except AIUnavailableError as e:
        logger.error(f"[traceId={trace_id}] LLM unavailable: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))

    return response_payload