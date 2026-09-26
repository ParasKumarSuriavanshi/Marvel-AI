import faiss
import numpy as np

from pathlib import Path
from langchain_ollama.embeddings import OllamaEmbeddings

from graph.state import MemoryManagerOutput , MemoryOperation
import logging
#==========Logger==============

logger = logging.getLogger(__name__)
#==========Logger===============


#------------------------
#   sql
#------------------------
import sqlite3
BASE_DIRT = Path(__file__).resolve().parent.parent
DB_PATHH = BASE_DIRT / "database" / "sql" / "episodic.db"

def get_connection():
    return sqlite3.connect(DB_PATHH)

#------------------------
#   sql
#------------------------



#------------------------
#   vector
#------------------------

DIMENSION = 768

BASE_DIR = Path(__file__).resolve().parents[1]

INDEX_PATH = (BASE_DIR/ "database"/ "vector"/ "episodic.index")

embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Load existing index or create a new one
if INDEX_PATH.exists():
    index = faiss.read_index(str(INDEX_PATH))
    logger.info(f"index for episodic vector file - {index}")
else:
    #logger.warning("episodic vector file doesn't exist")
    base_index = faiss.IndexFlatL2(DIMENSION)
    index = faiss.IndexIDMap2(base_index)
    logger.info(f"created index for episodic vector file - {index}")

#------------------------
#   vector
#------------------------







def create_vector(text,memory_id: int):
    """Create and add an episodic memory vector."""

    # conn = get_connection()
    # cursor = conn.cursor()
    # cursor.execute("""SELECT MAX(memory_id) FROM episodic_memories;""")
    # results = cursor.fetchone()
    # previous_memory_id = results[0] if results[0] is not None else 0
    # memory_id = previous_memory_id + 1

    logger.info("successfully called create episodic vector func")

    
        # Generate embedding
    vector = embedding.embed_query(text)

        # Shape: (1, 768)
    vector = np.array([vector],dtype=np.float32)

        # FAISS ID
    ids = np.array([memory_id],dtype=np.int64)

        # Add vector
    index.add_with_ids(vector,ids)

    # Make sure directory exists
    INDEX_PATH.parent.mkdir(parents=True,exist_ok=True)

    # Save index
    faiss.write_index(index,str(INDEX_PATH))

    logger.debug(f"return memory_id as - {memory_id}")
    return memory_id








def update_vector(text ,memory_id: int):
    """Update an existing episodic memory vector."""

    logger.info("update episodic vector successfully called")

    if memory_id == None:
        logger.debug("No memory id provided to the update episodic memeory")
        return
    
        # Generate new embedding
    new_vector = embedding.embed_query(text)

        # Convert to NumPy array
    new_vector = np.array([new_vector],dtype=np.float32)

        # Remove old vector
    index.remove_ids(np.array([memory_id],dtype=np.int64))

        # Add new vector with same ID
    index.add_with_ids(new_vector,np.array([memory_id],dtype=np.int64))



    # Save updated index
    faiss.write_index(index,str(INDEX_PATH))
    logger.debug(f"episodic vector updated at memory_id - {memory_id}")







def delete_vector(memory_id: int):

    logger.info("delete func episodic vector successfully called")    

    if memory_id == None:
        print("No memory id provided to the delete episodic memeory")
        return

    ids = np.array([memory_id], dtype=np.int64)

    removed = index.remove_ids(ids)
    faiss.write_index(index, str(INDEX_PATH))

    logger.debug(f"episodic vector deleted at memory_id - {memory_id}")



def retrive_vector(query):
    """This function help is searching the similar data present in the vector db and return there respective ID."""

    #read = faiss.read_index("database/vector/episodic.index")
    logger.info("retieve episodic vector successfully called")

    query_embedding = embedding.embed_query(query)
    query_vector = np.array([query_embedding],dtype=np.float32)

    distances, ids = index.search(query_vector,k=5)

    results = []

    for memory_id, distance in zip(ids[0], distances[0]):

        # -1 means FAISS didn't find a result
        if memory_id == -1:
            continue
        if distance > 1.5: 
            continue

#         results.append(int(memory_id))
        results.append({
            "memory_id": int(memory_id),
            "distance": float(distance)
         })

    logger.debug(f"relevant vector info returned = {results}") 

    if results:
        return results

    return None


# results.append({
#             "memory_id": int(memory_id),
#             "distance": float(distance)
#         })









def handle_vector(state):
    """Here we decide which function to call according to the need."""

    logger.info("successfully called episodic vector file")


    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT MAX(memory_id) FROM episodic_memories;""")
    results = cursor.fetchone()
    previous_memory_id = results[0] if results[0] is not None else 0
    current_memory_id = previous_memory_id + 1




    memory = []
    query = ""

    memory_data = state.get("memory_nodes", {})
    memories_list = memory_data.get("memories", [])

    for operation in memories_list:

        if operation.get("memory_type") != "episodic":
            logger.info("operation not episodic type")
            continue


        action = operation.get("action")
        data = operation.get("data", {})

        query = (
            f"Event: {data.get('event', '')}. "
            f"Context: {data.get('context', '')}. "
            f"Summary: {data.get('summary', '')}. "
            f"Date: {data.get('date', '')}.")


        if action == "create":
            logger.info("action is create")
            operation["memory_id"]=create_vector(query, current_memory_id)
            logger.debug(f"create episodic vector with memory_id as - {operation["memory_id"]}")
            current_memory_id += 1                                          # Increment the ID for the next creation

        elif action == "update":
            logger.info("action is create")
            id = retrive_vector(query=query)
            if id:
                extracted_id = id[0]["memory_id"]
                update_vector(text=query, memory_id=extracted_id)
                operation["memory_id"]=extracted_id
                logger.debug(f"updated the memeory_id by episodic vector in state as - {operation["memory_id"]}")
            else:
                logger.info("no memeory_id provide to update the episodic vector")

        elif action == "delete":
            logger.info("action is delete")
            id = retrive_vector(query=query)
            if id:
                extracted_id = id[0]["memory_id"]
                delete_vector(memory_id=extracted_id)
                operation["memory_id"]=extracted_id
                logger.debug(f"Deleted episodic memory with ID: {operation['memory_id']}.")
            else:
                logger.info("no memeory_id provide to delete the episodic vector")

        else:
            logger.warning(f"{action} action is invalid for episodic vector")






    # Update the memory_data dict with the mutated list
    memory_data["memories"] = memories_list

    # Return the exact top-level key defined in MarvelState
    return {"memory_nodes": memory_data}
        
