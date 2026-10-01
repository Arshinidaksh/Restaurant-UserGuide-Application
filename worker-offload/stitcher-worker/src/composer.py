"""
Slide Composer and Image Stitcher Engine
Executes in-memory fitting into PC hardware frames, typography layout, and resizing.
"""
import os
import io
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from .config import (
    SLIDE_WIDTH_PX, SLIDE_HEIGHT_PX,
    COLOR_BLUE, COLOR_GRAY, COLOR_DARK, COLOR_WHITE,
    PC_POS_X, PC_POS_Y,
    PC_SCREEN_X, PC_SCREEN_Y, PC_SCREEN_WIDTH, PC_SCREEN_HEIGHT,
    TEXT_COL_X, KICKER_Y, HEADING_Y, MAX_TEXT_WIDTH_PX,
    PC_FRAME_PATH, BG_CANVAS_PATH,
    FONT_REGULAR_PATH, FONT_SEMIBOLD_PATH
)

_cached_images = {}
_cached_fonts = {}

def get_cached_image(path: str) -> Image.Image:
    if path not in _cached_images:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Asset file not found: {path}")
        _cached_images[path] = Image.open(path).convert("RGBA")
    return _cached_images[path]

def get_cached_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _cached_fonts:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Font file not found: {path}")
        _cached_fonts[key] = ImageFont.truetype(path, size)
    return _cached_fonts[key]

def clean_unicode_arrows(text: str) -> str:
    if not text:
        return ""
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

def create_number_badge(num: int, size: int = 28, bg_color = COLOR_BLUE, fg_color = COLOR_WHITE) -> Image.Image:
    scale = 4
    im = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, size * scale - 1, size * scale - 1), fill=bg_color)
    font = get_cached_font(FONT_SEMIBOLD_PATH, int((size * 0.58) * scale))
    text = str(num)
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size * scale - tw) / 2
    ty = (size * scale - th) / 2 - 2 * scale
    d.text((tx, ty), text, font=font, fill=fg_color)
    return im.resize((size, size), Image.Resampling.LANCZOS)

def fit_screen_into_pc_mockup(screen_img: Image.Image) -> Image.Image:
    frame = get_cached_image(PC_FRAME_PATH).copy()
    screen_rgba = screen_img.convert("RGBA") if screen_img.mode != "RGBA" else screen_img

    target_w = PC_SCREEN_WIDTH
    target_h = PC_SCREEN_HEIGHT

    fitted_screen = screen_rgba.resize((target_w, target_h), Image.Resampling.LANCZOS)
    frame.paste(fitted_screen, (PC_SCREEN_X, PC_SCREEN_Y))
    return frame

def compose_slide(
    screen_img: Image.Image,
    kicker: str,
    heading: str,
    where: str = "",
    steps: Optional[List[str]] = None,
    note: str = ""
) -> Image.Image:
    steps = steps or []
    canvas = get_cached_image(BG_CANVAS_PATH).copy()

    # 1. Hardware Mockup with screen
    mockup_img = fit_screen_into_pc_mockup(screen_img)
    canvas.paste(mockup_img, (PC_POS_X, PC_POS_Y), mockup_img)

    # 2. Typography & Text layout
    draw = ImageDraw.Draw(canvas)

    f_kicker = get_cached_font(FONT_SEMIBOLD_PATH, 20)
    f_heading = get_cached_font(FONT_SEMIBOLD_PATH, 38)
    f_where = get_cached_font(FONT_REGULAR_PATH, 20)
    f_step_text = get_cached_font(FONT_REGULAR_PATH, 19)
    f_note = get_cached_font(FONT_REGULAR_PATH, 18)

    kicker_clean = clean_unicode_arrows(kicker)
    heading_clean = clean_unicode_arrows(heading)
    where_clean = clean_unicode_arrows(where)
    note_clean = clean_unicode_arrows(note)
    steps_clean = [clean_unicode_arrows(s) for s in steps]

    # Kicker
    if kicker_clean:
        draw.text((TEXT_COL_X, KICKER_Y), kicker_clean, font=f_kicker, fill=COLOR_BLUE)

    # Heading
    head_lines = wrap_text(heading_clean, f_heading, MAX_TEXT_WIDTH_PX, draw)
    curr_y = HEADING_Y
    for hl in head_lines:
        draw.text((TEXT_COL_X, curr_y), hl, font=f_heading, fill=COLOR_DARK)
        curr_y += 46

    # Where / Location
    if where_clean:
        curr_y += 6
        draw.text((TEXT_COL_X, curr_y), where_clean, font=f_where, fill=COLOR_GRAY)
        curr_y += 30

    curr_y += 18

    # Steps with badges
    step_badge_size = 28
    n_steps = len(steps_clean)
    step_gap = 40 if n_steps <= 5 else 34

    for idx, st_text in enumerate(steps_clean, 1):
        badge = create_number_badge(idx, size=step_badge_size, bg_color=COLOR_BLUE)
        canvas.paste(badge, (TEXT_COL_X, curr_y + 2), badge)

        text_x = TEXT_COL_X + step_badge_size + 16
        text_max_w = MAX_TEXT_WIDTH_PX - (step_badge_size + 16)
        s_lines = wrap_text(st_text, f_step_text, text_max_w, draw)
        for sli, sl in enumerate(s_lines):
            draw.text((text_x, curr_y + sli * 26), sl, font=f_step_text, fill=COLOR_DARK)
        curr_y += max(len(s_lines) * 26 + 10, step_gap)

    # Note
    if note_clean:
        curr_y += 8
        note_lines = wrap_text(note_clean, f_note, MAX_TEXT_WIDTH_PX, draw)
        for nli, nl in enumerate(note_lines):
            draw.text((TEXT_COL_X, curr_y + nli * 25), nl, font=f_note, fill=COLOR_BLUE)

    return canvas.convert("RGB")

def resize_image(image: Image.Image, target_width: int, target_height: Optional[int] = None) -> Image.Image:
    orig_w, orig_h = image.size
    if target_height is None:
        target_height = int(orig_h * (target_width / orig_w))
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)
