import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=True)
        page = await b.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto("https://app.restaurant-pos.isarva.in", timeout=30000)
        await page.wait_for_timeout(2000)
        if await page.locator('button:has-text("Activate")').count() > 0:
            await page.locator('input').first.fill("C001")
            await page.locator('button:has-text("Activate")').click()
            await page.wait_for_timeout(2000)
        if await page.locator('button:has-text("OK")').count() > 0:
            inputs = await page.locator('input').all()
            await inputs[0].fill("admin")
            await inputs[1].fill("0000")
            await page.locator('button:has-text("OK")').click()
            await page.wait_for_timeout(3000)
        
        el = page.locator('text="EN"').first
        box = await el.bounding_box()
        print('EN box:', box)
        parent = el.locator('..')
        p_box = await parent.bounding_box()
        print('Parent box:', p_box)
        p_parent = parent.locator('..')
        pp_box = await p_parent.bounding_box()
        print('Grandparent box:', pp_box)
        await b.close()

if __name__ == "__main__":
    asyncio.run(check())
