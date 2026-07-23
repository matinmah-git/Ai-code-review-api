import json_repair
import json
import re
from openai import OpenAI, RateLimitError, APITimeoutError, APIError
from app.core.config import settings
from app.core.prompts import build_review_prompt, SYSTEM_PROMPT


class AIService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.AI_API_KEY, base_url=settings.AI_BASE_URL)
        self.model = settings.AI_MODEL

    def _parse_response(self, response):
        """Parse LLM response using json-repair library."""
        try:
            content = response.choices[0].message.content

            if content is None:
                raise ValueError("LLM returned an empty response.")

            content = content.strip()

            # Remove markdown code blocks
            if content.startswith("```json"):
                content = content.removeprefix("```json").strip()
            if content.startswith("```"):
                content = content.removeprefix("```").strip()
            if content.endswith("```"):
                content = content.removesuffix("```").strip()

            # Try to extract JSON between curly braces
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()

            # Use json-repair to fix common issues
            repaired = json_repair.repair_json(content)
            result = json.loads(repaired)

            if not isinstance(result, dict):
                raise ValueError("LLM response is not a JSON object.")

            return result

        except Exception as exc:
            print(f"❌ JSON parsing error: {exc}")

            # Fallback to minimal valid response
            return {
                "overall_score": 5,
                "summary": "The AI response could not be parsed. Please try again.",
                "strengths": [],
                "bugs": [],
                "security": [],
                "performance": [],
                "maintainability": [],
                "best_practices": [],
                "priority_fixes": [],
                "files": []
            }

    def _build_messages(self, project_name: str, code: str, repository_url: str | None = None):
        user_prompt = build_review_prompt(
            project_name=project_name,
            code=code,
            repository_url=repository_url
        )

        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

    def _call_llm(self, messages: list[dict]):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=3000,
                response_format={"type": "json_object"},
            )
            return response
        except RateLimitError:
            raise RuntimeError("Rate limit exceeded.")
        except APITimeoutError:
            raise RuntimeError("LLM request timed out.")
        except APIError as exc:
            raise RuntimeError(f"LLM API error: {exc}")
        except Exception as exc:
            raise RuntimeError(f"Unexpected AI service error: {exc}")

    def review_code(self, project_name: str, code: str, repository_url: str | None = None):
        messages = self._build_messages(
            project_name=project_name,
            code=code,
            repository_url=repository_url
        )
        response = self._call_llm(messages)
        return self._parse_response(response)