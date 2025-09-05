from typing import Any, Optional
import os
from openai import OpenAI


class GeminiClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",
        base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/",
        temperature: float = 0.0,
    ) -> None:
        # Constants declared in constructor per project conventions
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def extract_structured(self, text: str, schema: dict[str, Any], system_prompt: Optional[str] = None) -> dict[str, Any]:
        prompt = (
            system_prompt
            or (
                "Parse Indian DRHP/RHP. JSON only per schema. Normalize to ₹ crore (2 decimals). "
                "If missing, leave null. If conflicting, include both with source_page. Use keys exactly as schema."
            )
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Schema:\n{schema}\n\nText:\n{text}"},
        ]
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=self.temperature,
        )
        content = resp.choices[0].message.content or "{}"
        try:
            import json

            return json.loads(content)
        except Exception:
            # If the model returns invalid JSON, return a minimal structure
            return {"extracted": {"meta": {}, "terms": {}, "financials": []}}