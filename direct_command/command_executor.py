from direct_command.command_info.application import APPLICATIONS
import subprocess
import logging
#==========Logger==============

logger = logging.getLogger(__name__)
#==========Logger===============







def open_application(application):
    """It opens the application which is specified."""
    logger.info("Successfully called open_applicatio.")

    app = APPLICATIONS.get(application)
    if not app:
        logger.error(f"No such application found in registry to open - {application}")
        return {"success": False, "error": "No such application found in the registry"}

    subprocess.Popen(app,stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL)
    logger.info(f"Successfully opened {application}")
    return{"success": True, "error": ""}


def close_application(application):
    """It close the application which is specified."""
    logger.info("Successfully called close_applicatio.")

    app = APPLICATIONS.get(application)
    if not app:
        logger.error(f"No such application found in registry to close- {application}")
        return {"success": False, "error": "No such application found in the registry"}

    subprocess.call(["pkill", "-f", app],stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL)

    logger.info(f"Successfully closed {application}")
    return{"success": True, "error": ""}







    

def set_volume(level):
    """It set the volume which is specified."""
    logger.info("Successfully called set_volume.")

    volume = (max(0,min(100,int(level))))/100
    command = ["wpctl","set-volume", "@DEFAULT_AUDIO_SINK@", f"{volume}"]

    subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    logger.info(f"Successfully set the volume to level - {level}")
    return{"success": True, "error": ""}

def increase_volume(level):
    """It increase the volume by level which is specified."""
    logger.info("Successfully called increase_volume.")

    volume = (max(0,min(100,int(level))))
    command = ["wpctl","set-volume", "@DEFAULT_AUDIO_SINK@", f"{volume}%+"]

    subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    logger.info(f"Successfully increased the volume by level - {level}")
    return{"success": True, "error": ""}

def decrease_volume(level):
    """It decrease the volume by level which is specified."""
    logger.info("Successfully called decrease_volume.")

    volume = (max(0,min(100,int(level))))
    command = ["wpctl","set-volume", "@DEFAULT_AUDIO_SINK@", f"{volume}%-"]

    subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    logger.info(f"Successfully decreased the volume by level - {level}")
    return{"success": True, "error": ""}









COMMAND_EXECUTOR = {
    "OPEN_APPLICATION":open_application,
    "CLOSE_APPLICATION":close_application,
    "SET_VOLUME":set_volume,
    "DECREASE_VOLUME":decrease_volume,
    "INCREASE_VOLUME":increase_volume,
    # "SET_BRIGHTNESS":set_brightness,
    # "DECREASE_BRIGHTNESS":decrease_brightness,
    # "INCREASE_BRIGHTNESS":increase_brightness,
    # "WEB_SEARCH":web_search
}
