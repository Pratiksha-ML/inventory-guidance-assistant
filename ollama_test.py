
from langchain_ollama import ChatOllama

# Connect Python to our local Llama model
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)

# Send a question to the model
response = llm.invoke(
    "What is Inventory Management? Explain in simple words."
)

# Display the answer
print("LLAMA RESPONSE:")
print(response.content)
