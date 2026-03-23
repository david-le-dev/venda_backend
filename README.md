# VedaTwin AI

VedaTwin AI is a bilingual, portfolio-grade AI application for reflective Vedic astrology experiences. It combines a FastAPI backend, Streamlit frontend, Gemini-powered agents, optional ChromaDB retrieval, and streaming output for a live "agent crew" feel.

## Core principles

- Entertainment and reflection, not scientific prediction.
- Vietnamese and English output.
- Positive, empowering, non-fatalistic responses.
- Mandatory disclaimers in every final report.
- Optional face and palm image analysis with strict safety boundaries.

## Repository layout

- `backend/`: FastAPI API, agents, services, prompts, models, safety logic.
- `frontend_streamlit/`: demo-ready Streamlit UI with live status and streamed report rendering.
- `docs/`: architecture notes and future build guidance.

## Quick start

1. Run `.\setup_local.ps1` from the repo root.
2. Edit `.env` and add `GOOGLE_API_KEY` if you want real Gemini output. Without it, the app still runs using safe fallback responses.
3. Start the backend with `.\run_backend.ps1`.
4. Start the frontend with `.\run_frontend.ps1`.
5. Open the Streamlit URL shown in the terminal.

## Manual run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
pip install -r frontend_streamlit\requirements.txt
Copy-Item .env.example .env
```

Backend:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```powershell
cd frontend_streamlit
..\.venv\Scripts\python.exe -m streamlit run app.py
```
