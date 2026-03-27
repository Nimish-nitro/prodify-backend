# progress_detector.py — compares current screen text with previous to detect progress

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def detect_progress(current_text, previous_text):
    """
    Compares current and previous OCR text using cosine similarity.
    Returns a progress score from 0 to 100.
    - High score = screen changed a lot = progress made
    - Low score  = screen barely changed = possible inactivity
    """
    # If either is empty, treat as full change
    if not current_text or not previous_text:
        return 100.0

    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([current_text, previous_text])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

        # Convert similarity to a change score (1 - similarity)
        # similarity=1 means identical screen → progress=0
        # similarity=0 means completely different → progress=100
        progress = round((1 - similarity) * 100, 1)
        print(f"[progress] Similarity: {round(similarity * 100, 1)}% → Progress score: {progress}")
        return progress

    except Exception as e:
        print(f"[progress] Error: {e}")
        return 50.0  # neutral fallback


def is_repeated_screen(current_text, previous_text, threshold=90.0):
    """
    Returns True if the screen has barely changed (similarity above threshold).
    Used to trigger a 'repeated screen' alert.
    """
    if not current_text or not previous_text:
        return False

    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([current_text, previous_text])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0] * 100
        return similarity >= threshold
    except:
        return False
