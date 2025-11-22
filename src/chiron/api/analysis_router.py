
from typing import List
from fastapi import APIRouter, HTTPException, Query
from chiron.models.blood_tests import BloodTestItem, BloodTestRequest
from chiron.services.analysis_service import AnalysisService


router = APIRouter()
analysis_service = AnalysisService()

@router.post("/blood-test/deterministic", tags=["analysis"])
async def analyze_blood_tests_deterministic(req: BloodTestRequest):

    if not req.tests:
        raise HTTPException(
            status_code=400,
            detail="Request must include at least one blood test"
        )
     
    tests_list = [t.model_dump() for t in req.tests]
    rule_output = analysis_service.analyze(tests_list)
    return {
        "user_id": req.user_id,
        **rule_output
    }