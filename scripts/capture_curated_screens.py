import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENS_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "project", "screens")
os.makedirs(SCREENS_DIR, exist_ok=True)

def capture_curated_screens():
    print("Launching Microsoft Edge to capture curated POS screens...", flush=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        # 1. Activation Screen
        print("Navigating to application URL...", flush=True)
        page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENS_DIR, '01_activate_pos.jpg'), quality=95)
        print("1. Captured: 01_activate_pos.jpg", flush=True)

        # Activate
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(3000)

        # 2. Login Screen
        page.screenshot(path=os.path.join(SCREENS_DIR, '02_admin_login.jpg'), quality=95)
        print("2. Captured: 02_admin_login.jpg", flush=True)

        # Login
        inputs = page.locator('input').all()
        inputs[0].fill('admin')
        inputs[1].fill('0000')
        page.locator('button:has-text("OK")').click()
        page.wait_for_timeout(3500)

        # Ensure Head Office is explicitly selected
        try:
            branch_btn = page.locator('button:has-text("Head Office"), div[role="button"]:has-text("Head Office")').first
            if branch_btn.count() > 0:
                branch_btn.click()
                page.wait_for_timeout(800)
                h001_opt = page.locator('text=H001 - Head Office').last
                h001_opt.click()
                page.wait_for_timeout(1500)
                print("Explicitly selected H001 - Head Office", flush=True)
        except Exception as e:
            print("Note on branch selection:", e, flush=True)

        # 3. Main Dashboard with Head Office
        page.screenshot(path=os.path.join(SCREENS_DIR, '03_main_dashboard.jpg'), quality=95)
        print("3. Captured: 03_main_dashboard.jpg", flush=True)

        # 4. Interactive Table Seating (Diagram View)
        page.locator('text=Dine In').first.click()
        page.wait_for_timeout(2500)
        # Click Diagram view for the rich architectural table floor layout
        diag_btn = page.locator('text=Diagram')
        if diag_btn.count() > 0:
            diag_btn.first.click()
            page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(SCREENS_DIR, '04_floor_tickets.jpg'), quality=95)
        print("4. Captured: 04_floor_tickets.jpg (Interactive Table Seating Diagram)", flush=True)

        # 5. Food Menu & Order Ticket Screen
        # Navigate to Quick Serve for the complete food ordering catalog & ticket builder
        page.goto('https://app.restaurant-pos.isarva.in/quick-serve', timeout=30000)
        page.wait_for_timeout(3000)
        page.screenshot(path=os.path.join(SCREENS_DIR, '05_payments_settle.jpg'), quality=95)
        page.screenshot(path=os.path.join(SCREENS_DIR, '05_menu_catalog_ticket.jpg'), quality=95)
        print("5. Captured: 05_menu_catalog_ticket.jpg (Food Menu & Ticket)", flush=True)

        # 6. Takeaway & Drive-thru
        page.goto('https://app.restaurant-pos.isarva.in/takeaway', timeout=30000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENS_DIR, '06_takeaway.jpg'), quality=95)
        print("6. Captured: 06_takeaway.jpg", flush=True)

        # 7. Kitchen Display (KDS / KOT)
        page.goto('https://app.restaurant-pos.isarva.in/kot', timeout=30000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENS_DIR, '10_kitchen_kot.jpg'), quality=95)
        print("7. Captured: 10_kitchen_kot.jpg (Kitchen Display Screen)", flush=True)

        # 8. Stock & Inventory
        page.goto('https://app.restaurant-pos.isarva.in/stock', timeout=30000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENS_DIR, '11_stock_inventory.jpg'), quality=95)
        print("8. Captured: 11_stock_inventory.jpg", flush=True)

        # 9. Reports & Analytics
        page.goto('https://app.restaurant-pos.isarva.in/reports', timeout=30000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENS_DIR, '14_reports.jpg'), quality=95)
        print("9. Captured: 14_reports.jpg (Reports Dashboard)", flush=True)

        # 10. Settings Hub
        page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCREENS_DIR, '15_settings.jpg'), quality=95)
        print("10. Captured: 15_settings.jpg (Settings Hub)", flush=True)

        browser.close()
        print("All curated screens successfully captured!", flush=True)

if __name__ == "__main__":
    capture_curated_screens()
