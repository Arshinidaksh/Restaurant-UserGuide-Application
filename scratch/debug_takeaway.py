import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.join(os.path.abspath("project"), "screens")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    # Viewport 1920x1000 for PC frame
    context = browser.new_context(viewport={'width': 1920, 'height': 1000})
    page = context.new_page()

    print("1. Opening POS landing page...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2500)

    # Check if activation is needed
    if page.locator('input').count() > 0 and page.locator('button:has-text("Activate")').count() > 0:
        print("Activating C001...", flush=True)
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(3000)

    # Login if needed
    if page.locator('button:has-text("OK")').count() > 0 or page.locator('button:has-text("Sign in")').count() > 0:
        print("Logging in admin...", flush=True)
        inputs = page.locator('input').all()
        if len(inputs) >= 2:
            inputs[0].fill('admin')
            inputs[1].fill('0000')
        btn = page.locator('button:has-text("OK"), button:has-text("Sign in")').first
        btn.click()
        page.wait_for_timeout(3500)

    print("Navigating to Takeaway...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
    page.wait_for_timeout(3000)

    page.screenshot(path=os.path.join(OUT_DIR, 'debug_takeaway.jpg'), quality=95)
    print("Takeaway URL:", page.url)
    print("Takeaway text sample:\n", page.locator('body').inner_text()[:600])

    browser.close()
