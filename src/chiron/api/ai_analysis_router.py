import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel

from chiron.agents.llm_client import AIUnavailableError, LLMClient
from chiron.api.dependencies import get_llm_client
from chiron.models.blood_tests import BloodTestItem, BloodTestRequest
from chiron.services.analysis_service import AnalysisService

logging.basicConfig(level=logging.INFO)

router = APIRouter()
analysis_service = AnalysisService()

@router.post("/blood-test/ai", tags=["analysis"])
async def analyze_blood_tests_ai(
    request: Request,
    req: BloodTestRequest,
    llm: LLMClient = Depends(get_llm_client)
    ):
    """
    Deterministic analysis followed by an optional LLM summary + lifestyle hints.
    """

    if not req.tests:
        raise HTTPException(
            status_code=400,
            detail="Request must include at least one blood test"
        )

    tests_list = [t.model_dump() for t in req.tests]
    rule_output = analysis_service.analyze(tests_list)

    response_payload = {
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
            profile=None # hook up profile fetching later
        )
        logging.error(f"response_payload: {response_payload}")
        response_payload["ai_summary"] = ai_out.get("ai_summary")
        response_payload["lifestyle_suggestions"] = ai_out.get("lifestyle_suggestions", [])
    except AIUnavailableError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )
    
    return response_payload
            
