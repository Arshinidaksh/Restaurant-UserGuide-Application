"""
Slide Composer Module
Renders high-fidelity, brand-compliant 1920x1080 slides inside PC monitor mockups.
Strictly ensures screenshots are unannotated with clean typography.
"""
import os
import sys
import json
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
RESTAURANT_APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app")
FONTS_DIR = os.path.join(APP_DIR, "fonts")

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from src.screen_composer import compose_pc_screen
from src.config import (
    PC_POS_X, PC_POS_Y,
    TEXT_COL_X, KICKER_Y, HEADING_Y,
    MAX_TEXT_WIDTH_PX
)
from src.cache import get_cached_base_background, get_cached_font

def clean_unicode_arrows(text: str) -> str:
    """Replaces Unicode arrows that fail to render in Rubik font."""
    return text.replace("→", ">").replace("←", "<")

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
    words = text.split(" ")
    lines = []
    current_line = []
    for w in words:
        test_line = " ".join(current_line + [w])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(w)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [w]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def create_number_badge(num: int, size: int = 28, bg_color = (18, 113, 208, 255), fg_color = (255, 255, 255, 255)) -> Image.Image:
    scale = 4
    im = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, size * scale - 1, size * scale - 1), fill=bg_color)
    font_path = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font = ImageFont.truetype(font_path, int((size * 0.58) * scale))
    text = str(num)
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size * scale - tw) / 2
    ty = (size * scale - th) / 2 - 2 * scale
    d.text((tx, ty), text, font=font, fill=fg_color)
    return im.resize((size, size), Image.Resampling.LANCZOS)

def render_slide_from_spec(kicker: str, slide_def: Dict[str, Any], screen_img: Image.Image, output_paths: List[str]) -> Image.Image:
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")

    canvas = get_cached_base_background(bg_trans_path).copy()

    # 1. PC Mockup Frame with unannotated clean screenshot
    mockup_img = compose_pc_screen(
        screen_img.convert("RGBA"),
        pc_frame_path,
        crop_top_only=False,
        crop_align="center"
    )
    canvas.paste(mockup_img, (PC_POS_X, PC_POS_Y), mockup_img)

    # 2. Text layout & typography
    draw = ImageDraw.Draw(canvas)
    c_blue = (18, 113, 208, 255)
    c_gray = (88, 88, 90, 255)
    c_dark = (35, 35, 35, 255)

    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    f_kicker = get_cached_font(font_semibold, 20)
    f_heading = get_cached_font(font_semibold, 38)
    f_where = get_cached_font(font_regular, 20)
    f_step_text = get_cached_font(font_regular, 19)
    f_note = get_cached_font(font_regular, 18)

    kicker_clean = clean_unicode_arrows(kicker)
    heading_clean = clean_unicode_arrows(slide_def.get("heading", ""))
    where_clean = clean_unicode_arrows(slide_def.get("where", ""))
    note_clean = clean_unicode_arrows(slide_def.get("note", ""))
    steps_clean = [clean_unicode_arrows(s) for s in slide_def.get("steps", [])]

    # Kicker
    draw.text((TEXT_COL_X, KICKER_Y), kicker_clean, font=f_kicker, fill=c_blue)

    # Heading
    head_lines = wrap_text(heading_clean, f_heading, MAX_TEXT_WIDTH_PX, draw)
    curr_y = HEADING_Y
    for hl in head_lines:
        draw.text((TEXT_COL_X, curr_y), hl, font=f_heading, fill=c_dark)
        curr_y += 46

    # Where location
    if where_clean:
        curr_y += 6
        draw.text((TEXT_COL_X, curr_y), where_clean, font=f_where, fill=c_gray)
        curr_y += 30

    curr_y += 18

    # Steps with number badges
    step_badge_size = 28
    n_steps = len(steps_clean)
    step_gap = 40 if n_steps <= 5 else 34

    for idx, st_text in enumerate(steps_clean, 1):
        badge = create_number_badge(idx, size=step_badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, curr_y + 2), badge)

        text_x = TEXT_COL_X + step_badge_size + 16
        text_max_w = MAX_TEXT_WIDTH_PX - (step_badge_size + 16)
        s_lines = wrap_text(st_text, f_step_text, text_max_w, draw)
        for sli, sl in enumerate(s_lines):
            draw.text((text_x, curr_y + sli * 26), sl, font=f_step_text, fill=c_dark)
        curr_y += max(len(s_lines) * 26 + 10, step_gap)

    # Note
    if note_clean:
        curr_y += 8
        note_lines = wrap_text(note_clean, f_note, MAX_TEXT_WIDTH_PX, draw)
        for nli, nl in enumerate(note_lines):
            draw.text((TEXT_COL_X, curr_y + nli * 25), nl, font=f_note, fill=c_blue)

    final_img = canvas.convert("RGB")
    for out_p in output_paths:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        final_img.save(out_p, "JPEG", quality=96, optimize=True)

    return final_img

def build_part_slides(spec_json_path: str, screens_dir: str):
    with open(spec_json_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    part_title = spec.get("part_title", "")
    output_dir_name = spec.get("output_dir", spec.get("part_id", "Output"))
    slides_out_dir = os.path.join(WORKSPACE_DIR, "Slides", output_dir_name)
    export_out_dir = os.path.join(WORKSPACE_DIR, "export", output_dir_name)

    os.makedirs(slides_out_dir, exist_ok=True)
    os.makedirs(export_out_dir, exist_ok=True)

    slides = spec.get("slides", [])
    print(f"Building {len(slides)} slides for {part_title}...")

    for s_idx, slide_def in enumerate(slides, 1):
        s_file = slide_def.get("screen_filename", "")
        screen_path = os.path.join(screens_dir, s_file)
        if not os.path.exists(screen_path):
            print(f"[{s_idx}/{len(slides)}] Warning: Screen not found: {screen_path}")
            continue

        screen_img = Image.open(screen_path)
        out_paths = [
            os.path.join(slides_out_dir, slide_def["filename"]),
            os.path.join(export_out_dir, slide_def["filename"])
        ]
        render_slide_from_spec(part_title, slide_def, screen_img, out_paths)
        print(f"[{s_idx}/{len(slides)}] Generated: {slide_def['filename']}")

    print("Slide compilation complete.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        build_part_slides(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python compose_slides.py <spec_json_path> <screens_dir>")
