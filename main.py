from langchain_core.messages import HumanMessage
from model.llm import llm
from graph.workflow import build
from agent.user_id import user_id_extractor

a = build()


while True:
    user_input = input("User1: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    # 1. Create the initial state payload with the user message
    initial_state = {"messages": [HumanMessage(content=user_input)]}
    
    # 2. Call the extractor outside the graph to get the user_id injected into state
    updated_state = user_id_extractor(initial_state)
    print(updated_state)

    user_id = updated_state.get("user_id", "paras")
    config = {
        "configurable": {
            "thread_id": f"{user_id}" 
        }
    }



    result = a.invoke(
        updated_state,
        config=config
    )

    # result = a.invoke(
    #     {
    #         "messages": [HumanMessage(content=user_input)]
    #     },
    #     config=config
    # )
    print(result.get("messages")[-1].content)



for message in result.get("messages", []):
    # This will print something like "human: how are you" or "ai: I'm doing well!"
    print("-" * 20) # Adds a separator line between messages
    print(f"{message.type}: {message.content}\n")
    print("-" * 20) # Adds a separator line between messages


# config = {
#     "configurable": {
#         "thread_id": "paras" 
#     }
# }

# current_state = a.get_state(config)

# # The messages are stored in the 'values' attribute
# history = current_state.values.get("messages", [])

# # LangChain messages have a built-in pretty_print() method
# for message in history:
#     message.pretty_print()

# print(len(history))  # This will print the number of messages in the history