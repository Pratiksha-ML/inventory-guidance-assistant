
from pathlib import Path
from functools import lru_cache

from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama

from pdf_reader import read_pdf
from text_chunker import split_text

from vector_database import (
    create_vector_database,
    search_vector_database
)


# ==========================================
# STEP 1: LOAD RAG RESOURCES ONCE
# ==========================================

@lru_cache(maxsize=1)
def load_rag_resources():

    print("\nLoading embedding model...")

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Reading inventory SOP PDF...")

    pdf_path = (
        Path(__file__).parent
        / "documents"
        / "inventory_sop.pdf"
    )

    document_text = read_pdf(pdf_path)

    print("Splitting document into chunks...")

    chunks = split_text(document_text)

    print("Creating FAISS vector database...")

    index = create_vector_database(
        chunks,
        embedding_model
    )

    print("Connecting to local Llama model...")

    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0
    )

    print("\nRAG pipeline initialized successfully!")

    return embedding_model, chunks, index, llm


# ==========================================
# STEP 2: INVENTORY SOP SEARCH FUNCTION
# ==========================================

def search_inventory_sop(question):

    # Load cached resources
    embedding_model, chunks, index, llm = (
        load_rag_resources()
    )

    # Retrieve relevant document chunks
    results = search_vector_database(
        question,
        chunks,
        embedding_model,
        index
    )

    # Prepare retrieved context
    context = "\n\n".join(
        result["text"] for result in results
    )

    # ======================================
    # STEP 3: STRICT RAG PROMPT
    # ======================================

    prompt = f"""
You are a reliable Inventory Management Assistant.

Your task is to answer user questions using only the
information available in the provided Inventory SOP context.

STRICT RULES:

1. Answer strictly using the provided SOP context.

2. Never invent, assume, or add information that is
   not explicitly mentioned in the context.

3. Do not create fictional names, job titles,
   departments, employee roles, policies, or procedures.

4. If the user asks for a specific person's name,
   job title, department, or role, and the context
   does not provide that information, clearly state:

   "The SOP does not specify this information."

5. If the answer is not available in the context,
   clearly say that the SOP does not provide the answer.

6. Do not use general knowledge to fill gaps in the SOP.

7. Do not provide guesses or possible explanations
   as if they were confirmed facts.

8. Keep answers clear, concise, and professional.

9. When answering questions about inventory policies,
   explain only the relevant information from the SOP.

10. If the context provides a section number,
    mention the section number when relevant.

SOP CONTEXT:
{context}

USER QUESTION:
{question}

INSTRUCTIONS FOR FINAL ANSWER:

Read the context carefully.
Identify the exact information relevant to the question.
If the requested information is missing, acknowledge it.
Never make up missing details.

FINAL ANSWER:
"""

    # ======================================
    # STEP 4: GENERATE ANSWER USING LLAMA
    # ======================================

    response = llm.invoke(prompt)

    return response.content


# ==========================================
# STEP 5: TEST RAG PIPELINE INDEPENDENTLY
# ==========================================

if __name__ == "__main__":

    print("\nINVENTORY SOP ASSISTANT")
    print("=======================")

    while True:

        question = input(
            "\nAsk an SOP question (or type exit): "
        )

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = search_inventory_sop(question)

        print("\nASSISTANT ANSWER")
        print("----------------")

        print(answer)
