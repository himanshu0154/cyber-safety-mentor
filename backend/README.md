# AI Cyber Safety Mentor — Backend

FastAPI backend for The Cyber Awakening hackathon project.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Interactive API docs (Swagger UI): http://localhost:8000/docs
Frontend can hit: http://localhost:8000

## Endpoints

### `POST /analyze/message`
For SMS or email text.

```json
{ "content": "URGENT! Your account is suspended, click here to verify: http://bit.ly/xyz" }
```

Optional: pass `"input_type": "SMS"` or `"EMAIL"` to skip auto-detection.

### `POST /analyze/url`
For a standalone URL.

```json
{ "url": "http://account-update-secure-login.xyz" }
```

### `POST /analyze`
Unified endpoint — auto-detects SMS / EMAIL / URL from a single `content` field.
Use this if the frontend doesn't want to decide which endpoint to call.

```json
{ "content": "https://bit.ly/suspicious-link" }
```

## Response shape (all endpoints)

```json
{
  "input_type": "SMS",
  "risk_level": "HIGH",
  "risk_score": 83,
  "phishing_probability": 0.83,
  "threat_type": "Phishing",
  "indicators": ["Urgency language", "Suspicious URL"],
  "explanation": "This sms shows strong signs of being a phishing attempt...",
  "recommendation": "Do not click any links or reply. Report and delete this message."
}
```

## Plugging in the real ML module

Currently `main.py` imports from `analyzers/mock_engine.py`:

```python
from analyzers.mock_engine import analyze_text, analyze_url
```

Once your ML teammate's module is ready, it just needs to expose:

```python
def analyze_text(content: str) -> dict: ...
def analyze_url(url: str) -> dict: ...
```

Each returning a dict with these keys:
`risk_score` (int 0-100), `risk_level` (LOW/MEDIUM/HIGH/CRITICAL),
`phishing_probability` (float 0-1), `threat_type` (str),
`detected_indicators` (list[str]), `recommendation` (str).

Then in `main.py`, swap the import line to point at their module
(e.g. `analyzers/real_engine.py`). No route or model changes needed.

## Plugging in a real LLM explanation

By default, `analyzers/llm_explainer.py` uses a template (no API key needed —
safe for offline demo/judging). To use a real Claude call instead, set the
`ANTHROPIC_API_KEY` environment variable before starting the server; it will
automatically switch to calling the Anthropic API, and falls back to the
template if the call fails for any reason (so a flaky network never breaks
your demo).

## Folder structure

```
backend/
├── main.py                    # FastAPI app + routes
├── models.py                  # Pydantic request/response schemas
├── analyzers/
│   ├── classifier.py          # detects SMS vs EMAIL vs URL
│   ├── mock_engine.py         # placeholder ML analysis (swap for real one)
│   └── llm_explainer.py       # turns structured result into plain-English explanation
├── requirements.txt
└── README.md
```
