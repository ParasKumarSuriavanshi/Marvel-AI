from graph.state import MarvelState
from model.llm import llm
from pydantic import BaseModel

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
                user_id = senten.split(" ")[0].strip()
                state["user_id"] = user_id
            except:
                pass
            break

    if not user_id:
        user_id = "paras"
        state["user_id"] = user_id






    #======================
    #       LLM Based
    #======================


    prompt = f"""
    Extract user_id information from the message.

        Message:
        {query}

        Rules:
        - If information is missing, return "paras".
        - Never return "unknown" or null.
        - Return only valid JSON.
        - User ID will be in the form of a name. 
        Example: 
            user_id = "paras"
            user_id = "jashan"

        Format:
        {{
            "user_id": "paras"
        }}
        """

    llm_st = llm.with_structured_output(struct)
    result = llm_st.invoke(prompt)

    state["user_id"] = result.user_id

    return state