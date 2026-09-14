from langchain_ollama import ChatOllama
import logging
#==========Logger==============


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(filename)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("log_info.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

#==========Logger===============
llm = ChatOllama(model = "qwen3:8b" ,  temperature = 0)
logger.info("llm load")

