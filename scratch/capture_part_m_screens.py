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

    # Modules to click
    modules = [
        ("M1", "Receipt Printer", "M1_receipt_printer.jpg"),
        ("M2", "KOT Printer", "M2_kot_printer.jpg"),
        ("M3", "Printer Mapping", "M3_printer_mapping.jpg"),
        ("M4", "Print designs", "M4_print_designs.jpg"),
    ]

    for code, title, out_name in modules:
        page.goto('https://app.restaurant-pos.isarva.in/settings?tab=printer', timeout=30000)
        page.wait_for_timeout(1500)

        tile = page.locator(f'div:has-text("{title}")').filter(has_text=title).last
        if tile.count() > 0:
            print(f"Clicking {title}...")
            tile.click()
            page.wait_for_timeout(2000)
            print(f"  URL after click: {page.url}")
            # wait 3s for any toast to disappear
            page.wait_for_timeout(3000)
            page.screenshot(path=f"project/screens_part_m/{out_name}")
            print(f"  Saved {out_name}")

    browser.close()
