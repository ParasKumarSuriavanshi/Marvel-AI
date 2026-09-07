import json
from pathlib import Path
from graph.state import MemoryManagerOutput

METADATA_PATH = Path("database/json/semantic_metadata.json")






def load_metadata():
    with open(METADATA_PATH, "r") as f:
        return json.load(f)

def save_metadata(metadata):
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)




def create(memory_id , data):
    metadata = load_metadata()

    metadata[str(memory_id)] = {"memory_id":memory_id , **data}

    save_metadata(metadata)


def searchjson(r):
    metadata = load_metadata()

    if not r:
        return "No relevant memories found."
    text = ""
    for i, result in enumerate(r):
        # Get data from JSON using the stringified ID
        id = result["memory_id"]
        json_data = metadata.get(str(id), "No additional data found")

        distance_score = result["distance"]
        text += f"reference {i} (faiss_distance: {distance_score}): {json_data} \n"
     
    # for i in range(r(len)):
    #     text = text + f"reference {i}: {metadata.get(str(r[i]["memory_id"]))} \n"

    return text




def update(memory_id: int, new_data: dict):

    if memory_id == None:
        print("No memory id provided to the update semantic memeory json")
    metadata = load_metadata()

    memory_id = str(memory_id)

    if memory_id not in metadata:
        raise ValueError(f"Memory ID {memory_id} not found")

    metadata[memory_id].update(new_data)

    save_metadata(metadata)


def delete(memory_id: int):

    if memory_id == None:
        print("No memory id provided to the delete semantic memeory json")
    metadata = load_metadata()

    memory_id = str(memory_id)

    if memory_id not in metadata:
        raise ValueError(f"Memory ID {memory_id} not found")

    del metadata[memory_id]

    save_metadata(metadata)


def handle_json(state):
    """THis function help in handling all the CRUD operation in JSON file."""
    #i=0
    memory_data = state.get("memory_nodes", {})

    for operation in memory_data.get("memories", []):
        if operation.get("memory_type") != "semantic":
            continue
        
        # Now you can access the keys for each individual operation
        action = operation.get("action")
        data = operation.get("data", {})
        memory_id = operation.get("memory_id")

        if memory_id is None:
            print(f"Error: memory_id is required for action '{action}' but is missing in semantic json.")
            break

        if action == "create":
            create(memory_id=memory_id ,data= data)
            print("semantic create success json")
        elif action == "delete":
            delete(memory_id)
            print("semantic delete success json")
        elif action == "update":
            update(memory_id,data)
            print("semantic update success json")
        else:
            print("error in semantic json")


#i=i+1