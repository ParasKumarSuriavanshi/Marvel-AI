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
from graph.route import main_router, empty_node, direct_command_router, command_router,reset_loop_state_node, llm_needed_or_not, simple_respose

from langgraph.graph import END, START, StateGraph

from agent.Marvel_AI import Marvel_ai
from graph.state import MarvelState
from model.llm import llm

from direct_command.normalizer import normalizer
from direct_command.command_parser import command_parser
from direct_command.workflow_command import workflow_command

import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============



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


    builder.add_node("Marvel_ai", Marvel_ai)
    builder.add_node("empty_node", empty_node)
    builder.add_node("direct_command_overwrite",reset_loop_state_node)
    builder.add_node("simple_response",simple_respose)
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


    builder.add_conditional_edges("empty_node", main_router,{"manager": "manager", "answer": "Marvel_ai"})
    builder.add_conditional_edges("user_id",direct_command_router,{"direct":"normalizer", "not_direct":"empty_node"})
    builder.add_conditional_edges("command_parser", command_router, {"workflow":"workflow_command", "llm":"empty_node"})
    builder.add_conditional_edges("workflow_command",llm_needed_or_not, {"llm_needed":"Marvel_ai","not_needed":"simple_response"})


    #--------------Direct Command------------

    builder.add_node("normalizer", normalizer)
    builder.add_node("command_parser",command_parser)
    builder.add_node("workflow_command", workflow_command)

    builder.add_edge("normalizer", "command_parser")

    #--------------Direct Command------------

    builder.add_edge("Marvel_ai" , "direct_command_overwrite")
    builder.add_edge("simple_response", "direct_command_overwrite")
    builder.add_edge("direct_command_overwrite", END)


    builder.set_entry_point("user_id")

    return builder.compile(checkpointer=memory)