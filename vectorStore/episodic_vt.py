import faiss
import numpy as np

from pathlib import Path
from langchain_ollama.embeddings import OllamaEmbeddings

from graph.state import MemoryManagerOutput , MemoryOperation


DIMENSION = 768

BASE_DIR = Path(__file__).resolve().parents[1]

INDEX_PATH = (BASE_DIR/ "database"/ "vector"/ "episodic.index")

embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Load existing index or create a new one
if INDEX_PATH.exists():
    index = faiss.read_index(str(INDEX_PATH))
else:
    base_index = faiss.IndexFlatL2(DIMENSION)
    index = faiss.IndexIDMap2(base_index)









def create_vector(
    memor: MemoryOperation,
    memory_id: int
):
    """Create and add an episodic memory vector."""

    data = memor["data"]
        
        # Convert memory data into text
    text = (
        f"Event: {data.get('event', '')}. "
        f"Context: {data.get('context', '')}. "
        f"Summary: {data.get('summary', '')}. "
        f"Date: {data.get('date', '')}.")
        

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









def update_vector(memor: MemoryOperation ,memory_id: int):
    """Update an existing episodic memory vector."""


    data = memor["data"]

        # Convert memory data into text
    text = (
        f"Event: {data.get('event', '')}. "
        f"Context: {data.get('context', '')}. "
        f"Summary: {data.get('summary', '')}. "
        f"Date: {data.get('date', '')}.")

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







def delete_vector(memory_id: int):
    ids = np.array([memory_id], dtype=np.int64)

    removed = index.remove_ids(ids)
    faiss.write_index(index, str(INDEX_PATH))

    return removed



def retrive_vector(query):
    """This function help is searching the similar data present in the vector db and return there respective ID."""

    #read = faiss.read_index("database/vector/episodic.index")

    query_embedding = embedding.embed_query(query)
    query_vector = np.array([query_embedding],dtype=np.float32)

    distances, ids = index.search(query_vector,k=5)

    results = []

    for memory_id, distance in zip(ids[0], distances[0]):

        # -1 means FAISS didn't find a result
        if memory_id == -1:
            continue

        results.append(int(memory_id))

    return results



# results.append({
#             "memory_id": int(memory_id),
#             "distance": float(distance)
#         })








def search_vector(query):
    """This function help is searching the similar data present in the vector db and return there respective ID so that it can be used in finding the info in sql memory."""

    #read = faiss.read_index("database/vector/episodic.index")

    query_embedding = embedding.embed_query(query)
    query_vector = np.array([query_embedding],dtype=np.float32)

    distances, ids = index.search(query_vector,k=1)

    results = []
    
    for memory_id, distance in zip(ids[0], distances[0]):

            # -1 means FAISS didn't find a result
        if memory_id == -1:
            continue
    
        results.append(int(memory_id))
    
    return results




def handle_vector(memor: MemoryOperation, memory_id):
    """Here we decide which function to call according to the need."""

    query = ""
    action = memor['action']
    data = memor["data"]

    query = (
        f"{data.get('event', '')} "
        f"{data.get('context', '')} "
        f"{data.get('summary', '')}"
    )

    if action == "create":
        create_vector(memor=memor,memory_id=memory_id)
    elif action == "update":
        id = search_vector(query=query)
        update_vector(memor=memor,memory_id=memory_id)
        return id
    elif action == " delete":
        id = search_vector(query=query)
        delete_vector(memory_id=memory_id)
        return id
    elif action == "retrieve":
        retrive_vector(query=query)
    else:
        retrive_vector(query=query)
    1
