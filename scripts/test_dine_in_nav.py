import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

os.makedirs('project/screens_real', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    print("Navigating to POS...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2500)
    
    # 1. Activate
    inp = page.locator('input').first
    inp.fill('C001')
    page.locator('button:has-text("Activate")').click()
    page.wait_for_timeout(3000)
    
    # 2. Login
    inputs = page.locator('input').all()
    inputs[0].fill('admin')
    inputs[1].fill('0000')
    page.locator('button:has-text("OK")').click()
    page.wait_for_timeout(3500)
    print("Logged in successfully. URL:", page.url, flush=True)
    
    # Let's inspect all clickable cards / buttons under Service
    print("Looking for Dine In element...", flush=True)
    # Let's find Dine In
    dine_in_el = page.locator('div:has-text("Dine In"), button:has-text("Dine In")')
    print(f"Dine in elements found: {dine_in_el.count()}", flush=True)
    for i in range(dine_in_el.count()):
        el = dine_in_el.nth(i)
        print(f"Dine in {i}: tag={el.evaluate('e => e.tagName')}, class={el.evaluate('e => e.className')[:40]}", flush=True)
        
    # Let's click the last Dine In element (usually the card)
    dine_in_el.last.click()
    page.wait_for_timeout(3000)
    print("After clicking Dine In. URL:", page.url, flush=True)
    page.screenshot(path='project/screens_real/dine_in_screen.jpg', quality=95)
    print("Saved dine_in_screen.jpg", flush=True)
    
    # Inspect what's on the screen
    print("Text on screen after clicking Dine In:\n", page.inner_text('body')[:600], flush=True)
    
    # Are there tables? Let's check buttons or divs for Table
    tables = page.locator('button:has-text("Table"), div:has-text("Table"), button:has-text("T")')
    print(f"Table elements found: {tables.count()}", flush=True)
    if tables.count() > 0:
        for i in range(min(5, tables.count())):
            print(f"Table {i}: {tables.nth(i).inner_text().strip()[:30]}")
            
    browser.close()
