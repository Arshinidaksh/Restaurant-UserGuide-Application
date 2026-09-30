import os
import sys
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
RESTAURANT_APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app")
FONTS_DIR = os.path.join(APP_DIR, "fonts")
SCREENS_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "project", "screens")

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

def render_step7_slide(output_paths: list):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")
    screen_path = os.path.join(SCREENS_DIR, "16_masters_new_dish.jpg")

    canvas = get_cached_base_background(bg_trans_path).copy()

    
    # 1. Compose PC monitor mockup with the food menu & catalog screen
    screen_img = Image.open(screen_path).convert("RGBA")
    mockup_img = compose_pc_screen(
        screen_img,
        pc_frame_path,
        crop_top_only=True,
        crop_align="left"
    )
    canvas.paste(mockup_img, (PC_POS_X, PC_POS_Y), mockup_img)

    # 2. Typography matching Libraries/Fonts.md
    draw = ImageDraw.Draw(canvas)
    c_blue = (18, 113, 208, 255)  # #1271D0
    c_gray = (88, 88, 90, 255)    # #58585A (Standard Paragraph Gray)
    c_green = (3, 142, 65, 255)

    font_medium = os.path.join(FONTS_DIR, "Rubik-Medium.ttf")
    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    # Kicker
    kicker = "PART B — FIRST-TIME SETUP (DO THIS ONLY ONCE PER TILL)"
    f_kicker = get_cached_font(font_medium, 22)
    draw.text((TEXT_COL_X, KICKER_Y + 5), kicker, font=f_kicker, fill=c_blue)

    # Heading
    heading = "Step 7 — Create your menu (Masters)"
    f_heading = get_cached_font(font_semibold, 44)
    h_lines = wrap_text(heading, f_heading, MAX_TEXT_WIDTH_PX, draw)
    cur_y = HEADING_Y + 8
    for hl in h_lines:
        draw.text((TEXT_COL_X, cur_y), hl, font=f_heading, fill=c_gray)
        cur_y += 52

    # Subtitle / Body
    body = "Follow Part N (Products / catalog) in detail. Short path:"
    f_body = get_cached_font(font_regular, 24)
    body_lines = wrap_text(body, f_body, MAX_TEXT_WIDTH_PX, draw)
    cur_y += 10
    for bl in body_lines:
        draw.text((TEXT_COL_X, cur_y), bl, font=f_body, fill=c_gray)
        cur_y += 34

    # Steps (1 to 5)
    steps = [
        "Open Masters (or Settings > Products).",
        "Create Categories, then Dishes.",
        "Create Addons and attach them to dishes.",
        "Set Tax, Units, Departments, Extra Charges as needed.",
        "Sync other tills after save."
    ]

    badge_size = 28
    f_step = get_cached_font(font_regular, 21)
    cur_y = max(cur_y + 20, 435)

    for i, text in enumerate(steps, start=1):
        badge = create_number_badge(i, size=badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, cur_y), badge)
        
        lines = wrap_text(text, f_step, MAX_TEXT_WIDTH_PX - badge_size - 16, draw)
        for j, line in enumerate(lines):
            draw.text((TEXT_COL_X + badge_size + 16, cur_y + 2 + j * 28), line, font=f_step, fill=c_gray)
        cur_y += max(46, len(lines) * 28 + 14)

    # Master Data Sync Note Card
    note_box_y = cur_y + 12
    box_w = MAX_TEXT_WIDTH_PX
    box_h = 76
    note_box = Image.new("RGBA", (box_w, box_h), (242, 248, 244, 255))
    d_note = ImageDraw.Draw(note_box)
    d_note.rectangle((0, 0, 4, box_h), fill=c_green)

    f_note_title = get_cached_font(font_semibold, 17)
    f_note_desc = get_cached_font(font_regular, 17)

    d_note.text((18, 12), "MULTI-TILL CATALOG SYNCHRONIZATION", font=f_note_title, fill=c_green)
    d_note.text((18, 34), "Once saved, dish prices and categories synchronize across all branch tills.", font=f_note_desc, fill=c_gray)
    d_note.text((18, 52), "Refer to Part N for advanced modifiers, combos, and recipe cost cards.", font=f_note_desc, fill=c_gray)

    canvas.paste(note_box, (TEXT_COL_X, note_box_y))

    for out_path in output_paths:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        canvas.convert("RGB").save(out_path, "JPEG", quality=96, optimize=True)
        print(f"Generated: {out_path}")

if __name__ == "__main__":
    targets = [
        os.path.join(WORKSPACE_DIR, "Slides", "Part B", "Step 7 - Create your menu (Masters).jpg"),
        os.path.join(WORKSPACE_DIR, "export", "Part B", "Step 7 - Create your menu (Masters).jpg"),
    ]
    render_step7_slide(targets)
