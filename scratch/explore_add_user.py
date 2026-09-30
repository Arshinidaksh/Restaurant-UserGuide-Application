import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.join(os.path.abspath("project"), "screens")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    # 1920x1000 aspect ratio matches PC screen monitor area
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

    print("2. Navigating to https://app.restaurant-pos.isarva.in/settings/users...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/settings/users', timeout=30000)
    page.wait_for_timeout(3000)

    print("Current URL:", page.url, flush=True)

    # Find and click "+ Add User" or "Add User" button
    add_btn = page.locator('button:has-text("Add User"), button:has-text("+ Add User"), button:has-text("Add user")').first
    if add_btn.count() > 0:
        print("Clicking Add User button...", flush=True)
        add_btn.click()
        page.wait_for_timeout(2000)
    else:
        print("Searching all buttons...", flush=True)
        for b in page.locator('button').all():
            txt = b.inner_text().strip().replace('\n', ' ')
            if 'user' in txt.lower():
                print("Found candidate button:", txt)
                b.click()
                page.wait_for_timeout(2000)
                break

    # Inspect inputs inside the dialog/modal
    inputs = page.locator('input').all()
    print(f"Total inputs on page/modal: {len(inputs)}")
    for i, inp in enumerate(inputs):
        placeholder = inp.get_attribute('placeholder') or ''
        name = inp.get_attribute('name') or ''
        val = inp.input_value()
        print(f"Input {i}: name='{name}', placeholder='{placeholder}', val='{val}'")

    # Let's inspect all text and labels
    modal = page.locator('div[role="dialog"], .modal, div:has-text("Add User"), div:has-text("User Details")').last
    print("Modal text sample:\n", modal.inner_text()[:400] if modal.count() > 0 else "No modal found")

    screenshot_path = os.path.join(OUT_DIR, 'test_users_modal.jpg')
    page.screenshot(path=screenshot_path, quality=95)
    print("Test screenshot saved to:", screenshot_path, flush=True)

    browser.close()
