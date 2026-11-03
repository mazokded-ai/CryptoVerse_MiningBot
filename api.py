
import sqlite3
from pathlib import Path
from datetime import date

from fastapi import FastAPI
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mining.db"

app = FastAPI(title="CryptoVerse Mining")


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                balance INTEGER DEFAULT 100,
                level INTEGER DEFAULT 1,
                last_daily TEXT DEFAULT ''
            )
        """)


init_db()


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/style.css")
def styles():
    return FileResponse(BASE_DIR / "style.css")


@app.get("/app.js")
def script():
    return FileResponse(BASE_DIR / "app.js")


@app.get("/api/state/{user_id}")
def get_state(user_id: str):
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        row = db.execute(
            "SELECT balance, level, last_daily FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

    return {
        "balance": row[0],
        "level": row[1],
        "last_daily": row[2]
    }


@app.post("/api/daily/{user_id}")
def daily(user_id: str):
    today = date.today().isoformat()

    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )

        row = db.execute(
            "SELECT last_daily FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if row[0] == today:
            return {"ok": False, "message": "Бонус уже получен сегодня"}

        db.execute(
            "UPDATE users SET balance = balance + 50, last_daily = ? WHERE user_id = ?",
            (today, user_id)
        )

    return {"ok": True, "bonus": 50}


@app.post("/api/upgrade/{user_id}")
def upgrade(user_id: str):
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )

        row = db.execute(
            "SELECT balance, level FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        cost = row[1] * 100

        if row[0] < cost:
            return {"ok": False, "message": "Недостаточно CV"}

        db.execute(
            "UPDATE users SET balance = balance - ?, level = level + 1 WHERE user_id = ?",
            (cost, user_id)
        )

    return {"ok": True}


@app.get("/health")
def health():
    return {"status": "ok"}
