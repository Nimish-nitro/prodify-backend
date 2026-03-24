# app.py — main Flask API that exposes all endpoints for Person 1 and Person 3

from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import run_pipeline
from db import (
    get_submissions_today,
    get_avg_score_today,
    get_all_employees,
    get_unresolved_alerts,
    get_employee_by_id,
    get_latest_submission
)
import hashlib
import os
import tempfile

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "received_screenshots"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ─── HELPER ───────────────────────────────────────────────────────────────────

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ─── PERSON 1 ENDPOINTS ───────────────────────────────────────────────────────

@app.route("/process", methods=["POST"])
def process():
    """Receives screenshot from Person 1, runs full AI pipeline."""
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    employee_id = request.form.get("employee_id", "unknown")
    image       = request.files["image"]

    # Save image temporarily
    path = os.path.join(UPLOAD_FOLDER, f"{employee_id}_latest.png")
    image.save(path)

    try:
        result = run_pipeline(path, employee_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    """Authenticates employee. Returns employee_id and role."""
    data        = request.get_json()
    employee_id = data.get("employee_id", "")
    password    = data.get("password", "")

    employee = get_employee_by_id(employee_id, hash_password(password))
    if not employee:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "employee_id": employee["id"],
        "name":        employee["name"],
        "role":        employee["role"]
    }), 200


@app.route("/score/<employee_id>", methods=["GET"])
def get_score(employee_id):
    """Returns today's average productivity score for an employee."""
    score       = get_avg_score_today(employee_id)
    submissions = get_submissions_today(employee_id)
    hours       = round(len(submissions) * 10 / 60, 1)  # estimate: 1 capture per 10 mins

    return jsonify({
        "employee_id":        employee_id,
        "productivity_score": score,
        "hours_tracked":      hours
    }), 200


@app.route("/submissions/<employee_id>", methods=["GET"])
def get_submissions(employee_id):
    """Returns today's submissions for an employee."""
    rows = get_submissions_today(employee_id)
    submissions = []
    for row in rows:
        submissions.append({
            "timestamp":          str(row["timestamp"]),
            "activity_class":     row["activity_class"],
            "productivity_score": row["productivity_score"],
            "progress_score":     row["progress_score"],
        })
    return jsonify({"submissions": submissions}), 200


@app.route("/notifications/<employee_id>", methods=["GET"])
def get_notifications(employee_id):
    """Returns unresolved alerts for a specific employee."""
    all_alerts = get_unresolved_alerts()
    notifications = []
    for alert in all_alerts:
        if alert["employee_id"] == employee_id:
            notifications.append({
                "type":      alert["alert_type"],
                "message":   alert["message"],
                "timestamp": str(alert["timestamp"]),
            })
    return jsonify({"notifications": notifications}), 200


# ─── PERSON 3 ENDPOINTS ───────────────────────────────────────────────────────

@app.route("/admin/team-summary", methods=["GET"])
def team_summary():
    """Returns all employees with today's average score."""
    employees = get_all_employees()
    summary   = []
    for emp in employees:
        score       = get_avg_score_today(emp["id"])
        submissions = get_submissions_today(emp["id"])
        latest      = get_latest_submission(emp["id"])
        summary.append({
            "employee_id":        emp["id"],
            "name":               emp["name"],
            "productivity_score": score,
            "submissions_today":  len(submissions),
            "last_activity":      latest["activity_class"] if latest else "No data",
            "status":             "Active" if score >= 60 else ("Alert" if score > 0 and score < 40 else "Idle")
        })
    return jsonify({"team": summary}), 200


@app.route("/admin/employee/<employee_id>", methods=["GET"])
def employee_detail(employee_id):
    """Returns full submission timeline for one employee."""
    submissions = get_submissions_today(employee_id)
    timeline    = []
    for row in submissions:
        timeline.append({
            "timestamp":          str(row["timestamp"]),
            "activity_class":     row["activity_class"],
            "productivity_score": row["productivity_score"],
            "progress_score":     row["progress_score"],
        })
    avg_score = get_avg_score_today(employee_id)
    return jsonify({
        "employee_id": employee_id,
        "avg_score":   avg_score,
        "timeline":    timeline
    }), 200


@app.route("/admin/alerts", methods=["GET"])
def admin_alerts():
    """Returns all unresolved alerts across all employees."""
    alerts = get_unresolved_alerts()
    result = []
    for alert in alerts:
        result.append({
            "id":          alert["id"],
            "employee_id": alert["employee_id"],
            "alert_type":  alert["alert_type"],
            "message":     alert["message"],
            "timestamp":   str(alert["timestamp"]),
            "resolved":    alert["resolved"]
        })
    return jsonify({"alerts": result}), 200


@app.route("/results/<employee_id>", methods=["GET"])
def results(employee_id):
    """Combined endpoint — returns score + submissions + notifications."""
    score       = get_avg_score_today(employee_id)
    submissions = get_submissions_today(employee_id)
    alerts      = get_unresolved_alerts()
    hours       = round(len(submissions) * 10 / 60, 1)

    return jsonify({
        "employee_id":        employee_id,
        "productivity_score": score,
        "hours_tracked":      hours,
        "submissions": [{
            "timestamp":          str(r["timestamp"]),
            "activity_class":     r["activity_class"],
            "productivity_score": r["productivity_score"],
        } for r in submissions],
        "notifications": [{
            "type":      a["alert_type"],
            "message":   a["message"],
            "timestamp": str(a["timestamp"]),
        } for a in alerts if a["employee_id"] == employee_id]
    }), 200


# ─── RUN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("✅ ProdiFy backend running on http://localhost:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)
