import asyncio
from playwright.async_api import async_playwright

async def capture_dashboard():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(channel="chrome", headless=True)
        except Exception:
            browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1.0
        )
        page = await context.new_page()

        print("Navigating to POS...")
        await page.goto("https://app.restaurant-pos.isarva.in", timeout=45000)
        await page.wait_for_timeout(3000)

        # 1. Activation
        if await page.locator('button:has-text("Activate")').count() > 0:
            print("Activating terminal C001...")
            await page.locator('input').first.fill("C001")
            await page.locator('button:has-text("Activate")').click()
            await page.wait_for_timeout(3000)

        # 2. Login
        if await page.locator('button:has-text("OK")').count() > 0:
            print("Logging in as admin...")
            inputs = await page.locator('input').all()
            if len(inputs) >= 2:
                await inputs[0].fill("admin")
                await inputs[1].fill("0000")
                await page.locator('button:has-text("OK")').click()
                await page.wait_for_timeout(4000)

        print(f"Current URL: {page.url}")
        # Wait 4 seconds for UI to settle
        await page.wait_for_timeout(4000)

        # Dismiss toast or sweetalerts if any
        try:
            await page.evaluate("""() => {
                document.querySelectorAll('.swal2-container, [role="status"], .toast, [class*="toast"], .notistack-Snackbar').forEach(el => el.remove());
            }""")
        except Exception:
            pass

        # Take screenshot
        out_path = "scratch/new_dashboard_raw.png"
        await page.screenshot(path=out_path, full_page=False)
        print(f"Saved screenshot to {out_path}")

        # Find language toggle elements
        print("\nSearching for language toggle / switch buttons...")
        lang_elements = await page.locator('text=/EN|عربي|English|Arabic/i').all()
        for idx, el in enumerate(lang_elements):
            try:
                box = await el.bounding_box()
                txt = await el.inner_text()
                print(f"  Element {idx}: text='{txt.strip()}', bbox={box}")
            except Exception as e:
                pass

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_dashboard())
