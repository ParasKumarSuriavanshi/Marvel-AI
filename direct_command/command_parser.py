from direct_command.command_info.rules import RULES
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger==============


def place_holder(token):
    return token.startswith("<") and token.endswith(">")


def matcher(object1):
    logger.info("Called matcher function in command_parser")
    matched = True
    for command, patterns in RULES.items():
        for pattern in patterns:
            # if len(object1) != len(pattern):
            #     continue
            arguments = {}
            matched = True
            for token,expected in zip(object1, pattern):
                if place_holder(expected):
                    arguments[expected[1:-1]] = token
                    break
                else:
                    if token != expected:
                        matched = False
            if matched:
                return {
                    "command":command,
                    "arguments": arguments
                }
    return None
                






def command_parser(state):
    """determines whether the query has an executable direct command"""
    logger.info("Successfully called command parser")
    w = state.get("direct_command")
    token = w.get("tokenized")

    input1 = w.get("normalize_input")

    
    ACTION_WORDS = [
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
        "volume"
        ]

    split = []
    o = 0
    while o < len(token):
        if token[o] in ACTION_WORDS: #or token[o] =="and":
            split.append(o)
            o += 1
        o+= 1  


    separated_commands = []

    for j in range(0,len(split)):
        try:
            separated_commands.append(token[split[j]:split[j+1]])
        except Exception:
            separated_commands.append(token[split[j]:])

    commands = []
    unmatch = []
    logger.debug(f"Commands by command parser is {separated_commands}")
    for i in separated_commands:
        result = matcher(i)

        if result is not None:
            commands.append(result)
        else:
            unmatch.append(i)
    
    logger.debug(f"commands passing to state are {commands}")
    logger.debug(f"commands Unmatched are {unmatch}")
    
    return {"direct_command":{
        "normalize_input": input1,
        "tokenized": token,
        "commands": commands,
        "unmatched_commands":unmatch
    }}

# command_parser(['open', 'netflix', 'search', 'mentalist'])