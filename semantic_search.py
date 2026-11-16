
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from pdf_reader import read_pdf
from text_chunker import split_text

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read the PDF
pdf_path = Path(__file__).parent / "documents" / "inventory_sop.pdf"
document_text = read_pdf(pdf_path)

# Split document into chunks
chunks = split_text(document_text)

# Generate embeddings for document chunks
chunk_embeddings = model.encode(chunks, convert_to_tensor=True)

# Ask a question
question = "Who must approve purchase orders?"

# Generate question embedding
question_embedding = model.encode(question, convert_to_tensor=True)

# Calculate similarity
similarity_scores = util.cos_sim(
    question_embedding,
    chunk_embeddings
)[0]

# Find the most relevant chunk
best_match_index = similarity_scores.argmax().item()

print("USER QUESTION:")
print(question)

print("\nMOST RELEVANT SOP INFORMATION:")
print(chunks[best_match_index])

print("\nSIMILARITY SCORE:")
print(similarity_scores[best_match_index].item())
