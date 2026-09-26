from graph.state import MarvelState
from memory.semantic_json import searchjson
from model.llm import llm
from pydantic import BaseModel
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

class struct(BaseModel):
    user_id: str


    
def user_id_extractor(state:MarvelState):
    """This function decide the user ID means which user is using the assistant and store it in the state."""


    query = state["messages"][-1].content.lower()

    phareses = [
        "create a new user" ,
         "switch user to",
         "switch to",
         "switch workspace to",
         "switch to a new user",
         "use the user",
         "shift to user",
         "shift to",
         "shift workspace to",
         "shift to a new user"
         ]
    user_id = None
    for i in phareses:
        if i in query:
            try:
                senten = query.split(i)[1].strip()
                user_id1 = senten.split(" ")[0].strip()
                user_id2 = user_id1.split(",")[0].strip()
                user_id = user_id2.split(".")[0].strip()
                state["user_id"] = user_id
                #state["user_id_changed"] = True
                logger.debug(f"new user_id is taken and updated in state - {state["user_id"]}")
            except:
                logger.debug("No new user id given")
                pass
            break

    if not user_id:
        user_id0 = state.get("user_id", "paras")  # Default to "paras" if no user_id is found
        logger.debug(f"old user_id is given this time also as - {user_id0}")
        state["user_id"] = user_id0






    # #======================
    # #       LLM Based
    # #======================


    # prompt = f"""
    # Extract user_id information from the message.

    #     Message:
    #     {query}

    #     Rules:
    #     - If information is missing, return "paras".
    #     - Never return "unknown" or null.
    #     - Return only valid JSON.
    #     - User ID will be in the form of a name. 
    #     Example: 
    #         user_id = "paras"
    #         user_id = "kashif"

    #     Format:
    #     {{
    #         "user_id": "paras"
    #     }}
    #     """

    # llm_st = llm.with_structured_output(struct)
    # result = llm_st.invoke(prompt)

    # state["user_id"] = result.user_id if result.user_id else "paras"
    return state