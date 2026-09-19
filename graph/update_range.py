import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

def update_message_range_node(state):
    """Micro-node to instantly update the message range."""

    logger.debug("message range starting point value updation is called.")

    messages_len = len(state.get("messages", []))

    logger.debug(f"new mesasge range starting value is - {messages_len}")
    
    return {"message_range": messages_len}