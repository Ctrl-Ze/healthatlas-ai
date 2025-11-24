import os
from unittest.mock import patch

from fastapi import FastAPI, Request

from chiron.agents.llm_client import LLMClient
from chiron.agents.prompts.chiron_prompt_builder import build_chiron_summary_prompt
from chiron.core.dependencies import get_analysis_service, get_llm_client
from chiron.services.analysis_service import AnalysisService

# -------------------------------------------------------------------
# PROMPT BUILDER TESTS (BEST PRACTICE SNAPSHOT-LIKE BEHAVIOR TESTING)
# -------------------------------------------------------------------


def test_prompt_contains_required_fields_and_rules():
    prompt = build_chiron_summary_prompt()

    # Required JSON keys
    assert '"ai_summary"' in prompt
    assert '"lifestyle_suggestions"' in prompt

    # Safety rules
    assert "Do NOT provide diagnoses" in prompt
    assert "VALID JSON" in prompt
    assert "Maximum 2 lifestyle suggestions" in prompt

    # Input description
    assert "{warnings: [...], tests: [...], profile: {...}}" in prompt


def test_prompt_has_no_unexpected_whitespace():
    prompt = build_chiron_summary_prompt()
    # Ensure no accidental whitespace regression
    assert prompt == prompt.strip()
    assert "\t" not in prompt  # no tabs allowed


def test_prompt_is_deterministic():
    p1 = build_chiron_summary_prompt()
    p2 = build_chiron_summary_prompt()
    assert p1 == p2


# -------------------------------------------------------------------
# DEPENDENCY PROVIDER TESTS
# -------------------------------------------------------------------


def test_get_analysis_service_returns_new_instance():
    s1 = get_analysis_service()
    s2 = get_analysis_service()

    assert isinstance(s1, AnalysisService)
    assert isinstance(s2, AnalysisService)
    assert s1 is not s2  # Should not share state


@patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=True)
def test_get_llm_client_returns_disabled_when_no_state():
    app = FastAPI()
    req = Request({"type": "http", "app": app})

    llm = get_llm_client(req)
    assert isinstance(llm, LLMClient)
    assert llm.client is None  # Disabled mode


def test_get_llm_client_returns_app_state_instance():
    app = FastAPI()
    fake_llm = LLMClient(api_key="TESTKEY")
    app.state.llm = fake_llm

    req = Request({"type": "http", "app": app})

    result = get_llm_client(req)
    assert result is fake_llm
