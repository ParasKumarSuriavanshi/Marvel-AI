from dataclasses import Field
from typing import Annotated, Optional, Any
from typing_extensions import TypedDict
from langgraph.graph.message import Literal, add_messages
from langchain_core.messages import AnyMessage

# class MemoryNotes(TypedDict):
#     memory_id: str
#     user_id: str
#     memory_type: Literal["working" , "Short-term" , "profile" , "episodic" , "semantic"]
#     action: str
#     data: dict[str, Any]
#     confidence: float
#     created_at: str
#     updated_at: str




class MarvelState(TypedDict):
    user_id: str
    messages: Annotated[list[AnyMessage], add_messages]
    memory_notes: dict[str, Any]
    final_response: Optional[str]
    memory_nodes: MemoryManagerOutput





from typing import TypedDict, Literal, Any


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
    memory_id:Optional[list[int]]
    user_id: str


class MemoryManagerOutput(TypedDict):
    memory_required: bool
    memories: list[MemoryOperation]



class episodic_memory(TypedDict):
    action: Literal["create" , "update" , "delete" , "retrieve"]
    confidence: float
    importance: float
    source: Literal["user_explicit" , "user_stated" , "conversation_inferred"]
    data: MemoryData
    reason: str