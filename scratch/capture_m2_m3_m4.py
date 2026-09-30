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

    # 1. M1 Receipt Printer Modal is already saved to project/screens_part_m/M1_receipt_printer_modal.jpg
    # Let's copy it to M1_receipt_printer.jpg

    # 2. M2 KOT Printer
    page.goto('https://app.restaurant-pos.isarva.in/settings/printers', timeout=30000)
    page.wait_for_timeout(2000)
    kot_tab = page.locator('div:has-text("KOT")').filter(has_text="Kitchen ticket").first
    if kot_tab.count() > 0:
        kot_tab.click()
        page.wait_for_timeout(1500)
        # click Add printer to show modal
        add_kot = page.locator('button:has-text("Add printer")').first
        if add_kot.count() > 0:
            add_kot.click()
            page.wait_for_timeout(1000)
            page.screenshot(path="project/screens_part_m/M2_kot_printer.jpg")
            print("M2 KOT modal saved!")
        else:
            page.screenshot(path="project/screens_part_m/M2_kot_printer.jpg")
            print("M2 KOT tab saved!")

    # 3. M3 Printer Mapping
    page.goto('https://app.restaurant-pos.isarva.in/settings/printers', timeout=30000)
    page.wait_for_timeout(2000)
    map_tab = page.locator('div:has-text("Mapping")').filter(has_text="Route KOT").first
    if map_tab.count() > 0:
        map_tab.click()
        page.wait_for_timeout(2000)
        page.screenshot(path="project/screens_part_m/M3_printer_mapping.jpg")
        print("M3 Mapping saved!")

    # 4. M4 Print designs / Template
    page.goto('https://app.restaurant-pos.isarva.in/settings/printers', timeout=30000)
    page.wait_for_timeout(2000)
    tmpl_tab = page.locator('div:has-text("Template")').filter(has_text="Layout").first
    if tmpl_tab.count() > 0:
        tmpl_tab.click()
        page.wait_for_timeout(2000)
        page.screenshot(path="project/screens_part_m/M4_print_designs.jpg")
        print("M4 Template saved!")

    browser.close()
