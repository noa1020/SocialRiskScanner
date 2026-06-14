import json
import os
import sqlite3

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts.db"))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                username TEXT NOT NULL,
                suicide_rate TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_post(content, username, analysis):

    if not analysis.get("is_risk", False):
        return {
            "saved": False,
            "reason": "not_risk"
        }

    init_db()

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO posts (content, username, suicide_rate) VALUES (?, ?, ?)",
            (content, username, json.dumps(analysis)),
        )
        conn.commit()

        post_id = cursor.lastrowid

    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM posts WHERE id=?",
            (post_id,)
        ).fetchone()

    return {
        "saved": True,
        "id": row["id"],
        "content": row["content"],
        "username": row["username"],
        "suicide_rate": json.loads(row["suicide_rate"]),
        "created_at": row["created_at"],
    }


def get_all_posts():
    init_db()

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY id DESC"
        ).fetchall()

    return [
        {
            "id": r["id"],
            "content": r["content"],
            "username": r["username"],
            "suicide_rate": json.loads(r["suicide_rate"]),
            "created_at": r["created_at"],
        }
        for r in rows
    ]