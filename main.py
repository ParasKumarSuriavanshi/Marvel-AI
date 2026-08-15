from langchain_core.messages import HumanMessage
from model.llm import llm
from graph.workflow import build

a = build()

config = {
    "configurable": {
        "thread_id": "customer_001"
    }
}
while True:
    user_input = input("User1: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    result = a.invoke(
        {
            "messages": [HumanMessage(content=user_input)]
        },
        config=config
    )
    print(result.get("messages")[-1].content)

for message in result.get("messages", []):
    # This will print something like "human: how are you" or "ai: I'm doing well!"
    print(f"{message.type}: {message.content}\n")
    print("-" * 20) # Adds a separator line between messages