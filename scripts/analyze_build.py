import os
import requests

with open("build.log", "r", errors="ignore") as f:
    log = f.read()[-5000:]

prompt = f"""
Analyze this Maven build failure.

Give:
1. Root cause
2. File causing issue
3. Suggested fix

Log:
{log}
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={os.environ['GEMINI_API_KEY']}"

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}

response = requests.post(url, json=payload)

print("\n===== AI ANALYSIS =====\n")
print(response.json()["candidates"][0]["content"]["parts"][0]["text"])
