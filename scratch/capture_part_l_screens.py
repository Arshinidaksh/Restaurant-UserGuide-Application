import sys
import os
import time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.join(os.path.abspath("project"), "screens_part_l")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    print("Opening POS landing page...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)

    # Activate
    if page.locator('button:has-text("Activate")').count() > 0:
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(2500)

    # Login
    if page.locator('button:has-text("OK")').count() > 0:
        inputs = page.locator('input').all()
        inputs[0].fill('admin')
        inputs[1].fill('0000')
        page.locator('button:has-text("OK")').click()
        page.wait_for_timeout(3000)

    print("Navigating to Settings...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
    page.wait_for_timeout(2500)

    # List of tiles to capture:
    # (Step_ID, search_text or selector, filename)
    tiles = [
        ("L1", "Company Details", "L1_company_details.jpg"),
        ("L2", "ZATCA e-invoice", "L2_zatca_setup.jpg"),
        ("L3", "ZATCA e-invoice", "L3_zatca_queue.jpg"), # We will check if 2nd zatca tile is queue
        ("L4", "Customers", "L4_customers.jpg"),
        ("L5", "Gift cards", "L5_gift_cards.jpg"),
        ("L6", "Food vouchers", "L6_food_vouchers.jpg"),
        ("L7", "Loyalty campaigns", "L7_loyalty_campaigns.jpg"),
        ("L8", "Vendor", "L8_vendor.jpg"),
        ("L9", "Delivery Boy", "L9_delivery_boy.jpg"),
        ("L10", "Notification Settings", "L10_notifications.jpg"),
        ("L11", "Delivery APIs", "L11_delivery_apis.jpg"),
        ("L12", "Table Area", "L12_table_area.jpg"),
        ("L13", "Table Management", "L13_table_management.jpg"),
        ("L14", "Menu timetable", "L14_menu_timetable.jpg"),
        ("L15", "Addons", "L15_addons.jpg"),
        ("L16", "Utility", "L16_card_terminal.jpg"), # We'll check Utility or Card
        ("L17", "Counter", "L17_counter.jpg"),
    ]

    # First, let's inspect all clickable tiles on the Settings page:
    tile_elements = page.locator('div:has-text("Company Details"), div:has-text("Customers"), div:has-text("Vendor"), div:has-text("Table Area")').all()
    print("Found tile elements:", len(tile_elements), flush=True)

    # Let's inspect the HTML of the settings cards:
    cards = page.locator('div[class*="cursor-pointer"], a, button, div[role="button"]').all()
    print("Clickable elements count:", len(cards), flush=True)

    # Let's save a reference of Settings home
    page.screenshot(path=os.path.join(OUT_DIR, "settings_home.jpg"), quality=95)

    for step_id, tile_name, fname in tiles:
        print(f"Processing {step_id}: {tile_name}...", flush=True)
        page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
        page.wait_for_timeout(1500)

        # Find matching tile
        matching = page.locator(f'text="{tile_name}"').all()
        if not matching:
            matching = page.locator(f':text-matches("{tile_name}", "i")').all()

        if matching:
            target = matching[0]
            if step_id == "L3" and len(matching) > 1:
                target = matching[1] # 2nd ZATCA tile is invoice queue!
            
            try:
                target.click()
                page.wait_for_timeout(2000)
                out_path = os.path.join(OUT_DIR, fname)
                page.screenshot(path=out_path, quality=95)
                print(f"Captured {fname} (URL: {page.url})", flush=True)
            except Exception as e:
                print(f"Error clicking {tile_name}: {e}", flush=True)
        else:
            print(f"Could not find tile: {tile_name}", flush=True)

    browser.close()
    print("Done capturing Part L screens!", flush=True)
