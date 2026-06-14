from transformers import pipeline
from threading import Lock

classifier = pipeline(
    "sentiment-analysis",
    model="sentinet/suicidality",
    truncation=True
)

model_lock = Lock()


def analyze_text(text):
    if not isinstance(text, str) or not text.strip():
        return {
            "label": "UNKNOWN",
            "score": 0.0,
            "is_risk": False,
            "risk_level": "none",
        }

    text = text.strip()

    with model_lock:
        result = classifier(text)[0]

    print(result)
    label = result.get("label", "UNKNOWN")
    score = float(result.get("score", 0.0))

    is_risk = label == "LABEL_1"

    risk_level = "none"

    if is_risk:
        if score >= 0.97:
            risk_level = "high"
        elif score >= 0.95:
            risk_level = "medium"
        else:
            risk_level = "low"

    return {
        "label": label,
        "score": score,
        "is_risk": is_risk,
        "risk_level": risk_level,
    }