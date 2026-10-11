
import sys
from faster_whisper import WhisperModel
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============

def transcribe1():
    """STT for marvel ai"""
    logger.info("Successfully called transcribe func.")

    model = WhisperModel("base",device="cpu",compute_type="int8")

    segments,info=model.transcribe("output.wav",beam_size=7)
    full_text=[]
    for segment in segments:
        full_text.append(segment.text)

    if len(full_text)==0:
        return
    text = " ".join(full_text)

   

    logger.info("Transcribed text generated")
    return text


if __name__ == "__main__":
    transcribe1()