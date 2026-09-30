import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "project", "screens_parts_fk")
os.makedirs(OUTPUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    print("Navigating to POS...", flush=True)
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2500)

    # Activate
    page.locator('input').first.fill('C001')
    page.locator('button:has-text("Activate")').click()
    page.wait_for_timeout(3000)

    # Login
    inputs = page.locator('input').all()
    inputs[0].fill('admin')
    inputs[1].fill('0000')
    page.locator('button:has-text("OK")').click()
    page.wait_for_timeout(3500)
    print("Logged in.", flush=True)

    # Let's inspect sidebar / menu
    menu_items = page.locator('nav a, nav button, div[role="button"]').all()
    print(f"Total nav items: {len(menu_items)}")
    for item in menu_items:
        t = item.inner_text().strip().replace('\n', ' ')
        if t:
            print("NAV:", t)

    # Test routes
    routes = [
        ("F_takeaway", "https://app.restaurant-pos.isarva.in/takeaway"),
        ("F_drive_thru", "https://app.restaurant-pos.isarva.in/drive-thru"),
        ("G_delivery", "https://app.restaurant-pos.isarva.in/delivery"),
        ("G_online", "https://app.restaurant-pos.isarva.in/online"),
        ("H_kitchen_kot", "https://app.restaurant-pos.isarva.in/kot"),
        ("I_delivery_rider", "https://app.restaurant-pos.isarva.in/delivery"),
        ("J_accounts", "https://app.restaurant-pos.isarva.in/accounts"),
        ("J_reports", "https://app.restaurant-pos.isarva.in/reports"),
        ("K_settings", "https://app.restaurant-pos.isarva.in/settings"),
    ]

    for name, url in routes:
        print(f"\nChecking route {name}: {url}...")
        try:
            page.goto(url, timeout=15000)
            page.wait_for_timeout(2500)
            out_file = os.path.join(OUTPUT_DIR, f"{name}.jpg")
            page.screenshot(path=out_file, quality=95)
            print(f"Captured {name}: {out_file}, current URL: {page.url}")
            # print page title or h1/h2
            headings = page.locator('h1, h2, h3, header').all()
            for h in headings[:3]:
                htxt = h.inner_text().strip().replace('\n', ' ')
                if htxt:
                    print("  Heading:", htxt)
        except Exception as e:
            print(f"Error on {name}: {e}")

    browser.close()
    print("\nExploration completed.")
