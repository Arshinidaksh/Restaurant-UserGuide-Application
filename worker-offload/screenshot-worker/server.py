"""
Screenshot Worker Service
Runs headless Playwright in Docker on screenshot-vm.
Captures pristine 1920x1080 screens from the live POS application with concurrency management.
"""
import os
import asyncio
import logging
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright, Browser, BrowserContext

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("screenshot-worker")

WORKER_CONCURRENCY = int(os.environ.get("WORKER_CONCURRENCY", "4"))
DEFAULT_POS_URL = os.environ.get("POS_BASE_URL", "https://app.restaurant-pos.isarva.in")

class ActionStep(BaseModel):
    type: str  # "wait", "click", "fill"
    selector: Optional[str] = None
    value: Optional[str] = None
    ms: Optional[int] = 1000

class CaptureRequest(BaseModel):
    route: str = Field(default="/settings", description="Target application route (e.g. /settings)")
    base_url: Optional[str] = Field(default=DEFAULT_POS_URL)
    actions: Optional[List[ActionStep]] = Field(default_factory=list)
    viewport_width: int = Field(default=1920)
    viewport_height: int = Field(default=1080)
    quality: int = Field(default=95)
    format: str = Field(default="jpeg")  # "jpeg" or "png"
    wait_after_actions_ms: int = Field(default=2000)

class WorkerState:
    playwright = None
    browser: Optional[Browser] = None
    semaphore: asyncio.Semaphore = asyncio.Semaphore(WORKER_CONCURRENCY)
    active_jobs: int = 0
    total_processed: int = 0

state = WorkerState()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Initializing Playwright on screenshot-vm (concurrency limit: {WORKER_CONCURRENCY})...")
    state.playwright = await async_playwright().start()
    state.browser = await state.playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-first-run",
            "--no-zygote",
            "--single-process"
        ]
    )
    logger.info("Chromium headless engine ready for captures.")
    yield
    if state.browser:
        await state.browser.close()
    if state.playwright:
        await state.playwright.stop()
    logger.info("Playwright shutdown complete.")

app = FastAPI(title="Screenshot Worker API", version="1.0.0", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "screenshot-worker",
        "hostname": os.environ.get("HOSTNAME", "screenshot-vm"),
        "concurrency_limit": WORKER_CONCURRENCY,
        "active_jobs": state.active_jobs,
        "total_processed": state.total_processed,
        "browser_ready": state.browser is not None
    }

async def execute_capture(req: CaptureRequest) -> bytes:
    if not state.browser:
        raise HTTPException(status_code=503, detail="Browser engine not initialized")

    context: BrowserContext = await state.browser.new_context(
        viewport={"width": req.viewport_width, "height": req.viewport_height},
        device_scale_factor=1.0
    )
    page = await context.new_page()

    try:
        base = (req.base_url or DEFAULT_POS_URL).rstrip("/")
        full_url = f"{base}{req.route}"
        logger.info(f"Navigating to {full_url}")

        await page.goto(base, timeout=45000, wait_until="networkidle")
        await page.wait_for_timeout(1500)

        # Check for Terminal Activation
        if await page.locator('button:has-text("Activate")').count() > 0:
            logger.info("Performing terminal activation (C001)...")
            await page.locator('input').first.fill("C001")
            await page.locator('button:has-text("Activate")').click()
            await page.wait_for_timeout(2500)

        # Check for Admin Login
        if await page.locator('button:has-text("OK")').count() > 0:
            logger.info("Performing admin login...")
            inputs = await page.locator('input').all()
            if len(inputs) >= 2:
                await inputs[0].fill("admin")
                await inputs[1].fill("0000")
                await page.locator('button:has-text("OK")').click()
                await page.wait_for_timeout(3000)

        # Navigate to target route if different
        if req.route and req.route != "/":
            await page.goto(full_url, timeout=30000, wait_until="networkidle")
            await page.wait_for_timeout(1500)

        # Execute actions
        for act in (req.actions or []):
            if act.type == "wait":
                await page.wait_for_timeout(act.ms or 1000)
            elif act.type == "click" and act.selector:
                loc = page.locator(act.selector)
                if await loc.count() > 0:
                    await loc.first.click()
                    await page.wait_for_timeout(act.ms or 800)
            elif act.type == "fill" and act.selector:
                loc = page.locator(act.selector)
                if await loc.count() > 0:
                    await loc.first.fill(act.value or "")
                    await page.wait_for_timeout(300)

        # Allow any toasts or animations to settle
        await page.wait_for_timeout(req.wait_after_actions_ms)

        img_format = "jpeg" if req.format.lower() in ("jpg", "jpeg") else "png"
        kwargs = {"type": img_format}
        if img_format == "jpeg":
            kwargs["quality"] = req.quality

        # Pristine unannotated screenshot
        screenshot_bytes = await page.screenshot(**kwargs)
        return screenshot_bytes

    finally:
        await page.close()
        await context.close()

@app.post("/capture")
async def capture_screen(req: CaptureRequest):
    async with state.semaphore:
        state.active_jobs += 1
        try:
            image_bytes = await execute_capture(req)
            state.total_processed += 1
            media_type = "image/jpeg" if req.format.lower() in ("jpg", "jpeg") else "image/png"
            return Response(content=image_bytes, media_type=media_type)
        except Exception as e:
            logger.error(f"Error capturing screenshot for {req.route}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            state.active_jobs -= 1

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
