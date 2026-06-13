import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "posts.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                username TEXT NOT NULL,
                suicide_rate TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def serialize_post(row):
    if not row:
        return None

    suicide_rate = row["suicide_rate"]
    if isinstance(suicide_rate, str):
        try:
            suicide_rate = json.loads(suicide_rate)
        except json.JSONDecodeError:
            suicide_rate = {"value": suicide_rate}

    return {
        "id": row["id"],
        "content": row["content"],
        "username": row["username"],
        "suicide_rate": suicide_rate,
        "created_at": row["created_at"],
    }


def save_post(content, username, suicide_rate):
    normalized_content = (content or "").strip()
    normalized_username = (username or "").strip()

    if not normalized_content or not normalized_username:
        return {
            "saved": False,
            "reason": "missing_content_or_username",
            "content": normalized_content,
            "username": normalized_username,
        }

    if not isinstance(suicide_rate, dict):
        suicide_rate = {"label": "UNKNOWN", "score": 0.0, "score_percentage": 0.0, "risk_level": "none", "is_high_risk": False}

    if not suicide_rate.get("is_high_risk", False):
        return {
            "saved": False,
            "reason": "below_risk_threshold",
            "content": normalized_content,
            "username": normalized_username,
            "suicide_rate": suicide_rate,
        }

    init_db()
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO posts (content, username, suicide_rate) VALUES (?, ?, ?)",
            (normalized_content, normalized_username, json.dumps(suicide_rate)),
        )
        conn.commit()
        post_id = cursor.lastrowid

    with get_connection() as conn:
        row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()

    return {"saved": True, **serialize_post(row)}


def get_all_posts():
    init_db()
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()

    return [serialize_post(row) for row in rows if serialize_post(row)]
