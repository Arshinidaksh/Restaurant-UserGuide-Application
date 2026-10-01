"""
Screenshot Worker Service
Runs headless Playwright in Docker on screenshot-vm.
Reuses authenticated browser sessions (cookies + localStorage) for ultra-fast screen captures.
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
    wait_after_actions_ms: int = Field(default=1500)

class WorkerState:
    playwright = None
    browser: Optional[Browser] = None
    storage_state: Optional[dict] = None
    auth_lock: asyncio.Lock = asyncio.Lock()
    semaphore: asyncio.Semaphore = asyncio.Semaphore(WORKER_CONCURRENCY)
    active_jobs: int = 0
    total_processed: int = 0

state = WorkerState()

async def ensure_authenticated_session(base_url: str, force_refresh: bool = False) -> dict:
    """Pre-authenticates and saves localStorage + cookies state to eliminate login overhead."""
    async with state.auth_lock:
        if state.storage_state is not None and not force_refresh:
            return state.storage_state

        logger.info(f"Authenticating master POS session at {base_url}...")
        context = await state.browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        try:
            base = base_url.rstrip("/")
            await page.goto(base, timeout=40000)
            await page.wait_for_timeout(2000)

            # 1. Terminal Activation
            if await page.locator('button:has-text("Activate")').count() > 0:
                logger.info("Activating terminal (C001)...")
                await page.locator('input').first.fill("C001")
                await page.locator('button:has-text("Activate")').click()
                await page.wait_for_timeout(2500)

            # 2. Admin Login
            if await page.locator('button:has-text("OK")').count() > 0:
                logger.info("Logging in as Admin (admin / 0000)...")
                inputs = await page.locator('input').all()
                if len(inputs) >= 2:
                    await inputs[0].fill("admin")
                    await inputs[1].fill("0000")
                    await page.locator('button:has-text("OK")').click()
                    await page.wait_for_timeout(3000)

            state.storage_state = await context.storage_state()
            logger.info("Master POS session captured successfully and cached for reuse.")
            return state.storage_state

        except Exception as e:
            logger.error(f"Error establishing authenticated session: {e}", exc_info=True)
            raise e
        finally:
            await page.close()
            await context.close()

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
            "--disable-gpu"
        ]
    )
    logger.info("Chromium headless engine ready. Warming up master session...")
    try:
        await ensure_authenticated_session(DEFAULT_POS_URL)
    except Exception as e:
        logger.warning(f"Initial warm-up failed, will authenticate on first request: {e}")

    yield

    if state.browser:
        await state.browser.close()
    if state.playwright:
        await state.playwright.stop()
    logger.info("Playwright shutdown complete.")

app = FastAPI(title="Screenshot Worker API", version="1.1.0", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "screenshot-worker",
        "hostname": os.environ.get("HOSTNAME", "screenshot-vm"),
        "concurrency_limit": WORKER_CONCURRENCY,
        "active_jobs": state.active_jobs,
        "total_processed": state.total_processed,
        "session_cached": state.storage_state is not None,
        "browser_ready": state.browser is not None
    }

@app.post("/refresh-session")
async def refresh_session():
    """Forces re-authentication and updates the cached session."""
    storage = await ensure_authenticated_session(DEFAULT_POS_URL, force_refresh=True)
    return {"status": "session_refreshed", "cookies": len(storage.get("cookies", []))}

async def execute_capture(req: CaptureRequest) -> bytes:
    if not state.browser:
        raise HTTPException(status_code=503, detail="Browser engine not initialized")

    base = (req.base_url or DEFAULT_POS_URL).rstrip("/")
    storage = await ensure_authenticated_session(base)

    # Spawn context with pre-authenticated storage state (zero login overhead)
    context: BrowserContext = await state.browser.new_context(
        storage_state=storage,
        viewport={"width": req.viewport_width, "height": req.viewport_height},
        device_scale_factor=1.0
    )
    page = await context.new_page()

    try:
        full_url = f"{base}{req.route}" if req.route else base
        logger.info(f"Navigating directly to {full_url} with reused session")

        await page.goto(full_url, timeout=30000)
        await page.wait_for_timeout(1000)

        # Fallback check if session expired or lost (only trigger if terminal activation or isolated 2-input login screen)
        needs_activate = await page.locator('button:has-text("Activate")').count() > 0
        needs_login = await page.locator('input').count() == 2 and await page.locator('aside, nav, .sidebar').count() == 0 and await page.locator('button:has-text("OK")').count() > 0

        if needs_activate or needs_login:
            logger.info("Session expired or unauthenticated. Re-authenticating...")
            if needs_activate:
                await page.locator('input').first.fill("C001")
                await page.locator('button:has-text("Activate")').click()
                await page.wait_for_timeout(2000)

            if await page.locator('button:has-text("OK")').count() > 0:
                inputs = await page.locator('input').all()
                if len(inputs) >= 2:
                    await inputs[0].fill("admin")
                    await inputs[1].fill("0000")
                    await page.locator('button:has-text("OK")').click()
                    await page.wait_for_timeout(2500)

            # Update master storage state
            state.storage_state = await context.storage_state()

            # Re-navigate to target
            if req.route and req.route != "/":
                await page.goto(full_url, timeout=20000)
                await page.wait_for_timeout(1000)

        # Execute custom user actions if specified
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

        # Settle any active UI transitions/toasts
        await page.wait_for_timeout(req.wait_after_actions_ms)

        img_format = "jpeg" if req.format.lower() in ("jpg", "jpeg") else "png"
        kwargs = {"type": img_format}
        if img_format == "jpeg":
            kwargs["quality"] = req.quality

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
