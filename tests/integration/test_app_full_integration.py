import pytest
from fastapi.testclient import TestClient

from chiron.app import create_app
from chiron.core.dependencies import get_llm_client
from chiron.core.errors import AIUnavailableError


class FakeLLM:
    async def summarize_with_lifestyle(self, *args, **kwargs):
        raise AIUnavailableError("LLM disabled for test")


@pytest.fixture
def client():
    app = create_app()  # <-- real, full application
    # Prevent real LLM calls
    app.dependency_overrides[get_llm_client] = lambda: FakeLLM()
    return TestClient(app)


def test_full_app_routes_exist(client):
    # deterministic endpoint under full prefix
    resp = client.post(
        "/api/v1/analyze/blood-test/deterministic",
        json={
            "user_id": "u1",
            "tests": [
                {"analyte": "LDL", "value": 150, "normal_low": 0, "normal_high": 120}
            ],
        },
    )
    assert resp.status_code == 200


def test_ai_route_prefix_exists(client):
    # With no API key => LLM is disabled => should still work
    resp = client.post(
        "/api/v1/analyze/blood-test/ai",
        json={
            "user_id": "u1",
            "tests": [
                {"analyte": "Glucose", "value": 90, "normal_low": 70, "normal_high": 99}
            ],
        },
    )
    # Should return 503 because LLM disabled
    assert resp.status_code == (503)
