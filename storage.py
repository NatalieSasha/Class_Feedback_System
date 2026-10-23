import json
import sqlite3
import threading
from datetime import datetime, timezone

class EventStore:
    # SQLite outbox for feedback events that have not reached the cloud yet.
    def __init__(self, database_path: str):
        self.database_path = database_path
        self._lock = threading.Lock()
        with self._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS event_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    sent INTEGER NOT NULL DEFAULT 0
                )
            ''')
            conn.commit()

    def _connect(self):
        conn = sqlite3.connect(self.database_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, event: dict) -> int:
        payload = json.dumps(event, separators=(",", ":"))
        created_at = datetime.now(timezone.utc).isoformat()
        with self._lock, self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO event_queue(event_json, created_at, sent) VALUES (?, ?, 0)",
                (payload, created_at),
            )
            conn.commit()
            return int(cur.lastrowid)

    def pending(self, limit: int = 100):
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT id, event_json FROM event_queue WHERE sent = 0 ORDER BY id LIMIT ?",
                (limit,),
            ).fetchall()
        return [(int(row["id"]), json.loads(row["event_json"])) for row in rows]

    def mark_sent(self, event_id: int):
        with self._lock, self._connect() as conn:
            conn.execute("UPDATE event_queue SET sent = 1 WHERE id = ?", (event_id,))
            conn.commit()

    def count_pending(self) -> int:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS n FROM event_queue WHERE sent = 0").fetchone()
            return int(row["n"])
