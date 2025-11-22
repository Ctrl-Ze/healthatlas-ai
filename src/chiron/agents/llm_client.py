import logging
from typing import Dict, List, Optional
import json
import os
from openai import APIConnectionError, APIError, AsyncOpenAI, OpenAI, RateLimitError

logging.basicConfig(level=logging.INFO)

class AIUnavailableError(Exception):
    """Raised when LLM cannot produce a response."""
    pass

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.api_key = None
            self.client = None
            self.model = None
            return
            
        self.api_key = api_key
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def summarize_with_lifestyle(self,
                                       warnings: List[str],
                                       tests: List[Dict],
                                       profile: Optional[Dict] = None,
                                       max_tokens: int = 200) -> Dict:
        """
        Returns a dict: {"ai_summary": str, "lifestyle_suggestions": [str]}
        Falls back gracefully if JSON parsing fails.
        """

        # Build compact tests text
        tests_lines =[]
        for t in tests:
            name = t.get("analyte") or "unknown"
            val = t.get("value")
            unit = t.get("unit") or ""
            nl = t.get("normal_low")
            nh = t.get("normal_high")
            tests_lines.append(f"{name}: {val} {unit} (normal {nl}-{nh})")

        tests_text = "\n".join(tests_lines)
        warnings_text = "\n".join(f"- {w}" for w in warnings) if warnings else "- none"
        profile_text = json.dumps(profile) if profile else "none"

        prompt_template = (
            "You are Chiron, a cautious health guidance assistant. "
            "Input: structured facts about blood tests (warnings and list of analytes). "
            "Produce a JSON object with two keys:\n"
            '{ "ai_summary": "<one-sentence, non-diagnostic summary, <= 30 words>", '
            '"lifestyle_suggestions": ["<short suggestion 1 <=12 words>", "<short suggestion 2 <=12 words>"] }\n'
            "Rules:\n"
            "- Do NOT provide diagnoses, medical instructions, or medication advice.\n"
            "- Do NOT use absolute phrases like 'you have' or 'you must'. Use 'may', 'consider', 'could'.\n"
            "- Provide at most 2 suggestions. Keep suggestions action-focused and generic (e.g., 'reduce refined carbs', 'add 20–30 min brisk walking daily').\n"
            "- If there are no important abnormalities, return an ai_summary that says results are largely within expected ranges and an empty suggestions list.\n"
            "Return ONLY the JSON (no additional text).\n\n"
            "INPUT:\n"
            "Warnings:\n"
            f"{warnings_text}\n\n"
            "Tests:\n"
            f"{tests_text}\n\n"
            "Profile:\n"
            f"{profile_text}\n"
        )

        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt_template}],
                max_tokens=max_tokens,
                temperature=0.2,
            )
        except (APIConnectionError, APIError, RateLimitError) as e:
            raise AIUnavailableError(f"LLM service unavailable: {e}")
        
        content_str = ""
        # Extract text
        try:
            if not resp.choices or not resp.choices[0].message:
                raise ValueError("LLM response structure invalid or empty.")
            # Attempt to parse JSON (strip whitespace)
            content_str = resp.choices[0].message.content.strip()
            logging.error(f"response: {content_str}")
            # Some models might add triple backticks or code fences; try to extract JSON substring
            # Quick heuristic: find first '{' and last '}' and load between
            first = content_str.find('{')
            logging.error(f"first: {first}")
            last = content_str.rfind('}')
            logging.error(f"last: {last}")
            if first != -1 and last != -1 and last > first:
                json_text = content_str[first:last+1]
            else:
                json_text = content_str
            logging.error(f"json_text: {json_text}")
            
            parsed = json.loads(json_text)
            logging.error(f"parsed: {parsed}")
            # Ensure keys exist and types are correct
            ai_summary = parsed.get("ai_summary", "").strip() if isinstance(parsed.get("ai_summary", ""), str) else ""
            logging.error(f"ai_summary: {ai_summary}")
            lifestyle = parsed.get("lifestyle_suggestions", [])
            logging.error(f"lifestyle: {lifestyle}")
            if not isinstance(lifestyle, list):
                lifestyle = []
            lifestyle = [str(s).strip() for s in lifestyle[:2]]
            logging.error(f"ai_summary: {ai_summary}")
            logging.error(f"lifestyle_suggestions: {lifestyle}")
            return {"ai_summary": ai_summary, "lifestyle_suggestions": lifestyle}
            
        except Exception as e:
            error_context = content_str if content_str else "Response content unavailable"
            logging.error(f"Failed to parse LLM JSON response. Raw content: '{error_context}'. Error: {e}")
            raise AIUnavailableError(f"Unexpected AI error: {str(e)}")