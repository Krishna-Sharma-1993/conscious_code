
"""
generator.py
Generate Playwright-compatible test cases (JSON) using an LLM API.
This is a minimal, clear template — replace the LLM client with your provider if needed.
"""
import os
import json
import argparse
from typing import List, Dict

# Using OpenAI as the default LLM provider in this template
try:
    import openai
except Exception:
    openai = None

SYSTEM_PROMPT = """You are an expert QA engineer. Given a URL or product description, generate a small set (3-8) of end-to-end test cases in JSON.
Each test case must include:
- title (string)
- priority (High/Medium/Low)
- steps: list of actions in order. Each step is an object with:
    - action: one of goto, click, fill, select, expect_visible, expect_text
    - selector: CSS selector (Playwright compatible) or blank (LLM may suggest)
    - value: optional value
- expected_result: string
Return only JSON array in your final output.
"""

def call_openai(prompt: str, max_tokens=800) -> str:
    if not openai:
        raise RuntimeError("openai package not installed")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.2
    )
    return resp["choices"][0]["message"]["content"].strip()

def generate_from_url(url: str) -> List[Dict]:
    prompt = f"Generate test cases for the web application: {url}. Produce JSON only."
    raw = call_openai(prompt)
    # Try to parse JSON from the model output
    try:
        data = json.loads(raw)
    except Exception:
        # fallback: attempt to extract json block
        start = raw.find('[')
        end = raw.rfind(']')
        data = json.loads(raw[start:end+1])
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--out", default="examples/generated_tests.json")
    args = parser.parse_args()

    tests = generate_from_url(args.url)
    Path = __import__('pathlib').Path
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, 'w') as f:
        json.dump(tests, f, indent=2)
    print(f"Wrote {len(tests)} tests to {args.out}")

if __name__ == '__main__':
    main()
