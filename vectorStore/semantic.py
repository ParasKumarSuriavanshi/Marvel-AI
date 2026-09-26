import faiss
from pathlib import Path
from langchain_ollama import OllamaEmbeddings
import numpy as np

from graph.state import MemoryManagerOutput
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============


DIMENSION = 768


BASE_DIR = Path(__file__).resolve().parents[1]
INDEX_PATH = (BASE_DIR / "database" / "vector" / "semantic.index")

embedding_model = OllamaEmbeddings(model = "nomic-embed-text")

#Load existing index or create a new one
if INDEX_PATH.exists():
    index = faiss.read_index(str(INDEX_PATH))
    logger.info(f"index for semantic vector file - {index}")
else:
    #logger.warning("sematic vector file doesn't exist")
    base_index = faiss.IndexFlatL2(DIMENSION)
    index = faiss.IndexIDMap2(base_index)
    logger.info(f"created index for semantic vector file - {index}")




#=================================
#           JSON
#=================================

import json
from pathlib import Path

METADATA_PATH = Path("database/json/semantic_metadata.json")

def load_metadata():
    try:
        with open(METADATA_PATH, "r") as f:
            return json.load(f)
    except:
        logger.exception("No file found for semantic json ")

def generate_memory_id(metadata: dict) -> int:
    if not metadata:
        logger.info(f"semantic json is empty so return memory_id - 0")
        return 0
    logger.info(f"semantic json is not empty so return memory_id - {max(map(int, metadata.keys())) + 1}")
    return max(map(int, metadata.keys())) + 1

#=================================
#           JSON
#=================================





def create_add(data: str , memory_id: int):
    """This function help in creating or adding a new info into the vector db."""

    # metadata = load_metadata()
    # memory_id = generate_memory_id(metadata=metadata)
    logger.info("create semantic vector successfully called")

    vector = embedding_model.embed_query(data)
    vector = np.array([vector],dtype=np.float32)

    ids = np.array([memory_id],dtype=np.int64)

    index.add_with_ids(vector , ids)

    INDEX_PATH.parent.mkdir(parents=True,exist_ok=True)
    
    # Save index
    faiss.write_index(index,str(INDEX_PATH))
    logger.debug(f"return memory_id as - {memory_id}")
    return memory_id





def update(data: str , memory_id: int):
    """This function helps in updateing the vector db info. Based on the Faiss ID provided in it."""

    logger.info("update semantic vector successfully called")

    if memory_id == None:
        logger.debug("No memory id provided to the update semantic memeory")
        return
    new_vector = embedding_model.embed_query(data)

        # Convert to NumPy array
    new_vector = np.array([new_vector],dtype=np.float32)

        # Remove old vector
    index.remove_ids(np.array([memory_id],dtype=np.int64))

        # Add new vector with same ID
    index.add_with_ids(new_vector,np.array([memory_id],dtype=np.int64))



    # Save updated index
    faiss.write_index(index,str(INDEX_PATH))
    logger.debug(f"semantic vector updated at memory_id - {memory_id}")





def search(data: str):
    """This function helps in searching the vector db based on the query."""


    query_embedding = embedding_model.embed_query(data)
    query_vector = np.array([query_embedding],dtype=np.float32)

    distances, ids = index.search(query_vector,k=5)

    results = []

    for memory_id, distance in zip(ids[0], distances[0]):

        # -1 means FAISS didn't find a result
        if memory_id == -1:
            continue
        if distance > 1.5: 
            continue

        # results.append({
        #     "memory_id": int(memory_id),
        #     "distance": float(distance)
        # })
        results.append(int(memory_id))


    # Safely return the first item if it exists, otherwise return None
        if results:
    
            return results[0]
        
        return None
    



def retieve(data: str):
    """This function helps in searching the vector db based on the query."""

    logger.info("retieve semantic vector successfully called")

    query_embedding = embedding_model.embed_query(data)
    query_vector = np.array([query_embedding],dtype=np.float32)

    distances, ids = index.search(query_vector,k=5)

    results = []

    for memory_id, distance in zip(ids[0], distances[0]):

        # -1 means FAISS didn't find a result
        if memory_id == -1:
            continue
        if distance > 1.5: 
            continue

        # results.append({
        #     "memory_id": int(memory_id),
        #     "distance": float(distance)
        # })
        results.append({
                    "memory_id": int(memory_id),
                    "distance": float(distance)
                 })

    logger.debug(f"relevant vector info returned = {results}") 
    
    if results:
        return results
                
    return None





def delete(memory_id: int):
    """This function helps in deleting the data from vector db based on the memory ID."""

    logger.info("delete func semantic vector successfully called")    

    if memory_id == None:
        print("No memory id provided to the delete semantic memeory")
        return

    ids = np.array([memory_id], dtype=np.int64)

    removed = index.remove_ids(ids)
    faiss.write_index(index, str(INDEX_PATH))

    logger.debug(f"semantic vector deleted at memory_id - {memory_id}")




def handle_semantic(state):
    """This function decide which CRUD operation to be carried out based on the input taken from the state."""

    logger.info("successfully called semantic vector file")

    query = ""
    current_id = generate_memory_id(load_metadata())
    memory_data = state.get("memory_nodes", {})
    memories_list = memory_data.get("memories", [])



    
    for operation in memories_list:

        if operation.get("memory_type") != "semantic":
            logger.info("operation not semantic type")
            continue
            
        action = operation.get("action")
        data = operation.get("data", {})


        query = (
            f"subject: {data.get('subject', '')}. "
            f"predicate: {data.get('predicate', '')}. "
            f"object: {data.get('object', '')}. "
            f"content: {data.get('content', '')}.")


        if action == "create":
            logger.info("action is create")
            operation["memory_id"] = create_add(query, current_id)

            logger.debug(f"Created semantic memory vector with ID: {operation['memory_id']}.")
            current_id += 1                                          # Increment the ID for the next creation

        elif action == "update":
            logger.info("action is update")
            id = retieve(query)
            if id:
                extract_id = id[0]["memory_id"]
                update(query , extract_id)
                operation["memory_id"] = extract_id
                logger.debug(f"Updated semantic memory with ID: {operation['memory_id']}.")
            else:
                logger.debug("No id found in semantic vt")

        elif action == "delete":
            logger.info("action is delete")
            id = retieve(query)
            if id:
                extract_id = id[0]["memory_id"]
                delete(extract_id)
                operation["memory_id"] = extract_id
                logger.debug(f"Deleted semantic memory with ID: {operation['memory_id']}.")
            else:
                logger.debug("No id found in semantic vt")

        else:
            logger.warning(f"Unknown action: {action} for semantic memory operation vt.")





    # Update the memory_data dict with the mutated list
    memory_data["memories"] = memories_list
    
        # Return the exact top-level key defined in MarvelState
    return {"memory_nodes": memory_data}