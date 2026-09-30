import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)
    page.locator('input').first.fill('C001')
    page.locator('button:has-text("Activate")').click()
    page.wait_for_timeout(2500)
    inputs = page.locator('input').all()
    inputs[0].fill('admin')
    inputs[1].fill('0000')
    page.locator('button:has-text("OK")').click()
    page.wait_for_timeout(3500)

    # Find the branch switcher button highlighted by user
    branch_btn = page.locator('button:has-text("Head Office"), div[role="button"]:has-text("Head Office")').first
    print("Branch button found:", branch_btn.inner_text().replace('\n', ' '), flush=True)
    
    # Click to open dropdown
    branch_btn.click()
    page.wait_for_timeout(1000)
    
    # Capture screenshot of branch dropdown open
    os.makedirs('project/screens_v2', exist_ok=True)
    page.screenshot(path='project/screens_v2/branch_dropdown_open.jpg', quality=95)
    print("Captured branch_dropdown_open.jpg", flush=True)
    
    # Inspect dropdown options
    options = page.locator('div[role="option"], li, button:has-text("H001"), div:has-text("H001")').all()
    print("Branch options found:", len(options), flush=True)
    for opt in options[:8]:
        txt = opt.inner_text().strip().replace('\n', ' ')
        if txt:
            print("Option:", txt)
            
    # Click H001 - Head Office option explicitly
    h001_opt = page.locator('text=H001 - Head Office').last
    h001_opt.click()
    page.wait_for_timeout(2000)
    print("Explicitly clicked H001 - Head Office", flush=True)
    
    browser.close()
