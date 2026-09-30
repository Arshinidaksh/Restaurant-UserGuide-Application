"""
Automated Browser Screen Capture Module
Takes a part specification JSON, navigates the live POS application,
prepares pristine application state (clears toasts, populates data when needed),
and captures 1920x1080 unannotated screenshots.
"""
import os
import sys
import json
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from playwright.sync_api import sync_playwright

def run_screen_capture(spec_json_path: str, output_screens_dir: str, pos_base_url: str = "https://app.restaurant-pos.isarva.in"):
    with open(spec_json_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    os.makedirs(output_screens_dir, exist_ok=True)
    slides = spec.get("slides", [])
    print(f"Starting screen capture for {len(slides)} slides into {output_screens_dir}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        # 1. Login / Activation
        print(f"Connecting to POS at {pos_base_url}...")
        page.goto(pos_base_url, timeout=40000)
        page.wait_for_timeout(2000)

        if page.locator('button:has-text("Activate")').count() > 0:
            print("Activating terminal...")
            page.locator('input').first.fill('C001')
            page.locator('button:has-text("Activate")').click()
            page.wait_for_timeout(2500)

        if page.locator('button:has-text("OK")').count() > 0:
            print("Logging in as Admin...")
            inputs = page.locator('input').all()
            if len(inputs) >= 2:
                inputs[0].fill('admin')
                inputs[1].fill('0000')
                page.locator('button:has-text("OK")').click()
                page.wait_for_timeout(3000)

        # 2. Iterate each slide
        for idx, slide in enumerate(slides, 1):
            route = slide.get("target_route", "/settings")
            screen_name = slide.get("screen_filename", f"step_{idx}.jpg")
            target_out_path = os.path.join(output_screens_dir, screen_name)

            full_url = f"{pos_base_url.rstrip('/')}{route}"
            print(f"[{idx}/{len(slides)}] Navigating to {full_url} for '{slide.get('heading', '')}'...")
            page.goto(full_url, timeout=30000)
            page.wait_for_timeout(1500)

            # Execute any custom setup actions specified in spec
            actions = slide.get("actions", [])
            for act in actions:
                a_type = act.get("type")
                if a_type == "wait":
                    page.wait_for_timeout(act.get("ms", 1000))
                elif a_type == "click":
                    sel = act.get("selector")
                    if sel and page.locator(sel).count() > 0:
                        page.locator(sel).first.click()
                        page.wait_for_timeout(act.get("ms", 800))
                elif a_type == "fill":
                    sel = act.get("selector")
                    val = act.get("value", "")
                    if sel and page.locator(sel).count() > 0:
                        page.locator(sel).first.fill(val)
                        page.wait_for_timeout(300)

            # Ensure transient toasts fade away
            page.wait_for_timeout(2500)

            # Clean screenshot without any bounding boxes or markers
            page.screenshot(path=target_out_path, quality=95, type="jpeg")
            print(f"  -> Captured clean screen: {target_out_path}")

        browser.close()
        print("Screen capture completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        run_screen_capture(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python capture_screens.py <spec_json_path> <output_screens_dir>")
