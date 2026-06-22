import os
import time

try:
    import google.generativeai as genai
except ImportError:
    print("google-generativeai package not installed")
    raise

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("GEMINI_API_KEY not found")
    exit(1)

genai.configure(api_key=API_KEY)

# Read build log
try:
    with open("build.log", "r", errors="ignore") as f:
        build_log = f.read()[-5000:]
except Exception as e:
    print(f"Unable to read build.log: {e}")
    exit(1)

prompt = f"""
Analyze this Maven build failure.

Provide:
1. Root Cause
2. File causing issue
3. Suggested Fix

Build Log:

{build_log}
"""

attempts = 3
backoff = 2

for attempt in range(1, attempts + 1):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        response = model.generate_content(
            prompt,
            request_options={"timeout": 30}
        )

        print("\n")
        print("=" * 60)
        print("GEMINI ANALYSIS")
        print("=" * 60)
        print(response.text)
        print("=" * 60)

        exit(0)

    except Exception as e:
        msg = str(e)

        print(f"Attempt {attempt} failed: {msg}")

        transient = (
            "high demand" in msg.lower()
            or "resource exhausted" in msg.lower()
            or "timeout" in msg.lower()
            or "timed out" in msg.lower()
            or "504" in msg
        )

        if transient and attempt < attempts:
            print(f"Retrying in {backoff} seconds...")
            time.sleep(backoff)
            backoff *= 2
            continue

        print("\n")
        print("=" * 60)
        print("GEMINI ANALYSIS FAILED")
        print("=" * 60)
        print(msg)
        print("=" * 60)
        exit(1)
