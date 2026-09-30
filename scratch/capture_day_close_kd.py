import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "project", "screens_parts_fk")

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
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

    # Click Day Close on Home
    print("Looking for Day Close button on Home...")
    dc = page.locator('button:has-text("Day Close"), div[role="button"]:has-text("Day Close")').first
    if dc.count() > 0:
        dc.click()
        page.wait_for_timeout(2500)
        print("URL after Day Close:", page.url)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "J_day_close_modal.jpg"), quality=95)
    
    # Go back home and click Kitchen Display
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)
    kd = page.locator('button:has-text("Kitchen Display"), div[role="button"]:has-text("Kitchen Display")').first
    if kd.count() > 0:
        kd.click()
        page.wait_for_timeout(2500)
        print("URL after Kitchen Display:", page.url)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "H_kitchen_display_modal.jpg"), quality=95)

    browser.close()
    print("Done.")
