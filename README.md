## IPO Scorecard Backend (minimal v1)

Single endpoint: `POST /analyze` accepts a SEBI DRHP/RHP PDF and returns the full summary (extraction → ratios → decision). Also connects to MCP memory (libsql) and lists available tools.

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py --serve
```

### Endpoints
- GET `/health`
- POST `/analyze` with form-data: `file` (PDF) and optional `slug`

### Env vars
- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (default `gpt-4o-mini`)
- `LIBSQL_URL` (default `file:./memory/ed.db`) 