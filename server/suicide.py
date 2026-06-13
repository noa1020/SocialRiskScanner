from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="sentinet/suicidality", truncation=True)
HIGH_RISK_THRESHOLD = 0.95


def analyze_text(text):
    """Return a generic risk-like signal for short social text.

    This is not a medical diagnostic tool. It only provides a provisional
    screening indicator that may be used to prioritize human review.
    """
    if not isinstance(text, str) or not text.strip():
        return {
            "label": "UNKNOWN",
            "score": 0.0,
            "score_percentage": 0.0,
            "risk_level": "none",
            "is_high_risk": False,
            "note": "No input text provided.",
        }

    result = classifier(text.strip())
    label = result[0].get("label", "UNKNOWN")
    score = float(result[0].get("score", 0.0))
    score_percentage = round(score * 100, 2)

    is_high_risk = score_percentage >= HIGH_RISK_THRESHOLD * 100
    risk_level = "high" if is_high_risk else "moderate" if score_percentage >= 70 else "low"

    return {
        "label": label,
        "score": score,
        "score_percentage": score_percentage,
        "risk_level": risk_level,
        "is_high_risk": is_high_risk,
        "note": "Provisional signal only; not a diagnosis.",
    }

