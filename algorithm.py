from transformers import pipeline
from threading import Lock

classifier = pipeline(
    "sentiment-analysis",
    model="sentinet/suicidality"
)

model_lock = Lock()


def analyze_text(text):
    if not isinstance(text, str) or not text.strip():
        return {
            "label": "UNKNOWN",
            "score": 0.0,
        }

    with model_lock:
        result = classifier(text.strip())

    label = result[0]["label"]
    score = result[0]["score"] * 100

    print(result)

    return {
        "label": label,
        "score": score
    }