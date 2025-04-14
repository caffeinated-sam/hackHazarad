import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss

# 1️⃣ Load the chunks from file
with open("./embeddings/all_chunks.pkl", "rb") as f:
    all_chunks = pickle.load(f)

texts = [chunk["chunk"] for chunk in all_chunks]
print(f"📄 Loaded {len(texts)} chunks.")

# 2️⃣ Load the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("🤖 Model loaded.")

# 3️⃣ Embed the chunks (batch + progress bar)
embeddings = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True
)
print("✅ Embeddings created.")

# 4️⃣ Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print(f"📦 FAISS index built with {index.ntotal} vectors.")

# 5️⃣ Save FAISS index and metadata
os.makedirs("./embeddings/faiss_medical_db", exist_ok=True)
faiss.write_index(index, "./embeddings/faiss_medical_db/index.faiss")

with open("./embeddings/faiss_medical_db/metadata.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

print("🎉 Vector store and metadata saved to ./embeddings/faiss_medical_db")
