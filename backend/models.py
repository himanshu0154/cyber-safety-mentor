"""
Request/response schemas shared across the API.
Keep this file as the single source of truth for the JSON contract
between Backend <-> Frontend and Backend <-> ML module.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class InputType(str, Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    URL = "URL"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ---------- Incoming requests ----------

class MessageRequest(BaseModel):
    content: str = Field(..., description="Raw SMS or email text to analyze")
    input_type: Optional[InputType] = Field(
        None, description="Optional hint: SMS or EMAIL. Auto-detected if omitted."
    )


class URLRequest(BaseModel):
    url: str = Field(..., description="Raw URL to analyze")


class UnifiedRequest(BaseModel):
    content: str = Field(..., description="SMS text, email text, or a URL — type is auto-detected")


# ---------- ML module output contract ----------
# This is the exact shape the ML teammate's module should return.
# mock_engine.py returns this shape today; swap the import later.

class MLAnalysisResult(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    phishing_probability: float = Field(..., ge=0, le=1)
    threat_type: str
    detected_indicators: List[str]
    recommendation: str


# ---------- Final API response (Backend -> Frontend) ----------

class AnalysisResponse(BaseModel):
    input_type: InputType
    risk_level: RiskLevel
    risk_score: int
    phishing_probability: float
    threat_type: str
    indicators: List[str]
    explanation: str
    recommendation: str
