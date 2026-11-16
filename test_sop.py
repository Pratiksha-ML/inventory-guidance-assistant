
from rag_pipeline import search_inventory_sop

question = (
    "What does the SOP say about approval "
    "for stock-changing actions?"
)

answer = search_inventory_sop(question)

print("\nDIRECT SOP TEST")
print("-------------------------")
print(answer)
