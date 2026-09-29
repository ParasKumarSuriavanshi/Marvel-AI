from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from groq import Groq
import os
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
load_dotenv()
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============


groq_api = os.getenv("groq_api")
anyscale = os.getenv("anyscale")
mistral_api = os.getenv("mistral_api")
# llm = ChatGroq(
#     model="qwen/qwen3.8-27b", 
#     temperature=0,
#     max_tokens=990,
#     api_key=groq_api
# )

llm = ChatMistralAI(
    model="open-mistral-7b", # or "open-mistral-7b", "mistral-small-latest"
    temperature=0,
    mistral_api_key=mistral_api
)


# llm = ChatOllama(model = "qwen3:8b" , temperature = 0)
logger.info("llm load")

