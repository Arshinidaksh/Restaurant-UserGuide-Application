import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

os.makedirs('project/screens', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    print("Navigating to https://app.restaurant-pos.isarva.in/...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2500)
    
    # 1. Screen: Activation
    inp = page.locator('input').first
    inp.fill('C001')
    page.locator('button:has-text("Activate")').click()
    page.wait_for_timeout(3000)
    
    # 2. Login
    inputs = page.locator('input').all()
    user_inp = inputs[0]
    pass_inp = inputs[1]
    
    user_inp.fill('admin')
    pass_inp.fill('0000')
    print("Filled admin / 0000", flush=True)
    page.wait_for_timeout(500)
    
    # Click OK button
    page.locator('button:has-text("OK")').click()
    page.wait_for_timeout(4000)
    
    # 3. Screen: After Login
    page.screenshot(path='project/screens/03_after_login.jpg', quality=95)
    print("Saved 03_after_login.jpg", flush=True)
    
    print("Current URL:", page.url, flush=True)
    print("Body text snippet:\n", page.inner_text('body')[:600], flush=True)

    # Let's inspect buttons / elements to see where branch switcher or menu is
    buttons = page.locator('button').all()
    print(f"Buttons count: {len(buttons)}", flush=True)
    for i, b in enumerate(buttons[:25]):
        txt = b.inner_text().replace('\n', ' ')
        print(f"Button {i}: '{txt}'", flush=True)

    browser.close()
    print("Done.", flush=True)
