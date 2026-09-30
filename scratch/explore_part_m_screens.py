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

    # Go to settings
    page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
    page.wait_for_timeout(2000)

    # Click 'Printer' tab on left sidebar
    printer_tab = page.locator('button:has-text("Printer"), div:has-text("Printer")').filter(has_text="Printer").first
    print("Printer tab locator count:", printer_tab.count())
    if printer_tab.count() > 0:
        printer_tab.click()
        page.wait_for_timeout(2000)
        print("Printer page URL:", page.url)
        page.screenshot(path='project/screens_part_m/printer_home.jpg')

        # List all buttons/cards/links on this page
        print("Buttons/Links on Printer page:")
        elements = page.locator('button, a, div[role="button"], div.cursor-pointer').all()
        for el in elements:
            txt = el.inner_text().strip().replace('\n', ' ')
            if txt and len(txt) < 80:
                print("  -", txt)

    # Also check direct routes like /settings/printer, /settings/printers, /settings/printer-mapping
    for route in ['/settings/printer', '/settings/printers', '/settings/printer-mapping', '/settings/kot-printer', '/settings/print-templates']:
        page.goto('https://app.restaurant-pos.isarva.in' + route, timeout=10000)
        page.wait_for_timeout(800)
        print(f"Route {route} -> {page.url}")

    browser.close()
