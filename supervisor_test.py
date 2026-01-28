import requests

url = "http://127.0.0.1:8000/analyze"

payload = {
    "messages": [
        {
            "role": "system",
            "content": "You are the supervisor agent."
        },
        {
            "role": "user",
            "content": "I’ve been working 12 hours a day and only sleeping 4 hours. Am I overworking?"
        }
    ]
}

response = requests.post(url, json=payload)

print("\n==== SUPERVISOR → AGENT TEST ====\n")
print("Status code:", response.status_code)
print("\nResponse JSON:\n", response.json())
