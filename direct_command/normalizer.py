import re
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
# nltk.download('punkt_tab')
# nltk.download('stopwords')
import logging
#==========Logger==============

logger = logging.getLogger(__name__)

#==========Logger===============


def normalizer(state):
    """normalize the text for easy use"""
    logger.info("successfully called normalizer for direct command")

    tokeni = RegexpTokenizer(r"\w+")
    fil_token = []
    custom_words = ['hey' , 'marvel']
    
    #pattern = "volume [\\w|\\d]+|open [\\w]+|launch [\\w]+"
    text = state["messages"][-1].content
    if not text:
        return {"direct_command":{"normalize_input":""}}

    text = text.strip()
    text = text.lower()
    text = text.strip(" \t\n\r.,!?;:")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r'(?i)^hey marvel,\s*', '', text)
    
    token = tokeni.tokenize(text)

    REMOVE_WORDS = [
    "a", "an", "the",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did",       # only remove if you're sure they're not intent-bearing
    "of", "at", "by",
    "for",
    "about",
    "as",
    "because",
    "again",
    "against",
    "each",
    "further",
    "here", "there",
    "it", "its",
    "me", "him", "her", "them",
    "myself", "yourself", "himself", "herself",
    "ourselves", "themselves",
    "very",
    "just"]
    # sw = stopwords.words('english')
    # sw.extend(custom_words)
        
    for i,word in enumerate(token):
        if word == "search":
            fil_token.append(word)
            a = " ".join(token[i + 1 :])
            fil_token.append(a)
            break
        elif word not in REMOVE_WORDS:
            fil_token.append(word)
    logger.debug(f"filter_token are - {fil_token}")
    return {"direct_command":{"normalize_input":text,"tokenized":fil_token}}

#     return {"direct_command":{"normalize_input":text}}
# normalizer("hey marvel.open netflix and play mentalist")
# normalizer("hey marvel, hi i am paras could you search piano lesson on youtube")
# normalizer("hey marvel, hi i am paras could you search what is the defination of hippo")




