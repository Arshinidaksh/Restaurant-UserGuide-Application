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

    # Inspect left sidebar nav items
    nav_items = page.locator('aside button, aside div.cursor-pointer, nav button, div:has-text("Settings") button').all()
    print(f"Found {len(nav_items)} sidebar elements:")
    for i, it in enumerate(nav_items):
        txt = it.inner_text().strip().replace('\n', ' ')
        print(f" [{i}] {txt}")

    # Click specifically the item with exact text 'Printer'
    p_item = page.locator('button:has-text("Printer"), a:has-text("Printer")').filter(has_text="Printer")
    print(f"Printer match count: {p_item.count()}")
    for idx in range(p_item.count()):
        btn = p_item.nth(idx)
        print(f"  Printer item {idx}: '{btn.inner_text().strip().replace(chr(10), ' ')}'")
        if "printer" in btn.inner_text().lower() and len(btn.inner_text().strip()) < 15:
            btn.click()
            page.wait_for_timeout(2000)
            print(f"Clicked Printer item {idx} -> URL: {page.url}")
            page.screenshot(path="project/screens_part_m/printer_screen.jpg")
            break

    browser.close()
