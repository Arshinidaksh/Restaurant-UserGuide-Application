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

    # Go to Dine In
    page.locator('text=Dine In').first.click()
    page.wait_for_timeout(2500)

    # 1. Capture Floor Map in Diagram View as well to see which is best
    diagram_btn = page.locator('text=Diagram')
    if diagram_btn.count() > 0:
        diagram_btn.first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(SCREENS_DIR, '04b_floor_diagram_view.jpg'), quality=95)
        print("Captured 04b_floor_diagram_view.jpg", flush=True)

    # Switch back to List
    list_btn = page.locator('text=List')
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(1500)

    # 2. Click "View Table Details" on Table 01 or "Tap to seat" on Table 02
    print("Clicking View Table Details on Table 01...", flush=True)
    table_btn = page.locator('text=View Table Details').first
    if table_btn.count() > 0:
        table_btn.click()
        page.wait_for_timeout(3000)
        page.screenshot(path=os.path.join(SCREENS_DIR, '05_active_order_ticket.jpg'), quality=95)
        print("Captured 05_active_order_ticket.jpg", flush=True)
        print("Screen text:\n", page.inner_text('body')[:500], flush=True)

    browser.close()
