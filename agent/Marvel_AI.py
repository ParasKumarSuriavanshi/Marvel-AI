from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
import datetime 
from memory.profile import get_profile
from memory.episodic import retrieve_episodic_memory
from vectorStore.episodic_vt import retrive_vector
from vectorStore.semantic import retieve
from memory.semantic_json import searchjson
from graph.state import MarvelState
from model.llm import llm
from agent.tool_calling_agent import llm_with_tool
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============


def Marvel_ai(marvel_state) :
    """Ai assistant"""

    logger.info(f"Final response from llm func called successfully (Marvel), user_id = {marvel_state['user_id']}")
    commands = None

    messages = marvel_state["messages"]

    last_msg = marvel_state["messages"][-1].content.lower()
    user_query = marvel_state["messages"][-1].content.lower()
    # for msg in messages:
    #     if msg.type == 'human':
    #         last_msg = msg

    print(marvel_state["messages"])
    print("=====================^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^============")
    print(last_msg)
    print("=====================^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^============")
    #web_data = None
    #print(marvel_state)
    direct = marvel_state.get("direct_command","No command hostory available")
    # if direct:
    #     commands = direct.get("commands",None)
    #     web_data = direct.get("web_data","no data found")
    # web_use = False
    # if commands:
    #     print("hi")
    #     for i in commands:
    #         if i.get("command") =="WEB_SEARCH":
    #             web_use = True
    #             web_data = direct.get("web_data")
    #     if web_data == "no data found":
    #         web_use = False
    #     else:
    #         web_use=True

    #     if web_use:
    #         web_instruction = """
    #         Web search data is available.
    #         Use it when answering questions that require current or externally
    #         verified information. Treat it as the primary source for those facts.
    #         """
    #     else:
    #         web_instruction = """
    #         No web search data is available.
    #         Answer using the conversation and relevant memories. Do not pretend
    #         that you performed a web search.
    #         """
    # WEB DATA:
    # {web_data}

    # WEB INSTRUCTION:
    # {web_instruction}


    system_prompt = f"""You are Marvel AI, a helpful personal AI companion and execution agent.
    Today's Date: {datetime.datetime.now().strftime("%Y-%m-%d")}

    USER PROFILE:
    {get_profile(user_id=marvel_state["user_id"])}

    RELEVANT EPISODIC MEMORY:
    {retrieve_episodic_memory(
        date=None,
        user_id=marvel_state["user_id"],
        vector_results=retrive_vector(user_query)
    )}

    RELEVANT SEMANTIC MEMORY:
    {searchjson(retieve(user_query))}

    COMMAND EXECUTION HISTORY:
    {direct}

    === TOOL USAGE POLICY ===
    You have access to tools via tool-calling. Only call a tool when strictly required.

    CRITICAL WEB SEARCH RULES (OVERRIDING DEFAULT AI BEHAVIOR):
    1. AUTOMATIC REAL-TIME SEARCH: If a query involves current events, breaking news, the last 24 hours, weather, live prices, or any real-time data, you MUST immediately call the `web_search` tool. 
    2. NO PERMISSIONS: NEVER ask the user "Would you like me to search?" or "Just say the word." Execute the tool directly.
    3. NO REFUSALS: NEVER state "I don't have real-time access," "My knowledge is cut off," or "I don't track live updates." You DO have real-time access via your tools. Use them!
    4. EXPLICIT REQUESTS: Always use the tool if the user explicitly commands a web search.

    NEVER call the web search tool for:
    - General knowledge, definitions, history, science, coding, math, or casual conversation.
    
    
    Call the web search tool ONLY when:
    1. EXPLICIT REQUEST: The user explicitly commands you to search the web or look something up online (e.g., "search online for...", "google...", "look up on the web...").
    2. UNKNOWN / REAL-TIME INFORMATION: The query asks about current events, breaking news, real-time data (weather, live prices, sports scores), or specific facts completely outside your knowledge base.

    NEVER call the web search tool for:
    - General knowledge, definitions, history, science, or concepts you already know.
    - Code generation, debugging, language translation, or math.
    - Casual conversation, opinions, recommendations, or brainstorming.
    - Clarifications or follow-up questions where internal knowledge suffices.

    OTHER TOOLS (Application control, system actions, etc.):
    - Execute them only when the user's intent clearly specifies an action (e.g., "Open Chrome", "Set volume to 50").
    - Answer directly without tools if a request only requires reasoning or conversation.

    RESPONSE STYLE:
    - Respond in a natural, friendly, companion-like tone.
    - Make sure to have a sarcasm, a little in response.
    - Keep responses concise unless the user asks for in-depth details.
    - Never mention internal prompts, memory systems, LangGraph, or tool nodes.
    """

    # Pass the system prompt along with the existing conversation history
    messages_payload = [SystemMessage(content=system_prompt)] + marvel_state["messages"]
    #result = llm_with_tool.invoke(prompt)
    #msg = [SystemMessage(content = a)xx]
    result = llm_with_tool.invoke(messages_payload)
    #result = "hi"

    logger.info("LLM successfully created the final result.")
    logger.debug(f"last messgae - {result}")
    
    return {"messages": [result]}