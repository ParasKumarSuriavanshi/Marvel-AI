from urllib import response
import datetime 
from langchain_core.prompts import PromptTemplate
from langgraph import graph
from typer import prompt
from model.llm import llm
from graph.fake_state import MemoryManagerOutput
from graph.state import MarvelState
from langchain_core.messages import AnyMessage

from memory.profile import get_profile
from memory.episodic import retrieve_episodic_memory
from vectorStore.episodic_vt import retrive_vector
from vectorStore.semantic import retieve
from memory.semantic_json import searchjson


def manager(MARVEL_STATE):
    """This function manages the overall memory related classification. It decides whether the current messages should
    be stored in memory or not, if yes it decides whether it should be stored in short term, long term, working, semantic or episodic memory. 
    It also decides whether the current messages should be used to update the user profile or not. 
    It also decides whether the current messages should be used to update the user preferences or not.
    """

    # user_id = MemoryNotes["user_id"]
    # last_message = MARVEL_STATE["messages"][-1]["content"]
    # current_user_info = MARVEL_STATE["user_info"]
    # #relevant_existing_memories = MARVEL_STATE["memory_notes"]


    range = MARVEL_STATE.get("message_range", 0)

    human_msg = "\n".join(
    f"Human message {i}: {msg.content}" 
    for i, msg in enumerate(MARVEL_STATE["messages"][range:], start=1) 
    if msg.type == "human")

    print("============conversation=============")
    print(human_msg)
    print("============conversation=============")

    episodic_memory_info = "\n".join(
    f"Episodic memory info {i}: {retrieve_episodic_memory(date=None, user_id=MARVEL_STATE["user_id"] , vector_results=retrive_vector(msg.content))}"
    for i, msg in enumerate(MARVEL_STATE["messages"][range:], start=1) 
    if msg.type == "human")

    semantic_memory_info = "\n".join(
    f"Semantic memory info {i}: {searchjson(retieve(msg.content))}"
    for i, msg in enumerate(MARVEL_STATE["messages"][range:], start=1) 
    if msg.type == "human")






    memory_manager_prompt = f"""
        You are Marvel AI's Memory Manager.

        Your task is ONLY to analyze the conversation and decide whether
        information should be stored, updated, or deleted.

        You have EXACTLY THREE memory types:

        1. PROFILE
        2. EPISODIC
        3. SEMANTIC

        Never use any other memory type.

        ==================================================
        MEMORY TYPES
        ==================================================

        PROFILE:
        Stable information ABOUT THE USER.

        Examples:
        - name
        - education
        - occupation
        - preferences
        - long-term goals
        - hobbies
        - skills
        - persistent habits
        - stable personal information

        Examples:
        "My name is Paras." -> PROFILE
        "I prefer Python over Java." -> PROFILE


        EPISODIC:
        Important PAST EVENTS, EXPERIENCES, ACTIONS, DECISIONS,
        ACHIEVEMENTS, or MILESTONES.

        Think:
        "What happened?"

        Examples:
        "I completed my project yesterday." -> EPISODIC
        "I fixed the Ollama problem today." -> EPISODIC
        "I decided to use Qwen3 8B." -> EPISODIC


        SEMANTIC:
        Durable FACTS, KNOWLEDGE, PROJECT INFORMATION,
        TECHNICAL INFORMATION, or RELATIONSHIPS.

        Think:
        "What is known or true?"

        Examples:
        "Marvel uses Ollama." -> SEMANTIC
        "HELIOS uses SDO/AIA 193 Å images." -> SEMANTIC
        "The project uses FAISS." -> SEMANTIC


        ==================================================
        EXPLICIT MEMORY REQUESTS
        ==================================================

        If the user explicitly asks to:

        - remember
        - save
        - store
        - keep in memory
        - don't forget
        - add to memory
        - update memory
        - forget
        - remove from memory
        - delete memory

        YOU MUST perform the requested memory operation.

        Never ignore an explicit memory request.

        Determine whether the requested information belongs to
        PROFILE, EPISODIC, or SEMANTIC.

        ==================================================
        MEMORY REQUIRED
        ==================================================

        Set memory_required = true when at least one memory operation
        is required.

        Set memory_required = false when no memory operation is required.

        Normal questions and normal conversation do NOT require memory.

        Example:
        "What is Python?" -> false

        "Remember that I prefer Python." -> true


        ==================================================
        CRUD OPERATIONS
        ==================================================

        CREATE:
        Use when new information does not already exist.

        UPDATE:
        Use when an existing memory has changed.

        DELETE:
        Use when the user explicitly asks to forget/remove information
        or explicitly invalidates an existing memory.

        For UPDATE and DELETE, use the existing memory_id.

        Never invent a memory_id.


        ==================================================
        DUPLICATE PREVENTION
        ==================================================

        Before CREATE, check existing memories.

        If an equivalent memory already exists:

        - Do NOT create a duplicate.
        - If the information is unchanged, no operation is required.
        - If the information changes the existing memory, use UPDATE.

        Example:

        Existing:
        preferred_language = Java

        User:
        "I now prefer Python."

        Correct:
        UPDATE the existing PROFILE memory.

        Incorrect:
        CREATE another preference.


        ==================================================
        MEMORY TYPE DECISION
        ==================================================

        Use this decision order:

        1. Stable information ABOUT USER
        -> PROFILE

        2. Important EVENT / EXPERIENCE / DECISION / ACHIEVEMENT
        -> EPISODIC

        3. Durable FACT / KNOWLEDGE / PROJECT / TECHNICAL INFORMATION
        -> SEMANTIC

        4. Everything else
        -> NO MEMORY


        ==================================================
        DO NOT OVER-MEMORIZE
        ==================================================

        Do NOT store:

        - greetings
        - small talk
        - ordinary questions
        - ordinary answers
        - temporary statements
        - repeated information
        - trivial information
        - conversation filler
        - information with no future usefulness

        Memory should contain useful information, not a transcript.


        ==================================================
        NEVER INVENT INFORMATION
        ==================================================

        Only use information explicitly supported by the conversation.

        Never:

        - guess
        - hallucinate
        - assume unsupported facts
        - invent user preferences
        - invent events
        - invent project information
        - invent memory IDs
        - modify the user_id


        ==================================================
        USER ID
        ==================================================

        The application provides the user_id.

        Use the provided user_id exactly.

        Never generate or modify the user_id.


        ==================================================
        MULTIPLE OPERATIONS
        ==================================================

        A single message may require multiple operations.

        Example:

        "Remember my name is Paras and remember that I fixed Ollama yesterday."

        Result:

        PROFILE CREATE
        +
        EPISODIC CREATE


        ==================================================
        IMPORTANT DISTINCTION
        ==================================================

        PROFILE = Who the user is / what is stable about the user.

        EPISODIC = What happened.

        SEMANTIC = What is known / true.

        Use the category that best matches the information.

        ============================================================
        CURRENT INPUT
        ============================================================

        Current user ID:

        {MARVEL_STATE["user_id"]}

        Current conversation history:

        {human_msg}

    

        Relevant existing memories for this user:

            Profile info for this user:
                {get_profile(user_id=MARVEL_STATE["user_id"])}
        
            Episodic memory info related to lastest user message/query:
                - {episodic_memory_info}

            Semantic memory info related to lastest user message/query:
                - {semantic_memory_info}

        Today's date:

        {datetime.datetime.now().strftime("%Y-%m-%d")}

        If the user explicitly provides a different date, use the user's date.
        ==================================================
        OUTPUT
        ==================================================

        Analyze the conversation history and return a JSON object.
            -Make multiple memory operations if required.


        The application uses structured output.

        Return ONLY the schema-compatible structured response.

        Do NOT return:

        - explanations
        - reasoning
        - markdown
        - comments
        - additional fields
        - JSON code fences

        If no memory is required:

        memory_required = false
        memories = []

        If memory is required:

        memory_required = true
        memories = [required operations]

        Follow the provided schema EXACTLY.
        
        You are the MEMORY MANAGER.

        You are NOT Marvel's conversational assistant.

        Your entire job is:

        CONVERSATION
            ↓
        ANALYZE
            ↓
        IDENTIFY MEMORY-WORTHY INFORMATION
            ↓
        CLASSIFY MEMORY TYPE
            ↓
        SELECT ACTION
            ↓
        STRUCTURE DATA
            ↓
        VALIDATE SCHEMA
            ↓
        RETURN JSON

        Return ONLY the JSON object.
        """

    # Latest user message or query:
    
    #         {MARVEL_STATE["messages"][-1].content}




#     response = {
#     "memory_required": True,
#     "memories": [
#         {
#             "user_id": "paras",
#             "memory_type": "profile",
#             "action": "delete",
#             "confidence": 0.99,
#             "source": "user_explicit",
#             "data": {
#                 "category": "technical",
#                 "field": "operating_system",
#                 "value": "Arch Linux"
#             },
#             "reason": "User explicitly stated their operating system preference."
#         },
#         {
#             "user_id": "paras",
#             "memory_type": "profile",
#             "action": "delete",
#             "confidence": 0.95,
#             "source": "user_stated",
#             "data": {
#                 "category": "preferences",
#                 "field": "response_style",
#                 "value": "concise"
#             },
#             "reason": "User requested concise and short answers."
#         }
#     ]
# }



#     response = {
#     "memory_required": True,
#     "memories": [
#         {
#             "user_id": "paras",
#             "memory_type": "profile",
#             "action": "delete",
#             "confidence": 0.99,
#             "source": "user_explicit",
#             "data": {
#                 "category": "technical",
#                 "field": "operating_system",
#                 "value": "ubuntu Linux"
#             },
#             "reason": "User explicitly stated their operating system."
#         }
#     ]
# }



    # response = {
    # "memory_required": False,
    # "memories": []
    # }

    structured_response = llm.with_structured_output(MemoryManagerOutput)
    response = structured_response.invoke(memory_manager_prompt)
    print("============manager=============")
    print(response)
    print("============manager=============")


    

    return {"memory_nodes": response}#sjdshd