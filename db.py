import sqlite3
import bcrypt
import base64
import pathlib
import io
from PIL import Image

DB_PATH = str(pathlib.Path.home() / "pixelpulse_ai.db")


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            title      TEXT    NOT NULL,
            created_at TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role       TEXT    NOT NULL,
            content    TEXT    NOT NULL,
            image_b64  TEXT,
            created_at TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (session_id) REFERENCES chat_sessions(id)
        );
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            task_title TEXT    NOT NULL,
            difficulty TEXT    NOT NULL,
            score      INTEGER NOT NULL,
            feedback   TEXT    NOT NULL,
            passed     INTEGER NOT NULL,
            created_at TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


# ── Auth ──────────────────────────────────────────────────────────────────────

def register_user(username: str, password: str) -> tuple:
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    try:
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conn = get_conn()
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username.lower().strip(), pw_hash)
        )
        conn.commit()
        conn.close()
        return True, "Account created!"
    except sqlite3.IntegrityError:
        return False, "Username already taken."
    except Exception as e:
        return False, str(e)


def login_user(username: str, password: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username.lower().strip(),)
    ).fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[1].encode()):
        return row[0]
    return None


# ── Chat sessions ─────────────────────────────────────────────────────────────

def create_session(user_id: int, title: str) -> int:
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO chat_sessions (user_id, title) VALUES (?, ?)",
        (user_id, title[:60])
    )
    session_id = cur.lastrowid
    conn.commit()
    conn.close()
    return session_id


def get_sessions(user_id: int) -> list:
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, title, created_at FROM chat_sessions WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def rename_session(session_id: int, title: str):
    conn = get_conn()
    conn.execute("UPDATE chat_sessions SET title = ? WHERE id = ?", (title[:60], session_id))
    conn.commit()
    conn.close()


def delete_session(session_id: int, user_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.execute(
        "DELETE FROM chat_sessions WHERE id = ? AND user_id = ?",
        (session_id, user_id)
    )
    conn.commit()
    conn.close()


# ── Messages ──────────────────────────────────────────────────────────────────

def add_message(session_id: int, role: str, content: str, image_b64: str = None):
    conn = get_conn()
    conn.execute(
        "INSERT INTO messages (session_id, role, content, image_b64) VALUES (?, ?, ?, ?)",
        (session_id, role, content, image_b64)
    )
    conn.commit()
    conn.close()


def get_messages(session_id: int) -> list:
    conn = get_conn()
    rows = conn.execute(
        "SELECT role, content, image_b64 FROM messages WHERE session_id = ? ORDER BY created_at ASC",
        (session_id,)
    ).fetchall()
    conn.close()
    return rows


# ── Quiz ──────────────────────────────────────────────────────────────────────

def save_quiz_attempt(user_id: int, task_title: str, difficulty: str,
                      score: int, feedback: str, passed: bool):
    conn = get_conn()
    conn.execute(
        """INSERT INTO quiz_attempts
           (user_id, task_title, difficulty, score, feedback, passed)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, task_title, difficulty, score, feedback, int(passed))
    )
    conn.commit()
    conn.close()


def get_quiz_history(user_id: int) -> list:
    conn = get_conn()
    rows = conn.execute(
        """SELECT task_title, difficulty, score, passed, created_at
           FROM quiz_attempts WHERE user_id = ? ORDER BY created_at DESC""",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_quiz_stats(user_id: int) -> dict:
    conn = get_conn()
    total = conn.execute(
        "SELECT COUNT(*) FROM quiz_attempts WHERE user_id = ?", (user_id,)
    ).fetchone()[0]
    passed = conn.execute(
        "SELECT COUNT(*) FROM quiz_attempts WHERE user_id = ? AND passed = 1", (user_id,)
    ).fetchone()[0]
    avg = conn.execute(
        "SELECT AVG(score) FROM quiz_attempts WHERE user_id = ?", (user_id,)
    ).fetchone()[0]
    conn.close()
    return {"total": total, "passed": passed, "avg_score": round(avg or 0, 1)}


# ── Image util ────────────────────────────────────────────────────────────────

def compress_image_b64(image: Image.Image, max_size: int = 512) -> str:
    img = image.copy().convert("RGB")
    img.thumbnail((max_size, max_size))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=72)
    return base64.b64encode(buf.getvalue()).decode()


def b64_to_image(b64: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(b64)))
