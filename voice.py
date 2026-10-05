import os
import ctypes
#import openwakeword
import pyaudio
from openwakeword.model import Model
#from pocketsphinx import LiveSpeech
import numpy as np

# 1. Define the ALSA error handler C-function type
ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

try:
    asound = ctypes.cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
except OSError:
    pass

#import speech_recognition

def speech1():
    r =  speech_recognition.Recognizer()

    with speech_recognition.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        print("Listening....",end="")
        audio=r.listen(source)
    text=""
    try:
        print("Recoganizing....")
        #text = r.recognize_whisper(audio, language="english", model="base")
        text = r.recognize_google(audio, language="english")
        
    except speech_recognition.UnknownValueError:
        pass
    except speech_recognition.RequestError as e:
        pass
    return text



def speech2(a):
    
    r = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone(device_index=a)
    
    with microphone as source:
        r.adjust_for_ambient_noise(source,duration=1)
        print("Listening2....",end="")
        audio=r.listen(source)
    text = ""
    try:
        print("Recoganizing....")
        #text = r.recognize_whisper(audio, language="english", model="base")
        text = r.recognize_google(audio, language="english")
    except speech_recognition.UnknownValueError:
        pass
    except speech_recognition.RequestError as e:
        pass
    return text

def speak():
    a = None
    text1=""
    for index, name in enumerate(speech_recognition.Microphone.list_microphone_names()):
        if "AB13X USB Audio:" in name:
            a=index
    if a is None:
        text1 = speech1()
    else:
        text1 = speech2(a)
    print(text1)
    return text1

def wake():
    # Leaving Model() empty in v0.4.0 automatically loads all built-in paths
    model = Model()
    
    p = pyaudio.PyAudio()
    stream = p.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=1280)

    print("Waiting for Wakeword ('hey jarvis')....")
    
    try:
        while True:
            audio = np.frombuffer(stream.read(1280, exception_on_overflow=False), dtype=np.int16)
            prediction = model.predict(audio)
            
            # The dictionary keys in v0.4.0 include version numbers (e.g., 'hey_jarvis_v0.1')
            # So we iterate through the keys to check for a match
            for key, score in prediction.items():
                if "jarvis" in key and score > 0.5:
                    print("WakeWord Detected....")
                    #speak()
                    return True
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
    

if __name__ == "__main__":
    
    #wake()
    speak()