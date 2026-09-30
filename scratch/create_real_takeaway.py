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

    # Go to Takeaway
    page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
    page.wait_for_timeout(2500)

    # Click + New ticket
    print("Clicking + New ticket...", flush=True)
    page.locator('button:has-text("New ticket")').first.click()
    page.wait_for_timeout(2000)

    # Screenshot right after creating ticket
    page.screenshot(path='scratch/takeaway_ticket_empty.png')
    print("Saved takeaway_ticket_empty.png", flush=True)

    # Click some food items to add them to ticket
    # Look for food buttons like 'Chicken Kabsa Full' or 'Roti & Curry' or any item
    items = page.locator('div:has-text("SAR")').all()
    print("Found items count:", len(items), flush=True)

    # Add 2 items:
    kabsa = page.locator('text=Chicken Kabsa Full').first
    if kabsa.count() > 0:
        kabsa.click()
        page.wait_for_timeout(800)

    roti = page.locator('text=Roti & Curry').first
    if roti.count() > 0:
        roti.click()
        page.wait_for_timeout(800)

    # Click Note button to add packing note if available
    note_btn = page.locator('button:has-text("Note")').first
    if note_btn.count() > 0:
        note_btn.click()
        page.wait_for_timeout(800)
        # Type in note input if a modal opens
        note_input = page.locator('textarea, input[placeholder*="note" i], input[type="text"]')
        if note_input.count() > 0:
            note_input.last.fill("Pack well with cover and bag")
            page.wait_for_timeout(500)
            ok_btn = page.locator('button:has-text("Save"), button:has-text("OK"), button:has-text("Done")')
            if ok_btn.count() > 0:
                ok_btn.first.click()
                page.wait_for_timeout(800)

    page.screenshot(path='scratch/takeaway_ticket_with_items.png')
    print("Saved takeaway_ticket_with_items.png", flush=True)

    browser.close()
