import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

SCREENS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "project", "screens")
os.makedirs(SCREENS_DIR, exist_ok=True)

def capture_screens():
    print(f"Target directory for screenshots: {SCREENS_DIR}", flush=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        # 1. Activation Screen
        print("Navigating to application URL...", flush=True)
        page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENS_DIR, '01_activate_pos.jpg'), quality=92)
        print("Captured: 01_activate_pos.jpg", flush=True)
        
        # Enter C001 & Activate
        inp = page.locator('input').first
        inp.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(3000)
        
        # 2. Login Screen
        page.screenshot(path=os.path.join(SCREENS_DIR, '02_admin_login.jpg'), quality=92)
        print("Captured: 02_admin_login.jpg", flush=True)
        
        # Enter admin / 0000
        inputs = page.locator('input').all()
        inputs[0].fill('admin')
        inputs[1].fill('0000')
        page.locator('button:has-text("OK")').click()
        page.wait_for_timeout(3500)
        
        # 3. Main Dashboard (Home)
        page.screenshot(path=os.path.join(SCREENS_DIR, '03_main_dashboard.jpg'), quality=92)
        print("Captured: 03_main_dashboard.jpg", flush=True)
        
        # Helper to click text and screenshot
        routes = [
            ("FLOOR", "04_floor_tickets.jpg"),
            ("PAYMENTS", "05_payments_settle.jpg"),
            ("TAKEAWAY", "06_takeaway.jpg"),
            ("DRIVE", "07_drive_thru.jpg"),
            ("DELIVERY", "08_delivery.jpg"),
            ("ONLINE", "09_online_orders.jpg"),
            ("KOT", "10_kitchen_kot.jpg"),
            ("STOCK", "11_stock_inventory.jpg"),
            ("EXPENSES", "12_expenses.jpg"),
            ("ACCOUNTS", "13_accounts.jpg"),
            ("REPORTS", "14_reports.jpg"),
            ("SETTINGS", "15_settings.jpg"),
        ]
        
        for nav_text, filename in routes:
            try:
                # Find nav button on sidebar
                nav_btn = page.locator(f'button:has-text("{nav_text}"), div:has-text("{nav_text}")').first
                if nav_btn.count() > 0:
                    nav_btn.click()
                    page.wait_for_timeout(2000)
                    out_path = os.path.join(SCREENS_DIR, filename)
                    page.screenshot(path=out_path, quality=92)
                    print(f"Captured: {filename} for {nav_text}", flush=True)
            except Exception as e:
                print(f"Could not capture {nav_text}: {e}", flush=True)
                
        browser.close()
        print("Screen capture completed successfully.", flush=True)

if __name__ == "__main__":
    capture_screens()
