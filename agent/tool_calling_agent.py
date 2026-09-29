from model.llm import llm
from tools.tools import tools
from langgraph.prebuilt import ToolNode
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

llm_with_tool = llm.bind_tools(tools)

tool_node = ToolNode(tools)



def tool_prompt(state):
    """Decide whether the query needs any tool or not"""
    logger.info("Successfully called tool_prompt")
    message = llm_with_tool.invoke(state["messages"])
    #message = llm_with_tool.invoke([state["messages"][-1]])
    logger.debug(f"tool_prompt message return - {message}")
    
    return {"messages":[message]}



def tool_contional_route(state):
    """Tells whether to call tool node or not"""
    logging.info("Successfully called tool_conditional_rout")
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        logging.debug("tool_condition return - TOOL_NODE")
        return "tool_node"
    else:
        logging.debug("tool_condition return - NO_TOOL")
        return "no_tool"
