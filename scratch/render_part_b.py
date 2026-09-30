import os
import sys
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
RESTAURANT_APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app")
FONTS_DIR = os.path.join(APP_DIR, "fonts")
SCREENS_DIR = os.path.join(RESTAURANT_APP_DIR, "project", "screens")

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

def create_number_badge(num: int, size: int = 32, bg_color = (18, 113, 208, 255), fg_color = (255, 255, 255, 255)):
    """Draws a crisp antialiased circular badge with step number."""
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

def render_step_slide_exact(
    kicker: str,
    heading: str,
    body: str,
    steps: list,
    ending_note: str,
    screen_path: str,
    output_paths: list
):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")

    canvas = get_cached_base_background(bg_trans_path).copy()
    
    # 1. Compose PC monitor mockup with the screenshot
    screen_img = Image.open(screen_path).convert("RGBA")
    mockup_img = compose_pc_screen(
        screen_img,
        pc_frame_path,
        crop_top_only=True,
        crop_align="center"
    )
    canvas.paste(mockup_img, (PC_POS_X, PC_POS_Y), mockup_img)

    # 2. Setup typography matching Libraries/Fonts.md exactly:
    # Kicker: Rubik-Medium, #1271D0
    # Heading: Rubik-SemiBold, #58585A
    # Body/Paragraph: Rubik-Regular, #58585A
    # Bullet/Steps: Rubik-Regular, #58585A
    draw = ImageDraw.Draw(canvas)
    c_blue = (18, 113, 208, 255)  # #1271D0
    c_gray = (88, 88, 90, 255)    # #58585A (Standard Brand Paragraph Gray)

    font_medium = os.path.join(FONTS_DIR, "Rubik-Medium.ttf")
    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    # Kicker (Rubik-Medium)
    f_kicker = get_cached_font(font_medium, 22)
    k_bbox = draw.textbbox((0, 0), kicker, font=f_kicker)
    if k_bbox[2] - k_bbox[0] > MAX_TEXT_WIDTH_PX:
        f_kicker = get_cached_font(font_medium, 20)
    draw.text((TEXT_COL_X, KICKER_Y + 5), kicker, font=f_kicker, fill=c_blue)

    # Heading (Rubik-SemiBold)
    # Check if single line fits at 44pt or 42pt
    f_heading = get_cached_font(font_semibold, 48)
    h_lines = wrap_text(heading, f_heading, MAX_TEXT_WIDTH_PX, draw)
    if len(h_lines) > 1:
        f_try_single = get_cached_font(font_semibold, 43)
        h_try = wrap_text(heading, f_try_single, MAX_TEXT_WIDTH_PX, draw)
        if len(h_try) == 1:
            f_heading = f_try_single
            h_lines = h_try
        else:
            f_heading = get_cached_font(font_semibold, 46)
            h_lines = wrap_text(heading, f_heading, MAX_TEXT_WIDTH_PX, draw)


    cur_y = HEADING_Y + 8
    for hl in h_lines:
        draw.text((TEXT_COL_X, cur_y), hl, font=f_heading, fill=c_gray)
        cur_y += 52

    # Paragraph / Body Text (Rubik-Regular, #58585A)
    f_body = get_cached_font(font_regular, 24)
    body_lines = wrap_text(body, f_body, MAX_TEXT_WIDTH_PX, draw)
    cur_y += 10
    for bl in body_lines:
        draw.text((TEXT_COL_X, cur_y), bl, font=f_body, fill=c_gray)
        cur_y += 34

    # Steps (Rubik-Regular, #58585A)
    num_steps = len(steps)
    if num_steps <= 3:
        badge_size = 34
        f_step = get_cached_font(font_regular, 24)
        line_height = 34
        step_spacing = 64
        cur_y = max(cur_y + 35, 480)
    else:
        badge_size = 28
        f_step = get_cached_font(font_regular, 22)
        line_height = 30
        step_spacing = 46
        cur_y = max(cur_y + 20, 440)

    for i, step_item in enumerate(steps, start=1):
        badge = create_number_badge(i, size=badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, cur_y), badge)

        text = str(step_item)
        if text.startswith(f"{i}. "):
            text = text[len(f"{i}. "):]

        lines = wrap_text(text, f_step, MAX_TEXT_WIDTH_PX - badge_size - 16, draw)
        for j, line in enumerate(lines):
            draw.text((TEXT_COL_X + badge_size + 16, cur_y + 2 + j * line_height), line, font=f_step, fill=c_gray)

        cur_y += max(step_spacing, len(lines) * line_height + 14)

    # Ending Note (Rubik-Regular, #58585A)
    if ending_note:
        f_ending = get_cached_font(font_regular, 22)
        end_lines = wrap_text(ending_note, f_ending, MAX_TEXT_WIDTH_PX, draw)
        cur_y += 15
        for el in end_lines:
            draw.text((TEXT_COL_X, cur_y), el, font=f_ending, fill=c_gray)
            cur_y += 32

    # Save output files
    for out_path in output_paths:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        canvas.convert("RGB").save(out_path, "JPEG", quality=96, optimize=True)
        print(f"Generated: {out_path}")

def generate_part_b_slides():
    kicker = "PART B — FIRST-TIME SETUP (DO THIS ONLY ONCE PER TILL)"

    # Step 1
    heading1 = "Step 1 — Open the POS website"
    body1 = "Open your web browser on the POS till terminal to access the cloud portal."
    steps1 = [
        "Open your browser.",
        "Go to: https://app.restaurant-pos.isarva.in",
        "Wait for the login / activate screen to open."
    ]
    screen1 = os.path.join(SCREENS_DIR, "02_admin_login.jpg")
    targets1 = [
        os.path.join(WORKSPACE_DIR, "Slides", "Part B", "Step 1 - Open the POS website.jpg"),
        os.path.join(WORKSPACE_DIR, "export", "Part B", "Step 1 - Open the POS website.jpg"),
    ]
    render_step_slide_exact(kicker, heading1, body1, steps1, "", screen1, targets1)

    # Step 2
    heading2 = "Step 2 — Activate this POS for your restaurant"
    body2 = "This is the first and most important step."
    steps2 = [
        "On the screen, find Activate POS (or company code box).",
        "Type your Company Code given by Isarva. Example: C001 (You can also use VAT / tax ID if Isarva registered that for you.)",
        "Company code must be at least 3 characters.",
        "Tap or click Activate POS.",
        "Wait until the screen shows your restaurant name.",
        "If activation fails, check the code again. If still failing, call Isarva support."
    ]
    ending2 = "After activation, this till belongs to your restaurant only."
    screen2 = os.path.join(SCREENS_DIR, "01_activate_pos.jpg")
    targets2 = [
        os.path.join(WORKSPACE_DIR, "Slides", "Part B", "Step 2 - Activate this POS for your restaurant.jpg"),
        os.path.join(WORKSPACE_DIR, "export", "Part B", "Step 2 - Activate this POS for your restaurant.jpg"),
    ]
    render_step_slide_exact(kicker, heading2, body2, steps2, ending2, screen2, targets2)

if __name__ == "__main__":
    generate_part_b_slides()
