## IPO Scorecard

Single endpoint: `POST /analyze` accepts a SEBI DRHP/RHP PDF and returns the summary (extraction → metrics → decision).

### Backend Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py 
```

#### Env vars (.env)
The extractor uses the Gemini API via the OpenAI-compatible endpoint.

Required:
- `GEMINI_API_KEY` — your Gemini API key

Example `.env`:
```env
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

### API Endpoints
- POST `/analyze` with form-data: `file` (PDF) and optional `slug`

---

### Frontend Setup (Next.js + Tailwind)
Assumes `frontend/` exists (created via `create-next-app`).

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and upload a DRHP/RHP PDF.

- The app posts to `http://localhost:8000/analyze` by default (see `src/lib/config.ts`).