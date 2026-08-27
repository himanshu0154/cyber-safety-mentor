import re
import joblib
from urllib.parse import urlparse

# Load trained ML components
model = joblib.load("/Users/himanshu/Documents/my documents/hackathon/cyber-safety-mentor/ml/model.pkl")
tfidf = joblib.load("/Users/himanshu/Documents/my documents/hackathon/cyber-safety-mentor/ml/vectorizer.pkl")


def detect_indicators(text):
    text = text.lower()
    indicators = []

    urgency_words = [
        "urgent", "immediately", "act now",
        "within 24 hours", "verify now", "hurry"
    ]

    if any(word in text for word in urgency_words):
        indicators.append("Urgency language")

    sensitive_words = ["otp", "password", "pin", "cvv", "card number"]

    if any(word in text for word in sensitive_words):
        indicators.append("Sensitive information mentioned")

    request_patterns = [
        r"(send|share|provide|give).{0,20}(otp|password|pin|cvv|card)",
        r"(enter|type).{0,20}(otp|password|pin|cvv|card)"
    ]

    if any(re.search(pattern, text) for pattern in request_patterns):
        indicators.append("Request for sensitive information")

    if re.search(r'https?://|www\.', text):
        indicators.append("Contains a link")

    threat_words = [
        "account blocked",
        "account has been blocked",
        "account suspended",
        "account has been suspended",
        "account will be closed",
        "legal action"
    ]

    if any(word in text for word in threat_words):
        indicators.append("Account threat")

    scam_words = [
        "you won", "winner", "lottery",
        "prize", "claim your reward"
    ]

    if any(word in text for word in scam_words):
        indicators.append("Prize/reward scam language")

    return indicators


def detect_threat_type(text):
    text = text.lower()

    if (
        any(phrase in text for phrase in
            ["do not share", "don't share", "never share"])
        and "otp" in text
    ):
        return "Legitimate / Security Message"

    if any(word in text for word in
           ["you won", "winner", "lottery", "prize", "reward"]):
        return "Prize Scam"

    if any(word in text for word in
           ["send your otp", "share your otp",
            "send us your otp", "password", "pin", "cvv"]):
        return "Credential Theft"

    if any(word in text for word in
           ["account blocked", "account suspended",
            "account has been blocked", "legal action"]):
        return "Account Threat"

    if re.search(r'https?://|www\.', text):
        return "Phishing"

    return "Unknown"


def analyze_message(text):
    text_tfidf = tfidf.transform([text])
    phishing_probability = model.predict_proba(text_tfidf)[0][1]

    indicators = detect_indicators(text)
    threat_type = detect_threat_type(text)

    risk_score = phishing_probability * 100

    indicator_weights = {
        "Urgency language": 5,
        "Contains a link": 5,
        "Account threat": 10,
        "Sensitive information mentioned": 2,
        "Request for sensitive information": 15,
        "Prize/reward scam language": 10
    }

    for indicator in indicators:
        risk_score += indicator_weights.get(indicator, 0)

    protective_phrases = [
        "do not share",
        "don't share",
        "never share",
        "do not disclose"
    ]

    if any(phrase in text.lower() for phrase in protective_phrases):
        risk_score -= 10

    risk_score = max(0, min(risk_score, 100))

    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    if risk_level == "LOW" and threat_type == "Unknown":
        threat_type = "Legitimate / No Threat Detected"

    return {
        "risk_score": round(float(risk_score), 2),
        "risk_level": risk_level,
        "threat_type": threat_type,
        "indicators": indicators
    }


def analyze_url(url):
    indicators = []
    score = 0

    parsed = urlparse(url if "://" in url else "http://" + url)
    domain = parsed.netloc.lower()

    # HTTP
    if parsed.scheme == "http":
        indicators.append("Uses HTTP instead of HTTPS")
        score += 15

    # IP address
    is_ip = re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain)

    if is_ip:
        indicators.append("Uses an IP address instead of a domain")
        score += 25

    # @ symbol
    if "@" in url:
        indicators.append("Contains @ symbol")
        score += 25

    # Long URL
    if len(url) > 100:
        indicators.append("Unusually long URL")
        score += 25

    # Excessive subdomains
    if not is_ip and domain.count(".") >= 4:
        indicators.append("Excessive subdomains")
        score += 15

    # Generic keywords — indicator only, no score
    suspicious_words = [
        "login", "verify", "verification",
        "secure", "account", "update",
        "confirm", "signin", "password"
    ]

    found_words = [
        word for word in suspicious_words
        if word in url.lower()
    ]

    if found_words:
        indicators.append(
            "Contains suspicious keywords: " +
            ", ".join(found_words)
        )

    score = min(score, 100)

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    threat_type = (
        "Phishing"
        if score >= 40
        else "Legitimate / No Threat Detected"
    )

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "threat_type": threat_type,
        "indicators": indicators
    }


if __name__ == "__main__":
    message = "URGENT! Your bank account has been blocked. Click https://evil.com immediately."
    print(analyze_message(message))

    url = "http://192.168.1.20/login/verify"
    print(analyze_url(url))