import sqlite3
from pathlib import Path
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============
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
    logger.info("successfully called create episodic sql func")
    logger.info("successfully connected to episodic sql")


    cursor.execute("""
        INSERT INTO episodic_memories (memory_id, user_id, event, date, context, summary, importance, confidence, source, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (memory_id, user_id, event, date, context, summary, importance, confidence, source))

    
    conn.commit()
    logger.info("successfully commited to episodic sql")
    conn.close()


def update_episodic_memory(memory_id, user_id, event, date, context, summary, importance, confidence, source , updated_at):

    logger.info("successfully called update episodic sql func")

    if memory_id == None:
        logger.warning("No memory id provided to the update episodic memeory sql")
    
    conn = get_connection()
    cursor = conn.cursor()
    logger.info("successfully connected to episodic sql")

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
    logger.info("successfully commited to episodic sql")
    conn.close()
    return updated > 0  # Return True if a row was updated, False otherwise


def delete_episodic_memory(memory_id, user_id):

    logger.info("successfully called delete episodic sql func")

    if memory_id == None:
        logger.warning("No memory id provided to the delete episodic memeory sql")
    
    conn = get_connection()
    cursor = conn.cursor()
    logger.info("successfully connected to episodic sql")

    cursor.execute("""
        DELETE FROM episodic_memories
        WHERE memory_id = ? AND user_id = ?
    """, (memory_id, user_id))

    conn.commit()
    deleted = cursor.rowcount
    logger.info("successfully commited to episodic sql")
    conn.close()
    return deleted > 0  # Return True if a row was deleted, False otherwise


def retrieve_episodic_memory(date: str | None, user_id: str, vector_results):

    logger.info("successfully called retrieve episodic sql func")

    if not vector_results:
        logger.debug("no id to retrieve from in episodic sql")
        return []
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    logger.info("successfully connected to episodic sql")
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
            logger.info("retrieve a row from episodic sql")
            memory_data = (dict(row))
            memory_data["faiss_distance"] = j["distance"]
            memories.append(memory_data)
    
    logger.info(f"successfully retrieve from episodic sql - {memories}")
    conn.close()

    return memories




def handle_episodic_memory(state):
    """Handles all the CRUD operation for episodic memeory."""

    logger.info("successfully called episodic sql file")
    memory_data = state.get("memory_nodes", {})


    for operation in memory_data.get("memories", []):

        if operation.get("memory_type") != "episodic":
            logger.info("operation not episodic type")
            continue

        action = operation.get("action")
        confidence = operation.get("confidence", 1.0)
        source = operation.get("source", "unknown")
        data = operation.get("data", {})
        importance = data.get("importance", 1.0)
        user_id = operation.get("user_id")
        memory_id = operation.get("memory_id")


        if memory_id is None:
            logger.warning(f"Error: memory_id is required for action '{action}' but is missing in episodic sql.")
            break


        if not user_id:
            logger.warning(f"No user_id for episodic sql in the state. user_id - {user_id}")


        if action == "create":
            logger.info("action is create")
            create_episodic_memory(memory_id=memory_id, user_id=user_id, event=data.get("event"),date=data.get("date"), context=data.get("context"), summary=data.get("summary"), importance=importance, confidence=confidence, source=source)
            logger.info("episodic create success sql")

        elif action == "update":
            logger.info("action is create")
            update_episodic_memory(memory_id=memory_id, user_id=user_id, event=data.get("event"),date=data.get("date"), context=data.get("context"), summary=data.get("summary"), importance=importance, confidence=confidence, source=source, updated_at=data.get("date"))
            logger.info("episodic update success sql")

        elif action == "delete":
            logger.info("action is delete")
            delete_episodic_memory(memory_id=memory_id, user_id=user_id)
            logger.info("episodic delete success sql")
                        
        else:
            logger.warning(f"{action} is not valid action")
#i=i+1






# if __name__ == "__main__":
#     init_db()

   