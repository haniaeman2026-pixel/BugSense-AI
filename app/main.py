import os
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

from app.graph import build_graph

graph = build_graph()
STATIC_DIR = Path(__file__).resolve().parent / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="BugSense AI",
    description="AI-powered bug report analysis using Groq and LangGraph.",
    version="1.0.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class BugRequest(BaseModel):
    description: str = Field(min_length=10, max_length=8000)

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "application": "BugSense AI"}

@app.post("/api/analyze")
def analyze_bug(request: BugRequest):
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="Groq API key is missing. Add GROQ_API_KEY to your .env file and restart the app."
        )
    try:
        result = graph.invoke({"bug_description": request.description.strip()})
        report = result.get("formatted_report")
        if not report:
            raise ValueError("The workflow did not produce a report.")
        return {"success": True, "report": report}
    except Exception as exc:
        # Do not expose stack traces or secret environment values to the browser.
        message = str(exc)
        if "API key" in message or "API_KEY" in message or "authentication" in message.lower():
            message = "Groq authentication failed. Check GROQ_API_KEY in your .env file."
        elif "quota" in message.lower() or "rate" in message.lower():
            message = "Groq request limit reached. Please wait and try again."
        else:
            message = "Analysis failed. Check your API key, internet connection, and terminal logs, then try again."
        raise HTTPException(status_code=502, detail=message)
