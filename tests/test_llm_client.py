from unittest.mock import AsyncMock, MagicMock

import pytest
from openai import APIConnectionError

from chiron.agents.llm_client import LLMClient
from chiron.core.errors import AIUnavailableError


# ---------------------------
# Test initialization
# ---------------------------
def test_llmclient_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = LLMClient()
    assert client.client is None
    assert client.model is None


@pytest.mark.asyncio
async def test_summarize_with_lifestyle_no_client(monkeypatch):
    client = LLMClient()
    client.client = None
    with pytest.raises(AIUnavailableError):
        await client.summarize_with_lifestyle([], [])


# ---------------------------
# Test successful response
# ---------------------------
@pytest.mark.asyncio
async def test_summarize_with_lifestyle_success(monkeypatch):
    fake_response = AsyncMock()
    fake_response.choices = [
        MagicMock(
            message=MagicMock(
                function_call=MagicMock(
                    arguments='{"ai_summary":"summary","lifestyle_suggestions":["exercise"]}'
                )
            )
        )
    ]

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=fake_response)

    client = LLMClient(api_key="fake-key")
    client.client = mock_client

    result = await client.summarize_with_lifestyle([], [])
    assert result["ai_summary"] == "summary"
    assert result["lifestyle_suggestions"] == ["exercise"]


# ---------------------------
# Test API failure and retries
# ---------------------------
# class FakeAPIConnectionError(Exception):
#     """Fake exception to simulate OpenAI APIConnectionError in tests."""

#     pass


@pytest.mark.asyncio
async def test_summarize_with_lifestyle_api_failure(monkeypatch):
    fake_request = MagicMock()
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=APIConnectionError(request=fake_request)
    )

    client = LLMClient(api_key="fake-key")
    client.client = mock_client

    with pytest.raises(AIUnavailableError):
        await client.summarize_with_lifestyle([], [], retries=2, backoff_factor=0)


# ---------------------------
# Test invalid JSON parsing
# ---------------------------
@pytest.mark.asyncio
async def test_summarize_with_lifestyle_invalid_json(monkeypatch):
    # LLM returns something invalid that can't be parsed by Pydantic
    fake_response = AsyncMock()
    fake_response.choices = [
        MagicMock(
            message=MagicMock(
                function_call=MagicMock(arguments={"not": "a json string"})
            )
        )
    ]

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=fake_response)

    client = LLMClient(api_key="fake-key")
    client.client = mock_client

    with pytest.raises(AIUnavailableError):
        await client.summarize_with_lifestyle([], [])
