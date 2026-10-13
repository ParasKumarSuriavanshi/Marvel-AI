
import time
import wave
from ctypes import *

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass  

try:
    asound = cdll.LoadLibrary('libasound.so.2')
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound.snd_lib_error_set_handler(c_error_handler)
except OSError:
    pass 

import pyaudio
from fastapi import FastAPI
import numpy as np
from audio_to_text.transcribe import transcribe1
from agent.tts_maker import tts_stop

import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

app = FastAPI()

FORMAT = pyaudio.paInt16
CHUNK = 1024
RATE =  48000#16000#44100
OUTPUT_FRAME = "output.wav"
CHANNEL = 1
SILENT_THRESHOLD = 500
SILENT_DURATION = 4

@app.get("/recoder")
def recoder():
    """Audio reocde"""
    logger.info("Successfully called recoder func.")
    audio = pyaudio.PyAudio()
    stream = audio.open(format = FORMAT, channels=CHANNEL, rate=RATE , input=True, frames_per_buffer=CHUNK)
    silent_time = None
    frame = []


    continuee = True
    
    print("Speak....")
    while True:
        try:
            data = stream.read(CHUNK)
            frame.append(data)
            audio_data = np.frombuffer(data, dtype=np.int16)
            rms = np.sqrt(np.mean(audio_data.astype(np.float64) ** 2))
            if rms < SILENT_THRESHOLD:
                if silent_time == None:
                    silent_time = time.time()
                else:
                    elapsed_time = time.time() - silent_time
                    if elapsed_time > SILENT_DURATION:
                        break
            else:
                silent_time = None
                #tts_stop()
                
                
                
        except:
            logger.error("Error while data generatio")
            break
    print("Recognazing....")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wavefile = wave.open(OUTPUT_FRAME,"wb")
    wavefile.setnchannels(CHANNEL)
    wavefile.setframerate(RATE)
    wavefile.setsampwidth(audio.get_sample_size(FORMAT))
    wavefile.writeframes(b''.join(frame))
    wavefile.close()

    logger.info("Audio file created")

    return transcribe1()

    

if __name__ ==  "__main__":
    recoder()