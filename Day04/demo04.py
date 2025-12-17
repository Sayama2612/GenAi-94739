import os
import json
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}", 
    "Content-Type": "application/json"
}

req_data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "You are a mother."},
        {"role": "user", "content": "Who is God of cricket?"},
        {"role": "assistant", "content": "Sachin Tendulkar."},
        {"role": "user", "content": "Where was he born?"}
    ]
}

response = requests.post(
    url,
    headers=headers,
    data=json.dumps(req_data),
)

print("Status code:", response.status_code)

data = response.json()

print("Reply:", data["choices"][0]["message"]["content"])
