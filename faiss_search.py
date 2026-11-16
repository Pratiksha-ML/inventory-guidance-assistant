
from pathlib import Path
from sentence_transformers import SentenceTransformer

from pdf_reader import read_pdf
from text_chunker import split_text
from vector_database import (
    create_vector_database,
    search_vector_database
)

# Step 1: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 2: Read inventory SOP PDF
pdf_path = (
    Path(__file__).parent
    / "documents"
    / "inventory_sop.pdf"
)

document_text = read_pdf(pdf_path)

# Step 3: Split document into chunks
chunks = split_text(document_text)

# Step 4: Create FAISS database
index = create_vector_database(chunks, model)

print("FAISS DATABASE CREATED!")
print("Total vectors:", index.ntotal)


# Step 5: Ask multiple questions
while True:

    question = input("\nAsk an inventory SOP question (or type 'exit'): ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    results = search_vector_database(
        question,
        chunks,
        model,
        index
    )

    for i, result in enumerate(results):
        print(f"\nRESULT {i + 1}:")
        print(result["text"])

        print("COSINE SIMILARITY:")
        print(result["score"])