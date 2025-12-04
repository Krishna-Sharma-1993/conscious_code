"""
runner.py
Execute JSON-formatted test cases using Playwright (sync API).
Each step supports basic actions: goto, click, fill, select, expect_visible, expect_text.
"""
import json
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright
from datetime import datetime
import os

def run_test_case(page, test):
    title = test.get("title")
    for step in test.get("steps", []):
        action = step.get("action")
        sel = step.get("selector") or None
        val = step.get("value")
        if action == "goto":
            page.goto(val, timeout=30000)
        elif action == "click":
            page.click(sel, timeout=10000)
        elif action == "fill":
            page.fill(sel, val, timeout=10000)
        elif action == "select":
            page.select_option(sel, val)
        elif action == "expect_visible":
            page.wait_for_selector(sel, timeout=10000)
        elif action == "expect_text":
            text = page.text_content(sel)
            assert val in (text or ""), f"Expected text '{val}' in selector {sel}"
        else:
            print(f"Unknown action: {action}")
    return True

def take_screenshot(page, out_dir, name):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    path = Path(out_dir) / f"{name}.png"
    page.screenshot(path=path, full_page=True)
    return str(path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON test file")
    parser.add_argument("--report", default="reports/report.html", help="HTML report output")
    args = parser.parse_args()

    with open(args.input) as f:
        tests = json.load(f)

    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        for i, test in enumerate(tests):
            result = {"title": test.get("title"), "status": "PASS", "errors": [], "screenshot": None}
            try:
                run_test_case(page, test)
            except Exception as e:
                result["status"] = "FAIL"
                result["errors"].append(str(e))
                screenshot = take_screenshot(page, "reports/screenshots", f"test_{i}_{int(datetime.utcnow().timestamp())}")
                result["screenshot"] = screenshot
            results.append(result)
        browser.close()

    # Simple HTML report
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    with open(args.report, 'w') as f:
        f.write('<html><body>')
        f.write('<h1>Test Report</h1>')
        for r in results:
            f.write(f"<h2>{r['title']} - {r['status']}</h2>")
            if r['errors']:
                f.write('<pre>' + '\\n'.join(r['errors']) + '</pre>')
            if r['screenshot']:
                f.write(f"<img src='{r['screenshot']}' style='max-width:600px;'/>")

        f.write('</body></html>')
    print(f"Report written to {args.report}")

if __name__ == '__main__':
    main()
