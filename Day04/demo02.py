import os
import requests
import time
from dotenv import load_dotenv
import json

load_dotenv()

api_key = "dummy-key"

url = "http://127.0.0.1:1234/v1/chat/completions"

headers = {
    "Authorization": f"Brearer {api_key}",
    "Content-Type": "application/json"
}

while True:
    user_prompt = input("Enter your prompt :")
    if user_prompt == "exit":
        break
    req_data = {
        "model": "microsoft/phi-4-mini-reasoning",
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    time1 = time.perf_counter()

    response = requests.post(url, data=json.dumps(req_data), headers=headers)

    time2 = time.perf_counter()

    data = response.json()

    print(data["choices"][0]["message"]["content"])
    print(f"Time required : {time2-time1:.2f} sec")
