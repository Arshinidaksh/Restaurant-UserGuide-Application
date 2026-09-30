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

    # 1. Takeaway: click ticket #5 or + New ticket
    print("Testing Takeaway...")
    page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
    page.wait_for_timeout(2000)
    # Click ticket #5 or open ticket
    ticket_btn = page.locator('button:has-text("#5"), div:has-text("#5")').first
    if ticket_btn.count() > 0:
        ticket_btn.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "F_takeaway_active_ticket.jpg"), quality=95)
        print("Captured F_takeaway_active_ticket.jpg")

    # 2. Kitchen KOT: let's send a quick KOT or see if an order can be sent
    # Let's create an order on takeaway or dine in and click KOT
    print("Creating order for KOT...")
    page.goto('https://app.restaurant-pos.isarva.in/floor', timeout=30000)
    page.wait_for_timeout(2000)
    # Click Table 02 or Table 03
    t_btn = page.locator('text=Table 02, text=Table 2').first
    if t_btn.count() > 0:
        t_btn.click()
        page.wait_for_timeout(2000)
        # Add food items
        add_btns = page.locator('button:has-text("+"), button:has-text("SAR")').all()
        if len(add_btns) > 0:
            add_btns[0].click()
            page.wait_for_timeout(500)
            if len(add_btns) > 1:
                add_btns[1].click()
                page.wait_for_timeout(500)
        # Click KOT button
        kot_send = page.locator('button:has-text("Send KOT"), button:has-text("KOT")').first
        if kot_send.count() > 0:
            kot_send.click()
            page.wait_for_timeout(1500)
    
    # Now check kitchen screen
    page.goto('https://app.restaurant-pos.isarva.in/kitchen', timeout=30000)
    page.wait_for_timeout(2500)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "H_kitchen_kot_with_orders.jpg"), quality=95)
    print("Captured H_kitchen_kot_with_orders.jpg")

    # 3. Delivery -> Rider App
    print("Testing Delivery Rider App...")
    page.goto('https://app.restaurant-pos.isarva.in/delivery', timeout=30000)
    page.wait_for_timeout(2000)
    rider_app_btn = page.locator('button:has-text("Rider app")').first
    if rider_app_btn.count() > 0:
        rider_app_btn.click()
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "I_delivery_rider_app_modal.jpg"), quality=95)
        print("Captured I_delivery_rider_app_modal.jpg, URL:", page.url)

    # 4. Accounts -> Day close
    print("Testing Accounts Day close...")
    page.goto('https://app.restaurant-pos.isarva.in/accounts', timeout=30000)
    page.wait_for_timeout(2000)
    # Click Day Close tile
    dc_tile = page.locator('text=Day Close').first
    if dc_tile.count() > 0:
        dc_tile.click()
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "J_day_close_screen.jpg"), quality=95)
        print("Captured J_day_close_screen.jpg, URL:", page.url)

    browser.close()
    print("All captures completed.")
