import hashlib
import json
import pathlib
from typing import Any, Optional

from loguru import logger

from clients.gemini_client import GeminiClient
from schemas.extract_schema import EXTRACT_SCHEMA
from utils.pdf import read_pdf_text
from utils.metrics import compute_metrics
from utils.decision_engine import DecisionEngine
from tools.mcp_memory import MCPLibsqlTools


class AnalyzeOrchestrator:
    def __init__(self, libsql_url: str) -> None:
        self.libsql_url = libsql_url
        self.mcp_tools = MCPLibsqlTools(libsql_url)
        self.gemini = GeminiClient()
        self.decision_engine = DecisionEngine()

    def ensure_dirs(self) -> None:
        pathlib.Path("uploads").mkdir(parents=True, exist_ok=True)
        pathlib.Path("memory").mkdir(parents=True, exist_ok=True)
        pathlib.Path("memory/responses").mkdir(parents=True, exist_ok=True)

    async def run(
        self,
        file_bytes: bytes,
        original_filename: Optional[str],
        slug: Optional[str] = None,
    ) -> dict[str, Any]:
        self.ensure_dirs()
        # Validate input
        if not original_filename or not original_filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are accepted")

        file_id = hashlib.sha256(file_bytes).hexdigest()
        pdf_path = pathlib.Path("uploads") / f"{file_id}.pdf"
        if not pdf_path.exists():
            pdf_path.write_bytes(file_bytes)
            logger.info("Saved uploaded PDF {} ({} bytes)", pdf_path, len(file_bytes))

        computed_slug = slug or (pathlib.Path(original_filename).stem.replace(" ", "-").lower() if original_filename else file_id)

        # Cache: check for prior structured response
        cache_file = pathlib.Path("memory/responses") / f"{file_id}.json"
        structured: dict[str, Any]
        if cache_file.exists():
            try:
                structured = json.loads(cache_file.read_text())
                logger.info("Cache hit for {}", file_id)
            except Exception:
                logger.warning("Failed to read cache for {}, recomputing", file_id)
                text = read_pdf_text(pdf_path)
                structured = self.gemini.extract_structured(text, EXTRACT_SCHEMA)
                cache_file.write_text(json.dumps(structured))
        else:
            text = read_pdf_text(pdf_path)
            structured = self.gemini.extract_structured(text, EXTRACT_SCHEMA)
            try:
                cache_file.write_text(json.dumps(structured))
                logger.info("Cached structured output at {}", cache_file)
            except Exception as e:
                logger.warning("Failed to write cache {}: {}", cache_file, e)

        extracted = structured.get("extracted", {})
        meta = extracted.get("meta", {})
        terms = extracted.get("terms", {})
        financials = extracted.get("financials", [])

        metrics = compute_metrics(financials)
        decision = self.decision_engine.decide(metrics)

        mcp_info = await self.mcp_tools.list_tools()

        blocks = [
            {
                "component": "terms_and_financials",
                "company": meta.get("company"),
                "terms": terms,
                "financials": financials,
                "reasons": ["Parsed from PDF via schema-constrained extraction"],
            },
            {
                "component": "financial_quality",
                "metrics": metrics,
                "valuation": {},
                "reasons": ["Deterministic calculations on extracted financials"],
            },
            {
                "component": "verdict",
                "verdict": decision["label"],
                "confidence": decision["confidence"],
                "why": decision["reasons"],
                "plain_english": " ".join(decision["reasons"][:2]) if decision["reasons"] else "",
            },
        ]

        return {
            "slug": computed_slug,
            "components": blocks,
            "sources": [{"title": "Uploaded PDF", "url": str(pdf_path)}],
            "mcp_memory": mcp_info,
        } 