from memory.profile import handle_profile_memory
from graph.route import memory_router
from langgraph.graph import END, StateGraph
from graph import state
from memory.checkpoint import memory
from graph.state import MarvelState
from memory.manager import manager
from model.llm import llm
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

    builder = StateGraph(MarvelState)

    #builder.add_node("answer" , answer)
    builder.add_node("manager", manager)
    builder.add_node("profile", handle_profile_memory)
    # builder.add_node("semantic", semantic)
    # builder.add_node("episodic", episodic)
    # builder.add_node("short_term", short_term)

    builder.add_conditional_edges(
    "manager",memory_router,
    {
        "profile": "profile",
        "semantic": "semantic",
        "episodic": "episodic",
        "short_term": "short_term",
        "end": END,
    }
    )

    builder.set_entry_point("manager")
    builder.add_edge("profile" , END)

    #builder.set_entry_point("answer")

    #builder.add_edge("answer" , END)

    return builder.compile(checkpointer=memory)