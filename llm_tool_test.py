
from langchain_ollama import ChatOllama
from langchain.tools import tool

from inventory_tools import (
    get_inventory_summary,
    get_low_stock_products
)


# Tool 1: Inventory summary
@tool
def inventory_summary_tool():
    """Get the total number of products and total available stock units."""
    return get_inventory_summary()


# Tool 2: Low-stock detection
@tool
def low_stock_tool():
    """Find products whose available stock is below their minimum stock."""
    return get_low_stock_products()


# Connect to Llama
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)


# Give Llama access to both tool descriptions
llm_with_tools = llm.bind_tools([
    inventory_summary_tool,
    low_stock_tool
])


# Ask Llama to choose a tool
response = llm_with_tools.invoke(
    "Which products currently have low stock? "
    "Use the appropriate inventory tool."
)


# Display the tool selected by Llama

# Available tools
available_tools = {
    "inventory_summary_tool": inventory_summary_tool,
    "low_stock_tool": low_stock_tool
}

print("\nLLAMA TOOL-CALLING TEST")
print("-----------------------")

# Execute the tool selected by Llama
for tool_call in response.tool_calls:

    tool_name = tool_call["name"]

    print("\nSelected tool:", tool_name)

    selected_tool = available_tools[tool_name]

    result = selected_tool.invoke(
        tool_call["args"]
    )

    print("\nTOOL EXECUTION RESULT:")
    print(result)
