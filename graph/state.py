from dataclasses import Field
from typing import Annotated, Optional, Any
from typing_extensions import TypedDict
from langgraph.graph.message import Literal, add_messages
from langchain_core.messages import AnyMessage
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

def reducer_memory_nodes(left :MemoryManagerOutput, right: MemoryManagerOutput) -> "MemoryManagerOutput":
    """Reducer function to safely merge memory_nodes from parallel branches."""
    if not left:
        return right
    if not right:
        return left
    
    merged_memories = []
    left_mems = left.get("memories", [])
    right_mems = right.get("memories", [])
    
    # Merge lists item by item
    for i in range(max(len(left_mems), len(right_mems))):
        l_mem = left_mems[i] if i < len(left_mems) else {}
        r_mem = right_mems[i] if i < len(right_mems) else {}
        
        # Combine the dictionaries. Both parallel node updates are preserved.
        merged_memories.append({**l_mem, **r_mem})
        
    return {
        "memory_required": right.get("memory_required", left.get("memory_required")),
        "memories": merged_memories
    }

logger.debug("State file called")


#===========Memory============

class MemoryData(TypedDict, total=False):
    # PROFILE
    category: str
    field: str
    value: str  #Any

    # SEMANTIC
    subject: str
    predicate: str
    object: Any
    content: str

    # EPISODIC
    event: str
    date: str
    context: str
    summary: str
    importance: float

    # SHORT TERM
    key: str
    ttl: int


class MemoryOperation(TypedDict):
    memory_type: Literal[
        "profile",
        "semantic",
        "episodic",
        "short_term"
    ]

    action: Literal[
        "create",
        "update",
        "append",
        "remove",
        "delete",
        "clear",
        "retrieve"
    ]

    confidence: float
    source: Literal[
        "user_explicit",
        "user_stated",
        "conversation_inferred"
    ]

    data: MemoryData
    reason: str
    memory_id:Optional[int]
    user_id: str


class MemoryManagerOutput(TypedDict):
    memory_required: bool
    memories: list[MemoryOperation]


#===========Memory============


#===========Direct Commands============


#class Direct_commands(TypedDict):
    

#===========Direct Commands============



class MarvelState(TypedDict):
    message_range:int
    user_id: str
    messages: Annotated[list[AnyMessage], add_messages]
    final_response: Optional[str]
    memory_nodes: MemoryManagerOutput #Annotated[MemoryManagerOutput, reducer_memory_nodes]
    #direct_command: Direct_commands



