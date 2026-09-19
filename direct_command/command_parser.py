


def command_parser(state):
    """determines whether the query has an executable direct command"""
    logger.info("Successfully called command parser")

    NON_COMMAND_PATTERNS = [
    "how do i",
    "how to",
    "explain how to",
    "what is",
    "what does",
    "why does",
    "can you explain",
    "tell me how"]


    COMMAND_STARTERS = [
    "open",
    "launch",
    "start",
    "close",
    "quit",
    "exit",
    "play",
    "search",
    "find",
    "set",
    "increase",
    "decrease",
    "turn"]


    