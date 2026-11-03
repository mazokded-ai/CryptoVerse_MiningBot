import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="CryptoVerse Mining")

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
DB_PATH = BASE_DIR / "mining.db"

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
    return FileResponse(WEB_DIR / "index.html")

app.mount("/web", StaticFiles(directory=WEB_DIR), name="web")

@app.get("/api/state/{user_id}")
def get_state(user_id: str):
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        row = db.execute(
            "SELECT balance, level FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

    return {"balance": row[0], "level": row[1]}

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
