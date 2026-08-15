import sqlite3
from pathlib import Path
import uuid

from graph.state import MarvelState
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "episodic.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodic_memories (
        memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        event TEXT NOT NULL,
        date TEXT,
        context TEXT,
        summary TEXT,
        importance REAL,
        confidence REAL,
        source TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    """)

    conn.commit()
    conn.close()

def create_episodic_memory(user_id, event, date, context, summary, importance, confidence, source, created_at):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO episodic_memories (user_id, event, date, context, summary, importance, confidence, source, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, event, date, context, summary, importance, confidence, source, created_at, created_at))

    memory_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return memory_id

def update_episodic_memory(memory_id, user_id, event, date, context, summary, importance, confidence, source , updated_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE episodic_memories
        SET
            event = ?,
            date = ?,
            context = ?,
            summary = ?,
            importance = ?,
            confidence = ?,
            source = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE memory_id = ?
        AND user_id = ?
    """, (event, date, context, summary, importance, confidence, source, updated_at))

    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0  # Return True if a row was updated, False otherwise


def delete_episodic_memory(memory_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM episodic_memories
        WHERE memory_id = ? AND user_id = ?
    """, (memory_id, user_id))

    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0  # Return True if a row was deleted, False otherwise


def retrieve_episodic_memory(date: str | None, user_id: str):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if date is None:
        cursor.execute("""
            SELECT *
            FROM episodic_memories
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT *
            FROM episodic_memories
            WHERE date = ?
            AND user_id = ?
            ORDER BY date DESC
        """, (date, user_id))

    memories = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return memories




def handle_episodic_memory(state: MarvelState, memory: dict):

    user_id = state["user_id"]
    action = memory["action"]
    confidence = memory.get("confidence", 1.0)
    importance = memory.get("importance", 1.0)
    source = memory.get("source", "unknown")
    data = memory.get("data", {})
    reason = memory.get("reason", "")


    if action == "create":
        memory_id = create_episodic_memory(user_id=user_id, event=data.get("event"),date=data.get("date"), context=data.get("context"), summary=data.get("summary"), importance=importance, confidence=confidence, source=source, created_at=data.get("date"))
        return {"status": "success", "memory_id": memory_id}
    elif action == "update":
        memory_id = memory.get("memory_id")

        if not memory_id:
            return {
                "status": "error",
                "message": "memory_id required for update"
            }
        updated = update_episodic_memory(memory_id=memory_id, user_id=user_id, event=data.get("event"),date=data.get("date"), context=data.get("context"), summary=data.get("summary"), importance=importance, confidence=confidence, source=source, updated_at=data.get("date"))
        return {"status": "success" if updated else "not_found"}
    elif action == "delete":
        deleted = delete_episodic_memory(memory_id=memory_id, user_id=user_id)
        return {"status": "success" if deleted else "not_found"}
                    
    elif action == "retrieve":
        date = data.get("date")
        memories = retrieve_episodic_memory(date=date, user_id=user_id)
        return {"status": "success", "memories": memories}