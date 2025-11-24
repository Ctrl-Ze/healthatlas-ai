import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from chiron.api.v1.deterministic_analysis import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


# ------------------------------------------------------------
# SUCCESS CASE
# ------------------------------------------------------------


def test_deterministic_analysis_success(client):
    payload = {
        "user_id": "user123",
        "tests": [
            {
                "analyte": "Glucose",
                "value": 110,
                "unit": "mg/dL",
                "normal_low": 70,
                "normal_high": 99,
            }
        ],
    }

    headers = {"X-Trace-Id": "abc-123"}

    resp = client.post("/blood-test/deterministic", json=payload, headers=headers)
    assert resp.status_code == 200

    data = resp.json()

    # top-level envelope
    assert data["traceId"] == "abc-123"
    assert data["user_id"] == "user123"

    # deterministic analysis structure
    assert "warnings" in data
    assert "analysis" in data
    assert "facts" in data
    assert "results" in data

    # known interpretation type
    assert isinstance(data["warnings"], list)
    assert isinstance(data["results"], list)


# ------------------------------------------------------------
# VALIDATION: EMPTY TESTS SHOULD FAIL
# ------------------------------------------------------------


def test_deterministic_analysis_requires_tests(client):
    payload = {"user_id": "u123", "tests": []}

    resp = client.post("/blood-test/deterministic", json=payload)

    assert resp.status_code == 400
    assert resp.json()["detail"] == "At least one test is required"
