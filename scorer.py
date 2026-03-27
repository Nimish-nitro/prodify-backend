# scorer.py — combines activity classification + progress into a final 0-100 productivity score

from progress_detector import detect_progress

# Base scores per activity class
BASE_SCORES = {
    "Productive":     80,
    "Non-productive": 20,
    "Idle":           5,
}

# Weight split between activity and progress
ACTIVITY_WEIGHT = 0.7
PROGRESS_WEIGHT = 0.3

def calculate_score(activity_class, current_text, previous_text):
    """
    Combines activity classification and screen progress into a final score.

    Formula:
        score = (activity_base * 0.7) + (progress_score * 0.3)

    Returns a float between 0 and 100.
    """
    base = BASE_SCORES.get(activity_class, 50)
    progress = detect_progress(current_text, previous_text)

    score = (base * ACTIVITY_WEIGHT) + (progress * PROGRESS_WEIGHT)
    score = round(min(max(score, 0), 100), 1)  # clamp between 0 and 100

    print(f"[scorer] Class: {activity_class} | Base: {base} | Progress: {progress} | Final: {score}")
    return score


def score_label(score):
    """Returns a human-readable label for a score."""
    if score >= 75:
        return "High"
    elif score >= 45:
        return "Medium"
    else:
        return "Low"
