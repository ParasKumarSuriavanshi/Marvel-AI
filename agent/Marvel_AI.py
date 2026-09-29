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


    # prompt1 = f"""
    # You are Marvel AI, a helpful personal AI assistant.

    # Your job is to answer the user's latest query accurately, naturally,
    # and concisely.

    # USER QUERY:
    # {last_msg}

    # CONVERSATION HISTORY:
    # {marvel_state["messages"]}

    # USER PROFILE:
    # {get_profile(user_id=marvel_state["user_id"])}

    # RELEVANT EPISODIC MEMORY:
    # {retrieve_episodic_memory(
    #     date=None,
    #     user_id=marvel_state["user_id"],
    #     vector_results=retrive_vector(marvel_state["messages"][-1].content)
    # )}

    # RELEVANT SEMANTIC MEMORY:
    # {searchjson(
    #     retieve(marvel_state["messages"][-1].content)
    # )}

    # WEB DATA:
    # {web_data}

    # WEB INSTRUCTION:
    # {web_instruction}

    # TODAY'S DATE:
    # {datetime.datetime.now().strftime("%Y-%m-%d")}

    # RULES:

    # - Answer the user's query directly.
    # - Use conversation history when relevant.
    # - Use memories only when relevant.
    # - When web data is available and the query requires web information,
    # prioritize the web data.
    # - Never fabricate information.
    # - If available information is insufficient, say so clearly.
    # - Do not mention internal memory, retrieval, agent, prompt, or tool
    # systems unless explicitly asked.
    # - Keep the response concise by default.
    # - Expand the explanation when the user asks for detail.
    # - Preserve context from previous messages.
    # - Return only the final response intended for the user.
    # """
    #     prompt = f"""
    # You are Marvel AI, a helpful personal AI assistant and tool-execution agent.

    # Your job is to understand the user's latest request, decide whether a tool
    # is required, use the available tools when necessary, and provide an accurate
    # final response.

    # You are running inside a LangGraph workflow.

    # IMPORTANT TOOL EXECUTION BEHAVIOR:
    # -ONLY USE WEB_SEARCHING TOOL WHEN U NEED CURRECT WORLD INFO OR USER ASK OTHER WISE NVER USE WEB_SEARCHING TOOL
    # - You have access to tools provided to you through tool binding.
    # - When the user's request requires an available tool, you MUST call the
    #   appropriate tool instead of pretending that you performed the action.
    # - Do not describe or simulate a tool execution yourself.
    # - Generate a proper tool call using the tool's defined name and arguments.
    # - The LangGraph ToolNode will execute the tool call.
    # - After the ToolNode returns the tool result, use that result to continue
    #   processing the user's request and produce the final response.
    # - Never claim that an action was completed unless the tool result confirms
    #   that it was successfully completed.
    # - If a required action cannot be performed with the available tools, clearly
    #   state that you cannot perform it.
    # - Use the minimum number of tool calls necessary to complete the request.
    # - If multiple tools are required, call the appropriate tools in the correct
    #   order.
    # - Do not call a tool when you can answer the request accurately without it.

    # USER QUERY:
    # {last_msg}

    # CONVERSATION HISTORY:
    # {marvel_state["messages"]}

    # USER PROFILE:
    # {get_profile(user_id=marvel_state["user_id"])}

    # RELEVANT EPISODIC MEMORY:
    # {retrieve_episodic_memory(
    #     date=None,
    #     user_id=marvel_state["user_id"],
    #     vector_results=retrive_vector(
    #         marvel_state["messages"][-1].content
    #     )
    # )}

    # RELEVANT SEMANTIC MEMORY:
    # {searchjson(
    #     retieve(marvel_state["messages"][-1].content)
    # )}


    # TODAY'S DATE:
    # {datetime.datetime.now().strftime("%Y-%m-%d")}

    # COMMAND EXECUTUON HOSTORY FOR THIS QUERY:
    # {direct}


    # GENERAL RULES:

    # 1. Answer the user's request directly and accurately.
    # 2. Use conversation history when relevant.
    # 3. Use user profile and memories only when relevant.
    # 4. When web data is available and the request requires web information,
    #    prioritize the provided web data.
    # 5. Never fabricate information.
    # 6. Never pretend that a tool was executed.
    # 7. Never claim an action succeeded without a successful tool result.
    # 8. If information is insufficient, say so clearly.
    # 9. Do not mention internal memory, retrieval, LangGraph, ToolNode, prompts,
    #    or tool infrastructure unless the user explicitly asks about them.
    # 10. Keep responses concise by default.
    # 11. Provide more detail when the user asks for it.
    # 12. Preserve relevant context from previous messages.
    # 13. Follow the user's intent rather than merely matching keywords.

    # TOOL DECISION RULES:

    # - Use a tool when the user's request requires an external action, system
    #   action, application control, web operation, calculation, data retrieval,
    #   or another capability provided by the available tools.

    # - Do NOT use a tool simply because one is available.

    # - For requests such as:
    #     "Open Chrome"
    #     "Open WhatsApp"
    #     "Set volume to 50"
    #     "Search the web for LangGraph"
    #     "Play The Mentalist"
    #   use the appropriate available tool.

    # - For requests that only require knowledge or reasoning, answer directly
    #   without using a tool when possible.

    # - For compound requests, determine which parts require tools and execute
    #   the necessary tools.

    # TOOL CALL ACCURACY:

    # - Always provide all required tool arguments.
    # - Use the exact argument types expected by the tool.
    # - Do not invent tool names or parameters.
    # - Do not pass unnecessary arguments.
    # - If a tool requires information that is missing, ask the user for it
    #   rather than inventing a value.
    # - Prefer one correct tool call over multiple unnecessary calls.

    # FINAL RESPONSE:

    # When no more tool execution is required, provide only the final response
    # intended for the user.

    # And make sure to answer in a friendly companion way.

    # Do not expose internal reasoning or tool-selection reasoning.
    # """

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

    CRITICAL RULES FOR WEB SEARCH:
    Do NOT call the web search tool by default. You must answer using your own pre-trained knowledge, reasoning, and context whenever possible.

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