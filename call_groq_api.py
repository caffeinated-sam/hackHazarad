#endpoint:  https://api.groq.com/openai/v1/chat/completions
#API: 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
import requests

# ✅ Use your actual API key here
api_key = "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"

api_url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# ✅ Update with a supported model name
data = {
    "model": "llama3-70b-8192",
    "messages": [
        {"role": "user", "content": "What are the early signs of breast cancer?"}
    ]
}

response = requests.post(api_url, headers=headers, json=data)

if response.status_code == 200:
    answer = response.json()
    print("🧠 Answer:", answer['choices'][0]['message']['content'])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
