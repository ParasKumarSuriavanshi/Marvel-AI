import asyncio
from langchain.tools import tool
from langgraph.types import interrupt
import time
import logging
import subprocess
from direct_command.command_info.application import APPLICATIONS
from web.brower_controller import web_search
from direct_command.command_executor import open_tab,close_tab,is_valid_url
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

#return{"success":True,"error":""}
@tool
def open_application(application:str):
    """Call it to open any application specified by the user.
    - only give name of application.
    - no url or anythig other than name"""
    logger.info("Successfully called open_applicatio.")

    app = APPLICATIONS.get(application.lower())
    if not app:
        logger.error(f"No such application found in registry to open - {application}")
        return {"tool":"open_application","tool_used":True,"execution_success":False,"error":"no such app in registry"}

    if is_valid_url(app):
        a = open_tab(app)
        logger.info(f"{application} opend - {a}")
        return {"tool":"open_application","tool_used":True,"execution_success":a["success"],"error":a["error"]}
    else:
        subprocess.run(['hyprctl', 'dispatch', 'workspace', 'empty'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1) 
        subprocess.Popen(app,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        logger.info(f"Successfully opened {application}")
    return{"tool":"open_application","tool_used":True,"execution_success":True,"error":""}

@tool
def close_application(application:str):
    """Call it to close close any application that user specify.
    - only give name of application.
    - no url or anythig other than name"""
    logger.info("Successfully called close_applicatio.")
    
    app = APPLICATIONS.get(application.lower())
    if not app:
        logger.error(f"No such application found in registry to close- {application}")
        return {"tool":"close_application","tool_used":True,"execution_success":False,"error":"no such app in registry"}

    if is_valid_url(app):
        a= close_tab(app)
        return {"tool":"close_application","tool_used":True,"execution_success":a["success"],"error":a["error"]}
        

    else:
        subprocess.call(["pkill", "-f", app],stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL)

        logger.info(f"Successfully closed {application}")
    return{"tool":"close_application","tool_used":True,"execution_success":True,"error":""}









    
@tool
def set_volume(level:int):
    """Call it to set the volume at the level specified by the user."""
    logger.info("Successfully called set_volume.")
    try:
        volume = (max(0,min(100,int(level))))/100
        command = ["wpctl","set-volume", "@DEFAULT_AUDIO_SINK@", f"{volume}"]

        subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        logger.info(f"Successfully set the volume to level - {level}")
        return{"tool":"set_volume","tool_used":True,"execution_success":True,"error":""}
    except:
        logger.warning("Error in set_volume")
        return{"tool":"set_volume","tool_used":True,"execution_success":False,"error":"Unable to set volumn"}

@tool
def increase_volume(level:int):
    """Call it if user says to increase the volume by a certain amount."""
    logger.info("Successfully called increase_volume.")
    try:
        volume = (max(0,min(100,int(level))))
        command = ["wpctl","set-volume", "@DEFAULT_AUDIO_SINK@", f"{volume}%+"]

        subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        logger.info(f"Successfully increased the volume by level - {level}")
        return{"tool":"increase_volume","tool_used":True,"execution_success":True,"error":""}
    except:
        logger.warning("Error in inc_volume")
        return{"tool":"increase_volume","tool_used":True,"execution_success":False,"error":"Unable to increase volumn"}

@tool
def decrease_volume(level:int):
    """Call it if user says to decrease the volume by a certain amount."""
    logger.info("Successfully called decrease_volume.")
    try:
        volume = (max(0,min(100,int(level))))
        # device = get_active_sink_id()
        # print(device)
        command = ["wpctl","set-volume", "@DEFAULT_AUDIO_SINK@", f"{volume}%-"]

        subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        logger.info(f"Successfully decreased the volume by level - {level}")
        return{"tool":"decrease_volume","tool_used":True,"execution_success":True,"error":""}
    except:
        logger.warning("Error in decrease_volume")
        return{"tool":"decrease_volume","tool_used":True,"execution_success":False,"error":"Unable to decrease volumn"}

@tool
def mute_or_unmute():
    """Call it when user says to mute or to unmute."""

    subprocess.run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"], check=True)

    return{"tool":"mute_or_unmute","tool_used":True,"execution_success":True,"error":""}






@tool
def set_brightness(level:int):
    """Call it when user says to set the brightness to a certain level specified by the user."""
    logger.info("Successfully called set_brightness.")
    try:
        brightness = (max(5,min(100,int(level))))
        command = ["brightnessctl","-q", "set", f"{brightness}%"]

        subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        logger.info(f"Successfully set the bightness to level - {level}")
        return{"tool":"set_brightness","tool_used":True,"execution_success":True,"error":""}
    except:
        logger.warning("Error in set_brightness")
        return{"tool":"set_brightness","tool_used":True,"execution_success":False,"error":"Unable to set brightness"}

@tool
def increase_brightness(level:int):
    """Call it if user says to increase the brightness by a certain amount."""
    logger.info("Successfully called increase_brightness.")
    try:
        brightness = (max(5,min(100,int(level))))
        command = ["brightnessctl","-q", "set", f"+{brightness}%"]

        subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        logger.info(f"Successfully increased the brightness by level - {level}")
        return{"tool":"increase_brightness","tool_used":True,"execution_success":True,"error":""}
    except:
        logger.warning("Error in increase_brightness")
        return{"tool":"increase_brightness","tool_used":True,"execution_success":False,"error":"Unable to increase brightnness"}

@tool
def decrease_brightness(level:int):
    """Call it if user says to decrease the brightness by a certain amount."""
    logger.info("Successfully called decrease_brightness.")
    try:
        brightness = (max(5,min(100,int(level))))
        command = ["brightnessctl","-q", "set", f"{brightness}%-"]

        subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        logger.info(f"Successfully decreased the brightness by level - {level}")
        return{"tool":"decrease_brightness","tool_used":True,"execution_success":True,"error":""}
    except:
        logger.warning("Error in decrease_brightnes")
        return{"tool":"decrease_brightness","tool_used":True,"execution_success":False,"error":"Unable to decrease brightness"}







@tool
def web_searching(query):
    """Searches the internet for real-time information.
    -if want to search a website give full url 
    EXAMPLE 
    https://www.xyz.com
    
    MUST be called immediately without asking permission for:
    - Current events, breaking news, or anything happening in recent days/hours.
    - Weather, live data, or real-time tracking.
    - Explicit user requests to search the web.
    
    Do NOT use this tool for general knowledge, coding, math, historical facts, or casual conversation.
    """
    a =asyncio.run(web_search(query))

    return{"tool":"web_searching","tool_used":True,"execution_success":a["success"],"error":a["error"],"web_data":a["vector_data"]}






@tool
def human_interruption(question:str):
    """Call this tool whenever you need to confirm an action with the user or ask them a clarifying question.
    ALWAYS use this tool if you have any doubt about the action you want to take.
    ALWAYS use this tool if you have any doubt about the user query and make sure to ask in that case.
    Do NOT use this tool for web searches, general knowledge, coding, or math.
    - Also keep the question concise and to the point, as the user will see it in a pop-up window.
    - ALWAYS ask even if u have the slightest doubt about the user query or action to be taken."""
   

    logger.info("Successfully called human_interruption.")


    user_response = interrupt(question)

    return{"tool":"human_interruption","tool_used":True,"execution_success":True,"error":"","user_response_to_question":user_response}


tools =[
    open_application,
    close_application,
    set_volume,
    increase_volume,
    decrease_volume,
    mute_or_unmute,
    set_brightness,
    increase_brightness,
    decrease_brightness,
    web_searching,
    human_interruption
]

