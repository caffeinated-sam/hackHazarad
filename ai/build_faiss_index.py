import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

with open("./embeddings/all_chunks.pkl", "rb") as f:
    all_chunks = pickle.load(f)

# Extract the text from chunks
texts = [chunk["chunk"] for chunk in all_chunks]

# Initialize the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True
)

# Check the shape of the embeddings
print("Shape of embeddings:", embeddings.shape)

# Safeguard to ensure 2D array
if len(embeddings.shape) != 2:
    raise ValueError(f"Expected 2D array for embeddings, but got {embeddings.shape}")

# Extract the dimension of the embeddings
dimension = embeddings.shape[1]

# Create the FAISS index
index = faiss.IndexFlatL2(dimension)

# Add the embeddings to the index
index.add(embeddings)

# Ensure the output folder exists
os.makedirs("./embeddings/faiss_medical_db", exist_ok=True)

# Save the FAISS index and metadata
faiss.write_index(index, "./embeddings/faiss_medical_db/index.faiss")

with open("./embeddings/faiss_medical_db/metadata.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

print(f"🎉 FAISS index built with {index.ntotal} vectors and saved.")
