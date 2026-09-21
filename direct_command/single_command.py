from direct_command.command_executor import COMMAND_EXECUTOR
import logging
#==========Logger==============

logger = logging.getLogger(__name__)
#==========Logger===============





def single_command(state):
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
            direct["error"] = "No exector found"
            logger.error("No executor found for single command execution")
            return{"direct_command":direct}
        print(arguments)
        if not arguments:
            direct["success"] = False
            direct["error"] = "No argument found"
            logger.error("no argumet to run the command")
            return{"direct_command":direct}

        logger.debug(f"command to execute is {command},{arguments}")

        value = executor(**arguments)
        direct["success"] = value.get("success")
        direct["error"] = value.get("error")
        return {"direct_command":direct}