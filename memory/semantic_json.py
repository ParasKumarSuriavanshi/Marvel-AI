import json
from pathlib import Path
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

METADATA_PATH = Path("database/json/semantic_metadata.json")






def load_metadata():
    try:
        with open(METADATA_PATH, "r") as f:
            return json.load(f)
    except:
        logger.exception("No file found for semantic json ")

def save_metadata(metadata):
    try:
        with open(METADATA_PATH, "w") as f:
            json.dump(metadata, f, indent=4)
    except:
        logger.exception("Cannot update the json file for semantic memory")




def create(memory_id , user_id, data):

    logger.info(f"create semantic json successfully called. memory_id - {memory_id},user_id - {user_id}")
    metadata = load_metadata()
    logger.debug("metadat for semantic json loaded successfully")

    metadata[str(memory_id)] = {"memory_id":memory_id ,"user_id":user_id, **data}

    save_metadata(metadata)


def searchjson(r):
    metadata = load_metadata()

    if not r:
        logger.warning("No relevant memories found in semantic json.")
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
    logger.info(f"json retrieved memoery is - {text}")
    return text




def update(memory_id: int, new_data: dict):

    if memory_id == None:
        logger.warning("No memory id provided to the update semantic memeory json")
    metadata = load_metadata()
    logger.debug("metadat for semantic json loaded successfully")

    memory_id = str(memory_id)

    if memory_id not in metadata:
        logger.warning("could not find the same memory_id to update in semantic json")
        raise ValueError(f"Memory ID {memory_id} not found")

    metadata[memory_id].update(new_data)
    
    save_metadata(metadata)


def delete(memory_id: int):

    if memory_id == None:
        logger.warning("No memory id provided to the delete semantic memeory json")
    metadata = load_metadata()

    logger.debug("metadat for semantic json loaded successfully")

    memory_id = str(memory_id)

    if memory_id not in metadata:
        logger.warning("could not find the same memory_id to delete in semantic json")
        raise ValueError(f"Memory ID {memory_id} not found")

    del metadata[memory_id]

    save_metadata(metadata)


def handle_json(state):
    """THis function help in handling all the CRUD operation in JSON file."""

    logger.info("successfully called semantic json file")
    #i=0
    memory_data = state.get("memory_nodes", {})

    for operation in memory_data.get("memories", []):
        if operation.get("memory_type") != "semantic":
            logger.info("operation not semantic type")
            continue
        
        # Now you can access the keys for each individual operation
        action = operation.get("action")
        data = operation.get("data", {})
        memory_id = operation.get("memory_id")
        user_id = operation.get("user_id")

        if memory_id is None:
            logger.warning(f"Error: memory_id is required for action '{action}' but is missing in semantic json.")
            break
        if not user_id:
            logger.warning(f"No user_id for semantic json in the state. user_id - {user_id}")
            break

        if action == "create":
            logger.info("action is create")
            create(memory_id=memory_id , user_id=user_id, data= data)
            logger.debug("semantic create success json")
        elif action == "delete":
            logger.info("action is delete")
            delete(memory_id)
            logger.debug("semantic delete success json")
        elif action == "update":
            logger.info("action is update")
            update(memory_id,data)
            logger.debug("semantic update success json")
        else:
            logger.warning(f"Unknown action: {action} for semantic memory operation json.")


#i=i+1