from langchain_ollama import ChatOllama
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============
llm = ChatOllama(model = "qwen3:8b" , temperature = 0)
logger.info("llm load")

