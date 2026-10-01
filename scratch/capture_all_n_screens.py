import asyncio
import httpx
import os
import time

SCREENSHOT_VM_URL = "http://139.59.20.202:8000/capture"
OUTPUT_DIR = "project/screens_part_n"

TILES = [
    ("N1_department_list.jpg", "Department List"),
    ("N2_menu_items.jpg", "Menu items"),
    ("N3_menu_details.jpg", "Menu details (tax & photos)"),
    ("N4_tax.jpg", "Tax"),
    ("N5_tax_update.jpg", "Tax Update"),
    ("N6_discount.jpg", "Discount"),
    ("N7_units.jpg", "Units"),
    ("N8_extra_charges.jpg", "Extra Charges"),
    ("N9_beverages_quantity.jpg", "Beverages Quantity Master"),
    ("N10_beverages_price.jpg", "Beverages Price Master"),
    ("N11_online_price_list.jpg", "Online Price List"),
]

async def capture_tile(client: httpx.AsyncClient, filename: str, tile_text: str, sem: asyncio.Semaphore):
    async with sem:
        t0 = time.time()
        print(f"[START] Capturing {filename} ({tile_text})...")
        payload = {
            "route": "/settings",
            "actions": [
                {"type": "click", "selector": "text=Catalog"},
                {"type": "wait", "ms": 600},
                {"type": "click", "selector": f"text={tile_text}"},
                {"type": "wait", "ms": 1500}
            ],
            "viewport_width": 1920,
            "viewport_height": 1080,
            "format": "jpeg",
            "quality": 95
        }
        try:
            resp = await client.post(SCREENSHOT_VM_URL, json=payload, timeout=60.0)
            resp.raise_for_status()
            out_path = os.path.join(OUTPUT_DIR, filename)
            with open(out_path, "wb") as f:
                f.write(resp.content)
            elapsed = time.time() - t0
            print(f"[SUCCESS] {filename} captured in {elapsed:.2f}s ({len(resp.content)//1024} KB)")
        except Exception as e:
            print(f"[ERROR] Failed to capture {filename}: {e}")

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sem = asyncio.Semaphore(10)
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=15)
    async with httpx.AsyncClient(limits=limits, timeout=90.0) as client:
        tasks = [capture_tile(client, fn, tt, sem) for fn, tt in TILES]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
