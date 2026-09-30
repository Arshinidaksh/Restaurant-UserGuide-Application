"""
Preview Renderer: Generates 1920x1080 pixel-perfect JPG slides using Pillow.
Optimized with in-memory background, font, and icon caching for ultra-fast execution.
"""
import os
from typing import Dict, Any, List, Union
from PIL import Image, ImageDraw, ImageFont

from .config import (
    SLIDE_WIDTH_PX,
    SLIDE_HEIGHT_PX,
    PC_POS_X,
    PC_POS_Y,
    TEXT_COL_X,
    KICKER_Y,
    HEADING_Y,
    BODY_Y,
    CHECK_ICON_SIZE,
    MAX_TEXT_WIDTH_PX
)
from .cache import (
    get_cached_font,
    get_cached_icon,
    get_cached_base_background
)

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
    """Wraps text within a maximum pixel width using cached font measurement."""
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

def render_slide_preview(
    content: Dict[str, Any],
    bg_path: str,
    pc_mockup: Image.Image,
    check_icon_path: str,
    fonts_dir: str,
    output_path: str
) -> str:
    """
    Renders a 1920x1080 high quality JPG of the slide matching Complete-design.jpg.
    Pure in-memory compositing with zero intermediate disk writes.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Base canvas from cached pre-composited background
    canvas = get_cached_base_background(bg_path).copy()

    # 2. Monitor Mockup
    canvas.paste(pc_mockup, (PC_POS_X, PC_POS_Y), pc_mockup)

    # 3. Setup Cached Fonts
    font_medium = os.path.join(fonts_dir, "Rubik-Medium.ttf")
    font_semibold = os.path.join(fonts_dir, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(fonts_dir, "Rubik-Regular.ttf")

    f_kicker = get_cached_font(font_medium, 28)
    f_heading = get_cached_font(font_semibold, 64)
    f_body = get_cached_font(font_regular, 24)
    f_bullet = get_cached_font(font_regular, 24)
    f_ending = get_cached_font(font_regular, 24)

    draw = ImageDraw.Draw(canvas)
    c_blue = (18, 113, 208, 255)  # #1271D0
    c_gray = (88, 88, 90, 255)    # #58585A

    # 4. Kicker (Optional)
    kicker_text = content.get("kicker", "").strip()
    if kicker_text:
        draw.text((TEXT_COL_X, KICKER_Y + 5), kicker_text, font=f_kicker, fill=c_blue)
        y_heading = HEADING_Y + 10
    else:
        y_heading = KICKER_Y + 15

    # 5. Heading (Auto-wrapped and responsive)
    heading_text = content.get("heading", "")
    h_bbox = draw.textbbox((0, 0), heading_text, font=f_heading)
    if h_bbox[2] - h_bbox[0] > MAX_TEXT_WIDTH_PX:
        f_heading_fitted = get_cached_font(font_semibold, 48)
        heading_lines = wrap_text(heading_text, f_heading_fitted, MAX_TEXT_WIDTH_PX, draw)
        f_use_heading = f_heading_fitted
        h_line_height = 54
    else:
        heading_lines = [heading_text]
        f_use_heading = f_heading
        h_line_height = 68

    cur_h_y = y_heading
    for h_line in heading_lines:
        draw.text((TEXT_COL_X, cur_h_y), h_line, font=f_use_heading, fill=c_gray)
        cur_h_y += h_line_height

    # 6. Body
    body_text = content.get("body", "")
    body_lines = wrap_text(body_text, f_body, MAX_TEXT_WIDTH_PX, draw)
    y_body = cur_h_y + (15 if len(heading_lines) > 1 else 20)
    for line in body_lines:
        draw.text((TEXT_COL_X, y_body), line, font=f_body, fill=c_gray)
        y_body += 33

    # 7. Bullets with Cached Icon
    bullets = content.get("bullets", [])
    icon = get_cached_icon(check_icon_path, (CHECK_ICON_SIZE, CHECK_ICON_SIZE))

    ending_text = content.get("ending", "").strip()
    bullet_spacing = 52 if not ending_text else 46
    y_bullet = max(y_body + 25, 470)

    for b in bullets:
        canvas.paste(icon, (TEXT_COL_X, y_bullet), icon)
        b_lines = wrap_text(b, f_bullet, MAX_TEXT_WIDTH_PX - CHECK_ICON_SIZE - 15, draw)
        for i, bl in enumerate(b_lines):
            draw.text((TEXT_COL_X + CHECK_ICON_SIZE + 12, y_bullet - 2 + i * 32), bl, font=f_bullet, fill=c_gray)
        y_bullet += max(bullet_spacing, len(b_lines) * 32 + 12)

    # 8. Optional ending sentence
    if ending_text:
        ending_lines = wrap_text(ending_text, f_ending, MAX_TEXT_WIDTH_PX, draw)
        y_ending = y_bullet + 15
        for line in ending_lines:
            draw.text((TEXT_COL_X, y_ending), line, font=f_ending, fill=c_gray)
            y_ending += 33

    # 9. Save final JPEG
    canvas.convert("RGB").save(output_path, "JPEG", quality=96, optimize=True)
    return output_path
