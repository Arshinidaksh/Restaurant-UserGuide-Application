import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

SCREENS_DIR = os.path.join(os.path.abspath("project"), "screens_v2")
os.makedirs(SCREENS_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    print("1. Opening POS landing page...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2500)
    page.screenshot(path=os.path.join(SCREENS_DIR, '01_activate_pos.jpg'), quality=95)

    # Activate
    page.locator('input').first.fill('C001')
    page.locator('button:has-text("Activate")').click()
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(SCREENS_DIR, '02_admin_login.jpg'), quality=95)

    # Login
    inputs = page.locator('input').all()
    inputs[0].fill('admin')
    inputs[1].fill('0000')
    page.locator('button:has-text("OK")').click()
    page.wait_for_timeout(3500)
    page.screenshot(path=os.path.join(SCREENS_DIR, '03_main_dashboard.jpg'), quality=95)
    print("Logged in successfully.", flush=True)

    # 2. Click Dine In
    print("Navigating to Dine In / Floor Map...", flush=True)
    # The Dine In button is in the Service section
    dine_in_btn = page.locator('text=Dine In').first
    dine_in_btn.click()
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(SCREENS_DIR, '04_dine_in_floor_map.jpg'), quality=95)
    print("Captured 04_dine_in_floor_map.jpg", flush=True)

    # Let's see what's on this screen
    body_text = page.inner_text('body')
    print("Screen text sample after Dine In:\n", body_text[:400], flush=True)

    # Let's look for tables or order items
    # Check if there are tables to click
    table_buttons = page.locator('button:has-text("Table"), button:has-text("T"), div:has-text("Table")').all()
    print(f"Table candidate elements: {len(table_buttons)}", flush=True)
    for tb in table_buttons[:6]:
        print("Candidate:", tb.inner_text().strip().replace('\n', ' '))

    # If there's a table button, click one
    t_click = page.locator('button:has-text("Table 1"), button:has-text("Table"), div[role="button"]:has-text("Table")')
    if t_click.count() > 0:
        print("Clicking table...", flush=True)
        t_click.first.click()
        page.wait_for_timeout(3000)
        page.screenshot(path=os.path.join(SCREENS_DIR, '05_order_menu_screen.jpg'), quality=95)
        print("Captured 05_order_menu_screen.jpg", flush=True)
        print("Screen text after clicking table:\n", page.inner_text('body')[:500], flush=True)
    else:
        # Check all clickable elements on this floor view
        all_buttons = page.locator('button').all()
        print("All buttons on floor view:", len(all_buttons))
        for i, b in enumerate(all_buttons[:15]):
            print(f"Btn {i}:", b.inner_text().strip().replace('\n', ' '))

    browser.close()
