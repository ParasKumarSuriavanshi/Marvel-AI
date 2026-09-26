from typing import Literal
import re
import logging

from langchain_core.messages import AIMessage
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

def main_router(state) -> Literal["manager", "answer"]:
    """
    Decide whether to route to the memory manager or directly to the answer node.
    Returns a single string for routing.
    """

    logger.info("conditional router func called successfully")
    
    range = state.get("message_range", 0)

    logger.debug(f"condition router starting range is - {range}")
    if len(state.get("messages")) - range >= 9:
        logger.debug("condition router returns - 'manger' , 'answer'")
        return ["manager", "answer"]
    else:
        logger.debug("cond`tional router return ONLY 'answer'")
        return "answer"




def direct_command_router(state):
    """normalize text for easy detection of direct command."""
    logger.info("successfully called direct command router")

    pattern = "volume [\\w|\\d]+|open [\\w]+|launch [\\w]+"
    text = state["messages"][-1].content
    if not text:
        return "not_direct"

    ACTION_WORDS = {
    "open",
    "launch",
    "start",
    "close",
    "stop",
    "increase",
    "decrease",
    "set",
    "turn",
    "play",
    "pause",
    "search",
    "volume"}

    NON_COMMAND_PATTERNS = [
        "how do i",
        "how to",
        "explain",
        "what is",
        "what does",
        "why does",
        "how",

        "tell me how"]


    if "search" not in text:
        for i in NON_COMMAND_PATTERNS:
            if i in text:
                logger.debug(f"direct commant router response - NOT DIRECT")
                return "not_direct"
    else:
        logger.debug(f"direct commant router response - DIRECT")
        return "direct"
    
    for i in ACTION_WORDS:
        if i in text:
            logger.debug(f"direct commant router response - DIRECT")
            return "direct"
    logger.debug(f"direct commant router response - NOT DIRECT")
    return "not_direct"
    


def command_router(state):
    """This decide wether the task is single ec=xecution, workflow or need llm to complete"""

    logger.info("Successfully called the command_router funct")

    direct = state.get("direct_command")
    command = direct.get("commands")
    unmatched = direct.get("unmatched_commands")
    if unmatched:
        logger.debug("command_parser respose is - LLM")
        return "llm"
    elif len(command) >= 1:
        logger.debug("commad_router respose is - WORKFLOW")
        return "workflow"
    
    else:
        logger.debug("commad_router respose is - LLM")
        return "llm"




def llm_needed_or_not(state):
    """THis decide whether the direct command has web search to use llm or not"""

    direct = state.get("direct_command")
    commands = direct.get("commands")
    if commands:
        for i in commands:
            if i.get("command") =="WEB_SEARCH":
                logger.debug("llm_needed or not response - LLM_NEEDED")
                return "llm_needed"
        logger.debug("llm_needed or not response - NOT_NEEDED")
        return "not_needed"
    logger.debug("llm_needed or not response - LLM_NEEDED")
    return "llm_needed"
























def simple_respose(state):
    """It will give direct simple respose foe cammand execution without llm"""
    logger.debug("simple response called no llm use")
    message = "Command Executed"
    direct = state.get("direct_command")
    error=direct.get("error")
    if error:
        message="Unable to execute the command"
    manual_ai_result = AIMessage(content=message)
    return {"messages": [manual_ai_result]}



def empty_node(state):
    logger.info("Successfully called empty node")
    return state
def get_empty_direct_command() :
    return {
        "normalize_input": "",
        "tokenized": [],
        "commands": [],
        "unmatched_commands": [],
        "success": False,
        "error": "",
        "web_data": []
    }
def reset_loop_state_node(state):
    logger.info("Successfully called loop_reset")
    # Overwrites the old dictionary with a fresh, empty one
    return {"direct_command": get_empty_direct_command()}