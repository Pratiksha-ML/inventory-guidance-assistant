
from langchain_ollama import ChatOllama

# Connect to local Llama model
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)

# Ask a question
response = llm.invoke(
    "A warehouse has 15 wireless mice. "
    "The minimum required stock is 25. "
    "Is this product low on stock? Explain why."
)

# Display response
print("LLAMA AGENT TEST")
print("----------------")
print(response.content)
