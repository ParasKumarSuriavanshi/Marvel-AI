import faiss
from pathlib import Path
from langchain_ollama import OllamaEmbeddings
import numpy as np

from graph.state import MemoryData , MemoryOperation


DIMENSION = 768


BASE_DIR = Path(__file__).resolve().parents[1]
INDEX_PATH = (BASE_DIR / "database" / "vector" / "semantic.index")

embedding_model = OllamaEmbeddings(model = "nomic-embed-text")

#Load existing index or create a new one
if INDEX_PATH.exists():
    index = faiss.read_index(str(INDEX_PATH))
else:
    base_index = faiss.IndexFlatL2(DIMENSION)
    index = faiss.IndexIDMap2(base_index)




#=================================
#           JSON
#=================================

import json
from pathlib import Path

METADATA_PATH = Path("database/vector/json/semantic_metadata.json")

def load_metadata():
    with open(METADATA_PATH, "r") as f:
        return json.load(f)

def generate_memory_id(metadata: dict) -> int:
    if not metadata:
        return 0

    return max(map(int, metadata.keys())) + 1

#=================================
#           JSON
#=================================





def create_add(data: str , ):
    """This function help in creating or adding a new info into the vector db."""

    metadata = load_metadata()
    memory_id = generate_memory_id(metadata=metadata)

    vector = embedding_model.embed_query(data)
    vector = np.array([vector],dtype=np.float32)

    ids = np.array([memory_id],dtype=np.int64)

    index.add_with_ids(vector , ids)

    INDEX_PATH.parent.mkdir(parents=True,exist_ok=True)
    
    # Save index
    faiss.write_index(index,str(INDEX_PATH))





def update(data: str , memory_id: int):
    """This function helps in updateing the vector db info. Based on the Faiss ID provided in it."""


    new_vector = embedding_model.embed_query(data)

        # Convert to NumPy array
    new_vector = np.array([new_vector],dtype=np.float32)

        # Remove old vector
    index.remove_ids(np.array([memory_id],dtype=np.int64))

        # Add new vector with same ID
    index.add_with_ids(new_vector,np.array([memory_id],dtype=np.int64))



    # Save updated index
    faiss.write_index(index,str(INDEX_PATH))





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

        results.append({
            "memory_id": int(memory_id),
            "distance": float(distance)
        })


    return results





def delete(memory_id: int):
    """This function helps in deleting the data from vector db based on the memory ID."""


    ids = np.array([memory_id], dtype=np.int64)

    removed = index.remove_ids(ids)
    faiss.write_index(index, str(INDEX_PATH))

    return removed




def handle_semantic(memory: MemoryData , ope: MemoryOperation):
    """This function decide which CRUD operation to be carried out based on the input taken from the state."""


    data = memory["content"]
    action = ope["action"]

    if action == "create":
        create_add(data)
    elif action == "update":
        id = search(data)
        update(data , id["memory_id"])
    elif action == "retrieve":
        search(data)
    elif action == "delete":
        id = search(data)
        update(data , id["memory_id"])