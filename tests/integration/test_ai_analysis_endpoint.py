import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from chiron.agents.llm_client import AIUnavailableError
from chiron.api.v1.ai_analysis import router
from chiron.core.dependencies import get_analysis_service, get_llm_client
from chiron.services.analysis_service import AnalysisService


# --------------------------------------------------------------------
# Fake LLM Client
# --------------------------------------------------------------------
class FakeLLMClient:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    async def summarize_with_lifestyle(self, warnings, tests, profile=None):
        if self.should_fail:
            raise AIUnavailableError("LLM temporarily unavailable")

        return {
            "ai_summary": "Everything looks fine.",
            "lifestyle_suggestions": ["Drink more water", "Regular exercise"],
        }


# --------------------------------------------------------------------
# Fake Analysis Service
# --------------------------------------------------------------------
class FakeAnalysisService(AnalysisService):
    def analyze(self, tests_list):
        # Return deterministic mock analysis for integration test
        return {
            "warnings": ["High cholesterol detected"],
            "analysis": {
                "abnormal_count": 1,
                "risk_level": "moderate",
            },
            "results": [{"analyte": "LDL", "value": 190}],
            "facts": {"low": [], "high": ["LDL"], "normal": []},
        }


# --------------------------------------------------------------------
# FastAPI test app using dependency overrides
# --------------------------------------------------------------------
@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)

    # Default fakes
    app.dependency_overrides[get_llm_client] = lambda: FakeLLMClient()
    app.dependency_overrides[get_analysis_service] = lambda: FakeAnalysisService()

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


# --------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------


def test_ai_integration_success(client):
    payload = {
        "user_id": "abc123",
        "tests": [
            {
                "analyte": "LDL",
                "value": 190,
                "normal_low": 0,
                "normal_high": 130,
            }
        ],
    }

    response = client.post("/blood-test/ai", json=payload)
    assert response.status_code == 200

    data = response.json()

    # Core checks
    assert data["user_id"] == "abc123"
    assert data["summary"]["abnormal_count"] == 1
    assert data["summary"]["risk_level"] == "moderate"

    # AI results
    assert data["ai_summary"] == "Everything looks fine."
    assert "Drink more water" in data["lifestyle_suggestions"]


def test_ai_integration_empty_tests(client):
    payload = {"user_id": "abc123", "tests": []}

    response = client.post("/blood-test/ai", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "At least one test is required"


def test_ai_integration_llm_unavailable(app, client):
    # Override LLM to throw an error
    app.dependency_overrides[get_llm_client] = lambda: FakeLLMClient(should_fail=True)

    payload = {
        "user_id": "abc123",
        "tests": [
            {
                "analyte": "LDL",
                "value": 190,
                "normal_low": 0,
                "normal_high": 130,
            }
        ],
    }

    response = client.post("/blood-test/ai", json=payload)

    assert response.status_code == 503
    assert "LLM temporarily unavailable" in response.json()["detail"]
