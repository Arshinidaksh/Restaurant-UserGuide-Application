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
    page.wait_for_timeout(3000)
    print("Takeaway URL:", page.url)
    page.screenshot(path='scratch/live_takeaway_landing.png')

    # Look for existing queue tickets or click one
    queue_cards = page.locator('div:has-text("Open"), div:has-text("SAR")').all()
    print("Queue count:", len(queue_cards))

    # Let's see all text on page
    print("Page text snippet:\n", page.locator('body').inner_text()[:600])

    # If there is a ticket #5 or open ticket, click it
    t5 = page.locator('text=#5').first
    if t5.count() > 0:
        print("Clicking #5...")
        t5.click()
        page.wait_for_timeout(2000)
        page.screenshot(path='scratch/live_takeaway_ticket5.png')

    # Also let's check Drive-thru
    page.goto('https://app.restaurant-pos.isarva.in/drive', timeout=30000)
    page.wait_for_timeout(3000)
    page.screenshot(path='scratch/live_drive_landing.png')

    browser.close()
