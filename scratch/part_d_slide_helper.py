import os
import sys
from PIL import Image, ImageDraw, ImageFont

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

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw):
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

def create_number_badge(num: int, size: int = 30, bg_color = (18, 113, 208, 255), fg_color = (255, 255, 255, 255)):
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

def draw_pill(draw, xy, text, font, fill, text_fill, outline=None, radius=6):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x, y = xy
    w = tw + 20
    h = max(th + 12, 34)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill, outline=outline, width=1 if outline else 0)
    tx = x + (w - tw) / 2
    ty = y + (h - th) / 2 - 2
    draw.text((tx, ty), text, font=font, fill=text_fill)
    return w, h

def render_part_d_step_slide(step_num: int, heading: str, body: str, steps: list, screen_img: Image.Image, output_paths: list):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")

    canvas = get_cached_base_background(bg_trans_path).copy()

    # 1. Compose PC monitor mockup with the screen
    mockup_img = compose_pc_screen(
        screen_img.convert("RGBA"),
        pc_frame_path,
        crop_top_only=False,
        crop_align="center"
    )
    canvas.paste(mockup_img, (PC_POS_X, PC_POS_Y), mockup_img)

    # 2. Typography
    draw = ImageDraw.Draw(canvas)
    c_blue = (18, 113, 208, 255)  # #1271D0
    c_gray = (88, 88, 90, 255)    # #58585A
    c_dark = (35, 35, 35, 255)

    font_medium = os.path.join(FONTS_DIR, "Rubik-Medium.ttf")
    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    # Kicker
    kicker = "PART D — HOW TO TAKE A DINE-IN ORDER (FLOOR)"
    f_kicker = get_cached_font(font_medium, 22)
    draw.text((TEXT_COL_X, KICKER_Y + 5), kicker, font=f_kicker, fill=c_blue)

    # Heading
    f_heading = get_cached_font(font_semibold, 42)
    h_lines = wrap_text(heading, f_heading, MAX_TEXT_WIDTH_PX, draw)
    cur_y = HEADING_Y + 4
    for hl in h_lines:
        draw.text((TEXT_COL_X, cur_y), hl, font=f_heading, fill=c_gray)
        cur_y += 50

    # Body description
    if body:
        f_body = get_cached_font(font_regular, 23)
        b_lines = wrap_text(body, f_body, MAX_TEXT_WIDTH_PX, draw)
        cur_y += 8
        for bl in b_lines:
            draw.text((TEXT_COL_X, cur_y), bl, font=f_body, fill=c_gray)
            cur_y += 32

    # Steps
    badge_size = 28
    f_step = get_cached_font(font_regular, 21)
    cur_y = max(cur_y + 18, 410)

    # Auto adjust step spacing based on number of steps
    n_steps = len(steps)
    step_gap = 42 if n_steps <= 6 else 36

    for i, text in enumerate(steps, start=1):
        badge = create_number_badge(i, size=badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, cur_y), badge)
        
        lines = wrap_text(text, f_step, MAX_TEXT_WIDTH_PX - badge_size - 16, draw)
        for j, line in enumerate(lines):
            draw.text((TEXT_COL_X + badge_size + 16, cur_y + 2 + j * 27), line, font=f_step, fill=c_gray)
        cur_y += max(step_gap, len(lines) * 27 + 10)

    for out_path in output_paths:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        canvas.convert("RGB").save(out_path, "JPEG", quality=96, optimize=True)
        print(f"Generated: {out_path}")

print("Helper loaded successfully!")
