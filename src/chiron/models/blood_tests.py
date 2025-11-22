from typing import List
from typing import Optional
from pydantic import BaseModel

class BloodTestItem(BaseModel):
    analyte: str
    value: float
    unit: Optional[str] = None
    normal_low: Optional[float] = None
    normal_high: Optional[float] = None

class BloodTestRequest(BaseModel):
    user_id: str
    tests: List[BloodTestItem]