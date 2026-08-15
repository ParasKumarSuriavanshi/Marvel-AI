from typing import Literal

from graph.state import MemoryManagerOutput


def memory_router(state: MemoryManagerOutput) -> Literal[
    "profile",
    "semantic",
    "episodic",
    "short_term",
    "end"
]:
    """
    Decide which memory node should receive the memory-manager output.
    """

    memory_required = state.get("memory_required", False)
    if memory_required:
        memory_type = state.get("memory_type")
        if memory_type == "profile":
            return "profile"
        elif memory_type == "semantic":
            return "semantic"
        elif memory_type == "episodic":
            return "episodic"
        elif memory_type == "short_term":
            return "short_term"
    else:
        return "end"