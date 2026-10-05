from agent.tts_maker import tts_stop
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command
import requests
from voice import speak, wake
from graph.workflow import build
from rich import print
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
require_wake=True
while True:
    # if require_wake:
    #     wake()
    #     require_wake = False
    # text = speak()







    print(("====================================="))
    #print(text)
    user_input = input("You: ")#text.lower()
    tts_stop()
    print(("====================================="))    


    # if user_input == "bye" or user_input == "thats it" or user_input == "that's it" or user_input == "okay":
    #     require_wake = True
    #     continue
    if not user_input or user_input.isspace():
        logger.debug("No speech detected or understood. Restarting loop.")
        require_wake=True
        continue

    if user_input.lower() in ["exit", "quit"]:
        break

    
    config = {
    "configurable": {
        "thread_id": f"{user_id(user_input.lower())}"
        }
    }
    user_query = input("You: ") 
    
    result = a.invoke(
        {
            "messages": [HumanMessage(content=user_input)]
        },
        config=config
    )



    state = a.get_state(config)
    while state.next:

        if state.tasks[0] and state.tasks[0].interrupts:
            question_from_ai = state.tasks[0].interrupts[0].value
            print(f"AI asks: {question_from_ai}")
            

            try:
                requests.post("http://127.0.0.1:8000/tts", json={"text": question_from_ai}, timeout=10)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error occurred while sending text to TTS service: {e}")
                pass

            user_input = input("Your answer: ")
            tts_stop()


            
            result = a.invoke(
                Command(resume=user_input),
                config=config
            )
            state = a.get_state(config)
        else:
            break
    print(result.get("messages")[-1].content)



for message in result.get("messages", []):
    # This will print something like "human: how are you" or "ai: I'm doing well!"
    print(f"{message.type}: {message.content}\n")
    print("-" * 20) # Adds a separator line between messages

logger.info("Successfully Exited code with Convo history display.")

