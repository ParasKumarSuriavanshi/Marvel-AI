from urllib.parse import urlparse
from direct_command.command_info.application import APPLICATIONS
from web.brower_controller import web_search
import subprocess
from pynput.keyboard import Key, Controller
import time
import logging
from playwright.sync_api import sync_playwright
#==========Logger==============

logger = logging.getLogger(__name__)
#==========Logger===============




def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        # A valid URL must have a scheme (http/https) and a domain (netloc)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def close_tab(url):
    """It search for the the url and closes that particular tab"""
    logger.info("called close_tab")

    playwright = sync_playwright().start()
    try:
        browser =playwright.chromium.connect_over_cdp("http://localhost:9222")

        context = browser.contexts[0]

        for p in context.pages:
            if url in p.url :
                page = p
                break

        page.close()
        playwright.stop()
        return{"success":True,"error":""}
    except:
        logger.warning("Didnt found tab to close")
        playwright.stop()
        return{"success":False,"error":"Didn't found the webpage to close"}
    playwright.stop()


def open_tab(query):
    """It open a tab"""
    logger.info("called open_tab")
    playwright = sync_playwright().start()
    result = subprocess.run(['pgrep', '-i', 'chromium'], capture_output=True)
    running = (result.returncode == 0)


    if not running:
        logger.debug("New chrome window is opened")
        subprocess.run(['hyprctl', 'dispatch', 'workspace', 'empty'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen("chromium",stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2) 
    browser =playwright.chromium.connect_over_cdp("http://localhost:9222")

    context = browser.contexts[0]

    page = None
    context = browser.contexts[0]
    exist = False
    for p in context.pages:
        if query in p.url :
            page = p
            exist = True
            page.bring_to_front()
            subprocess.run(["hyprctl", "dispatch", "focuswindow", "class:chromium"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            playwright.stop()
            return{"success":True,"error":""}
            break
        elif "about:blank" in p.url or 'chrome://new-tab-page/' in p.url or "chrome-extension://hipekcciheckooncpjeljhnekcoolahp/index.html" in p.url:
            page = p
            break
    if not exist:
        if not page:
            page = context.new_page()
        try:
            page.goto(query, wait_until='load')
            subprocess.run(["hyprctl", "dispatch", "focuswindow", "class:chromium"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            playwright.stop()
            return{"success":True,"error":""}
        except:
            logger.warning("Error in opeing the website")
            playwright.stop()
            return{"success":False,"error":"unable to open the webpage"}
    
    

    playwright.stop()




def open_application(application):
    """It opens the application which is specified."""
    logger.info("Successfully called open_applicatio.")

    app = APPLICATIONS.get(application)
    if not app:
        logger.error(f"No such application found in registry to open - {application}")
        return {"success": False, "error": "No such application found in the registry"}

    if is_valid_url(app):
        a = open_tab(app)
        logger.info(f"{application} opend - {a}")
        return a
    else:
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

    if is_valid_url(app):
        keyboard = Controller()
        a= close_tab(app)
        return a
        # # 1. Ensure Chromium is the focused window in Hyprland
        # subprocess.run(["hyprctl", "dispatch", "focuswindow", "class:chromium"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # time.sleep(0.1) # Small buffer for focus swap
        # subprocess.run(['wtype', '-M', 'ctrl', 'w'])

    else:
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







def set_brightness(level):
    """It set the brightness which is specified."""
    logger.info("Successfully called set_brightness.")

    brightness = (max(5,min(100,int(level))))
    command = ["brightnessctl","-q", "set", f"{brightness}%"]

    subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    logger.info(f"Successfully set the bightness to level - {level}")
    return{"success": True, "error": ""} 

def increase_brightness(level):
    """It increase the brightness by level which is specified."""
    logger.info("Successfully called increase_brightness.")

    brightness = (max(5,min(100,int(level))))
    command = ["brightnessctl","-q", "set", f"+{brightness}%"]

    subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    logger.info(f"Successfully increased the brightness by level - {level}")
    return{"success": True, "error": ""}

def decrease_brightness(level):
    """It decrease the brightness by level which is specified."""
    logger.info("Successfully called decrease_brightness.")

    brightness = (max(5,min(100,int(level))))
    command = ["brightnessctl","-q", "set", f"{brightness}%-"]

    subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    logger.info(f"Successfully decreased the brightness by level - {level}")
    return{"success": True, "error": ""}







    








COMMAND_EXECUTOR = {
    "OPEN_APPLICATION":open_application,
    "CLOSE_APPLICATION":close_application,
    "SET_VOLUME":set_volume,
    "DECREASE_VOLUME":decrease_volume,
    "INCREASE_VOLUME":increase_volume,
    "SET_BRIGHTNESS":set_brightness,
    "DECREASE_BRIGHTNESS":decrease_brightness,
    "INCREASE_BRIGHTNESS":increase_brightness,
    "WEB_SEARCH":web_search
}
