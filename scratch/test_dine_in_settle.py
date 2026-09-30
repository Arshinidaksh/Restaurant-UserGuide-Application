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

    # Wait for header connection status to be Connected
    print("Waiting for status Connected...", flush=True)
    for _ in range(20):
        h_text = page.locator('body').inner_text()
        if "Connected" in h_text and "Syncing" not in h_text:
            print("Connected verified!", flush=True)
            break
        page.wait_for_timeout(1000)

    # 1. Open Dine In floor
    print("Clicking Dine In...", flush=True)
    page.locator('text=Dine In').first.click()
    page.wait_for_timeout(3000)

    # Click on Table 01 (which is Occupied) or Table 02
    print("Clicking Table 01...", flush=True)
    page.locator('text=Table 01').first.click()
    page.wait_for_timeout(3000)

    # Check if modal opened
    print("Modal opened. Clicking Settle button...", flush=True)
    settle_btn = page.locator('button:has-text("Settle")').last
    settle_btn.click()
    page.wait_for_timeout(2500)

    # Inside Settle window
    print("Settle window opened. Looking for Cash buttons...", flush=True)
    print("Text in settle:\n", page.locator('body').inner_text()[:600])

    # Click Cash or Rest -> Cash
    cash_choice = page.locator('button:has-text("Rest → Cash"), button:has-text("Rest -> Cash"), button:has-text("Cash")').first
    if cash_choice.count() > 0:
        print("Clicking Cash option...", flush=True)
        cash_choice.click()
        page.wait_for_timeout(1500)

    # Click Confirm or Settle to finish payment
    confirm_pay = page.locator('button:has-text("Confirm split"), button:has-text("Confirm"), button:has-text("Settle"), button:has-text("Pay")').last
    print("Clicking Confirm payment...", flush=True)
    confirm_pay.click()
    page.wait_for_timeout(3000)

    print("Post-settle text:\n", page.locator('body').inner_text()[:800], flush=True)

    screenshot_path = os.path.join(OUT_DIR, '20_settle_receipt_screen.jpg')
    page.screenshot(path=screenshot_path, quality=95)
    print("Screenshot saved to:", screenshot_path, flush=True)

    browser.close()
