from direct_command.command_executor import COMMAND_EXECUTOR
import asyncio
import inspect
import logging
#==========Logger==============

logger = logging.getLogger(__name__)
#==========Logger===============





def workflow_command(state):
    """It execute the command, like one at a time"""

    direct = state.get("direct_command")
    commands = direct.get("commands")
    workflow = []
    for i in commands:
        command =i.get("command")
        executor = COMMAND_EXECUTOR.get(command)
        arguments = i.get("arguments")

        

        if executor is None:
            direct["success"] = False
            direct["error"] = "No executor found"
            logger.error("No executor found for single command execution")
            return{"direct_command":direct}
        print(arguments)
        if not arguments:
            direct["success"] = False
            direct["error"] = "No argument found"
            logger.error("no argumet to run the command")
            return{"direct_command":direct}

        logger.debug(f"command to execute is {command},{arguments}")
        if inspect.iscoroutinefunction(executor):
            value = asyncio.run(executor(**arguments))
        else:
            value = executor(**arguments)
        #value = executor(**arguments)
        direct["success"] = value.get("success")
        direct["error"] = value.get("error")
        direct["web_data"] = value.get("vector_data", "No data found")
        if value.get("success") is False:
            logger.debug(f"Error after calling {executor}")
            break
    return {"direct_command":direct}