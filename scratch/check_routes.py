import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)

    # Activate & Login
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

    # Check search in settings
    page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
    page.wait_for_timeout(2000)

    # Check Utility in settings
    page.goto('https://app.restaurant-pos.isarva.in/settings/utility', timeout=30000)
    page.wait_for_timeout(2000)
    print('Utility URL:', page.url)
    page.screenshot(path='project/screens_part_l/utility_page.jpg')

    # Check Payments on left nav
    page.goto('https://app.restaurant-pos.isarva.in/payments', timeout=30000)
    page.wait_for_timeout(2000)
    print('Payments URL:', page.url)
    page.screenshot(path='project/screens_part_l/payments_page.jpg')

    # Check potential card terminal routes
    for route in ['/settings/terminal', '/settings/hardware', '/settings/card', '/settings/softpos', '/settings/mada', '/settings/payment']:
        page.goto('https://app.restaurant-pos.isarva.in' + route, timeout=10000)
        page.wait_for_timeout(800)
        print(route, '->', page.url)
        if 'settings' in page.url and page.url != 'https://app.restaurant-pos.isarva.in/settings':
            page.screenshot(path=f'project/screens_part_l/{route.replace("/settings/", "")}.jpg')

    browser.close()
