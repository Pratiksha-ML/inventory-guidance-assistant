
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

from inventory_tools import (
    get_inventory_summary,
    get_low_stock_products,
    get_replenishment_recommendations
)

from rag_pipeline import search_inventory_sop


# ----------------------------------
# 1. Define Inventory Tools
# ----------------------------------

@tool
def inventory_summary_tool():
    """Get total products and total available stock units."""
    return get_inventory_summary()


@tool
def low_stock_tool():
    """Find products with available stock below minimum stock."""
    return get_low_stock_products()


@tool
def inventory_sop_tool(question: str):
    """Search the inventory SOP for policies, procedures,
    approval rules and inventory guidelines."""
    return search_inventory_sop(question)


@tool
def replenishment_recommendation_tool():
    """Calculate recommended replenishment quantities
    for products below minimum stock."""
    return get_replenishment_recommendations()


tools = [
    inventory_summary_tool,
    low_stock_tool,
    inventory_sop_tool,
    replenishment_recommendation_tool
]


# ----------------------------------
# 2. Initialize Local LLM
# ----------------------------------

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)


# ----------------------------------
# 3. Define Agent Instructions
# ----------------------------------

system_message = """
You are a reliable Inventory Management Assistant.

You help users understand inventory information
and inventory management policies.

AVAILABLE TOOLS:

1. inventory_summary_tool:
   Use for total product and stock summary questions.

2. low_stock_tool:
   Use to identify products below minimum stock.

3. inventory_sop_tool:
   Use for questions about inventory policies,
   approval rules and SOP procedures.

4. replenishment_recommendation_tool:
   Use to calculate replenishment quantities.

TOOL USAGE RULES:

1. Select the appropriate tool for the user's question.
2. Use the tool result to prepare your final answer.
3. Do not repeatedly call the same tool for the same
   question unless additional information is needed.
4. After receiving a tool result, provide a final answer.
5. Do not stop after requesting a tool call.

ACCURACY RULES:

1. Never invent inventory quantities or product details.
2. Never invent employee names or job titles.
3. Never invent departments or approval roles.
4. Use only information returned by the tools.
5. If the SOP says "authorized team member",
   do not assume a specific job title.
6. If the SOP does not specify requested information,
   explicitly say:
   "The SOP does not specify this information."
7. If information is unavailable, clearly say so.

FINAL RESPONSE RULES:

1. Always provide a direct natural-language answer.
2. Never display raw tool-call JSON to the user.
3. Include every relevant product returned by a tool.
4. Keep answers clear and professional.
"""


# ----------------------------------
# 4. Define Agent Node
# ----------------------------------

def call_model(state: MessagesState):

    messages = [
        ("system", system_message)
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# ----------------------------------
# 5. Build LangGraph Workflow
# ----------------------------------

builder = StateGraph(MessagesState)

builder.add_node("agent", call_model)

builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition
)

builder.add_edge("tools", "agent")

agent = builder.compile()


# ----------------------------------
# 6. Create Reusable Agent Function
# ----------------------------------



def ask_inventory_agent(question):

    # 1. Check whether the question is inventory-related.

    inventory_keywords = [
        "inventory",
        "stock",
        "product",
        "warehouse",
        "replenishment",
        "replenish",
        "replenished",
        "restock",
        "restocking",
        "purchase order",
        "sop",
        "approval",
        "supplier",
        "quantity",
        "low stock",
        "available units"
    ]

    question_lower = question.lower()

    is_inventory_question = any(
        keyword in question_lower
        for keyword in inventory_keywords
    )

    if not is_inventory_question:
        return (
            "I can help with inventory management, "
            "stock levels, replenishment recommendations "
            "and inventory SOP policies. "
            "This question is outside my scope."
        )

    # 2. Run the LangGraph agent.

    result = agent.invoke(
        {
            "messages": [
                ("user", question)
            ]
        },
        config={
            "recursion_limit": 10
        }
    )

    messages = result["messages"]

    # 3. Check whether the SOP tool was executed.

    for message in reversed(messages):

        if getattr(message, "name", None) == "inventory_sop_tool":

            sop_answer = message.content

            # If the SOP tool returned a valid answer,
            # use that answer rather than a vague summary.

            if sop_answer and sop_answer.strip():
                return sop_answer

    # 4. Otherwise return the final assistant response.

    final_message = messages[-1]

    if final_message.tool_calls:
        return (
            "I could not complete the answer using "
            "the available tools. Please try again."
        )

    return final_message.content



# ----------------------------------
# 7. Run Agent Independently
# ----------------------------------

if __name__ == "__main__":

    print("\nINVENTORY GUIDANCE ASSISTANT")
    print("============================")

    while True:

        question = input("\nAsk your question (or type exit): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = ask_inventory_agent(question)

        print("\nASSISTANT ANSWER")
        print("----------------")
        print(answer)
