from config import settings
import sqlite3
import json
from datetime import datetime, timezone

def get_connection():
    conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            sport TEXT NOT NULL,
            duree_min INTEGER NOT NULL,
            ressenti TEXT NOT NULL,
            sentiment TEXT,
            signaux_faibles TEXT,
            ton_utilise TEXT,
            message_genere TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_seances_user 
        ON seances(user_id, created_at DESC)
    ''')
    conn.commit()
    conn.close()

def enregistrer_seance(
    user_id: str, sport: str, duree_min: int, ressenti: str,
    sentiment: str | None = None,
    signaux: list | None = None,
    ton: str | None = None,
    message: str | None = None,
) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO seances (user_id, sport, duree_min, ressenti, sentiment, signaux_faibles, ton_utilise, message_genere, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        sport,
        duree_min,
        ressenti,
        sentiment,
        json.dumps(signaux or []),
        ton,
        message,
        datetime.now(timezone.utc).isoformat()
    ))
    conn.commit()
    seance_id = cursor.lastrowid
    conn.close()
    return seance_id

def historique_utilisateur(user_id: str, limite: int = 5) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT *
        FROM seances
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (user_id, limite))
    rows = cursor.fetchall()
    conn.close()
    return [
        {**dict(row), "signaux_faibles": json.loads(row["signaux_faibles"] or "[]")}
        for row in rows
    ]

def compter_seances(user_id: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) as count
        FROM seances
        WHERE user_id = ?
    ''', (user_id,))
    count = cursor.fetchone()["count"]
    conn.close()
    return count