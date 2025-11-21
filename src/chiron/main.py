from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Chiron - HealthAtlas AI", version="0.1.0")

@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello, Chiron!"}


# a simple model for a blood test value (example)
class BloodTestItem(BaseModel):
    test_name: str
    value: float
    unit: Optional[str] = None
    measured_at: Optional[datetime] = None

@app.post("/api/v1/analyze/blood-test", tags=["analysis"])
async def analyze_blood_test(user_id: str, tests: List[BloodTestItem]):
    """
    Very small MVP analysis: echo the incoming tests and produce a trivial insight.
    Later we'll replace this with real rule-based analysis.
    """
    warnings = []
    for t in tests:
        if t.test_name.lower() == "glucose" and t.value > 120:
            warnings.append(f"High glucose: {t.value} {t.unit or ''}".strip())

    insight = {
        "user_id": user_id,
        "warnings": warnings,
        "summary": f"Received {len(tests)} tests",
    }
    return insight
