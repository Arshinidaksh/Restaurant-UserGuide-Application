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

    page.goto('https://app.restaurant-pos.isarva.in/settings/printers', timeout=30000)
    page.wait_for_timeout(2000)

    # Let's see the 4 tab elements:
    # They contain text 'Receipt', 'KOT', 'Mapping', 'Template'
    tabs = page.locator('div.border, div.cursor-pointer, button').all()
    print("Listing tab candidates:")
    for idx, t in enumerate(tabs):
        txt = t.inner_text().strip().replace('\n', ' ')
        if any(k in txt for k in ["Receipt", "KOT", "Mapping", "Template"]):
            print(f"Candidate {idx}: tag={t.evaluate('el => el.tagName')}, class={t.get_attribute('class')}, text='{txt}'")

    # Click KOT tab using exact text
    page.locator('text=Kitchen ticket printers').click()
    page.wait_for_timeout(2000)
    page.screenshot(path="project/screens_part_m/M2_kot_printer.jpg")
    print("Saved M2 KOT by clicking 'Kitchen ticket printers'")

    # Click Mapping tab
    page.locator('text=Route KOT printers by department').click()
    page.wait_for_timeout(2000)
    page.screenshot(path="project/screens_part_m/M3_printer_mapping.jpg")
    print("Saved M3 Mapping by clicking 'Route KOT printers by department'")

    # Click Template tab
    page.locator('text=Layout, header, footer, and paper size').click()
    page.wait_for_timeout(2000)
    page.screenshot(path="project/screens_part_m/M4_print_designs.jpg")
    print("Saved M4 Template by clicking 'Layout, header, footer, and paper size'")

    browser.close()
