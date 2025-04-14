import os
import fitz  # PyMuPDF
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter

BASE_PATH = './data/medical-papers'
os.makedirs("./embeddings", exist_ok=True)

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
                        text = "".join([page.get_text() for page in doc])
                        all_text.append({
                            "disease": disease_folder,
                            "filename": filename,
                            "text": text
                        })
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
    return all_text
def get_relevant_context(user_input):
    docs = db.similarity_search(user_input, k=3)
    return "\n\n".join([doc.page_content for doc in docs])

def chunk_text(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_chunks = []
    for doc in docs:
        chunks = splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk": chunk,
                "disease": doc["disease"],
                "source_file": doc["filename"],
                "chunk_id": i
            })
    return all_chunks

if __name__ == "__main__":
    extracted_data = extract_all_text(BASE_PATH)
    chunks = chunk_text(extracted_data)

    with open("./embeddings/all_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ {len(chunks)} chunks saved to ./embeddings/all_chunks.pkl")