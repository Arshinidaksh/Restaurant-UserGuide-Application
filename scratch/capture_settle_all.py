import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.join(os.path.abspath("project"), "screens_part_e")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    print("Navigating to POS...")
    page.goto("https://app.restaurant-pos.isarva.in/", timeout=30000)
    page.wait_for_timeout(3000)

    # Login
    if page.locator('button:has-text("OK")').count() > 0 or page.locator('button:has-text("Sign in")').count() > 0:
        inputs = page.locator("input").all()
        if len(inputs) >= 2:
            inputs[0].fill("admin")
            inputs[1].fill("0000")
        page.locator('button:has-text("OK"), button:has-text("Sign in")').first.click()
        page.wait_for_timeout(3500)

    print("Opening Dine In...")
    page.locator("text=Dine In").first.click()
    page.wait_for_timeout(2500)

    # Table 01
    page.locator("text=Table 01").first.click()
    page.wait_for_timeout(2000)
    if page.locator('button:has-text("Open with")').count() > 0:
        page.locator('button:has-text("Open with")').click()
        page.wait_for_timeout(2000)

    # 1. Main Settle Screen
    page.locator('button:has-text("Settle")').last.click()
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(OUT_DIR, "E01_settle_modal.jpg"))
    print("Saved E01_settle_modal.jpg")

    # 2. Food Voucher view
    if page.locator('button:has-text("Food Voucher")').count() > 0:
        page.locator('button:has-text("Food Voucher")').click()
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(OUT_DIR, "E05_food_voucher.jpg"))
        print("Saved E05_food_voucher.jpg")
        # Close voucher or go back if cancel exists
        if page.locator('button:has-text("Cancel"), button:has-text("Back"), button:has-text("Close")').count() > 0:
            page.locator('button:has-text("Cancel"), button:has-text("Back"), button:has-text("Close")').first.click()
            page.wait_for_timeout(1000)

    # 3. Card view
    if page.locator('button:has-text("Card")').count() > 0:
        page.locator('button:has-text("Card")').click()
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(OUT_DIR, "E08_card_options.jpg"))
        print("Saved E08_card_options.jpg")
        if page.locator('button:has-text("Cancel"), button:has-text("Back"), button:has-text("Close")').count() > 0:
            page.locator('button:has-text("Cancel"), button:has-text("Back"), button:has-text("Close")').first.click()
            page.wait_for_timeout(1000)

    # 4. Split bill view
    if page.locator('button:has-text("Split bill")').count() > 0:
        page.locator('button:has-text("Split bill")').click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, "E03_split_equal.jpg"))
        print("Saved E03_split_equal.jpg")

        # Custom split tab
        if page.locator('button:has-text("Custom"), [role="tab"]:has-text("Custom"), div:has-text("Custom")').count() > 0:
            page.locator('button:has-text("Custom"), [role="tab"]:has-text("Custom"), div:has-text("Custom")').first.click()
            page.wait_for_timeout(1500)
            page.screenshot(path=os.path.join(OUT_DIR, "E04_split_custom.jpg"))
            print("Saved E04_split_custom.jpg")

    browser.close()
    print("Capture complete!")
