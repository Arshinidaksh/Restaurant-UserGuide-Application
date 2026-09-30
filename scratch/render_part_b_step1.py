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
    SLIDE_WIDTH_PX, SLIDE_HEIGHT_PX,
    PC_POS_X, PC_POS_Y,
    TEXT_COL_X, KICKER_Y, HEADING_Y, BODY_Y,
    MAX_TEXT_WIDTH_PX
)
from src.cache import get_cached_base_background, get_cached_font, get_cached_icon

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

def create_number_badge(num: int, size: int = 34, bg_color = (18, 113, 208, 255), fg_color = (255, 255, 255, 255)):
    """Draws a crisp antialiased circular badge with step number."""
    scale = 4
    im = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, size * scale - 1, size * scale - 1), fill=bg_color)
    
    font_path = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font = ImageFont.truetype(font_path, int(20 * scale))
    text = str(num)
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size * scale - tw) / 2
    ty = (size * scale - th) / 2 - 2 * scale
    d.text((tx, ty), text, font=font, fill=fg_color)
    
    return im.resize((size, size), Image.Resampling.LANCZOS)

def render_step_slide(
    kicker: str,
    heading: str,
    body: str,
    steps: list,
    screen_path: str,
    output_path: str
):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")

    canvas = get_cached_base_background(bg_trans_path).copy()
    
    # 1. Compose PC monitor mockup with the screen
    screen_img = Image.open(screen_path).convert("RGBA")
    mockup_img = compose_pc_screen(
        screen_img,
        pc_frame_path,
        crop_top_only=True,
        crop_align="center"
    )
    canvas.paste(mockup_img, (PC_POS_X, PC_POS_Y), mockup_img)

    # 2. Setup typography
    draw = ImageDraw.Draw(canvas)
    c_blue = (18, 113, 208, 255)  # #1271D0
    c_gray = (88, 88, 90, 255)    # #58585A
    c_dark = (35, 35, 35, 255)

    font_medium = os.path.join(FONTS_DIR, "Rubik-Medium.ttf")
    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    # Kicker auto-fit
    f_kicker = get_cached_font(font_medium, 24)
    k_bbox = draw.textbbox((0, 0), kicker, font=f_kicker)
    if k_bbox[2] - k_bbox[0] > MAX_TEXT_WIDTH_PX:
        f_kicker = get_cached_font(font_medium, 21)

    draw.text((TEXT_COL_X, KICKER_Y + 5), kicker, font=f_kicker, fill=c_blue)

    # Heading
    f_heading = get_cached_font(font_semibold, 52)
    h_bbox = draw.textbbox((0, 0), heading, font=f_heading)
    if h_bbox[2] - h_bbox[0] > MAX_TEXT_WIDTH_PX:
        f_heading = get_cached_font(font_semibold, 44)
    
    draw.text((TEXT_COL_X, HEADING_Y + 5), heading, font=f_heading, fill=c_gray)

    # Body
    f_body = get_cached_font(font_regular, 24)
    body_lines = wrap_text(body, f_body, MAX_TEXT_WIDTH_PX, draw)
    cur_y = HEADING_Y + 75
    for line in body_lines:
        draw.text((TEXT_COL_X, cur_y), line, font=f_body, fill=c_gray)
        cur_y += 34

    # Steps with circular number badges
    cur_y = max(cur_y + 40, 480)
    badge_size = 36
    f_step_text = get_cached_font(font_medium, 24)

    for i, step_item in enumerate(steps, start=1):
        badge = create_number_badge(i, size=badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, cur_y), badge)
        
        text = str(step_item)
        cleaned_text = text
        if cleaned_text.startswith(f"{i}. "):
            cleaned_text = cleaned_text[len(f"{i}. "):]
        
        lines = wrap_text(cleaned_text, f_step_text, MAX_TEXT_WIDTH_PX - badge_size - 18, draw)
        for j, line in enumerate(lines):
            draw.text((TEXT_COL_X + badge_size + 18, cur_y + 3 + j * 34), line, font=f_step_text, fill=(50, 50, 50, 255))
        cur_y += max(68, len(lines) * 34 + 30)

    # Optional subtle tip banner at bottom
    tip_y = cur_y + 10
    if tip_y <= 780:
        tip_box = Image.new("RGBA", (MAX_TEXT_WIDTH_PX, 72), (242, 246, 252, 255))
        d_tip = ImageDraw.Draw(tip_box)
        # Left blue accent bar
        d_tip.rectangle((0, 0, 4, 72), fill=c_blue)
        f_tip_bold = get_cached_font(font_semibold, 18)
        f_tip_reg = get_cached_font(font_regular, 18)
        d_tip.text((20, 14), "PRO TIP FOR CASHIERS & MANAGERS", font=f_tip_bold, fill=c_blue)
        d_tip.text((20, 38), "Bookmark this web URL on your browser bar for instant 1-tap launch.", font=f_tip_reg, fill=c_gray)
        canvas.paste(tip_box, (TEXT_COL_X, tip_y))


    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.convert("RGB").save(output_path, "JPEG", quality=96, optimize=True)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    kicker = "PART B — FIRST-TIME SETUP (DO THIS ONLY ONCE PER TILL)"
    heading = "Step 1 — Open the POS website"
    body = "Open Google Chrome or Microsoft Edge on your till terminal and navigate to the cloud portal."
    steps = [
        "Open your browser.",
        "Go to: https://app.restaurant-pos.isarva.in",
        "Wait for the login / activate screen to open."
    ]
    screen = os.path.join(SCREENS_DIR, "02_admin_login.jpg")
    
    # Save single slide file
    out_file1 = os.path.join(WORKSPACE_DIR, "Slides", "Part B", "Step 1 - Open the POS website.jpg")
    render_step_slide(kicker, heading, body, steps, screen, out_file1)
    
    out_file2 = os.path.join(WORKSPACE_DIR, "export", "Part B", "Step 1 - Open the POS website.jpg")
    render_step_slide(kicker, heading, body, steps, screen, out_file2)


