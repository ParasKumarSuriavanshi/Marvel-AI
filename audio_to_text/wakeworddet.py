from ctypes import *
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass  # Ignores the error strings entirely

try:
    asound = cdll.LoadLibrary('libasound.so.2')
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound.snd_lib_error_set_handler(c_error_handler)
except OSError:
    pass 
import asyncio
from livekit.wakeword import WakeWordListener, WakeWordModel
from audio_to_text.voice import recoder
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============



model = WakeWordModel(models=["my_wakeword1.onnx", "my_wakeword2.onnx"])


async def wake():
    """Detect the wake word from the user"""



    logger.info("Successfully called wakeword function")
    async with WakeWordListener(model, threshold=0.10,debounce=1.0) as listener:
        print("waiting for wakword")
        while True:
            logger.info("Waiting for wakeword")
            detection =await listener.wait_for_detection()
            print("wakeword detected")
            logger.debug(f"deteced the {detection.name} {detection.confidence}")
            #print(f"deteced the {detection.name} {detection.confidence}")
            #print(recoder())
            break

# asyncio.run(wake())