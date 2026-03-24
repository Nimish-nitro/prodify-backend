# classifier.py — loads trained model and classifies extracted screen text

import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

# Load model once when module is imported
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def classify(text):
    """
    Takes extracted OCR text as input.
    Returns one of: 'Productive', 'Non-productive', 'Idle'
    """
    if not text or len(text.strip()) < 5:
        return "Idle"

    prediction = model.predict([text])[0]
    confidence = max(model.predict_proba([text])[0])

    print(f"[classifier] {prediction} (confidence: {round(confidence * 100, 1)}%)")
    return prediction


def classify_with_confidence(text):
    """Returns both the label and confidence score as a dict."""
    if not text or len(text.strip()) < 5:
        return {"label": "Idle", "confidence": 100.0}

    prediction = model.predict([text])[0]
    confidence = round(max(model.predict_proba([text])[0]) * 100, 1)

    return {"label": prediction, "confidence": confidence}
