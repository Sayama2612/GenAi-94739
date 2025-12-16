import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

prompt = input("Enter your prompt: ")

# -------------------------
# GROQ CALL
# -------------------------
def call_groq(prompt):
    try:
        start = time.time()

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )

        data = response.json()

        if "choices" in data:
            ans = data["choices"][0]["message"]["content"]
            return ans, time.time() - start
        else:
            return f"Groq API Error: {data}", None

    except Exception as e:
        return f"Groq Exception: {e}", None


# -------------------------
# GEMINI CALL (REST API)
# -------------------------
def call_gemini(prompt):
    try:
        start = time.time()
        api_key = os.getenv("GOOGLE_API_KEY")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        data = response.json()

        # Handle Gemini API errors
        if "error" in data:
            return f"Gemini API Error: {data['error']['message']}", None

        ans = data["candidates"][0]["content"]["parts"][0]["text"]
        return ans, time.time() - start

    except Exception as e:
        return f"Gemini Exception: {e}", None


# -------------------------
# EXECUTION
# -------------------------
groq_ans, groq_time = call_groq(prompt)
gemini_ans, gemini_time = call_gemini(prompt)

print("\n==============================")
print("GROQ RESPONSE:")
print(groq_ans)
print("TIME:", groq_time)

print("\nGEMINI RESPONSE:")
print(gemini_ans)
print("TIME:", gemini_time)
print("==============================")