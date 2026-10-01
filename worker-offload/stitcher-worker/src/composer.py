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
    base_canvas = Image.new("RGBA", (SLIDE_WIDTH_PX, SLIDE_HEIGHT_PX), COLOR_WHITE)
    bg_img = get_cached_image(BG_CANVAS_PATH)
    base_canvas.paste(bg_img, (0, 0), bg_img)
    canvas = base_canvas

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

def compose_info_slide(
    kicker: str,
    heading: str,
    description: str = "",
    items: Optional[List[Any]] = None,
    note: str = "",
    columns: int = 2
) -> Image.Image:
    """
    Renders high-fidelity Information Slides (Checklists, Troubleshooting, Security, Support)
    without PC monitor mockups, utilizing full-bleed structured card layouts.
    """
    items = items or []
    base_canvas = Image.new("RGBA", (SLIDE_WIDTH_PX, SLIDE_HEIGHT_PX), COLOR_WHITE)
    bg_img = get_cached_image(BG_CANVAS_PATH)
    base_canvas.paste(bg_img, (0, 0), bg_img)
    canvas = base_canvas
    draw = ImageDraw.Draw(canvas)

    f_kicker = get_cached_font(FONT_SEMIBOLD_PATH, 24)
    f_heading = get_cached_font(FONT_SEMIBOLD_PATH, 42)
    f_desc = get_cached_font(FONT_REGULAR_PATH, 22)
    f_item_title = get_cached_font(FONT_SEMIBOLD_PATH, 20)
    f_item_text = get_cached_font(FONT_REGULAR_PATH, 19)
    f_note = get_cached_font(FONT_REGULAR_PATH, 18)

    # 1. Header
    curr_y = 100
    if kicker:
        draw.text((100, curr_y), clean_unicode_arrows(kicker), font=f_kicker, fill=COLOR_BLUE)
        curr_y += 38

    head_lines = wrap_text(clean_unicode_arrows(heading), f_heading, 1720, draw)
    for hl in head_lines:
        draw.text((100, curr_y), hl, font=f_heading, fill=COLOR_DARK)
        curr_y += 50

    if description:
        curr_y += 6
        desc_lines = wrap_text(clean_unicode_arrows(description), f_desc, 1720, draw)
        for dl in desc_lines:
            draw.text((100, curr_y), dl, font=f_desc, fill=COLOR_GRAY)
            curr_y += 30

    curr_y += 24
    content_start_y = curr_y

    # 2. Content Layout (2 columns or 1 column)
    import re
    col_width = 820 if columns == 2 else 1720
    col_gap = 80
    badge_size = 28

    n_items = len(items)
    items_per_col = (n_items + 1) // 2 if columns == 2 else n_items

    if columns == 1:
        row_height = 85 if n_items <= 6 else 65
    else:
        if n_items <= 8:
            row_height = 85
        elif n_items <= 12:
            row_height = 70
        else:
            row_height = 54

    for idx, item in enumerate(items, 1):
        if columns == 2 and idx > items_per_col:
            col_x = 100 + col_width + col_gap
            item_y = content_start_y + (idx - 1 - items_per_col) * row_height
        else:
            col_x = 100
            item_y = content_start_y + ((idx - 1) % items_per_col) * row_height

        if isinstance(item, dict):
            t_title = clean_unicode_arrows(item.get("title", ""))
            t_desc = clean_unicode_arrows(item.get("desc", item.get("body", "")))
            badge_text = item.get("badge", str(idx))
        else:
            t_title = clean_unicode_arrows(str(item))
            t_desc = ""
            badge_text = str(idx)

        # Strip duplicate leading numbers like "1. " if already using numeric badge
        t_title = re.sub(r'^\d+\.\s*', '', t_title)

        # Draw number / check badge
        badge = create_number_badge(badge_text if badge_text.isdigit() else idx, size=badge_size, bg_color=COLOR_BLUE)
        canvas.paste(badge, (col_x, item_y + 2), badge)

        text_x = col_x + badge_size + 14
        max_w = col_width - (badge_size + 14)

        if t_desc:
            draw.text((text_x, item_y), t_title, font=f_item_title, fill=COLOR_DARK)
            desc_lines = wrap_text(t_desc, f_item_text, max_w, draw)
            for dli, dline in enumerate(desc_lines):
                draw.text((text_x, item_y + 26 + dli * 24), dline, font=f_item_text, fill=COLOR_GRAY)
        else:
            lines = wrap_text(t_title, f_item_text, max_w, draw)
            for li, line in enumerate(lines):
                draw.text((text_x, item_y + li * 24), line, font=f_item_text, fill=COLOR_DARK)

    # 3. Footer Note (placed safely above www.isarvait.com footer bar)
    if note:
        note_clean = clean_unicode_arrows(note)
        draw.text((100, 815), note_clean, font=f_note, fill=COLOR_BLUE)

    return canvas.convert("RGB")

def resize_image(image: Image.Image, target_width: int, target_height: Optional[int] = None) -> Image.Image:
    orig_w, orig_h = image.size
    if target_height is None:
        target_height = int(orig_h * (target_width / orig_w))
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)

