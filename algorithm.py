from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="sentinet/suicidality")


def analyze_text(text):
    result = classifier(text)
    label = result[0]["label"]
    score = result[0]["score"] * 100
    return {"score": score, "label": label}

