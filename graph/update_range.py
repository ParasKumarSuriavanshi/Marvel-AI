import logging
#==========Logger==============


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(filename)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("log_info.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

#==========Logger===============

def update_message_range_node(state):
    """Micro-node to instantly update the message range."""

    logger.debug("message range starting point value updation is called.")

    messages_len = len(state.get("messages", []))

    logger.debug(f"new mesasge range starting value is - {messages_len}")
    
    return {"message_range": messages_len}