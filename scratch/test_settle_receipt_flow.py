import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.join(os.path.abspath("project"), "screens")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
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

    # Wait for header connection status to be Connected / Online
    print("Waiting for connection status to be Connected...", flush=True)
    for _ in range(15):
        h_text = page.locator('body').inner_text()
        if "Connected" in h_text and "Syncing" not in h_text:
            print("Status is now Connected!", flush=True)
            break
        page.wait_for_timeout(1000)

    print("Opening Quick Serve...", flush=True)
    page.locator('text=Quick Serve').first.click()
    page.wait_for_timeout(3000)

    # Add 2 items
    food_btns = page.locator('button:has-text("SAR")').all()
    if len(food_btns) >= 2:
        print("Adding item 1...", flush=True)
        food_btns[0].click()
        page.wait_for_timeout(1200)
        print("Adding item 2...", flush=True)
        food_btns[1].click()
        page.wait_for_timeout(1200)

    # Click Settle
    print("Clicking Settle...", flush=True)
    page.locator('button:has-text("Settle")').first.click()
    page.wait_for_timeout(2500)

    print("Modal text after clicking Settle:\n", page.inner_text('body')[:600], flush=True)
    page.screenshot(path=os.path.join(OUT_DIR, 'test_settle_modal.jpg'), quality=95)

    # Click Rest -> Cash or Cash settle
    cash_btn = page.locator('button:has-text("Rest → Cash"), button:has-text("Rest -> Cash"), button:has-text("Cash")').first
    if cash_btn.count() > 0:
        print("Found Cash button, clicking...", flush=True)
        cash_btn.click()
        page.wait_for_timeout(1500)

    # Confirm settle / Confirm pay
    confirm_btn = page.locator('button:has-text("Confirm"), button:has-text("Settle"), button:has-text("Pay")').last
    if confirm_btn.count() > 0:
        print("Clicking Confirm button...", flush=True)
        confirm_btn.click()
        page.wait_for_timeout(3000)

    print("Text after confirm:\n", page.inner_text('body')[:600], flush=True)
    page.screenshot(path=os.path.join(OUT_DIR, 'test_receipt_view.jpg'), quality=95)

    browser.close()
