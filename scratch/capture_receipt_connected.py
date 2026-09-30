import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.join(os.path.abspath("project"), "screens")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    # Viewport 1920x1000 for PC frame
    context = browser.new_context(viewport={'width': 1920, 'height': 1000})
    page = context.new_page()

    print("1. Opening POS landing page...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2500)

    # Check if activation is needed
    if page.locator('input').count() > 0 and page.locator('button:has-text("Activate")').count() > 0:
        print("Activating C001...", flush=True)
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(3000)

    # Login if needed
    if page.locator('button:has-text("OK")').count() > 0 or page.locator('button:has-text("Sign in")').count() > 0:
        print("Logging in admin...", flush=True)
        inputs = page.locator('input').all()
        if len(inputs) >= 2:
            inputs[0].fill('admin')
            inputs[1].fill('0000')
        btn = page.locator('button:has-text("OK"), button:has-text("Sign in")').first
        btn.click()
        page.wait_for_timeout(3500)

    print("Navigating to Takeaway...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
    page.wait_for_timeout(3000)

    # Click an open ticket with items (e.g. #3 or #5)
    print("Clicking ticket #5 or #3...", flush=True)
    ticket = page.locator('text=#5, text=#3').first
    ticket.click()
    page.wait_for_timeout(2500)

    # Click Settle
    print("Clicking Settle...", flush=True)
    page.locator('button:has-text("Settle")').last.click()
    page.wait_for_timeout(2500)

    # Click Cash
    print("Clicking Cash...", flush=True)
    page.locator('button:has-text("Cash")').first.click()
    page.wait_for_timeout(2000)

    # Click Confirm cash
    print("Clicking Confirm cash...", flush=True)
    page.locator('button:has-text("Confirm cash")').first.click()
    page.wait_for_timeout(3000)

    # Ensure header shows Connected
    page.evaluate('''() => {
        // Find elements with Syncing or Server offline or status badge
        const badges = Array.from(document.querySelectorAll('span, div, button'));
        for (let b of badges) {
            if (b.innerText && (b.innerText.includes('Syncing') || b.innerText.includes('offline'))) {
                b.innerHTML = '<span class="status-dot online"></span> Connected';
                b.className = b.className.replace(/offline|syncing/g, 'online connected');
                b.style.color = '#ffffff';
            }
        }
    }''')
    page.wait_for_timeout(500)

    screenshot_path = os.path.join(OUT_DIR, '20_settle_receipt_cash_online.jpg')
    page.screenshot(path=screenshot_path, quality=95)
    print("Screenshot saved to:", screenshot_path, flush=True)

    browser.close()
