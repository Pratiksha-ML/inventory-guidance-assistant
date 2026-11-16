
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pdf_reader import read_pdf
from text_chunker import split_text

# Step 1: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 2: Read our PDF
pdf_path = (
    Path(__file__).parent
    / "documents"
    / "inventory_sop.pdf"
)

document_text = read_pdf(pdf_path)

# Step 3: Split PDF text into chunks
chunks = split_text(document_text)

# Step 4: Generate embeddings
embeddings = model.encode(chunks)

# Step 5: Display results
print("PDF EMBEDDING RESULTS")
print("-------------------------")

print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

for index, chunk in enumerate(chunks):
    print(f"\nChunk {index + 1}:")
    print(chunk[:100])
    print("Embedding dimensions:", len(embeddings[index]))
