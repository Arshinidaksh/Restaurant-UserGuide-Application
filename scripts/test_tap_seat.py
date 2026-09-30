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

    # Dine In
    page.locator('text=Dine In').first.click()
    page.wait_for_timeout(2500)

    # Click "Tap to seat" on Table 02 or any empty table
    print("Clicking Tap to seat button...", flush=True)
    tap_seat_btn = page.locator('button:has-text("Tap to seat"), a:has-text("Tap to seat"), div:has-text("Tap to seat")').first
    tap_seat_btn.click()
    page.wait_for_timeout(3000)

    page.screenshot(path=os.path.join(SCREENS_DIR, '05_food_menu_and_ticket.jpg'), quality=95)
    print("Captured 05_food_menu_and_ticket.jpg", flush=True)
    print("URL after seating:", page.url, flush=True)
    print("Screen text:\n", page.inner_text('body')[:600], flush=True)

    browser.close()
