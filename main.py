import os
import subprocess
import requests
import json
import sqlite3

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import to avoid deprecation

from ai.check_pdf import check_pdfs
# from ai.conversation_db import save_conversation_history  # Uncomment if using conversation logging

# === SETTINGS ===
AI_DIR = os.path.join(os.path.dirname(__file__), "ai")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "medical-papers")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "embeddings", "faiss_medical_db")
API_KEY_PATH = os.path.join(AI_DIR, "config.py")
MODEL_NAME = "llama3-70b-8192"

# === Load API Key ===
with open(API_KEY_PATH, "r") as key_file:
    GROQ_API_KEY = key_file.read().strip()

# === STEP 1: Vectorization Pipeline ===
def run_vector_pipeline():
    try:
        print("📂 Checking PDF files in the directory...")
        check_pdfs(DATA_DIR)

        print("🧠 Extracting and chunking medical documents...")
        subprocess.run(["python", os.path.join(AI_DIR, "extract_and_chunk.py")], check=True)

        print("📈 Building FAISS vector index...")
        subprocess.run(["python", os.path.join(AI_DIR, "build_faiss_index.py")], check=True)

        index_file = os.path.join(INDEX_DIR, "index.faiss")
        if os.path.exists(index_file):
            print(f"🎉 FAISS index created successfully at {index_file}")
        else:
            print("❌ FAISS index creation failed.")

        return "✅ Vector pipeline executed successfully."
    except subprocess.CalledProcessError as e:
        return f"❌ Pipeline failed: {str(e)}"

# === STEP 2: Context Retrieval ===
def get_relevant_context(user_input):
    try:
        # Check if FAISS index exists
        if not os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
            return "⚠️ FAISS index not found. Please run the vector pipeline first."

        # Initialize embeddings
        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Load the FAISS index
        print("🔧 Loading FAISS index...")
        db = FAISS.load_local(INDEX_DIR, embedding)  # Removed 'allow_dangerous_deserialization=True'

        # Perform the similarity search
        print("🔍 Performing similarity search...")
        docs = db.similarity_search(user_input, k=3)
        
        # If no relevant documents are found
        if not docs:
            print("📭 No matching documents found.")
            return "No relevant context found."

        # Return the context from the most relevant documents
        return "\n\n".join([doc.page_content for doc in docs])

    except Exception as e:
        print(f"❌ Error while fetching context: {e}")
        return "⚠️ Failed to fetch context."

# === STEP 3: GROQ API Call ===
def get_groq_response(context, user_input, debug=False):
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful medical assistant. Only answer using the context provided."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {user_input}"
            }
        ],
        "temperature": 0.3
    }

    try:
        if debug:
            print("📡 Sending request to GROQ API...")
            print("Payload:\n", json.dumps(data, indent=2))

        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        if debug:
            print("✅ Response received:", json.dumps(response_json, indent=2))

        if 'choices' in response_json and response_json['choices']:
            return response_json['choices'][0]['message']['content']
        else:
            return "⚠️ GROQ responded, but no answer was found."

    except requests.exceptions.RequestException as e:
        return f"🚫 Request to GROQ API failed: {e}"
    except ValueError:
        return f"🚫 Received non-JSON response: {response.text}"
    except KeyError as e:
        return f"🚫 Missing expected data in response: {e}"

# === CAMERA CONNECT ===
def run_object_detection():
    subprocess.run(["python", "detect_objects.py"])

# === ENTRY POINT ===
if __name__ == "__main__":
    print("🚀 Starting Health AI Vector + GROQ pipeline...")

    initialize_conversation_db("database/conversation.db")

    # Optionally run the pipeline (only needed once)
    # status = run_vector_pipeline()
    # print(status)

    while True:
        user_input = input("\n💬 Ask a health question (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("👋 Exiting chatbot.")
            break

        context = get_relevant_context(user_input)
        reply = get_groq_response(context, user_input)

        print("\n🤖 GROQ Health Bot:")
        print(reply)

        # save_conversation_history("user", user_input)
        # save_conversation_history("assistant", reply)
