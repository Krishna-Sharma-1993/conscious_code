"""
healer.py
A minimal template for attempting selector 'self-heal' using LLM suggestions.
You supply the failed selector and a DOM snapshot; the LLM suggests an alternative selector.
"""
import os
import json
try:
    import openai
except Exception:
    openai = None

PROMPT_TEMPLATE = """You are a QA automation expert. Suggest a more robust CSS selector for the target element in the given DOM snippet.
Failed selector: {selector}
DOM snippet:
{dom}
Return only the suggested CSS selector as a single-line string.
"""

def suggest_selector(selector: str, dom: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    prompt = PROMPT_TEMPLATE.format(selector=selector, dom=dom[:8000])
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=64,
        temperature=0.0
    )
    return resp["choices"][0]["message"]["content"].strip()
