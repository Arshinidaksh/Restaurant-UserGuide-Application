"""
Image Stitcher and Resizer Worker Service
Runs FastAPI with Pillow in Docker on image-stitcher-vm.
Handles high-fidelity slide composition, PC mockup stitching, typography rendering, and image resizing.
"""
import os
import io
import json
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Response
from PIL import Image

from src.composer import compose_slide, compose_info_slide, resize_image

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("stitcher-worker")

WORKER_CONCURRENCY = int(os.environ.get("WORKER_CONCURRENCY", "8"))
thread_pool = ThreadPoolExecutor(max_workers=WORKER_CONCURRENCY)

class WorkerState:
    active_jobs: int = 0
    total_processed: int = 0
    semaphore: asyncio.Semaphore = asyncio.Semaphore(WORKER_CONCURRENCY)

state = WorkerState()
app = FastAPI(title="Image Stitcher and Resizer Worker API", version="1.0.0")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "image-stitcher-worker",
        "hostname": os.environ.get("HOSTNAME", "image-stitcher-vm"),
        "concurrency_limit": WORKER_CONCURRENCY,
        "active_jobs": state.active_jobs,
        "total_processed": state.total_processed
    }

def _sync_compose_and_encode(
    screen_bytes: bytes,
    kicker: str,
    heading: str,
    where: str,
    steps_list: List[str],
    note: str,
    quality: int,
    resize_width: Optional[int]
) -> bytes:
    screen_img = Image.open(io.BytesIO(screen_bytes))
    slide = compose_slide(
        screen_img=screen_img,
        kicker=kicker,
        heading=heading,
        where=where,
        steps=steps_list,
        note=note
    )

    if resize_width and resize_width < slide.width:
        slide = resize_image(slide, target_width=resize_width)

    out_buf = io.BytesIO()
    slide.save(out_buf, format="JPEG", quality=quality, optimize=True)
    return out_buf.getvalue()

def _sync_resize(image_bytes: bytes, width: int, height: Optional[int], quality: int) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    resized = resize_image(img, target_width=width, target_height=height)
    out_buf = io.BytesIO()
    fmt = img.format if img.format in ("PNG", "JPEG") else "JPEG"
    resized.save(out_buf, format=fmt, quality=quality, optimize=True)
    return out_buf.getvalue()

@app.post("/compose")
async def compose_endpoint(
    file: UploadFile = File(..., description="Pristine screenshot image (JPEG/PNG)"),
    kicker: str = Form(default=""),
    heading: str = Form(default=""),
    where: str = Form(default=""),
    steps: str = Form(default="[]", description="JSON array of step strings"),
    note: str = Form(default=""),
    quality: int = Form(default=96),
    resize_width: Optional[int] = Form(default=None)
):
    async with state.semaphore:
        state.active_jobs += 1
        try:
            steps_list = []
            if steps:
                try:
                    steps_list = json.loads(steps)
                except Exception:
                    steps_list = [steps]

            screen_bytes = await file.read()
            loop = asyncio.get_running_loop()

            result_bytes = await loop.run_in_executor(
                thread_pool,
                _sync_compose_and_encode,
                screen_bytes,
                kicker,
                heading,
                where,
                steps_list,
                note,
                quality,
                resize_width
            )

            state.total_processed += 1
            return Response(content=result_bytes, media_type="image/jpeg")

        except Exception as e:
            logger.error(f"Error composing slide '{heading}': {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            state.active_jobs -= 1

def _sync_compose_info_and_encode(
    kicker: str,
    heading: str,
    description: str,
    items_list: list,
    note: str,
    columns: int,
    quality: int
) -> bytes:
    slide = compose_info_slide(
        kicker=kicker,
        heading=heading,
        description=description,
        items=items_list,
        note=note,
        columns=columns
    )
    out_buf = io.BytesIO()
    slide.save(out_buf, format="JPEG", quality=quality, optimize=True)
    return out_buf.getvalue()

@app.post("/compose-info")
async def compose_info_endpoint(
    kicker: str = Form(default=""),
    heading: str = Form(default=""),
    description: str = Form(default=""),
    items: str = Form(default="[]", description="JSON array of items/strings/dicts"),
    note: str = Form(default=""),
    columns: int = Form(default=2),
    quality: int = Form(default=96)
):
    async with state.semaphore:
        state.active_jobs += 1
        try:
            items_list = []
            if items:
                try:
                    items_list = json.loads(items)
                except Exception:
                    items_list = [items]

            loop = asyncio.get_running_loop()
            result_bytes = await loop.run_in_executor(
                thread_pool,
                _sync_compose_info_and_encode,
                kicker,
                heading,
                description,
                items_list,
                note,
                columns,
                quality
            )

            state.total_processed += 1
            return Response(content=result_bytes, media_type="image/jpeg")

        except Exception as e:
            logger.error(f"Error composing info slide '{heading}': {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            state.active_jobs -= 1

@app.post("/resize")
async def resize_endpoint(
    file: UploadFile = File(..., description="Source image to resize"),
    width: int = Form(..., description="Target width in pixels"),
    height: Optional[int] = Form(default=None, description="Optional target height"),
    quality: int = Form(default=95)
):
    async with state.semaphore:
        state.active_jobs += 1
        try:
            image_bytes = await file.read()
            loop = asyncio.get_running_loop()
            result_bytes = await loop.run_in_executor(
                thread_pool,
                _sync_resize,
                image_bytes,
                width,
                height,
                quality
            )
            state.total_processed += 1
            return Response(content=result_bytes, media_type="image/jpeg")
        except Exception as e:
            logger.error(f"Error resizing image: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            state.active_jobs -= 1

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
