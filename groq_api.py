import requests
import json

def get_groq_response(context, user_input, api_key_path="ai/config.py", debug=True):
    """Call the GROQ API and get the processed response."""
    # Load API key from a configuration file
    try:
        with open(api_key_path, 'r') as key_file:
            api_key = key_file.read().strip()
    except FileNotFoundError:
        return "❌ Error: API key file not found."

    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
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
            print("🔧 [DEBUG] Sending request to GROQ API...")
            print("URL:", api_url)
            print("Headers:", headers)
            print("Payload:", json.dumps(data, indent=2))

        response = requests.post(api_url, headers=headers, json=data)
        
        if debug:
            print("🔧 [DEBUG] Response status code:", response.status_code)
            print("🔧 [DEBUG] Response body:", response.text)

        response.raise_for_status()

        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0:
            return response_json['choices'][0]['message']['content']
        else:
            return "⚠️ Error: No response content found."
    
    except requests.exceptions.RequestException as e:
        return f"🚫 Error: Request failed - {e}"
    except ValueError:
        return f"🚫 Error: Invalid JSON response - {response.text}"
    except KeyError:
        return "🚫 Error: Missing key in JSON response."
