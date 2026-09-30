import sys
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)
    if page.locator('button:has-text("Activate")').count() > 0:
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(2500)
    if page.locator('button:has-text("OK")').count() > 0:
        inputs = page.locator('input').all()
        inputs[0].fill('admin')
        inputs[1].fill('0000')
        page.locator('button:has-text("OK")').click()
        page.wait_for_timeout(3000)
    page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
    page.wait_for_timeout(2000)

    # Click each left tab in settings to see what they contain
    tabs = ['Printer', 'Catalog', 'User', 'Accounts', 'Ingredients', 'Inventory', 'Database']
    for tab in tabs:
        btn = page.locator(f'button:has-text("{tab}"), div:has-text("{tab}")').filter(has_text=tab).first
        if btn.count() > 0:
            print(f'Tab {tab}: visible')

    # Also search for 'POS Web' or other cards
    print("All tiles in Settings:")
    tiles = page.locator('div.rounded-2xl, div.rounded-xl, div.shadow-sm').all()
    for t in tiles:
        text = t.inner_text().strip().replace('\n', ' ')
        if len(text) > 0 and len(text) < 60:
            print("  Tile:", text)

    browser.close()
