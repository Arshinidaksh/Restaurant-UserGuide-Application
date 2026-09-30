import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
    page.wait_for_timeout(2500)

    # Click New ticket
    page.locator('button:has-text("New ticket")').first.click()
    page.wait_for_timeout(2000)

    # Let's inspect food item cards
    # Let's find cards containing text 'Roti & Curry' or 'Chicken Kabsa'
    card = page.locator('text=Roti & Curry').first
    print("Found Roti & Curry:", card.count())
    # Click card or its parent
    card.click()
    page.wait_for_timeout(1000)

    # Click Chicken Kabsa
    kabsa = page.locator('text=Chicken Kabsa Full').first
    if kabsa.count() > 0:
        kabsa.click()
        page.wait_for_timeout(1000)

    # Click Fries
    fries = page.locator('text=Fries').first
    if fries.count() > 0:
        fries.click()
        page.wait_for_timeout(1000)

    # Click 'Note' button at top right of ticket
    note_btn = page.locator('button:has-text("Note")').first
    if note_btn.count() > 0:
        note_btn.click()
        page.wait_for_timeout(1000)
        # Check if modal is visible
        txt = page.locator('textarea, input[type="text"]').last
        if txt.count() > 0:
            txt.fill('Pack with extra garlic sauce and napkins')
            page.wait_for_timeout(500)
            # Find save/done/ok button
            done = page.locator('button:has-text("Save"), button:has-text("OK"), button:has-text("Done")').first
            if done.count() > 0:
                done.click()
                page.wait_for_timeout(1000)

    page.screenshot(path='scratch/takeaway_live_complete.png')
    print("Saved scratch/takeaway_live_complete.png")

    browser.close()
