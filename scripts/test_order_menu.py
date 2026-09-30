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
    page.wait_for_timeout(2000)

    # Click T01
    print("Clicking T01...", flush=True)
    t01 = page.locator('text=T01, text=Table 01').first
    t01.click()
    page.wait_for_timeout(3000)

    page.screenshot(path=os.path.join(SCREENS_DIR, '05_dine_in_order_ticket.jpg'), quality=95)
    print("Captured 05_dine_in_order_ticket.jpg", flush=True)
    print("Page URL:", page.url, flush=True)
    print("Text on screen:\n", page.inner_text('body')[:600], flush=True)

    # If there's Settle button, click Settle to see the settle modal!
    settle_btn = page.locator('button:has-text("Settle"), div:has-text("Settle")')
    if settle_btn.count() > 0:
        print("Clicking Settle button...", flush=True)
        settle_btn.first.click()
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENS_DIR, '06_settle_payment_modal.jpg'), quality=95)
        print("Captured 06_settle_payment_modal.jpg", flush=True)
        print("Settle modal text:\n", page.inner_text('body')[:500], flush=True)

    browser.close()
