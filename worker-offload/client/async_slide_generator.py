"""
Asynchronous Multi-Slide Generator Client
Dispatches screenshot captures and slide composition concurrently to:
- screenshot-vm (Playwright headless capture)
- image-stitcher-vm (Pillow mockup composition & typography)
"""
import os
import sys
import json
import time
import asyncio
import argparse
from typing import Dict, Any, List
import httpx

from config import load_config

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

async def check_worker_health(client: httpx.AsyncClient, name: str, url: str) -> dict:
    health_url = f"{url.rstrip('/')}/health"
    try:
        resp = await client.get(health_url, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        print(f"[HEALTH] {name} ({url}) is ONLINE (capacity: {data.get('concurrency_limit', 'N/A')})")
        return data
    except Exception as e:
        print(f"[HEALTH ERROR] Could not reach {name} at {health_url}: {e}")
        return {}

async def capture_screenshot(
    client: httpx.AsyncClient,
    screenshot_url: str,
    slide_def: Dict[str, Any],
    pos_base_url: str,
    semaphore: asyncio.Semaphore
) -> bytes:
    endpoint = f"{screenshot_url.rstrip('/')}/capture"
    payload = {
        "base_url": pos_base_url,
        "route": slide_def.get("target_route", "/settings"),
        "actions": slide_def.get("actions", []),
        "viewport_width": 1920,
        "viewport_height": 1080,
        "format": "jpeg",
        "quality": 95,
        "wait_after_actions_ms": 2000
    }

    async with semaphore:
        t0 = time.time()
        print(f"  [CAPTURE START] Route '{payload['route']}' for '{slide_def.get('heading', '')}'...")
        resp = await client.post(endpoint, json=payload, timeout=60.0)
        resp.raise_for_status()
        elapsed = time.time() - t0
        print(f"  [CAPTURE DONE] Route '{payload['route']}' finished in {elapsed:.2f}s ({len(resp.content)//1024} KB)")
        return resp.content

async def stitch_slide(
    client: httpx.AsyncClient,
    stitcher_url: str,
    kicker: str,
    slide_def: Dict[str, Any],
    screen_bytes: bytes,
    semaphore: asyncio.Semaphore
) -> bytes:
    endpoint = f"{stitcher_url.rstrip('/')}/compose"
    files = {
        "file": (slide_def.get("screen_filename", "screen.jpg"), screen_bytes, "image/jpeg")
    }
    data = {
        "kicker": kicker,
        "heading": slide_def.get("heading", ""),
        "where": slide_def.get("where", ""),
        "steps": json.dumps(slide_def.get("steps", [])),
        "note": slide_def.get("note", ""),
        "quality": 96
    }

    async with semaphore:
        t0 = time.time()
        print(f"  [STITCH START] Composing slide '{slide_def.get('heading', '')}'...")
        resp = await client.post(endpoint, data=data, files=files, timeout=60.0)
        resp.raise_for_status()
        elapsed = time.time() - t0
        print(f"  [STITCH DONE] Slide '{slide_def.get('heading', '')}' rendered in {elapsed:.2f}s ({len(resp.content)//1024} KB)")
        return resp.content

async def process_single_slide(
    client: httpx.AsyncClient,
    kicker: str,
    slide_def: Dict[str, Any],
    cfg: dict,
    screens_dir: str,
    slides_out_dir: str,
    export_out_dir: str,
    cap_sem: asyncio.Semaphore,
    stitch_sem: asyncio.Semaphore,
    pos_base_url: str
):
    slide_filename = slide_def.get("filename", "slide.jpg")
    screen_filename = slide_def.get("screen_filename", "screen.jpg")
    screen_local_path = os.path.join(screens_dir, screen_filename)

    # 1. Capture screen via screenshot-vm (or use local screen cache if present and requested)
    screen_bytes = None
    if os.path.exists(screen_local_path):
        print(f"  [CACHE] Using locally cached screen for '{screen_filename}'")
        with open(screen_local_path, "rb") as f:
            screen_bytes = f.read()
    else:
        screen_bytes = await capture_screenshot(
            client=client,
            screenshot_url=cfg["screenshot_worker_url"],
            slide_def=slide_def,
            pos_base_url=pos_base_url,
            semaphore=cap_sem
        )
        # Cache screen locally
        with open(screen_local_path, "wb") as f:
            f.write(screen_bytes)

    # 2. Pipeline directly to stitcher-vm for composition & resizing
    slide_bytes = await stitch_slide(
        client=client,
        stitcher_url=cfg["stitcher_worker_url"],
        kicker=kicker,
        slide_def=slide_def,
        screen_bytes=screen_bytes,
        semaphore=stitch_sem
    )

    # 3. Save final output
    p1 = os.path.join(slides_out_dir, slide_filename)
    p2 = os.path.join(export_out_dir, slide_filename)
    with open(p1, "wb") as f:
        f.write(slide_bytes)
    with open(p2, "wb") as f:
        f.write(slide_bytes)

    print(f"  -> Successfully generated: {slide_filename}")

async def run_async_pipeline(spec_path: str, force_recapture: bool = False):
    cfg = load_config()
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    part_id = spec.get("part_id", "custom").lower()
    part_title = spec.get("part_title", "")
    output_dir_name = spec.get("output_dir", spec.get("part_id", "Output"))
    pos_base_url = spec.get("pos_base_url", "https://app.restaurant-pos.isarva.in")
    slides = spec.get("slides", [])

    screens_dir = os.path.join(WORKSPACE_DIR, "project", f"screens_part_{part_id}")
    slides_out_dir = os.path.join(WORKSPACE_DIR, "Slides", output_dir_name)
    export_out_dir = os.path.join(WORKSPACE_DIR, "export", output_dir_name)

    os.makedirs(screens_dir, exist_ok=True)
    os.makedirs(slides_out_dir, exist_ok=True)
    os.makedirs(export_out_dir, exist_ok=True)

    if force_recapture:
        for f in os.listdir(screens_dir):
            try:
                os.remove(os.path.join(screens_dir, f))
            except Exception:
                pass

    print("=" * 70)
    print(f"DISTRIBUTED ASYNC SLIDE GENERATION: {part_title} ({len(slides)} slides)")
    print(f"Screenshot Worker: {cfg['screenshot_worker_url']} (concurrency: {cfg['screenshot_concurrency']})")
    print(f"Stitcher Worker:   {cfg['stitcher_worker_url']} (concurrency: {cfg['stitcher_concurrency']})")
    print("=" * 70)

    limits = httpx.Limits(max_keepalive_connections=20, max_connections=40)
    async with httpx.AsyncClient(limits=limits, timeout=cfg["request_timeout_sec"]) as client:
        # Check health
        h1 = await check_worker_health(client, "screenshot-vm", cfg["screenshot_worker_url"])
        h2 = await check_worker_health(client, "image-stitcher-vm", cfg["stitcher_worker_url"])

        if not h1 or not h2:
            print("[WARNING] One or more workers are not reachable. Check IPs in config.json or start services.")

        cap_sem = asyncio.Semaphore(cfg["screenshot_concurrency"])
        stitch_sem = asyncio.Semaphore(cfg["stitcher_concurrency"])

        t_start = time.time()
        tasks = [
            process_single_slide(
                client=client,
                kicker=part_title,
                slide_def=slide,
                cfg=cfg,
                screens_dir=screens_dir,
                slides_out_dir=slides_out_dir,
                export_out_dir=export_out_dir,
                cap_sem=cap_sem,
                stitch_sem=stitch_sem,
                pos_base_url=pos_base_url
            )
            for slide in slides
        ]

        await asyncio.gather(*tasks)
        total_time = time.time() - t_start

        print("=" * 70)
        print(f"ALL {len(slides)} SLIDES GENERATED IN {total_time:.2f}s!")
        print(f"Average throughput: {len(slides)/total_time:.2f} slides/sec")
        print(f"Outputs written to: {slides_out_dir}")
        print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed Async Slide Generator Client")
    parser.add_argument("--spec", required=True, help="Path to Part specification JSON")
    parser.add_argument("--force-recapture", action="store_true", help="Force redownloading screens from screenshot-vm")
    args = parser.parse_args()

    asyncio.run(run_async_pipeline(args.spec, force_recapture=args.force_recapture))
