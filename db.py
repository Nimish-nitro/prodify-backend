# db.py — MySQL connection + all insert and query functions

import mysql.connector
import os

# Railway MySQL service reference variables
DB_CONFIG = {
    "host":     os.getenv("MYSQLHOST", "localhost"),
    "port":     int(os.getenv("MYSQLPORT", 3306)),
    "user":     os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", ""),
    "database": os.getenv("MYSQLDATABASE", "prodify")
}

def get_connection():
    """Returns a fresh MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


# ─── INSERT ───────────────────────────────────────────────────────────────────

def insert_submission(employee_id, extracted_text, activity_class,
                      progress_score, productivity_score,
                      app_detected="", image_path=""):
    """Inserts one processed screenshot result into the submissions table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO submissions
            (employee_id, extracted_text, app_detected, activity_class,
             progress_score, productivity_score, image_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (employee_id, extracted_text, app_detected, activity_class,
          progress_score, productivity_score, image_path))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"[db] Submission inserted for {employee_id}")


def insert_alert(employee_id, alert_type, message):
    """Inserts a new alert into the alerts table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alerts (employee_id, alert_type, message)
        VALUES (%s, %s, %s)
    """, (employee_id, alert_type, message))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"[db] Alert inserted for {employee_id}: {alert_type}")


# ─── QUERY ────────────────────────────────────────────────────────────────────

def get_submissions_today(employee_id):
    """Returns all submissions for an employee from today."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM submissions
        WHERE employee_id = %s
          AND DATE(timestamp) = CURDATE()
        ORDER BY timestamp DESC
    """, (employee_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_latest_submission(employee_id):
    """Returns the most recent submission for an employee."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM submissions
        WHERE employee_id = %s
        ORDER BY timestamp DESC
        LIMIT 1
    """, (employee_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_avg_score_today(employee_id):
    """Returns today's average productivity score for an employee."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(productivity_score) FROM submissions
        WHERE employee_id = %s
          AND DATE(timestamp) = CURDATE()
    """, (employee_id,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return round(result, 1) if result else 0


def get_all_employees():
    """Returns all employees."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, role FROM employees")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_unresolved_alerts():
    """Returns all unresolved alerts across all employees."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM alerts
        WHERE resolved = FALSE
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_employee_by_id(employee_id, password_hash):
    """Returns employee if credentials match, else None."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, name, role FROM employees
        WHERE id = %s AND password_hash = %s
    """, (employee_id, password_hash))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row
