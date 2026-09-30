"""
waCRM Ultra-Fast In-Memory Slide Generator CLI
Generates high-resolution JPG slides adhering to brand guidelines.
100% In-Memory execution with zero intermediate disk I/O, pre-warmed caching, and dynamic scrubbing.
"""
import argparse
import os
import sys
import time
import orjson

# Ensure app directory is on path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE_DIR, "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from src.screen_composer import compose_pc_screen
from src.preview_renderer import render_slide_preview
from src.info_renderer import render_info_slide
from src.scrubber import scrub_screenshot

def load_slides_data() -> dict:
    content_file = os.path.join(APP_DIR, "content", "slides_data.json")
    with open(content_file, "rb") as f:
        return orjson.loads(f.read())

def generate_slide_jpg(slide_id: str, output_path: str = None, verbose: bool = True) -> str:
    t0 = time.perf_counter()

    all_data = load_slides_data()
    if slide_id not in all_data:
        raise ValueError(f"Slide ID '{slide_id}' not found in slides_data.json")

    slide_data = all_data[slide_id]

    # Asset paths
    bg_trans_path = os.path.join(BASE_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(BASE_DIR, "Libraries", "Parts", "PC-Screen.png")
    check_icon_path = os.path.join(APP_DIR, "brand_check_icon.png")
    fonts_dir = os.path.join(APP_DIR, "fonts")

    # Output JPG path
    if not output_path:
        out_dir = os.path.join(BASE_DIR, "output")
        os.makedirs(out_dir, exist_ok=True)
        heading = slide_data.get("heading", slide_id).strip()
        if heading.startswith(slide_id):
            clean_heading = heading[len(slide_id):].strip().lstrip(".- ")
        else:
            clean_heading = heading
        safe_heading = clean_heading.lower().replace(" ", "-").replace("&", "and").replace("?", "").replace(":", "").replace("(", "").replace(")", "").replace("/", "-").replace("--", "-").strip("-")
        output_path = os.path.join(out_dir, f"{slide_id}-{safe_heading}.jpg")

    # Check if this is an Information Slide (without screenshot)
    layout = slide_data.get("layout", "screenshot")
    if layout == "info" or not slide_data.get("screen_filename"):
        # Render clean multi-card information slide
        render_info_slide(
            content=slide_data,
            fonts_dir=fonts_dir,
            output_path=output_path
        )
        dur_ms = (time.perf_counter() - t0) * 1000
        if verbose:
            print(f"[SUCCESS] Generated Info slide {slide_id} in {dur_ms:.1f}ms -> {output_path}")
        return output_path

    screenshot_name = slide_data.get("screen_filename", f"{slide_id}.jpg")
    screenshot_path = os.path.join(BASE_DIR, "project", "screens", screenshot_name)

    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"Screenshot not found at {screenshot_path}")

    # 1. In-Memory Dynamic Scrubbing (Zero Disk I/O)
    scrub_rules = slide_data.get("scrub_rules", [])
    scrubbed_img = scrub_screenshot(screenshot_path, rules=scrub_rules)

    # 2. In-Memory Monitor Frame Fitting & Resampling
    crop_align = slide_data.get("crop_align", "left")
    mockup_img = compose_pc_screen(
        scrubbed_img,
        pc_frame_path,
        crop_top_only=True,
        crop_align=crop_align
    )

    # 3. In-Memory Composition onto Pre-Warmed Canvas & Direct JPG Save
    render_slide_preview(
        content=slide_data,
        bg_path=bg_trans_path,
        pc_mockup=mockup_img,
        check_icon_path=check_icon_path,
        fonts_dir=fonts_dir,
        output_path=output_path
    )

    dur_ms = (time.perf_counter() - t0) * 1000
    if verbose:
        print(f"[SUCCESS] Generated slide {slide_id} in {dur_ms:.1f}ms -> {output_path}")

    return output_path

def generate_all_slides(verbose: bool = True):
    all_data = load_slides_data()
    t_start = time.perf_counter()
    count = 0
    for s_id in all_data.keys():
        generate_slide_jpg(s_id, verbose=verbose)
        count += 1
    total_ms = (time.perf_counter() - t_start) * 1000
    print(f"\n[DONE] Batch generated {count} slides in {total_ms:.1f}ms (avg {total_ms/count:.1f}ms/slide)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Isarva Restaurant POS & waCRM Ultra-Fast Slide Generator CLI")
    parser.add_argument("--slide", type=str, default="POS-1.0", help="Slide section ID (e.g. 'POS-1.0', 'POS-4.1', '2.1')")
    parser.add_argument("--output", type=str, default=None, help="Custom output JPG path")
    parser.add_argument("--all", action="store_true", help="Generate all configured slides")
    parser.add_argument("--list", action="store_true", help="List all available slide IDs")
    args = parser.parse_args()

    if args.list:
        all_data = load_slides_data()
        print("\nAvailable Slide IDs:")
        for s_id, s_val in all_data.items():
            print(f" - {s_id:8s}: {s_val.get('heading', '')} [{s_val.get('layout', 'screenshot')}]")
        sys.exit(0)

    if args.all:
        generate_all_slides()
    else:
        generate_slide_jpg(args.slide, args.output)
