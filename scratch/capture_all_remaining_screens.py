import asyncio
import httpx
import os
import time

SCREENSHOT_VM_URL = "http://139.59.20.202:8000/capture"

# Screens to capture grouped by part
SCREEN_JOBS = [
    # Part O
    ("project/screens_part_o", "O1_user_list.jpg", "/settings", [{"type": "click", "selector": "text=User"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=User list, text=Users"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_o", "O2_roles.jpg", "/settings", [{"type": "click", "selector": "text=User"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Roles"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_o", "O3_role_privilege.jpg", "/settings", [{"type": "click", "selector": "text=User"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Role Privilege, text=Privileges"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_o", "O4_pin_login.jpg", "/settings", [{"type": "click", "selector": "text=User"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=PIN, text=Login"}, {"type": "wait", "ms": 1500}]),

    # Part P
    ("project/screens_part_p", "P1_accounts_hub.jpg", "/settings", [{"type": "click", "selector": "text=Accounts"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_p", "P2_payment_types.jpg", "/settings", [{"type": "click", "selector": "text=Accounts"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Payment types"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_p", "P3_expense_types.jpg", "/settings", [{"type": "click", "selector": "text=Accounts"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Expense types"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_p", "P4_expense_details.jpg", "/settings", [{"type": "click", "selector": "text=Accounts"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Expense details, text=Expenses"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_p", "P5_sales_ledger.jpg", "/back-office", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_p", "P6_day_close.jpg", "/back-office", [{"type": "click", "selector": "text=Day Close"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_p", "P7_shift.jpg", "/back-office", [{"type": "click", "selector": "text=Shift"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_p", "P8_time_clock.jpg", "/back-office", [{"type": "click", "selector": "text=Time clock"}, {"type": "wait", "ms": 1500}]),

    # Part Q
    ("project/screens_part_q", "Q1_ingredient_master.jpg", "/settings", [{"type": "click", "selector": "text=Ingredients"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Ingredient Master"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_q", "Q2_item_recipes.jpg", "/masters", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_q", "Q3_recipe_usage.jpg", "/settings", [{"type": "click", "selector": "text=Ingredients"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Recipe usage"}, {"type": "wait", "ms": 1500}]),

    # Part R
    ("project/screens_part_r", "R1_storage_locations.jpg", "/settings", [{"type": "click", "selector": "text=Inventory"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Storage locations"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_r", "R2_yield_conversions.jpg", "/settings", [{"type": "click", "selector": "text=Inventory"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Yield conversions"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_r", "R3_stock_receiving.jpg", "/settings", [{"type": "click", "selector": "text=Inventory"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Stock receiving"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_r", "R4_stock_transfer.jpg", "/settings", [{"type": "click", "selector": "text=Inventory"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Stock transfer"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_r", "R5_purchase_orders.jpg", "/settings", [{"type": "click", "selector": "text=Inventory"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Purchase Orders, text=PO"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_r", "R6_stock_master.jpg", "/stock", [{"type": "wait", "ms": 1500}]),

    # Part S
    ("project/screens_part_s", "S1_export.jpg", "/settings", [{"type": "click", "selector": "text=Database"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Export"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_s", "S2_import.jpg", "/settings", [{"type": "click", "selector": "text=Database"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Import"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_s", "S3_backup.jpg", "/settings", [{"type": "click", "selector": "text=Database"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Backup"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_s", "S4_data_cleaning.jpg", "/settings", [{"type": "click", "selector": "text=Database"}, {"type": "wait", "ms": 500}, {"type": "click", "selector": "text=Data Cleaning, text=Clean"}, {"type": "wait", "ms": 1500}]),

    # Part T
    ("project/screens_part_t", "T1_reports_hub.jpg", "/reports", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_t", "T2_sales_reports.jpg", "/reports", [{"type": "click", "selector": "text=Sales Summary"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_t", "T3_control_reports.jpg", "/reports", [{"type": "click", "selector": "text=Void audit, text=Void"}, {"type": "wait", "ms": 1500}]),
    ("project/screens_part_t", "T4_stock_reports.jpg", "/reports", [{"type": "click", "selector": "text=Stock Summary"}, {"type": "wait", "ms": 1500}]),

    # Part U
    ("project/screens_part_u", "U1_home.jpg", "/home", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_u", "U2_dine_in.jpg", "/dine-in", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_u", "U3_payments.jpg", "/payments", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_u", "U4_takeaway.jpg", "/takeaway", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_u", "U5_delivery.jpg", "/delivery", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_u", "U6_kitchen.jpg", "/kitchen", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_u", "U7_masters.jpg", "/masters", [{"type": "wait", "ms": 1500}]),
    ("project/screens_part_u", "U8_back_office.jpg", "/back-office", [{"type": "wait", "ms": 1500}])
]

async def capture_job(client: httpx.AsyncClient, out_dir: str, filename: str, route: str, actions: list, sem: asyncio.Semaphore):
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"[SKIP] {filename} already captured ({os.path.getsize(out_path)//1024} KB)")
        return

    async with sem:
        t0 = time.time()
        print(f"[START] Capturing {filename} via {route}...")
        payload = {
            "route": route,
            "actions": actions,
            "viewport_width": 1920,
            "viewport_height": 1080,
            "format": "jpeg",
            "quality": 95
        }
        try:
            resp = await client.post(SCREENSHOT_VM_URL, json=payload, timeout=70.0)
            resp.raise_for_status()
            with open(out_path, "wb") as f:
                f.write(resp.content)
            elapsed = time.time() - t0
            print(f"[DONE] {filename} saved in {elapsed:.2f}s ({len(resp.content)//1024} KB)")
        except Exception as e:
            print(f"[ERROR] Failed {filename}: {e}")

async def main():
    sem = asyncio.Semaphore(10)
    limits = httpx.Limits(max_connections=25, max_keepalive_connections=20)
    async with httpx.AsyncClient(limits=limits, timeout=100.0) as client:
        tasks = [
            capture_job(client, od, fn, rt, acts, sem)
            for od, fn, rt, acts in SCREEN_JOBS
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
