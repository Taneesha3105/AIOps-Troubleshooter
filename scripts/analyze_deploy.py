import os
import time
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

with open("deploy.log", "r", errors="ignore") as f:
    deploy_log = f.read()[-5000:]

prompt = f"""
Analyze this deployment failure.

Provide:
1. Root Cause
2. Impact
3. Suggested Fix

Deployment Log:

{deploy_log}
"""

for attempt in range(3):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        response = model.generate_content(
            prompt,
            request_options={"timeout": 30}
        )

        print("\n===== DEPLOYMENT AI ANALYSIS =====\n")
        print(response.text)
        break

    except Exception as e:
        print(e)
        time.sleep(2)
