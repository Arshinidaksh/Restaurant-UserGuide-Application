import sys
import os
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1000})
    page = context.new_page()
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2500)

    if page.locator('input').count() > 0 and page.locator('button:has-text("Activate")').count() > 0:
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(3000)

    if page.locator('button:has-text("OK")').count() > 0 or page.locator('button:has-text("Sign in")').count() > 0:
        inputs = page.locator('input').all()
        if len(inputs) >= 2:
            inputs[0].fill('admin')
            inputs[1].fill('0000')
        btn = page.locator('button:has-text("OK"), button:has-text("Sign in")').first
        btn.click()
        page.wait_for_timeout(3500)

    print('Current URL:', page.url)
    page.goto('https://app.restaurant-pos.isarva.in/floor', timeout=30000)
    page.wait_for_timeout(3000)
    print('Floor URL:', page.url)

    # Let's take a screenshot of floor
    os.makedirs('scratch/part_d_screens', exist_ok=True)
    page.screenshot(path='scratch/part_d_screens/01_floor_initial.png')
    print('Saved scratch/part_d_screens/01_floor_initial.png')

    browser.close()
