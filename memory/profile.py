#from graph.state import MemoryManagerOutput

from pathlib import Path
import sqlite3
import logging
#==========Logger==============


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(filename)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("log_info.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

#==========Logger===============

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "sql" / "profile.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            category TEXT NOT NULL,
            field TEXT NOT NULL,
            value TEXT NOT NULL,
            confidence REAL DEFAULT 1.0,
            importance REAL DEFAULT 0.5,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(user_id, category, field)
        )
    """)

    conn.commit()
    conn.close()

def update_profile(user_id: str,category: str,field: str,value,confidence: float,importance: float,source: str):
    conn = get_connection()

    cursor = conn.cursor()
    logger.info("successfully called create profile sql func")
    logger.info("successfully connected to profile sql")

    cursor.execute("""
        INSERT INTO profile_memories (user_id,category, field, value,confidence,importance,source) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, category, field)
        DO UPDATE SET
            value = excluded.value,
            confidence = excluded.confidence,
            importance = excluded.importance,
            source = excluded.source,
            updated_at = CURRENT_TIMESTAMP
    """, (user_id,category,field,str(value),confidence,importance, source))

    conn.commit()
    logger.info("successfully commited in profile sql")
    conn.close()



def delete_profile( user_id: str, category: str, field: str):
    conn = get_connection()

    cursor = conn.cursor()
    logger.info("successfully called delete profile sql func")
    logger.info("successfully connected to profile sql")

    cursor.execute("""
        DELETE FROM profile_memories
        WHERE user_id = ?
        AND category = ?
        AND field = ?
    """, (
        user_id,
        category,
        field
    ))

    conn.commit()

    deleted = cursor.rowcount
    logger.info("successfully commited in profile sql")
    conn.close()

    return deleted > 0





def get_profile(
    user_id: str,
    category: str | None = None,
    field: str | None = None
    ):

    if not user_id:
        logger.warning("No user_id provided for profile retrieve sql")
        return
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    logger.info("successfully called retrieve profile sql func")
    logger.info("successfully connected to profile sql")

    if category and field:
        logger.info('to retrieve profile info category and field provided')
        cursor.execute("""
            SELECT
                category,
                field,
                value,
                confidence,
                importance,
                source
            FROM profile_memories
            WHERE user_id = ?
            AND category = ?
            AND field = ?
        """, (
            user_id,
            category,
            field
        ))

    elif category:
        logger.info('to retrieve profile ONLY category provided')
        cursor.execute("""
            SELECT
                category,
                field,
                value,
                confidence,
                importance,
                source
            FROM profile_memories
            WHERE user_id = ?
            AND category = ?
        """, (
            user_id,
            category
        ))

    else:
        logger.info('to retrieve profile ONLY user_id provided')
        cursor.execute("""
            SELECT
                category,
                field,
                value,
                confidence,
                importance,
                source
            FROM profile_memories
            WHERE user_id = ?
        """, (
            user_id,
        ))

    memories = [dict(row) for row in cursor.fetchall()]

    conn.close()
    logger.info(f"retrieved memories from profile sql is - {memories}")

    return memories





def handle_profile_memory(state):
    """Handles all the CRUD operation for the profile memory."""

    logger.info("successfully called profile sql file")

    memory_data = state.get("memory_nodes", {})

    for operation in memory_data.get("memories", []):
        
        if operation.get("memory_type") != "profile":
            logger.info("operation not profile type")
            continue

        action = operation.get("action")
        user_id = operation.get("user_id")
        data = operation.get("data",{})
        category = data.get('category', '')
        field = data.get('field', '')
        value = data.get('value', '')
        importance = data.get('importance', 0.5)
        confidence = operation.get("confidence",0.5)
        source = operation.get("source")

    

        if action in ("create", "update"):
            logger.info(f"action is create or update - {action}")

            update_profile(
                user_id=user_id,
                category=category,
                field=field,
                value=value,
                confidence=confidence,
                importance=importance,
                source=source
            )

            logger.debug(f"profile {action} success")



        elif action == "delete":
            logger.info("action is delete")
            deleted = delete_profile(
                user_id=user_id,
                category=category,
                field=field
            )

            logger.debug("profile deleted success")
        else:
            logger.warning(f"Unsupported profile action: {action}")

        


# if __name__ == "__main__":

#     init_db()

   