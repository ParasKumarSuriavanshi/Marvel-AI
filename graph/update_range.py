def update_message_range_node(state):
    """Micro-node to instantly update the message range."""
    messages_len = len(state.get("messages", []))
    return {"message_range": messages_len}