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

    # Let's inspect header connection status
    print("Checking header...", flush=True)
    header_text = page.locator('header, div.header, div:has-text("Connected")').first.inner_text() if page.locator('header, div.header, div:has-text("Connected")').count() > 0 else ""
    print("Header snippet:", header_text[:200])

    # 1. Open one test table or takeaway order
    # Let's check Quick Serve or Takeaway or Dine In
    # Quick Serve is fastest to add items and settle:
    print("Testing Quick Serve / Takeaway...", flush=True)
    qs_btn = page.locator('text=Quick Serve').first
    if qs_btn.count() > 0:
        qs_btn.click()
        page.wait_for_timeout(3000)
        print("Opened Quick Serve. URL:", page.url)

    # Inspect food items on screen
    food_items = page.locator('button:has-text("SAR"), div:has-text("SAR")').all()
    print("Found food items count:", len(food_items))

    # Click first 2 food items to add to order
    food_btns = page.locator('button:has-text("SAR")').all()
    if len(food_btns) >= 2:
        print("Clicking food item 1...", flush=True)
        food_btns[0].click()
        page.wait_for_timeout(1000)
        print("Clicking food item 2...", flush=True)
        food_btns[1].click()
        page.wait_for_timeout(1000)
    elif len(food_items) >= 2:
        food_items[0].click()
        page.wait_for_timeout(1000)
        food_items[1].click()
        page.wait_for_timeout(1000)

    # Inspect action buttons (KOT, Save, Settle, etc.)
    all_btns = page.locator('button').all()
    print("All buttons on screen:")
    for i, b in enumerate(all_btns):
        txt = b.inner_text().strip().replace('\n', ' ')
        if any(k in txt.lower() for k in ['kot', 'settle', 'pay', 'cash', 'save']):
            print(f"Btn {i}: {txt}")

    # Look for Settle or Pay button
    settle_btn = page.locator('button:has-text("Settle"), button:has-text("Pay")').first
    if settle_btn.count() > 0:
        print("Clicking Settle...", flush=True)
        settle_btn.click()
        page.wait_for_timeout(2500)

    print("Screen text after Settle:\n", page.inner_text('body')[:500])

    page.screenshot(path=os.path.join(OUT_DIR, 'test_settle_view.jpg'), quality=95)
    print("Captured test_settle_view.jpg")

    browser.close()
