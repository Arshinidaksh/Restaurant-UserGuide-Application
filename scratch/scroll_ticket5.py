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

    page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
    page.wait_for_timeout(2500)

    # Click ticket #5
    t5 = page.locator('text=#5').first
    if t5.count() > 0:
        t5.click()
        page.wait_for_timeout(2000)

    # Scroll the order panel or page down
    page.evaluate('''() => {
        // find scrollable elements on the right
        const els = document.querySelectorAll('*');
        for (const el of els) {
            if (el.scrollHeight > el.clientHeight && el.getBoundingClientRect().left > 1400) {
                el.scrollTop = el.scrollHeight;
            }
        }
    }''')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/takeaway_ticket5_scrolled.png')
    print("Saved scratch/takeaway_ticket5_scrolled.png")
    browser.close()
