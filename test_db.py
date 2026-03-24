# test_db.py — run this to confirm DB is connected and working

from db import insert_submission, get_submissions_today, get_avg_score_today

print("--- Testing DB connection ---")

# Insert a dummy submission
insert_submission(
    employee_id="EMP001",
    extracted_text="def calculate import pandas SELECT FROM WHERE",
    activity_class="Productive",
    progress_score=72.5,
    productivity_score=85.0,
    app_detected="VS Code",
    image_path="screenshots/test.png"
)

# Read it back
rows = get_submissions_today("EMP001")
print(f"\nSubmissions today for EMP001: {len(rows)}")
for row in rows:
    print(f"  → {row['timestamp']} | {row['activity_class']} | score: {row['productivity_score']}")

# Check average score
avg = get_avg_score_today("EMP001")
print(f"\nAverage score today: {avg}")

print("\n✅ DB test passed.")
