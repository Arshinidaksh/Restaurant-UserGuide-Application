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

    # 1. Clean Timetable without toast
    page.goto('https://app.restaurant-pos.isarva.in/settings/menu-timetable', timeout=30000)
    page.wait_for_timeout(4000) # wait for toast to fade
    page.screenshot(path='project/screens_part_l/L14_menu_timetable.jpg')
    print("Clean L14 saved!")

    # 2. Table Management: let's see if we can add a table or check what is there
    page.goto('https://app.restaurant-pos.isarva.in/settings/floor?tab=tables', timeout=30000)
    page.wait_for_timeout(2000)
    # If there is 'Add table' button, click it to see if modal opens or if there are sample tables
    add_btn = page.locator('button:has-text("Add table")').first
    if add_btn.count() > 0:
        add_btn.click()
        page.wait_for_timeout(1000)
        # fill table number and seats
        t_inputs = page.locator('input').all()
        for inp in t_inputs:
            ph = inp.get_attribute('placeholder') or ''
            if 'table' in ph.lower() or 'name' in ph.lower():
                inp.fill('T-01')
            elif 'seat' in ph.lower() or 'capacity' in ph.lower():
                inp.fill('4')
        # Click save
        save_btn = page.locator('button:has-text("Save"), button:has-text("Add"), button:has-text("Create")').last
        if save_btn.count() > 0:
            save_btn.click()
            page.wait_for_timeout(4000) # wait for toast to disappear
            page.screenshot(path='project/screens_part_l/L13_table_management.jpg')
            print("L13 with table saved!")

    browser.close()
