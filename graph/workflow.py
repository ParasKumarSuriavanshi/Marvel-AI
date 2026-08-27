from graph import state
from graph.state import MemoryManagerOutput
from memory.checkpoint import memory

from memory.manager import manager
from memory.profile import handle_profile_memory
from memory.semantic_json import handle_json
from vectorStore.semantic import handle_semantic
from memory.episodic import handle_episodic_memory
from vectorStore.episodic_vt import handle_vector
from graph.route import memory_router

from langgraph.graph import END, StateGraph
from langchain_core.messages import AIMessage, HumanMessage



# def answer(marvel_state: MarvelState):
#     """answer node for the Marvel AI system"""
#     last_msg = marvel_state["messages"][-1].content.lower()
#     prompt = f"""You are a AI system that answers questions about any thing. You are a helpful assistant. You are given the following user input: {last_msg}. 
#     Please provide a detailed and informative response to the user's query.
#     Here is the conversation history between the user and the AI system:{marvel_state["messages"]}. Please provide a response that is relevant to the user's query and takes into account the context of the conversation history."""
#     result = llm.invoke(prompt)
#     #print(result)
#     return {"messages": [result]}

def build():
    """create workflow graph for the Marvel AI system"""

    builder = StateGraph(MemoryManagerOutput)

    builder.add_node("manager", manager)
    builder.add_node("profile", handle_profile_memory)
    builder.add_node("semantic", handle_semantic)
    builder.add_node("semantic_json", handle_json)
    builder.add_node("episodic", handle_episodic_memory)
    builder.add_node("episodic_vt", handle_vector)

    builder.add_conditional_edges(
    "manager",memory_router,
    {
        "profile": "profile",
        "semantic": "semantic",
        "episodic": "episodic",
        "episodic_vt": "episodic_vt",
        "short_term": "short_term",
        "end": END,
    }
    )
    builder.add_edge("profile", END)
    builder.add_edge("episodic_vt", "episodic")
    builder.add_edge("episodic", END)
    builder.add_edge("semantic", "semantic_json")
    builder.add_edge("semantic_json", END)
    
    builder.set_entry_point("manager")
    

    #builder.set_entry_point("answer")

    #builder.add_edge("answer" , END)

    return builder.compile(checkpointer=memory)