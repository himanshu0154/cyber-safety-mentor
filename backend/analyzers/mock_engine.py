"""
MOCK ML/rule analysis engine.

This stands in for your teammate's real analysis module. Once they're done,
replace the import in main.py:

    from analyzers.mock_engine import analyze_text, analyze_url
    # becomes:
    from analyzers.real_engine import analyze_text, analyze_url

...as long as the real module exposes functions with these exact
signatures and returns a dict matching MLAnalysisResult, nothing else
in the backend needs to change.
"""

import random
from analyzers.classifier import extract_urls

SUSPICIOUS_KEYWORDS = [
    "urgent", "verify your account", "act now", "suspended", "click here",
    "limited time", "confirm your password", "winner", "claim your prize",
    "bank account", "unusual activity", "otp", "one time password",
]

SUSPICIOUS_URL_HINTS = ["bit.ly", "tinyurl", "-verify", "secure-login", "account-update"]


def _score_indicators(content: str):
    text = content.lower()
    indicators = []

    for kw in SUSPICIOUS_KEYWORDS:
        if kw in text:
            indicators.append(f"Suspicious phrase: '{kw}'")

    urls = extract_urls(content)
    for url in urls:
        if any(hint in url.lower() for hint in SUSPICIOUS_URL_HINTS):
            indicators.append(f"Suspicious URL pattern: {url}")
        else:
            indicators.append(f"Embedded link detected: {url}")

    if text.count("!") >= 2:
        indicators.append("Excessive urgency punctuation")

    return indicators


def _derive_risk(indicators):
    count = len(indicators)
    if count == 0:
        score = random.randint(5, 20)
    elif count <= 2:
        score = random.randint(30, 55)
    elif count <= 4:
        score = random.randint(56, 80)
    else:
        score = random.randint(81, 98)

    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


def analyze_text(content: str) -> dict:
    """Mock analysis for SMS or EMAIL content."""
    indicators = _score_indicators(content)
    score, level = _derive_risk(indicators)

    threat_type = "Phishing" if indicators else "None detected"
    recommendation = (
        "Do not click any links or reply. Report and delete this message."
        if level in ("HIGH", "CRITICAL")
        else "Message appears low-risk, but stay cautious with unknown senders."
    )

    return {
        "risk_score": score,
        "risk_level": level,
        "phishing_probability": round(score / 100, 2),
        "threat_type": threat_type,
        "detected_indicators": indicators or ["No strong indicators detected"],
        "recommendation": recommendation,
    }


def analyze_url(url: str) -> dict:
    """Mock analysis for a standalone URL."""
    indicators = []
    lower = url.lower()

    if any(hint in lower for hint in SUSPICIOUS_URL_HINTS):
        indicators.append("URL shortener or suspicious keyword in domain")
    if lower.count("-") >= 3:
        indicators.append("Excessive hyphens in domain (common spoofing pattern)")
    if not lower.startswith("https://"):
        indicators.append("Not using HTTPS")
    if any(c.isdigit() for c in lower.split("/")[2]) if "//" in lower else False:
        indicators.append("Numeric characters in domain name")

    score, level = _derive_risk(indicators)
    threat_type = "Malicious/Phishing URL" if indicators else "None detected"
    recommendation = (
        "Avoid visiting this URL. It shows signs of a phishing/spoofed domain."
        if level in ("HIGH", "CRITICAL")
        else "URL appears relatively safe, but always verify the sender."
    )

    return {
        "risk_score": score,
        "risk_level": level,
        "phishing_probability": round(score / 100, 2),
        "threat_type": threat_type,
        "detected_indicators": indicators or ["No strong indicators detected"],
        "recommendation": recommendation,
    }
