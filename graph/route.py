from typing import Literal

from graph.state import MemoryManagerOutput


def memory_router(state):
    """
    Decide which memory node(s) should receive the memory-manager output.
    Returns a single string or a list of strings for parallel routing.
    """
    memory_data = state.get("memory_nodes", {})
    memory_required = memory_data.get("memory_required", False)

    # If no memory is required, skip straight to the end/answer
    if not memory_required:
        return "end"

    # Use a set to avoid duplicate routes (e.g., if there are 2 profile memories)
    destinations = set()

    for operation in memory_data.get("memories", []):
        memory_type = operation.get("memory_type")
        #action = operation.get("action")
        
        if memory_type == "profile":
            destinations.add("profile")
        elif memory_type == "semantic":
            destinations.add("semantic")
        elif memory_type == "episodic":
            destinations.add("episodic_vt")
        elif memory_type == "short_term":
            destinations.add("short_term")

    # If the loop finished but we found no valid destinations, go to end
    if not destinations:
        return "end"

    # Convert the set to a list so LangGraph can route to all of them in parallel!
    return list(destinations)