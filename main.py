import subprocess
import os
import requests
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from ai.check_pdf import check_pdfs  # Ensure this is the correct path for your check_pdfs function
import json

# === SETTINGS ===
AI_DIR = os.path.join(os.path.dirname(__file__), "ai")  # Adjust based on your folder structure
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "medical-papers")  # Path to your documents
API_KEY_PATH = "ai/config.py"  # Replace with the correct path to your GROQ API key
MODEL_NAME = "llama3-70b-8192"  # Your model name for the GROQ API

# === STEP 1: Run Vector Pipeline ===
def run_vector_pipeline():
    """Run the vectorization and indexing pipeline."""
    try:
        print("📂 Checking PDF files in the directory...")
        check_pdfs(DATA_DIR)  # Ensure check_pdfs properly checks your documents in the folder

        print("🧠 Extracting and chunking medical documents...")
        subprocess.run(["python", os.path.join(AI_DIR, "extract_and_chunk.py")], check=True)

        print("📈 Building FAISS vector index...")
        subprocess.run(["python", os.path.join(AI_DIR, "build_faiss_index.py")], check=True)

        # Confirm that the FAISS index file has been created
        faiss_index_path = "./embeddings/faiss_medical_db/index.faiss"
        if os.path.exists(faiss_index_path):
            print(f"🎉 FAISS index created successfully at {faiss_index_path}")
        else:
            print("❌ FAISS index creation failed.")

        return "✅ Vector pipeline executed successfully."
    except subprocess.CalledProcessError as e:
        return f"❌ Pipeline failed: {str(e)}"

# === STEP 2: Get Context from FAISS ===

def get_relevant_context(user_input):
    """Fetch the most relevant context from the FAISS vector store."""
    
    try:
        # Define the FAISS index path (replace with your actual index path)
        index_path = 'D:/study/practice/JeevDead/embeddings/faiss_medical_db'  # Make sure this points to the correct folder where your .faiss file is
        faiss_index_path = os.path.abspath(index_path)  # Convert to absolute path

        # Load the FAISS index using the embedding model
        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local(faiss_index_path, embedding, allow_dangerous_deserialization=True)

        # Perform similarity search to get the most relevant documents
        docs = db.similarity_search(user_input, k=3)  # Adjust the number 'k' for how many results you want

        # Return the content of the top 'k' documents
        return "\n\n".join([doc.page_content for doc in docs])

    except Exception as e:
        # Handle any errors that occur (e.g., file not found, loading issues)
        print(f"Error while fetching context: {e}")
        return "Sorry, I couldn't fetch the context at the moment. Please try again later."

# === STEP 3: Call GROQ API ===
def get_groq_response(context, user_input, api_key_path="ai/config.py"):
    """Call the GROQ API and get the processed response."""
    # Load API key from a configuration file
    try:
        with open(api_key_path, 'r') as key_file:
            api_key = key_file.read().strip()
    except FileNotFoundError:
        return "Error: API key file not found."
    
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,  # Use your actual model name
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
        "temperature": 0.3  # Adjust the temperature to control the randomness of the response
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP error codes

        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0:
            return response_json['choices'][0]['message']['content']  # Return the answer from GROQ
        else:
            return "Error: No response content found."
    except requests.exceptions.RequestException as e:
        return f"Error: Request failed - {e}"
    except ValueError:
        return f"Error: Invalid JSON response - {response.text}"
    except KeyError:
        return "Error: Missing key in JSON response."

# === ENTRY POINT ===
if __name__ == "__main__":
    print("🚀 Starting Health AI Vector + GROQ pipeline...")

    # Run the vector pipeline for setting up the FAISS index
    status = run_vector_pipeline()
    print(status)

    # Loop for asking questions and getting answers from the system
    while True:
        user_input = input("\n💬 Ask a health question (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("👋 Exiting chatbot.")
            break

        # Retrieve the most relevant context from FAISS
        context = get_relevant_context(user_input)

        # Send the context and question to GROQ for processing
        reply = get_groq_response(context, user_input)
        
        print("\n🤖 GROQ Health Bot:")
        print(reply)

# === CAMERA CONNECT ===
def run_object_detection():
    """Run object detection script."""
    subprocess.run(["python", "detect_objects.py"])  # Run the external object detection script
