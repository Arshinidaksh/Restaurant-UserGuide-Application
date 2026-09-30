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

    print("Opening Add user modal...", flush=True)
    plus_btn = page.locator('button:has-text("+")')
    if plus_btn.count() > 0:
        plus_btn.first.click()
    page.wait_for_timeout(2000)

    # Fill "Staff User" in NAME field
    print("Filling Name: Staff User...", flush=True)
    inputs = page.locator('input').all()
    if len(inputs) > 0:
        inputs[0].fill('Staff User')
    page.wait_for_timeout(1000)

    # Click AR auto button / label
    print("Clicking AR auto button...", flush=True)
    ar_btn = page.locator('text=AR auto').first
    if ar_btn.count() > 0:
        ar_btn.click()
        page.wait_for_timeout(2000)

    # Check input values
    for i, inp in enumerate(page.locator('input').all()):
        print(f"Input {i}: val='{inp.input_value()}'")

    screenshot_path = os.path.join(OUT_DIR, '18_users_add_staff_user.jpg')
    page.screenshot(path=screenshot_path, quality=95)
    print("Screenshot saved to:", screenshot_path, flush=True)

    browser.close()
