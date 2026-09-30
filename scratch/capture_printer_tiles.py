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

    page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
    page.wait_for_timeout(2000)

    # Click Printer tab on left nav
    p_btn = page.locator('button:has-text("Printer")').first
    p_btn.click()
    page.wait_for_timeout(1500)

    print("Current URL:", page.url)
    tiles = page.locator('div:has-text("Receipt Printer"), div:has-text("KOT Printer"), div:has-text("Printer Mapping"), div:has-text("Print designs")').all()
    print("Found tiles:", len(tiles))

    for name, out in [("Receipt Printer", "M1_receipt_printer.jpg"),
                      ("KOT Printer", "M2_kot_printer.jpg"),
                      ("Printer Mapping", "M3_printer_mapping.jpg"),
                      ("Print designs", "M4_print_designs.jpg")]:
        # Click the tile card
        card = page.locator(f'div.rounded-2xl:has-text("{name}"), div.rounded-xl:has-text("{name}"), div.shadow-sm:has-text("{name}")').first
        if card.count() == 0:
            card = page.locator(f'text="{name}"').first
        
        print(f"Clicking {name}...")
        card.click()
        page.wait_for_timeout(2000)
        print(f"  URL: {page.url}")
        page.wait_for_timeout(2500) # wait for toast
        page.screenshot(path=f"project/screens_part_m/{out}")
        print(f"  Saved: {out}")

        # Navigate back to printer tab
        p_btn.click()
        page.wait_for_timeout(1500)

    browser.close()
