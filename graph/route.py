from typing import Literal
from langgraph.types import Command
import logging
#==========Logger==============


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(filename)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("log_info.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

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
        logger.debug("condtional router return ONLY 'answer'")
        return "answer"