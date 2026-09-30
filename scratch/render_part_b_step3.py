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

def create_number_badge(num: int, size: int = 30, bg_color = (18, 113, 208, 255), fg_color = (255, 255, 255, 255)):
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

def render_step3_slide(output_paths: list):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")
    screen_path = os.path.join(SCREENS_DIR, "02_admin_login.jpg")

    canvas = get_cached_base_background(bg_trans_path).copy()
    
    # 1. Compose PC monitor mockup with the login screen
    screen_img = Image.open(screen_path).convert("RGBA")
    mockup_img = compose_pc_screen(
        screen_img,
        pc_frame_path,
        crop_top_only=True,
        crop_align="center"
    )
    canvas.paste(mockup_img, (PC_POS_X, PC_POS_Y), mockup_img)

    # 2. Setup typography matching Libraries/Fonts.md
    draw = ImageDraw.Draw(canvas)
    c_blue = (18, 113, 208, 255)  # #1271D0
    c_gray = (88, 88, 90, 255)    # #58585A (Standard Paragraph Gray)
    c_orange = (255, 92, 53, 255) # Brand Orange #FF5C35

    font_medium = os.path.join(FONTS_DIR, "Rubik-Medium.ttf")
    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    # Kicker
    kicker = "PART B — FIRST-TIME SETUP (DO THIS ONLY ONCE PER TILL)"
    f_kicker = get_cached_font(font_medium, 22)
    draw.text((TEXT_COL_X, KICKER_Y + 5), kicker, font=f_kicker, fill=c_blue)

    # Heading
    heading = "Step 3 — Sign in as Admin"
    f_heading = get_cached_font(font_semibold, 48)
    draw.text((TEXT_COL_X, HEADING_Y + 8), heading, font=f_heading, fill=c_gray)

    # Primary Steps 1 to 4
    steps = [
        "Enter your Admin username.",
        "Enter your PIN or password.",
        "Tap Sign in.",
        "You should see the Home / main menu."
    ]

    badge_size = 30
    f_step = get_cached_font(font_regular, 23)
    cur_y = HEADING_Y + 82

    for i, text in enumerate(steps, start=1):
        badge = create_number_badge(i, size=badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, cur_y), badge)
        
        lines = wrap_text(text, f_step, MAX_TEXT_WIDTH_PX - badge_size - 16, draw)
        for j, line in enumerate(lines):
            draw.text((TEXT_COL_X + badge_size + 16, cur_y + 2 + j * 32), line, font=f_step, fill=c_gray)
        cur_y += max(50, len(lines) * 32 + 16)

    # "If login fails:" Troubleshooting Card
    card_y = cur_y + 20
    card_w = MAX_TEXT_WIDTH_PX
    card_h = 160
    
    card_img = Image.new("RGBA", (card_w, card_h), (247, 248, 250, 255))
    d_card = ImageDraw.Draw(card_img)
    # Left brand orange accent bar
    d_card.rectangle((0, 0, 4, card_h), fill=c_orange)

    f_card_title = get_cached_font(font_semibold, 19)
    f_card_item = get_cached_font(font_regular, 18)

    d_card.text((22, 16), "IF LOGIN FAILS:", font=f_card_title, fill=c_orange)

    fail_items = [
        "1. Check Caps Lock on physical keyboard.",
        "2. Tap Refresh on the login screen and try again.",
        "3. Ask Isarva support if your user account is active."
    ]

    item_y = 48
    for item in fail_items:
        d_card.text((22, item_y), item, font=f_card_item, fill=c_gray)
        item_y += 32

    canvas.paste(card_img, (TEXT_COL_X, card_y))

    # Save to targets
    for out_path in output_paths:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        canvas.convert("RGB").save(out_path, "JPEG", quality=96, optimize=True)
        print(f"Generated: {out_path}")

if __name__ == "__main__":
    targets = [
        os.path.join(WORKSPACE_DIR, "Slides", "Part B", "Step 3 - Sign in as Admin.jpg"),
        os.path.join(WORKSPACE_DIR, "export", "Part B", "Step 3 - Sign in as Admin.jpg"),
    ]
    render_step3_slide(targets)
