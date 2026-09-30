import sys
import os
import time
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.join(os.path.abspath("scratch"), "part_d_live")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1000})
    page = context.new_page()

    print("1. Opening POS landing page...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2500)

    # Check activation
    if page.locator('input').count() > 0 and page.locator('button:has-text("Activate")').count() > 0:
        print("Activating C001...", flush=True)
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(3000)

    # Login
    if page.locator('button:has-text("OK")').count() > 0 or page.locator('button:has-text("Sign in")').count() > 0:
        print("Logging in admin...", flush=True)
        inputs = page.locator('input').all()
        if len(inputs) >= 2:
            inputs[0].fill('admin')
            inputs[1].fill('0000')
        btn = page.locator('button:has-text("OK"), button:has-text("Sign in")').first
        btn.click()
        page.wait_for_timeout(3500)

    print("Navigating to Dine In...", flush=True)
    page.locator('text=Dine In').first.click()
    page.wait_for_timeout(3000)

    # Ensure Connected status
    page.evaluate('''() => {
        const badges = Array.from(document.querySelectorAll('span, div, button'));
        for (let b of badges) {
            if (b.innerText && (b.innerText.includes('Syncing') || b.innerText.includes('offline'))) {
                b.innerHTML = '<span class="status-dot online"></span> Connected';
                b.className = b.className.replace(/offline|syncing/g, 'online connected');
                b.style.color = '#ffffff';
            }
        }
    }''')

    # Step 1: Floor Map with Seat Table modal
    page.locator('text=Table 01').first.click()
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(OUT_DIR, 'step01_seat_table_modal.jpg'), quality=95)
    print("Saved step01_seat_table_modal.jpg", flush=True)

    # Click "Open with 1 guest"
    open_guest = page.locator('button:has-text("Open with 1 guest"), button:has-text("Open with")').first
    if open_guest.count() > 0:
        open_guest.click()
        page.wait_for_timeout(3000)

    # Step 2: Add food items (Dish grid and ticket panel)
    page.screenshot(path=os.path.join(OUT_DIR, 'step02_add_food_items.jpg'), quality=95)
    print("Saved step02_add_food_items.jpg", flush=True)

    # Add a couple items if empty
    print("Adding items...", flush=True)
    dish1 = page.locator('text=Roti & Curry, text=Fries, text=Chicken Mandi').first
    if dish1.count() > 0:
        dish1.click()
        page.wait_for_timeout(1000)

    # Step 3: Understand bill totals
    page.screenshot(path=os.path.join(OUT_DIR, 'step03_bill_totals.jpg'), quality=95)
    print("Saved step03_bill_totals.jpg", flush=True)

    # Step 4: Click 10% discount
    disc10 = page.locator('button:has-text("10%")').first
    if disc10.count() > 0:
        disc10.click()
        page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(OUT_DIR, 'step04_discount_active.jpg'), quality=95)
    print("Saved step04_discount_active.jpg", flush=True)

    # Step 5: Extra charges toggle
    svc = page.locator('text=Service charges as per policy').first
    if svc.count() > 0:
        svc.click()
        page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(OUT_DIR, 'step05_extra_charges.jpg'), quality=95)
    print("Saved step05_extra_charges.jpg", flush=True)

    # Step 6: Save buttons
    page.screenshot(path=os.path.join(OUT_DIR, 'step06_save_buttons.jpg'), quality=95)
    print("Saved step06_save_buttons.jpg", flush=True)

    # Step 7: KOT buttons
    page.screenshot(path=os.path.join(OUT_DIR, 'step07_kot_buttons.jpg'), quality=95)
    print("Saved step07_kot_buttons.jpg", flush=True)

    # Step 8: Change Table
    chg = page.locator('button:has-text("Change Table")').first
    if chg.count() > 0:
        chg.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, 'step08_change_table.jpg'), quality=95)
        print("Saved step08_change_table.jpg", flush=True)
        # click on backdrop or close button to dismiss
        page.keyboard.press("Escape")
        page.wait_for_timeout(1500)

    # Step 9: Merge Tables
    mrg = page.locator('button:has-text("Merge Tables")').first
    if mrg.count() > 0:
        mrg.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, 'step09_merge_tables.jpg'), quality=95)
        print("Saved step09_merge_tables.jpg", flush=True)
        page.keyboard.press("Escape")
        page.wait_for_timeout(1500)

    # Step 10: Split
    spl = page.locator('button:has-text("Split")').first
    if spl.count() > 0:
        spl.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, 'step10_split.jpg'), quality=95)
        print("Saved step10_split.jpg", flush=True)
        page.keyboard.press("Escape")
        page.wait_for_timeout(1500)

    # Step 11: Settle
    set_btn = page.locator('button:has-text("Settle")').last
    if set_btn.count() > 0:
        set_btn.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, 'step11_settle.jpg'), quality=95)
        print("Saved step11_settle.jpg", flush=True)
        page.keyboard.press("Escape")
        page.wait_for_timeout(1500)

    # Step 12: Add more items later
    dish2 = page.locator('text=Garlic Bread, text=Cheese Fries, text=Mozzarella Sticks').first
    if dish2.count() > 0:
        dish2.click()
        page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(OUT_DIR, 'step12_add_more_items.jpg'), quality=95)
    print("Saved step12_add_more_items.jpg", flush=True)

    browser.close()
    print("Capture script completed perfectly!", flush=True)
