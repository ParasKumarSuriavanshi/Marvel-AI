import requests
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============



def tts_maker(state):
    """Call the tts maker function"""
    logger.info("Successfully called tts_maker")

    text = state["speech_messages"]
    try:
        requests.post("http://127.0.0.1:8000/tts", json={"text": text}, timeout=10)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while sending text to TTS service: {e}")
        pass

    return
    

def tts_stop():
    """Call the tts stop function"""
    logger.info("Successfully called tts_stop")

    try:
        requests.post("http://127.0.0.1:8000/stop", timeout=10)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while sending request to TTS service: {e}")
        pass
    return