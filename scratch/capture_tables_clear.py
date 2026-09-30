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

    # Table Management: clear search box
    page.goto('https://app.restaurant-pos.isarva.in/settings/floor?tab=tables', timeout=30000)
    page.wait_for_timeout(2000)
    # Click search input and clear it
    search_inp = page.locator('input[placeholder*="Search"]').first
    if search_inp.count() > 0:
        search_inp.fill('')
        page.wait_for_timeout(1000)

    page.screenshot(path='project/screens_part_l/L13_table_management.jpg')
    print("L13 with all tables saved!")

    browser.close()
