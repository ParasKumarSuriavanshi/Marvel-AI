from langchain_core.prompts import PromptTemplate
import datetime 
from memory.profile import get_profile
from memory.episodic import retrieve_episodic_memory
from vectorStore.episodic_vt import retrive_vector
from vectorStore.semantic import retieve
from memory.semantic_json import searchjson
from graph.state import MarvelState
from model.llm import llm
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============


def Marvel_ai(marvel_state) :
    """Ai assistant"""

    logger.info(f"Final response from llm func called successfully (Marvel), user_id = {marvel_state['user_id']}")

    last_msg = marvel_state["messages"][-1].content.lower()
    direct = marvel_state.get("direct_command")
    commands = direct.get("commands")
    web_data = None
    web_use = False
    if commands:
        print("hi")
        for i in commands:
            if i.get("command") =="WEB_SEARCH":
                web_use = True
                web_data = direct.get("web_data")

    if web_use:
        web_instruction = """
        Web search data is available.
        Use it when answering questions that require current or externally
        verified information. Treat it as the primary source for those facts.
        """
    else:
        web_instruction = """
        No web search data is available.
        Answer using the conversation and relevant memories. Do not pretend
        that you performed a web search.
        """


    prompt = f"""
    You are Marvel AI, a helpful personal AI assistant.

    Your job is to answer the user's latest query accurately, naturally,
    and concisely.

    USER QUERY:
    {last_msg}

    CONVERSATION HISTORY:
    {marvel_state["messages"]}

    USER PROFILE:
    {get_profile(user_id=marvel_state["user_id"])}

    RELEVANT EPISODIC MEMORY:
    {retrieve_episodic_memory(
        date=None,
        user_id=marvel_state["user_id"],
        vector_results=retrive_vector(marvel_state["messages"][-1].content)
    )}

    RELEVANT SEMANTIC MEMORY:
    {searchjson(
        retieve(marvel_state["messages"][-1].content)
    )}

    WEB DATA:
    {web_data}

    WEB INSTRUCTION:
    {web_instruction}

    TODAY'S DATE:
    {datetime.datetime.now().strftime("%Y-%m-%d")}

    RULES:

    - Answer the user's query directly.
    - Use conversation history when relevant.
    - Use memories only when relevant.
    - When web data is available and the query requires web information,
    prioritize the web data.
    - Never fabricate information.
    - If available information is insufficient, say so clearly.
    - Do not mention internal memory, retrieval, agent, prompt, or tool
    systems unless explicitly asked.
    - Keep the response concise by default.
    - Expand the explanation when the user asks for detail.
    - Preserve context from previous messages.
    - Return only the final response intended for the user.
    """

    result = llm.invoke(prompt)

    logger.info("LLM successfully created the final result.")
    
    return {"messages": [result]}