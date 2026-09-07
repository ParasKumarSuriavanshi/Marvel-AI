
from typing import TypedDict, Literal, Any, Optional
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
    user_id: Optional[str]


class MemoryManagerOutput(TypedDict):
    memory_required: bool
    memories: list[MemoryOperation]

