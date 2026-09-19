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
    sw = stopwords.words('english')
    sw.extend(custom_words)
        
    for word in token:
        if word not in sw:
            fil_token.append(word)
    logger.debug(f"filter_token are - {fil_token}")
    return {"direct_command":{"normalize_input":text,"tokenized":fil_token}}

#     return {"direct_command":{"normalize_input":text}}
# normalizer("hey marvel.open netflix and play mentalist")
# normalizer("hey marvel, hi i am paras could you search piano lesson on youtube")
# normalizer("hey marvel, hi i am paras could you search what is the defination of hippo")




