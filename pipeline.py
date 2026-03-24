# pipeline.py — chains preprocessor → OCR → classifier → progress → scorer → db

from ocr_engine import extract_text
from classifier import classify
from progress_detector import detect_progress, is_repeated_screen
from scorer import calculate_score
from db import insert_submission, insert_alert, get_latest_submission

def run_pipeline(image_path, employee_id):
    """
    Full pipeline for one screenshot.
    1. Extract text via OCR
    2. Classify activity
    3. Compare with previous screen
    4. Calculate productivity score
    5. Store result in DB
    6. Trigger alerts if needed
    Returns the result dict.
    """
    print(f"\n[pipeline] Starting for {employee_id} — {image_path}")

    # Step 1: OCR
    current_text = extract_text(image_path)

    # Step 2: Classify
    activity_class = classify(current_text)

    # Step 3: Get previous screen text for comparison
    previous = get_latest_submission(employee_id)
    previous_text = previous["extracted_text"] if previous else ""

    # Step 4: Score
    productivity_score = calculate_score(activity_class, current_text, previous_text)
    progress_score     = detect_progress(current_text, previous_text)

    # Step 5: Store in DB
    insert_submission(
        employee_id      = employee_id,
        extracted_text   = current_text,
        activity_class   = activity_class,
        progress_score   = progress_score,
        productivity_score = productivity_score,
        image_path       = image_path
    )

    # Step 6: Alerts
    if productivity_score < 40:
        insert_alert(
            employee_id = employee_id,
            alert_type  = "low_productivity",
            message     = f"Score dropped to {productivity_score} — possible distraction"
        )
        print(f"[pipeline] ⚠ Alert: low productivity ({productivity_score})")

    if is_repeated_screen(current_text, previous_text):
        insert_alert(
            employee_id = employee_id,
            alert_type  = "repeated_screen",
            message     = "Same screen detected for multiple captures"
        )
        print(f"[pipeline] ⚠ Alert: repeated screen detected")

    result = {
        "employee_id":        employee_id,
        "activity_class":     activity_class,
        "progress_score":     progress_score,
        "productivity_score": productivity_score,
        "extracted_text":     current_text[:200],  # trimmed for response
    }

    print(f"[pipeline] ✅ Done — {activity_class} | Score: {productivity_score}")
    return result


if __name__ == "__main__":
    # Quick test — put any screenshot in F:\person2 and run this
    import sys
    image  = sys.argv[1] if len(sys.argv) > 1 else "test_screenshot.png"
    emp_id = sys.argv[2] if len(sys.argv) > 2 else "EMP001"
    result = run_pipeline(image, emp_id)
    print("\n--- Pipeline Result ---")
    for k, v in result.items():
        if k != "extracted_text":
            print(f"  {k}: {v}")
