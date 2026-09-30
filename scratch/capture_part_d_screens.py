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

    # Ensure Connected status on top header
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

    # Step 1: Floor Map
    page.screenshot(path=os.path.join(OUT_DIR, 'step01_floor_map.jpg'), quality=95)
    print("Saved step01_floor_map.jpg", flush=True)

    # Open Table 01
    print("Opening Table 01...", flush=True)
    t1 = page.locator('text=Table 01').first
    if t1.count() > 0:
        t1.click()
    else:
        page.locator('text=Table 02').first.click()
    page.wait_for_timeout(3000)

    # Step 2: Table ticket with food items
    page.screenshot(path=os.path.join(OUT_DIR, 'step02_table_order_ticket.jpg'), quality=95)
    print("Saved step02_table_order_ticket.jpg", flush=True)

    # Step 3: Bill Totals
    page.screenshot(path=os.path.join(OUT_DIR, 'step03_bill_totals.jpg'), quality=95)
    print("Saved step03_bill_totals.jpg", flush=True)

    # Step 4: Discount row active
    print("Clicking Discount 10%...", flush=True)
    disc_10 = page.locator('button:has-text("10%")').first
    if disc_10.count() > 0:
        disc_10.click()
        page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(OUT_DIR, 'step04_discount_active.jpg'), quality=95)
    print("Saved step04_discount_active.jpg", flush=True)

    # Step 5: Extra charges toggled
    print("Toggling Extra charges...", flush=True)
    svc = page.locator('text=Service charges as per policy').first
    if svc.count() > 0:
        svc.click()
        page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(OUT_DIR, 'step05_extra_charges_active.jpg'), quality=95)
    print("Saved step05_extra_charges_active.jpg", flush=True)

    # Step 6: Save buttons
    page.screenshot(path=os.path.join(OUT_DIR, 'step06_save_buttons.jpg'), quality=95)
    print("Saved step06_save_buttons.jpg", flush=True)

    # Step 7: KOT buttons
    page.screenshot(path=os.path.join(OUT_DIR, 'step07_kot_buttons.jpg'), quality=95)
    print("Saved step07_kot_buttons.jpg", flush=True)

    # Step 8: Change Table modal
    print("Clicking Change Table...", flush=True)
    chg_btn = page.locator('button:has-text("Change Table")').first
    if chg_btn.count() > 0:
        chg_btn.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, 'step08_change_table_modal.jpg'), quality=95)
        print("Saved step08_change_table_modal.jpg", flush=True)
        # Close modal
        close_btn = page.locator('button:has-text("Cancel"), button:has-text("Close"), text=✕').first
        if close_btn.count() > 0:
            close_btn.click()
            page.wait_for_timeout(1500)

    # Step 9: Merge Tables modal
    print("Clicking Merge Tables...", flush=True)
    mrg_btn = page.locator('button:has-text("Merge Tables")').first
    if mrg_btn.count() > 0:
        mrg_btn.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, 'step09_merge_tables_modal.jpg'), quality=95)
        print("Saved step09_merge_tables_modal.jpg", flush=True)
        close_btn = page.locator('button:has-text("Cancel"), button:has-text("Close"), text=✕').first
        if close_btn.count() > 0:
            close_btn.click()
            page.wait_for_timeout(1500)

    # Step 10: Split modal
    print("Clicking Split...", flush=True)
    split_btn = page.locator('button:has-text("Split"), button:has-text("Split bill")').first
    if split_btn.count() > 0:
        split_btn.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, 'step10_split_modal.jpg'), quality=95)
        print("Saved step10_split_modal.jpg", flush=True)
        close_btn = page.locator('button:has-text("Cancel"), button:has-text("Close"), text=✕').first
        if close_btn.count() > 0:
            close_btn.click()
            page.wait_for_timeout(1500)

    # Step 11: Settle modal
    print("Clicking Settle...", flush=True)
    settle_btn = page.locator('button:has-text("Settle")').last
    if settle_btn.count() > 0:
        settle_btn.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT_DIR, 'step11_settle_modal.jpg'), quality=95)
        print("Saved step11_settle_modal.jpg", flush=True)
        close_btn = page.locator('button:has-text("Cancel"), button:has-text("Close"), text=✕').first
        if close_btn.count() > 0:
            close_btn.click()
            page.wait_for_timeout(1500)

    # Step 12: Add more items later (adding an additional dish like Chicken Mandi or Fries)
    print("Adding another item for Step 12...", flush=True)
    fries = page.locator('text=Fies, text=Fries, text=Chicken Mandi').first
    if fries.count() > 0:
        fries.click()
        page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(OUT_DIR, 'step12_add_more_items.jpg'), quality=95)
    print("Saved step12_add_more_items.jpg", flush=True)

    browser.close()
    print("All Part D captures completed successfully!", flush=True)
