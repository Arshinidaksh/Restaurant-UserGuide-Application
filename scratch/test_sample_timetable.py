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
    page.goto('https://app.restaurant-pos.isarva.in/settings/menu-timetable', timeout=30000)
    page.wait_for_timeout(2000)

    # Click 'Load sample schedules' or 'Load samples'
    btn = page.locator('button:has-text("Load sample"), button:has-text("Load samples")').first
    if btn.count() > 0:
        btn.click()
        page.wait_for_timeout(1500)
        page.screenshot(path='project/screens_part_l/L14_menu_timetable_loaded.jpg')
        print("Loaded sample schedules screenshot saved!")

    # Check tables on floor?tab=tables or Add Table
    page.goto('https://app.restaurant-pos.isarva.in/settings/floor?tab=tables', timeout=30000)
    page.wait_for_timeout(1500)
    # Check if there is a 'Load sample' or 'Add table' button
    add_btn = page.locator('button:has-text("Add table")').first
    print("Table tab URL:", page.url)

    browser.close()
