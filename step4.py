import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# STEP 1: Extract text from PDFs
BASE_PATH = r"C:\Users\Lenovo\OneDrive\Desktop\Chatbot\data\medical-papers"

def extract_all_text(base_path):
    all_text = []
    for disease_folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, disease_folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        doc = fitz.open(file_path)
                        text = ""
                        for page in doc:
                            text += page.get_text()
                        all_text.append({
                            "disease": disease_folder,
                            "filename": filename,
                            "text": text
                        })
                    except Exception as e:
                        print(f"Error extracting text from {filename}: {e}")
                        continue
    return all_text

extracted_data = extract_all_text(BASE_PATH)
print(f"✅ Extracted {len(extracted_data)} documents.")

# STEP 2: Chunk the text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

all_chunks = []

for doc in extracted_data:
    chunks = splitter.split_text(doc["text"])
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "chunk": chunk,
            "disease": doc["disease"],
            "source_file": doc["filename"],
            "chunk_id": i
        })

print(f"✅ Total Chunks Created: {len(all_chunks)}")

import pickle

# Save chunks to a file for later use
os.makedirs("./embeddings", exist_ok=True)

with open("./embeddings/all_chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

print("✅ all_chunks saved to ./embeddings/all_chunks.pkl")




