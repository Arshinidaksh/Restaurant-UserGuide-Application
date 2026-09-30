import os
import sys
import time
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.join(os.path.abspath("project"), "screens_part_e")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    print("Navigating to POS...")
    page.goto("https://app.restaurant-pos.isarva.in/", timeout=30000)
    page.wait_for_timeout(3000)

    # Activate
    if page.locator("input").count() > 0 and page.locator('button:has-text("Activate")').count() > 0:
        print("Activating till...")
        page.locator("input").first.fill("C001")
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(3000)

    # Login
    if page.locator('button:has-text("OK")').count() > 0 or page.locator('button:has-text("Sign in")').count() > 0:
        print("Logging in...")
        inputs = page.locator("input").all()
        if len(inputs) >= 2:
            inputs[0].fill("admin")
            inputs[1].fill("0000")
        page.locator('button:has-text("OK"), button:has-text("Sign in")').first.click()
        page.wait_for_timeout(3500)

    print("Opening Dine In...")
    page.locator("text=Dine In").first.click()
    page.wait_for_timeout(2500)

    # Click Table 01
    print("Opening Table 01...")
    page.locator("text=Table 01").first.click()
    page.wait_for_timeout(2000)

    if page.locator('button:has-text("Open with")').count() > 0:
        page.locator('button:has-text("Open with")').click()
        page.wait_for_timeout(2000)

    # Check if empty, add item if needed
    if page.locator("text=Roti & Curry").count() > 0:
        page.locator("text=Roti & Curry").first.click()
        page.wait_for_timeout(1000)

    # Click Settle
    print("Clicking Settle...")
    page.locator('button:has-text("Settle")').last.click()
    page.wait_for_timeout(2500)

    page.screenshot(path=os.path.join(OUT_DIR, "E01_settle_main.jpg"))
    print("Saved E01_settle_main.jpg")

    # Let's inspect buttons inside Settle
    buttons = page.locator("button").all_inner_texts()
    print("Buttons on page:", [b.strip() for b in buttons if b.strip()])

    # Check for Split bill or tabs
    split_btn = page.locator('button:has-text("Split bill"), button:has-text("Split")')
    if split_btn.count() > 0:
        print("Clicking Split bill...")
        split_btn.first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, "E02_split_view.jpg"))
        print("Saved E02_split_view.jpg")
        print("Buttons in split:", [b.strip() for b in page.locator("button").all_inner_texts() if b.strip()])

    browser.close()
