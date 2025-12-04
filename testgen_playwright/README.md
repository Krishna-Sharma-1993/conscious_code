# AI-Driven Playwright Test Case Generator

This repository is a starter skeleton for an **AI-Driven Test Case Generator & Executor** using **Playwright (Python)** and **LLMs (OpenAI / Claude / Gemini)**.

## Project Overview

**Goal:** Generate, execute, evaluate, and self-heal UI test cases using LLMs.

Core components:
- `generator.py` — Generate test cases (JSON) from prompts or product docs using LLM APIs.
- `runner.py` — Execute the generated test cases using Playwright (Python).
- `healer.py` — Attempt automatic selector healing on failures using LLM.
- `utils.py` — Common helpers (reporting, screenshots, JSON I/O).
- `examples/` — Example test case JSON and demo data.
- `.github/workflows/ci.yml` — Example CI pipeline to run tests and report.

## Quickstart (local)

1. Clone this repo:
#bash
git clone <repo>
cd testgen_playwright

2. Create a virtual environment and install:
#bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Set environment variables (example for OpenAI):
#bash
export OPENAI_API_KEY="<your_openai_api_key>"
# If using Claude/Gemini, set the respective keys/endpoints

4. Generate tests (example):
#bash
python src/generator.py --url https://example.com --out examples/generated_tests.json

5. Run tests:
#bash
python src/runner.py --input examples/generated_tests.json --report reports/report.html

6. View reports in reports/.
