import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.abspath("project"), "screens_parts_fk")

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    # Let's test standard desktop and mobile viewports for rider
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)
    page.locator('input').first.fill('C001')
    page.locator('button:has-text("Activate")').click()
    page.wait_for_timeout(3000)
    page.wait_for_selector('input', timeout=10000)
    inputs = page.locator('input').all()
    if len(inputs) > 1:
        inputs[0].fill('admin')
        inputs[1].fill('0000')
        page.locator('button:has-text("OK")').click()
        page.wait_for_timeout(3000)

    print("Navigating to /rider...")
    page.goto('https://app.restaurant-pos.isarva.in/rider', timeout=30000)
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "I_rider_screen_desktop.jpg"), quality=95)
    print("Captured desktop rider screen.")

    # Also mobile rider context
    page_mobile = browser.new_page(viewport={'width': 414, 'height': 896}) # iPhone XR size
    page_mobile.goto('https://app.restaurant-pos.isarva.in/rider', timeout=30000)
    page_mobile.wait_for_timeout(3000)
    page_mobile.screenshot(path=os.path.join(OUTPUT_DIR, "I_rider_screen_mobile.jpg"), quality=95)
    print("Captured mobile rider screen.")

    browser.close()
    print("Done.")
