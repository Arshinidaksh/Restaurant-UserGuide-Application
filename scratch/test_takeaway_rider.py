import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.abspath("project"), "screens_parts_fk")

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})

    # Activate & login
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

    # 1. Takeaway
    print("Testing Takeaway...")
    page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
    page.wait_for_timeout(2500)
    # Let's find all clickable elements in the queue
    queue_items = page.locator('text=#5').all()
    print("Queue items for #5:", len(queue_items))
    if queue_items:
        queue_items[0].click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "F_takeaway_ticket_open.jpg"), quality=95)
        print("Captured F_takeaway_ticket_open.jpg")

    # 2. Delivery - Rider app button
    print("Testing Delivery Rider app...")
    page.goto('https://app.restaurant-pos.isarva.in/delivery', timeout=30000)
    page.wait_for_timeout(2500)
    # Check if there is a Rider app button
    ra_btn = page.locator('button:has-text("Rider app"), a:has-text("Rider app")').first
    if ra_btn.count() > 0:
        print("Found Rider app button, clicking...")
        # might open popup or navigate
        with page.expect_popup() as popup_info:
            try:
                ra_btn.click(timeout=3000)
                popup = popup_info.value
                popup.wait_for_timeout(2000)
                popup.screenshot(path=os.path.join(OUTPUT_DIR, "I_rider_app_popup.jpg"), quality=95)
                print("Captured rider popup:", popup.url)
            except Exception as e:
                print("No popup, check page URL:", page.url)
                page.screenshot(path=os.path.join(OUTPUT_DIR, "I_rider_app_page.jpg"), quality=95)

    browser.close()
    print("Done testing.")
