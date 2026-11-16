
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from inventory_tools import (
    get_inventory_summary,
    get_low_stock_products
)


# Step 1: Define state
class AgentState(TypedDict):
    question: str
    answer: str


# Step 2: Create inventory summary node
def inventory_summary_node(state: AgentState):

    result = get_inventory_summary()

    answer = (
        f"Total products: {result['total_products']}\n"
        f"Total stock units: {result['total_stock_units']}"
    )

    return {"answer": answer}


# Step 3: Create low stock node
def low_stock_node(state: AgentState):

    products = get_low_stock_products()

    if not products:
        answer = "No low-stock products found."
    else:
        answer = "Low-stock products:\n"

        for product in products:
            answer += (
                f"\n{product['product_name']}: "
                f"{product['available_stock']} available, "
                f"{product['minimum_stock']} minimum"
            )

    return {"answer": answer}


# Step 4: Create router
def route_question(state: AgentState):

    question = state["question"].lower()

    if "low stock" in question or "below minimum" in question:
        return "low_stock"

    return "inventory_summary"


# Step 5: Build graph
graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "inventory_summary",
    inventory_summary_node
)

graph_builder.add_node(
    "low_stock",
    low_stock_node
)

graph_builder.add_conditional_edges(
    START,
    route_question,
    {
        "inventory_summary": "inventory_summary",
        "low_stock": "low_stock"
    }
)

graph_builder.add_edge("inventory_summary", END)
graph_builder.add_edge("low_stock", END)


# Step 6: Compile graph
agent = graph_builder.compile()


# Step 7: Test agent
while True:

    question = input("\nAsk your inventory agent (or type exit): ")

    if question.lower() == "exit":
        break

    result = agent.invoke({
        "question": question,
        "answer": ""
    })

    print("\nAGENT RESPONSE:")
    print(result["answer"])
