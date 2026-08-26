import json
from pathlib import Path

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

    save_metadata()


def search(r):
    metadata = load_metadata()

    text = ""
     
    for i in r(len):
        text = text + f"reference {i}: {metadata.get(str(r[i]["memory_id"]))} \n"
            



def update(memory_id , data):
    metadata = load_metadata()
    metadata[str(memory_id)] 



def delete(memory_id):
    metadata = load_metadata()
