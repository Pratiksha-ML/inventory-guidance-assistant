
import faiss
import numpy as np


def create_vector_database(chunks, model):

    # Convert text chunks into embeddings
    embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    )

    # Convert embeddings to float32
    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Store embeddings
    index.add(embeddings)

    return index


def search_vector_database(question, chunks, model, index):

    # Convert question into embedding
    question_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )

    question_embedding = np.array(
        question_embedding,
        dtype="float32"
    )

    # Search FAISS database
    scores, indices = index.search(
        question_embedding,
        k=2
    )

    results = []

    for i in range(len(indices[0])):
        chunk_index = indices[0][i]
        score = scores[0][i]

        results.append({
            "text": chunks[chunk_index],
            "score": float(score)
        })

    return results