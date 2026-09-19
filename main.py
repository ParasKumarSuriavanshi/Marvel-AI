
from langchain_core.messages import HumanMessage
from graph.workflow import build
import logging


#==========Logger==============
def setup_global_logger():
    # Get the ROOT logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s:%(name)s:%(filename)s:%(funcName)s:%(levelname)s:%(message)s")

    file_handler = logging.FileHandler("log_info.log")
    file_handler.setFormatter(formatter)

    # Add the handler only if it doesn't already have one (prevents duplicates)
    if not logger.handlers:
        logger.addHandler(file_handler)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

#==========Logger===============

a = build()

value = None

def user_id(query):
    global value
    b= None
    phareses = [
        "create a new user" ,
         "switch user to",
         "switch to",
         "switch workspace to",
         "switch to a new user",
         "use the user",
         "shift to user",
         "shift to",
         "shift workspace to",
         "shift to a new user"
         ]
    for i in phareses:
        if i in query:
            try:
                senten = query.split(i)[1].strip()
                user_id1 = senten.split(" ")[0].strip()
                user_id2 = user_id1.split(",")[0].strip()
                user_id = user_id2.split(".")[0].strip()
                b = user_id
                #state["user_id_changed"] = True
                logger.debug(f"new user_id is taken as - {b}")
            except:
                logger.debug("No new user id given")
                pass
            break    

    
    if value is None:
        if b is None:
            value = "paras"
        else:
            value = b
    else:
        if b is not None:
            value = b
        else:
            value = value

    logger.debug(f"user_id to config_main is - {value}")
    return value


setup_global_logger()
logger = logging.getLogger(__name__)

while True:
    user_input = input("User1: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    
    config = {
    "configurable": {
        "thread_id": f"{user_id(user_input.lower())}"
        }
    }
    
    result = a.invoke(
        {
            "messages": [HumanMessage(content=user_input)]
        },
        config=config
    )
    print(result.get("messages")[-1].content)



for message in result.get("messages", []):
    # This will print something like "human: how are you" or "ai: I'm doing well!"
    print("-" * 20) # Adds a separator line between messages
    print(f"{message.type}: {message.content}\n")
    print("-" * 20) # Adds a separator line between messages

logger.info("Successfully Exited code with Convo history display.")

