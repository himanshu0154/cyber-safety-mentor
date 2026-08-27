"""
Lightweight heuristic classifier: decides whether input is a URL, EMAIL, or SMS.
This is NOT the phishing detector — just routes the input to the right analyzer.
"""

import re

URL_PATTERN = re.compile(r"^(https?://|www\.)\S+$", re.IGNORECASE)
LOOSE_URL_PATTERN = re.compile(r"\b(?:https?://|www\.)[^\s]+", re.IGNORECASE)
EMAIL_HEADER_HINTS = re.compile(
    r"\b(from:|to:|subject:|dear\s+customer|dear\s+user|unsubscribe)\b", re.IGNORECASE
)


def detect_input_type(content: str) -> str:
    """
    Returns one of: "URL", "EMAIL", "SMS"
    """
    text = content.strip()

    # Whole input is just a URL
    if URL_PATTERN.match(text):
        return "URL"

    # Looks like an email: has header-like structure or is long + has "unsubscribe" etc.
    if EMAIL_HEADER_HINTS.search(text) or (len(text) > 300 and "@" in text):
        return "EMAIL"

    # Default: short text with/without an embedded link -> SMS
    return "SMS"


def extract_urls(content: str):
    """Pull out any URLs embedded in a larger SMS/email body."""
    return LOOSE_URL_PATTERN.findall(content)
