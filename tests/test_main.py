from ast import List
from datetime import datetime
from fastapi.testclient import TestClient
from pydantic import BaseModel
from chiron.main import BloodTestItem, app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, Chiron!"}

def test_analyze():
    current_time_string = datetime.now().isoformat()
    payload = [
        {
            "test_name": "glucose", 
            "value": 130, 
            "unit": "mg/dL",
            "measured_at": current_time_string
        }
    ]

    r = client.post("/api/v1/analyze/blood-test?user_id=test-user", json=payload)
    # --- DEBUGGING STEP ---
    if r.status_code != 200:
        print("\n--- Pydantic Validation Error ---")
        print(r.json())
        print("-----------------------------------")
    # ----------------------
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "test-user"
    assert any("glucose" in w.lower() for w in body["warnings"])