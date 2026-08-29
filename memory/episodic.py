import sqlite3
from pathlib import Path
import uuid

from graph.state import MemoryManagerOutput
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "sql" / "episodic.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodic_memories (
        memory_id INTEGER PRIMARY KEY,
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

def create_episodic_memory(memory_id, user_id, event, date, context, summary, importance, confidence, source):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO episodic_memories (memory_id, user_id, event, date, context, summary, importance, confidence, source, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (memory_id, user_id, event, date, context, summary, importance, confidence, source))

    
    conn.commit()
    conn.close()


def update_episodic_memory(memory_id, user_id, event, date, context, summary, importance, confidence, source , updated_at):

    if memory_id == None:
        print("No memory id provided to the update episodic memeory sql")
    
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
    """, (event, date, context, summary, importance, confidence, source, memory_id, user_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0  # Return True if a row was updated, False otherwise


def delete_episodic_memory(memory_id, user_id):

    if memory_id == None:
        print("No memory id provided to the delete episodic memeory sql")
    
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


def retrieve_episodic_memory(date: str | None, user_id: str, vector_results):

    if not vector_results:
        return []
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    memories = []
    
    for j in vector_results:
        i = j["memory_id"]
        if date is None:
            cursor.execute("""
                SELECT *
                FROM episodic_memories
                WHERE user_id = ?
                AND memory_id = ?
                ORDER BY date DESC
            """, (user_id, i))
        else:
            cursor.execute("""
                SELECT *
                FROM episodic_memories
                WHERE date = ?
                AND user_id = ?
                AND memory_id = ?
                ORDER BY date DESC
            """, (date, user_id, i))
        row = cursor.fetchone()
        if row:
            memory_data = (dict(row))
            memory_data["faiss_distance"] = j["distance"]
            memories.append(memory_data)
    

    conn.close()

    return memories




def handle_episodic_memory(state):
    """Handles all the CRUD operation for episodic memeory."""

    i=0
    memory_data = state.get("memory_notes", {})
    for operation in memory_data.get("memories", []):
        if operation.get("memory_type") != "episodic":
            continue
            
        action = operation.get("action")
        confidence = operation.get("confidence", 1.0)
        source = operation.get("source", "unknown")
        data = operation.get("data", {})
        importance = data.get("importance", 1.0)
        user_id = operation.get("user_id")
        memory_id = operation.get("memory_id")[i]

        if not user_id:
            return {"status": "error", "message": "user_id is missing from state"}

        if action == "create":
            create_episodic_memory(memory_id=memory_id, user_id=user_id, event=data.get("event"),date=data.get("date"), context=data.get("context"), summary=data.get("summary"), importance=importance, confidence=confidence, source=source)
            print("episodic create success")
        elif action == "update":
            if not memory_id:
                return {
                    "status": "error",
                    "message": "memory_id required for update"
                }
            update_episodic_memory(memory_id=memory_id, user_id=user_id, event=data.get("event"),date=data.get("date"), context=data.get("context"), summary=data.get("summary"), importance=importance, confidence=confidence, source=source, updated_at=data.get("date"))
            print("episodic update success")
        elif action == "delete":
            delete_episodic_memory(memory_id=memory_id, user_id=user_id)
            #return {"status": "success" if deleted else "not_found"}
            print("episodic delete success")
                        
        elif action == "retrieve":
            date = data.get("date")
            memories = retrieve_episodic_memory(date=date, user_id=user_id, memory_id= memory_id)
            return {"memories": memories}
        else:
            print("error in episodoic.py")
        i=i+1






# if __name__ == "__main__":

#     init_db()

   