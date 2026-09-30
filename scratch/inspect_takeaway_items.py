import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)

    # Activate
    if page.locator('button:has-text("Activate")').count() > 0:
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(2500)

    # Login
    if page.locator('button:has-text("OK")').count() > 0:
        inputs = page.locator('input').all()
        inputs[0].fill('admin')
        inputs[1].fill('0000')
        page.locator('button:has-text("OK")').click()
        page.wait_for_timeout(3000)

    page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
    page.wait_for_timeout(2500)

    # Click on ticket #8 (which has SAR 0.00, i.e. 0 items) or #10 or #11
    # Let's see all ticket buttons in queue
    t_new = page.locator('text=SAR 0.00').first
    if t_new.count() > 0:
        print("Clicking empty ticket in queue...")
        t_new.click()
        page.wait_for_timeout(2000)
    else:
        page.locator('button:has-text("New ticket")').first.click()
        page.wait_for_timeout(2000)

    # Click on 'Food' category or 'All'
    cat = page.locator('button:has-text("Food"), div:has-text("Food")').first
    if cat.count() > 0:
        cat.click()
        page.wait_for_timeout(1000)

    # Look for food items
    print("Catalog items:")
    for el in page.locator('div[role="button"], button').all()[:40]:
        t = el.inner_text().strip()
        if 'SAR' in t:
            print("Item with SAR:", t.replace('\n', ' | '))

    page.screenshot(path='scratch/takeaway_ticket_empty_cat.png')
    browser.close()
