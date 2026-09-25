from langchain_core.messages import AIMessage

from graph.update_range import update_message_range_node
from memory.checkpoint import memory

from agent.user_id import user_id_extractor
from memory.manager import manager
from memory.profile import handle_profile_memory
from memory.semantic_json import handle_json
from vectorStore.semantic import handle_semantic
from memory.episodic import handle_episodic_memory
from vectorStore.episodic_vt import handle_vector
from graph.route import main_router, empty_node, direct_command_router, command_router

from langgraph.graph import END, START, StateGraph

from memory.profile import get_profile
from memory.episodic import retrieve_episodic_memory
from vectorStore.episodic_vt import retrive_vector
from vectorStore.semantic import retieve
from memory.semantic_json import searchjson
from graph.state import MarvelState
from model.llm import llm

from direct_command.normalizer import normalizer
from direct_command.command_parser import command_parser
from direct_command.workflow_command import workflow_command


import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============


def answer(marvel_state: MarvelState):
    """answer node for the Marvel AI system"""

    logger.info(f"Final response from llm func called successfully (answer), user_id = {marvel_state['user_id']}")

    last_msg = marvel_state["messages"][-1].content.lower()


    prompt = f"""You are a AI system that answers questions about any thing. You are a helpful assistant. You are given the following user input: {last_msg}. 
    Please provide a detailed and informative response to the user's query.
    Here is the conversation history between the user and the AI system:{marvel_state["messages"]}. Please provide a response that is relevant to the user's query and takes into account the context of the conversation history.
    Relevant existing memories for this user:
        Profile info for this user:
            {get_profile(user_id=marvel_state["user_id"])}
            
        Episodic memory info related to lastest user message/query:
            {retrieve_episodic_memory(date=None, user_id=marvel_state["user_id"] , vector_results=retrive_vector(marvel_state["messages"][-1].content))}
    
         Semantic memory info related to lastest user message/query:
            {searchjson(retieve(marvel_state["messages"][-1].content))}
    """

    result = llm.invoke(prompt)

    logger.info("LLM successfully created the final result.")
    
    return {"messages": [result]}


def a(state):
    logger.info("a")


    direct = state.get("direct_command")
    commands = direct.get("commands")
    print("")
    print("==========state============")
    print(state.get("direct_command"))
    print("==========state============")

   

    prompt=""
    for i in commands:
        if i.get("command") =="WEB_SEARCH":
            arguments = i.get("arguments")
            query = arguments.get("query")
            prompt = f"""User asked a query using web search, so your resposibility is to answer the query using the web data provided to you from the internet.
                        USER QUERY:
                            {query}
                        WEB DATA:
                            {direct.get("web_data")}

                        make sure to keep answer short to medium length ad concise."""
        else:
            message="Command executed"

    if prompt:
        result = llm.invoke(prompt)
        
        logger.info("LLM successfully created the final result for web search.")
            
        return {"messages": [result]}
    else:
        manual_ai_result = AIMessage(content=message)
        return {"messages": [manual_ai_result]}

            


def build():
    """create workflow graph for the Marvel AI system"""
    logger.info("Graph build frnc called successfully")
    builder = StateGraph(MarvelState)


    builder.add_node("answer", answer)
    builder.add_node("empty_node", empty_node)
    #builder.add_node("user", user_id_extractor)
    #builder.add_node("main_router", main_router)


    #------------Memory---------------------

    builder.add_node("user_id", user_id_extractor)
    builder.add_node("update", update_message_range_node)
    builder.add_node("manager", manager)
    builder.add_node("profile", handle_profile_memory)
    builder.add_node("semantic", handle_semantic)
    builder.add_node("semantic_json", handle_json)
    builder.add_node("episodic", handle_episodic_memory)
    builder.add_node("episodic_vt", handle_vector)

    builder.add_edge("manager", "semantic")
    builder.add_edge("semantic", "semantic_json")
    builder.add_edge("semantic_json", "episodic_vt")
    builder.add_edge("episodic_vt", "episodic")
    builder.add_edge("episodic", "profile")
    builder.add_edge("profile", "update")
    builder.add_edge("update", END)


    #------------Memory---------------------


    builder.add_conditional_edges("empty_node", main_router,{"manager": "manager", "answer": "answer"})
    builder.add_conditional_edges("user_id",direct_command_router,{"direct":"normalizer", "not_direct":"empty_node"})
    builder.add_conditional_edges("command_parser", command_router, {"workflow":"workflow_command", "llm":"empty_node"})


    #--------------Direct Command------------

    builder.add_node("normalizer", normalizer)
    builder.add_node("command_parser",command_parser)
    builder.add_node("workflow_command", workflow_command)
    builder.add_node("a",a)

    builder.add_edge("normalizer", "command_parser")
    builder.add_edge("workflow_command", "a")

    builder.add_edge("a",END)

    #--------------Direct Command------------



    #builder.add_edge("user_id", "manager")

    # builder.add_conditional_edges(
    # "manager",memory_router,
    # {
    #     "profile": "profile",
    #     "semantic": "semantic",
    #     "episodic_vt": "episodic_vt",
    #     "short_term": "answer",
    #     "end": "answer",
    # }
    # )



    


    #builder.set_entry_point("answer")

    builder.add_edge("answer" , END)
    builder.set_entry_point("user_id")

    return builder.compile(checkpointer=memory)