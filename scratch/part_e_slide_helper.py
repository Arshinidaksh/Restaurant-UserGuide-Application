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

def render_part_e_step_slide(step_num: int, heading: str, body: str, steps: list, screen_img: Image.Image, output_paths: list):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")

    canvas = get_cached_base_background(bg_trans_path).copy()

    # 1. Compose PC monitor mockup with the screen - full height visible without top cropping
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

    f_kicker = get_cached_font(font_semibold, 20)
    f_heading = get_cached_font(font_semibold, 42)
    f_body = get_cached_font(font_regular, 20)
    f_step_num = get_cached_font(font_semibold, 16)
    f_step_text = get_cached_font(font_regular, 20)
    f_brand = get_cached_font(font_semibold, 28)

    # Kicker
    kicker_text = "PART E — SETTLE SCREEN (PAYMENT & SPLIT)"
    draw.text((TEXT_COL_X, KICKER_Y), kicker_text, font=f_kicker, fill=c_blue)

    # Heading (wrapped)
    head_lines = wrap_text(heading, f_heading, MAX_TEXT_WIDTH_PX, draw)
    curr_y = HEADING_Y
    for hl in head_lines:
        draw.text((TEXT_COL_X, curr_y), hl, font=f_heading, fill=c_dark)
        curr_y += 50

    # Body
    curr_y += 10
    body_lines = wrap_text(body, f_body, MAX_TEXT_WIDTH_PX, draw)
    for bl in body_lines:
        draw.text((TEXT_COL_X, curr_y), bl, font=f_body, fill=c_gray)
        curr_y += 30

    curr_y += 22

    # Steps list
    step_badge_size = 28
    for idx, st_text in enumerate(steps, 1):
        badge = create_number_badge(idx, size=step_badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, curr_y + 2), badge)

        text_x = TEXT_COL_X + step_badge_size + 16
        text_max_w = MAX_TEXT_WIDTH_PX - (step_badge_size + 16)
        s_lines = wrap_text(st_text, f_step_text, text_max_w, draw)
        for sli, sl in enumerate(s_lines):
            draw.text((text_x, curr_y + sli * 28), sl, font=f_step_text, fill=c_dark)
        curr_y += max(len(s_lines) * 28 + 14, 38)


    final_img = canvas.convert("RGB")
    for out_p in output_paths:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        final_img.save(out_p, "JPEG", quality=96, optimize=True)
        print(f"Generated: {out_p}")

    return final_img
