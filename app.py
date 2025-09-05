import argparse
import os
from typing import Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from services.orchestrator import AnalyzeOrchestrator

load_dotenv()

APP_HOST = "0.0.0.0"
APP_PORT = 8000
APP_RELOAD = True
LIBSQL_URL = "file:./memory/ed.db"

app = FastAPI(title="IPO Scorecard v1", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    app.state.orchestrator = AnalyzeOrchestrator(libsql_url=LIBSQL_URL)


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), slug: Optional[str] = Form(default=None)) -> dict[str, Any]:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    content = await file.read()
    try:
        result = await app.state.orchestrator.run(
            file_bytes=content,
            original_filename=file.filename,
            slug=slug,
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


if __name__ == "__main__":
    uvicorn.run("app:app", host=APP_HOST, port=APP_PORT, reload=APP_RELOAD)
