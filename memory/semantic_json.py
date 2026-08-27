import json
from pathlib import Path
from graph.state import MemoryManagerOutput

METADATA_PATH = Path("database/vector/json/semantic_metadata.json")






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

    text = ""
    for i, mem_id in enumerate(r):
        # Get data from JSON using the stringified ID
        json_data = metadata.get(str(mem_id), "No additional data found")
        
        text += f"reference {i}: {json_data} \n"
     
    # for i in range(r(len)):
    #     text = text + f"reference {i}: {metadata.get(str(r[i]["memory_id"]))} \n"

    return text




def update(memory_id: int, new_data: dict):
    metadata = load_metadata()

    memory_id = str(memory_id)

    if memory_id not in metadata:
        raise ValueError(f"Memory ID {memory_id} not found")

    metadata[memory_id].update(new_data)

    save_metadata(metadata)


def delete(memory_id: int):
    metadata = load_metadata()

    memory_id = str(memory_id)

    if memory_id not in metadata:
        raise ValueError(f"Memory ID {memory_id} not found")

    del metadata[memory_id]

    save_metadata(metadata)


def handle_json(state):
    """THis function help in handling all the CRUD operation in JSON file."""
    i=0
    for operation in state.get("memories", []):
        
        # Now you can access the keys for each individual operation
        action = operation.get("action")
        data = operation.get("data", {})
        memory_id = operation.get("memory_id",[])[i]

        if action == "create":
            create(memory_id=memory_id ,data= data)
            print("semantic create success")
        elif action == "delete":
            delete(memory_id)
            print("semantic delete success")
        elif action == "update":
            update(memory_id,data)
            print("semantic update success")
        else:
            print("error in semantic json")


        i=i+1