import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.join(os.path.abspath("project"), "screens_parts_fk")

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})

    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)
    # Activate & login
    page.locator('input').first.fill('C001')
    page.locator('button:has-text("Activate")').click()
    page.wait_for_timeout(2500)
    inputs = page.locator('input').all()
    inputs[0].fill('admin')
    inputs[1].fill('0000')
    page.locator('button:has-text("OK")').click()
    page.wait_for_timeout(3000)

    # 1. Click KOT in sidebar
    print("Navigating to KOT...")
    kot_nav = page.locator('text=KOT').first
    kot_nav.click()
    page.wait_for_timeout(3000)
    print("KOT URL:", page.url)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "H_kitchen_kot_live.jpg"), quality=95)

    # 2. Check Delivery -> Riders or Rider App
    print("Navigating to Delivery...")
    page.goto('https://app.restaurant-pos.isarva.in/delivery', timeout=30000)
    page.wait_for_timeout(2000)
    # check for Rider app button or Riders button
    rider_btns = page.locator('button:has-text("Rider"), a:has-text("Rider")').all()
    print("Rider buttons found:", len(rider_btns))
    for rb in rider_btns:
        print("  Rider btn:", rb.inner_text().strip())
    # Click Rider app or Riders
    if page.locator('text=Riders').count() > 0:
        page.locator('text=Riders').first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "I_delivery_riders_view.jpg"), quality=95)
    
    # 3. Check Accounts -> Day close
    print("Navigating to Accounts...")
    page.goto('https://app.restaurant-pos.isarva.in/accounts', timeout=30000)
    page.wait_for_timeout(2000)
    # find Day close tab or button
    dc_btns = page.locator('text=Day close, text=Day Close, button:has-text("Day"), a:has-text("Day")').all()
    print("Day close elements:", len(dc_btns))
    for dc in dc_btns:
        print("  Day close elem:", dc.inner_text().strip())
    if page.locator('text=Day close').count() > 0:
        page.locator('text=Day close').first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "J_day_close_live.jpg"), quality=95)
    else:
        page.screenshot(path=os.path.join(OUTPUT_DIR, "J_day_close_live.jpg"), quality=95)

    # 4. Check Settings
    print("Navigating to Settings...")
    page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
    page.wait_for_timeout(2500)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "K_settings_live.jpg"), quality=95)
    # Check tabs or categories
    tabs = page.locator('div[role="tab"], button, div:has-text("Business")').all()
    print("Settings tabs count:", len(tabs))
    page.screenshot(path=os.path.join(OUTPUT_DIR, "K_settings_live.jpg"), quality=95)

    browser.close()
    print("Done deep exploration.")
