from langchain_core.prompts import PromptTemplate
from langgraph import graph
from model.llm import llm
from graph.state import MarvelState
from langchain_core.messages import AnyMessage


def profile_extract(MarvelState: MarvelState) -> AnyMessage:
    """Help in extracting useful information about the user and identifying which user is speaking."""
    prompt = PromptTemplate(
        input_variables=["messages"],
        template="Extract the user's profile information from the following messages: {messages}. "
                 "Return the information in a structured format."
                 ""
    )
    messages = MarvelState["messages"]
    response = llm.invoke([prompt.format(messages=messages)])
    return response


# if __name__ == '__main__':
#     # Minimal demo runner. Run this from the project root so sibling packages are importable:
#     #   cd /home/paras_k_s/Marvel-AI
#     #   python -u agent/profile.py
    
#     demo_state = {
#         "user_info": {"name": "Demo User"},
#         "messages": ["Hi, I'm Demo User. I like music and coding."],
#         "final_response": None,
#     }

#     try:
#         result = profile_extract(demo_state)
#         print("\nprofile_extract returned state update:\n", result)
#     except Exception as exc:
#         import traceback
#         print("Demo run failed with an exception:", exc)
#         traceback.print_exc()
#         print("\nIf you see import errors, run from the project root or set PYTHONPATH to the project folder.")