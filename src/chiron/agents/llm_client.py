import asyncio
import logging
from typing import Dict, List, Optional
import json
import os
from openai import APIConnectionError, APIError, AsyncOpenAI, RateLimitError
from pydantic import BaseModel, ValidationError

from chiron.agents.prompts.chiron_prompt_builder import build_chiron_summary_prompt
from chiron.core.errors import AIUnavailableError

logger = logging.getLogger(__name__)

class LifestyleOutput(BaseModel):
    ai_summary: str
    lifestyle_suggestions: List[str]

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("LLMClient initialized WITHOUT API KEY — AI features disabled.")
            self.client = None
            self.model = None
            return

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = AsyncOpenAI(api_key=self.api_key)
        logger.info(f"LLMClient initialized with model={self.model}")

    async def summarize_with_lifestyle(
            self,
            warnings: List[str],
            tests: List[Dict],
            profile: Optional[Dict] = None,
            max_tokens: int = 200,
            retries: int = 3,
            backoff_factor: float = 1.5,
        ) -> Dict:
                                    
        """
        Returns a dict: {"ai_summary": str, "lifestyle_suggestions": [str]}
        Falls back gracefully if JSON parsing fails.
        """
        if not self.client:
            raise AIUnavailableError("LLMClient is disabled (no API key).")
        
        user_payload = {
        "warnings": warnings,
        "tests": tests,
        "profile": profile or {},
        }

        system_prompt = build_chiron_summary_prompt()

        attempt = 0
        while attempt <= retries:
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": json.dumps(user_payload)},
                    ],
                    functions=[
                        {
                            "name": "chiron_blood_report",
                            "description": "Structured output for AI blood report",
                            "parameters": LifestyleOutput.model_json_schema()
                        }
                    ],
                    function_call={"name": "chiron_blood_report"},
                    max_tokens=max_tokens,
                    timeout=30,
                )

            except (APIConnectionError, APIError, RateLimitError) as e:
                logger.warning(f"LLM API call failed on attempt {attempt+1}/{retries}: {e}")
                attempt += 1
                if attempt > retries:
                    logger.error(f"LLM service unavailable after {retries} retries.")
                    raise AIUnavailableError(f"LLM service unavailable: {e}")
                sleep_time = backoff_factor ** attempt
                await asyncio.sleep(sleep_time)

            try:
                json_output = response.choices[0].message.function_call.arguments
                parsed = LifestyleOutput.model_validate_json(json_output)
                return parsed.model_dump()
            
            except ValidationError as ve:
                logger.exception(f"Failed to parse LLM JSON response: {ve}")
                raise AIUnavailableError(f"Unexpected AI output error: {ve}")


            except Exception as e:
                logger.exception(f"Failed to parse JSON-mode LLM response: {e}")
                raise AIUnavailableError(f"Unexpected AI output error: {e}")