"""
Turns structured ML output into a plain-English explanation for beginners.

Default mode: template-based (no API key needed, works offline, judge-safe).
Optional mode: real LLM call via Anthropic API if ANTHROPIC_API_KEY is set.

To wire up the real Claude call, uncomment the `_llm_call` block and set
the ANTHROPIC_API_KEY environment variable. Keeping this isolated means
your teammates' pipeline still works even if the API key/network isn't
available during judging/demo.
"""

import os

USE_REAL_LLM = bool(os.getenv("ANTHROPIC_API_KEY"))


def _template_explanation(input_type: str, result: dict) -> str:
    level = result["risk_level"]
    threat = result["threat_type"]
    indicators = result["detected_indicators"]

    if level in ("HIGH", "CRITICAL"):
        opening = (
            f"This {input_type.lower()} is high risk and may be a "
            f"{threat.lower()}."
        )
    elif level == "MEDIUM":
        opening = (
            f"This {input_type.lower()} has some suspicious "
            f"characteristics and should be checked carefully."
        )
    else:
        opening = (
            f"This {input_type.lower()} does not show major warning "
            f"signs based on our current checks."
        )

    indicator_text = ", ".join(indicators)

    return (
        f"{opening} "
        f"We detected: {indicator_text}. "
        f"Risk score: {result['risk_score']}/100. "
        f"{result['recommendation']}"
    )

def _llm_call(input_type: str, content: str, result: dict) -> str:
    """
    Real LLM call — requires `requests` and ANTHROPIC_API_KEY.
    Left here for when you're ready to plug in the real explanation step.
    """
    import requests

    prompt = (
        f"You are a cybersecurity assistant explaining risk to a beginner.\n"
        f"Input type: {input_type}\n"
        f"Original content: {content}\n"
        f"Analysis result: {result}\n\n"
        f"In 2-3 simple sentences, explain WHY this was flagged and what the "
        f"user should do. Avoid jargon."
    )

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=10,
    )
    data = response.json()
    return data["content"][0]["text"]


def generate_explanation(input_type: str, content: str, result: dict) -> str:
    if USE_REAL_LLM:
        try:
            return _llm_call(input_type, content, result)
        except Exception:
            # Fail safe: never let a demo crash because the LLM call failed.
            return _template_explanation(input_type, result)
    return _template_explanation(input_type, result)
