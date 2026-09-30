import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

SCREENS_DIR = os.path.join(os.path.abspath("project"), "screens_v2")

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)
    page.locator('input').first.fill('C001')
    page.locator('button:has-text("Activate")').click()
    page.wait_for_timeout(2500)
    inputs = page.locator('input').all()
    inputs[0].fill('admin')
    inputs[1].fill('0000')
    page.locator('button:has-text("OK")').click()
    page.wait_for_timeout(3000)

    # 1. Click Quick Serve
    print("Clicking Quick Serve...", flush=True)
    page.locator('text=Quick Serve').first.click()
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(SCREENS_DIR, '05_quick_serve_menu.jpg'), quality=95)
    print("Captured 05_quick_serve_menu.jpg. URL:", page.url, flush=True)
    print("Screen text:\n", page.inner_text('body')[:500], flush=True)

    browser.close()
