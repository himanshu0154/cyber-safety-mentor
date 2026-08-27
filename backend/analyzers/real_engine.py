import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "ml"))

from analyzer import analyze_message as _analyze_message
from analyzer import analyze_url as _analyze_url


def analyze_text(content: str) -> dict:
    result = _analyze_message(content)

    return {
        "risk_score": int(round(result["risk_score"])),
        "risk_level": result["risk_level"],
        "phishing_probability": round(result["risk_score"] / 100, 2),
        "threat_type": result["threat_type"],
        "detected_indicators": (
            result["indicators"]
            if result["indicators"]
            else ["No strong indicators detected"]
        ),
        "recommendation": (
            "Do not click links or provide sensitive information. "
            "Verify the message through an official source."
            if result["risk_level"] in ("HIGH", "CRITICAL")
            else
            "The message appears relatively safe, but remain cautious "
            "with unknown senders."
        ),
    }


def analyze_url(url: str) -> dict:
    result = _analyze_url(url)

    return {
        "risk_score": int(round(result["risk_score"])),
        "risk_level": result["risk_level"],
        "phishing_probability": round(result["risk_score"] / 100, 2),
        "threat_type": result["threat_type"],
        "detected_indicators": (
            result["indicators"]
            if result["indicators"]
            else ["No strong indicators detected"]
        ),
        "recommendation": (
    "Avoid visiting this URL. It shows signs of a potentially "
    "suspicious or phishing URL."
    if result["risk_level"] in ("HIGH", "CRITICAL")
    else
    "This URL has some suspicious characteristics. Verify the "
    "domain independently before entering sensitive information."
    if result["risk_level"] == "MEDIUM"
    else
    "No major warning signs were detected, but always verify "
    "the website before entering sensitive information."
),
    }