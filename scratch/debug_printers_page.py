import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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

    # Go to settings/printers directly
    page.goto('https://app.restaurant-pos.isarva.in/settings/printers', timeout=30000)
    page.wait_for_timeout(2000)
    print("Direct /settings/printers URL:", page.url)

    # Let's inspect all tabs / buttons on this page
    print("Tabs/cards on page:")
    cards = page.locator('div.cursor-pointer, button, div[role="tab"]').all()
    for c in cards:
        t = c.inner_text().strip().replace('\n', ' ')
        if len(t) > 0 and len(t) < 50:
            print("  -", t)

    browser.close()
