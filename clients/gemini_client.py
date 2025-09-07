from typing import Any, Optional
import os
import json
from openai import OpenAI
from loguru import logger

class GeminiClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",
        base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/",
        temperature: float = 0.0,
        default_system_prompt: Optional[str] = None,
    ) -> None:
        # Constants declared in constructor per project conventions
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.default_system_prompt = default_system_prompt or (
            """
You are an expert data extraction engine for Indian IPO DRHP/RHP documents.
Your task is to produce a SINGLE valid JSON object that STRICTLY conforms to the provided JSON schema.

Hard requirements:
- Output ONLY the JSON object. No prose, no markdown, no code fencing.x
- Keys MUST match the schema exactly. Do NOT add or rename keys.
- Values MUST be valid per schema types. Use null when data is missing or uncertain.
- Monetary amounts MUST be normalized to INR crore as floats with 2 decimals.
- Prefer consolidated figures over standalone when both exist.
- Prefer figures from sections named "Summary of Financial Information", "Financial Information", or equivalent summary tables.
- If multiple conflicting values exist, choose the one from the most authoritative summary table. If still ambiguous, return null.
- Do NOT invent or infer values you cannot locate. Use null.

Normalization rules:
- Currency parsing: Convert lakhs/millions/billions to crore.
  Examples:
    - 1,234 million = 123.4 crore
    - 12,34,56,789 (Indian digits) → parse then convert to crore
    - Values with parentheses indicate negative numbers (losses): (123.4) → -123.4
- Price band: array of numbers [low, high] in INR, in crore normalized scale is NOT required here. Keep as absolute INR numbers; if amounts are in rupees, use numeric rupee values (e.g., 95, 100). If unclear, null or single value array when only one bound.
- Lot size: integer (number of shares per lot).
- Dates: open_date/close_date in ISO format YYYY-MM-DD when exact day is available; if only month/year is present, set null.
- Financial rows: include up to the last 5 fiscal years if available, ascending by FY (oldest first). Each row fields are numbers or null.

Schema-conformance:
- The top-level must include {"extracted": {"meta": {...}, "terms": {...}, "financials": [...]}}
- No additional properties beyond the schema in nested objects/rows.

Return ONLY the JSON object.
            """
        )

    def extract_structured(self, text: str, schema: dict[str, Any], system_prompt: Optional[str] = None) -> dict[str, Any]:
        prompt = system_prompt or self.default_system_prompt
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"JSON_SCHEMA:\n{json.dumps(schema)}\n\nDOCUMENT_TEXT:\n{text}"},
        ]
        # calculate approx tokens
        tokens = len(text.split())
        print(f"Approx tokens: {tokens}")
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=self.temperature,
        )
        content = resp.choices[0].message.content or "{}"
        try:
            content = json.loads(content)
            logger.info(f"LLM RESPONSE: {json.dumps(content, indent=2)}")
            return json.loads(content)
        except Exception:
            return {"extracted": {"meta": {}, "terms": {}, "financials": []}}