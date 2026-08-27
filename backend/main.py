"""
AI Cyber Safety Mentor - Backend API
The Cyber Awakening Hackathon

Run locally:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Docs auto-generated at:
    http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import (
    MessageRequest,
    URLRequest,
    UnifiedRequest,
    AnalysisResponse,
    InputType,
)
from analyzers.classifier import detect_input_type

# --- swap this single import line once the real ML module is ready ---
# from analyzers.mock_engine import analyze_text, analyze_url
from analyzers.real_engine import analyze_text, analyze_url
# -----------------------------------------------------------------------

from analyzers.llm_explainer import generate_explanation


app = FastAPI(
    title="AI Cyber Safety Mentor API",
    description="Backend for detecting phishing/scam risk in SMS, email, and URLs.",
    version="1.0.0",
)

# Wide-open CORS for hackathon speed — tighten if you have time later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_response(input_type: str, content: str, ml_result: dict) -> AnalysisResponse:
    explanation = generate_explanation(input_type, content, ml_result)
    return AnalysisResponse(
        input_type=input_type,
        risk_level=ml_result["risk_level"],
        risk_score=ml_result["risk_score"],
        phishing_probability=ml_result["phishing_probability"],
        threat_type=ml_result["threat_type"],
        indicators=ml_result["detected_indicators"],
        explanation=explanation,
        recommendation=ml_result["recommendation"],
    )


@app.get("/")
def root():
    return {"status": "ok", "service": "AI Cyber Safety Mentor API"}


@app.post("/analyze/message", response_model=AnalysisResponse)
def analyze_message(req: MessageRequest):
    """Analyze SMS or email content."""
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="content cannot be empty")

    input_type = req.input_type.value if req.input_type else detect_input_type(req.content)
    if input_type == "URL":
        # Whole message was just a URL — route it correctly anyway
        result = analyze_url(req.content.strip())
        input_type = "URL"
    else:
        result = analyze_text(req.content)

    return _build_response(input_type, req.content, result)


@app.post("/analyze/url", response_model=AnalysisResponse)
def analyze_url_endpoint(req: URLRequest):
    """Analyze a standalone URL."""
    if not req.url.strip():
        raise HTTPException(status_code=400, detail="url cannot be empty")

    result = analyze_url(req.url.strip())
    return _build_response(InputType.URL.value, req.url, result)


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_unified(req: UnifiedRequest):
    """
    Single entry point: auto-detects whether content is a URL, SMS, or EMAIL
    and routes to the right analyzer. Handy if the frontend doesn't want to
    decide which endpoint to call.
    """
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="content cannot be empty")

    input_type = detect_input_type(req.content)

    if input_type == "URL":
        result = analyze_url(req.content.strip())
    else:
        result = analyze_text(req.content)

    return _build_response(input_type, req.content, result)
