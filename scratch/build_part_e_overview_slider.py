import os
import sys
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
sys.path.insert(0, APP_DIR)

from src.cache import get_cached_font, get_cached_image, get_cached_icon

FONTS_DIR = os.path.join(APP_DIR, "fonts")
SLIDES_DIR = os.path.join(WORKSPACE_DIR, "Slides", "Part E")
EXPORT_DIR = os.path.join(WORKSPACE_DIR, "export", "Part E")

os.makedirs(SLIDES_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

# Brand Colors
COLOR_GREEN = (3, 142, 65, 255)         # #038E41 Brand Green
COLOR_GRAY_DARK = (30, 41, 59, 255)     # Deep dark title
COLOR_GRAY_TEXT = (88, 88, 90, 255)     # Body text #58585A
COLOR_CARD_BORDER = (218, 226, 236, 255)# Card border

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

def get_flow_arrow_badge(size: int = 34, arrow_color = COLOR_GREEN, direction: str = "right") -> Image.Image:
    scale = 4
    big_size = size * scale
    im = Image.new("RGBA", (big_size, big_size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    pad = 2 * scale
    d.ellipse((pad, pad, big_size - pad, big_size - pad), fill=(235, 248, 241, 255), outline=(180, 226, 202, 255), width=int(2.0 * scale))

    cx = big_size // 2
    cy = big_size // 2
    line_w = int(3.2 * scale)

    if direction == "right":
        d.line([(cx - 8 * scale, cy), (cx + 7 * scale, cy)], fill=arrow_color, width=line_w)
        d.line([(cx + 1 * scale, cy - 6 * scale), (cx + 7 * scale, cy)], fill=arrow_color, width=line_w)
        d.line([(cx + 1 * scale, cy + 6 * scale), (cx + 7 * scale, cy)], fill=arrow_color, width=line_w)
        d.ellipse((cx + 7 * scale - line_w//2, cy - line_w//2, cx + 7 * scale + line_w//2, cy + line_w//2), fill=arrow_color)
        d.ellipse((cx + 1 * scale - line_w//2, cy - 6 * scale - line_w//2, cx + 1 * scale + line_w//2, cy - 6 * scale + line_w//2), fill=arrow_color)
        d.ellipse((cx + 1 * scale - line_w//2, cy + 6 * scale - line_w//2, cx + 1 * scale + line_w//2, cy + 6 * scale + line_w//2), fill=arrow_color)
        d.ellipse((cx - 8 * scale - line_w//2, cy - line_w//2, cx - 8 * scale + line_w//2, cy + line_w//2), fill=arrow_color)

    return im.resize((size, size), Image.Resampling.LANCZOS)

def render_part_e_slider():
    bg_p = os.path.join(WORKSPACE_DIR, "restaurant-app", "Libraries", "complete-design-format", "Only-background-transparent.png")
    canvas = Image.new("RGBA", (1920, 1080), (255, 255, 255, 255))
    if os.path.exists(bg_p):
        bg = get_cached_image(bg_p)
        canvas.paste(bg, (0, 0), bg)

    draw = ImageDraw.Draw(canvas)

    # Fonts
    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_medium = os.path.join(FONTS_DIR, "Rubik-Medium.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    f_kicker = get_cached_font(font_semibold, 30)
    f_heading = get_cached_font(font_semibold, 48)
    f_sub = get_cached_font(font_regular, 22)
    f_pil_t = get_cached_font(font_semibold, 21)
    f_pil_d = get_cached_font(font_regular, 17)
    f_card_tag = get_cached_font(font_semibold, 13)

    accent_rgb = COLOR_GREEN

    # 1. Kicker
    kicker_text = "PART E — SETTLE SCREEN (PAYMENT, SPLIT, VOUCHERS)"
    bar_x = 90
    bar_y = 125
    draw.rectangle((bar_x, bar_y + 3, bar_x + 8, bar_y + 37), fill=accent_rgb)
    draw.text((bar_x + 22, bar_y), kicker_text, font=f_kicker, fill=accent_rgb)

    # 2. Main Notice Board
    cx1, cy1, cx2, cy2 = 90, 200, 1830, 930
    draw.rounded_rectangle((cx1 - 2, cy1 + 6, cx2 + 2, cy2 + 10), radius=22, fill=(232, 237, 244, 150))
    draw.rounded_rectangle((cx1, cy1, cx2, cy2), radius=20, fill=(255, 255, 255, 255), outline=COLOR_CARD_BORDER, width=2)

    # Pin
    pin_x = cx1 + 90
    draw.rectangle((pin_x - 3, cy1 - 32, pin_x + 3, cy1), fill=(100, 116, 139, 255))
    draw.ellipse((pin_x - 15, cy1 - 46, pin_x + 15, cy1 - 18), fill=accent_rgb, outline=(255, 255, 255, 255), width=3)
    draw.ellipse((pin_x - 5, cy1 - 37, pin_x + 5, cy1 - 27), fill=(255, 255, 255, 255))

    # Top ribbon
    draw.rounded_rectangle((cx1, cy1, cx2, cy1 + 6), radius=4, fill=accent_rgb)

    pad_x = cx1 + 75
    board_content_w = cx2 - cx1 - 150

    # 3. Heading inside board
    heading_text = "Part E — Settle screen (payment, split, food voucher, gift card)"
    draw.text((pad_x, cy1 + 45), heading_text, font=f_heading, fill=COLOR_GRAY_DARK)

    # 4. Subtitle inside board
    subheading_text = (
        "This is the window titled Settle — Table XX (same idea for Takeaway / Quick Serve / Barcode settle)."
    )
    sub_lines = wrap_text(subheading_text, f_sub, board_content_w, draw)
    sub_y = cy1 + 115
    for sl in sub_lines:
        draw.text((pad_x, sub_y), sl, font=f_sub, fill=COLOR_GRAY_TEXT)
        sub_y += 30

    # 5. 3x2 Grid Cards
    items = [
        {
            "title": "Single-Touch Full Settle",
            "description": "Settle entire guest bill in 1 tap with Cash, Card (mada/Visa), or Online (Apple Pay). Verify Remaining reaches SAR 0.00.",
            "tag": "SIMPLE"
        },
        {
            "title": "Equal Split Between Guests",
            "description": "Evenly divide total bill across 2, 3, 4+ dining guests. System calculates equal portions and allows separate payment tenders.",
            "tag": "EQUAL"
        },
        {
            "title": "Custom Split Payments",
            "description": "Divide check by flexible amounts across multiple tenders (e.g. SAR 200 Cash + SAR 70 mada) until remaining balance is 0.00.",
            "tag": "CUSTOM"
        },
        {
            "title": "Food Voucher Redemption",
            "description": "Apply pre-created food vouchers from Settings. System validates voucher code, deducts value, and updates amount due.",
            "tag": "VOUCHER"
        },
        {
            "title": "Gift Cards & Loyalty CRM",
            "description": "Select loyalty customers to earn or redeem points, and apply preloaded gift card balances directly toward the check.",
            "tag": "CARDS & CRM"
        },
        {
            "title": "Receipt, Tax & Table Close",
            "description": "Finalize settlement to auto-print official ZATCA tax receipt, record cashier shift journals, and free occupied dining tables.",
            "tag": "ZATCA RECEIPT"
        }
    ]

    card_fill = (246, 250, 248, 255)
    card_border = (200, 230, 215, 255)
    icon_path = os.path.join(APP_DIR, "brand_check_green.png")
    icon_26 = get_cached_icon(icon_path, (26, 26)) if os.path.exists(icon_path) else None

    arrow_size = 36
    arrow_right = get_flow_arrow_badge(arrow_size, COLOR_GREEN, direction="right")

    num_cols = 3
    col_gap_x = 44  # Space for flow arrow between cards
    col_w = (board_content_w - (num_cols - 1) * col_gap_x) // num_cols  # ~500px
    row_h = 168
    row_gap_y = 28
    start_grid_y = sub_y + 28

    for idx, item in enumerate(items):
        col = idx % num_cols
        row = idx // num_cols
        bx = pad_x + col * (col_w + col_gap_x)
        by = start_grid_y + row * (row_h + row_gap_y)

        # Card Box
        draw.rounded_rectangle((bx, by, bx + col_w, by + row_h), radius=12, fill=card_fill, outline=card_border, width=1)

        # Icon
        if icon_26:
            canvas.paste(icon_26, (bx + 18, by + 18), icon_26)
        else:
            draw.ellipse((bx + 18, by + 18, bx + 44, by + 44), fill=accent_rgb)

        # Title
        draw.text((bx + 54, by + 20), item["title"], font=f_pil_t, fill=(20, 30, 45, 255))

        # Tag
        tag = item["tag"]
        tb_bbox = draw.textbbox((0, 0), tag, font=f_card_tag)
        tb_w = tb_bbox[2] - tb_bbox[0] + 16
        tb_x = bx + col_w - tb_w - 16
        tb_y = by + 19
        draw.rounded_rectangle((tb_x, tb_y, tb_x + tb_w, tb_y + 24), radius=5, fill=(255, 255, 255, 255), outline=accent_rgb, width=1)
        draw.text((tb_x + 8, tb_y + 4), tag, font=f_card_tag, fill=accent_rgb)

        # Description
        d_lines = wrap_text(item["description"], f_pil_d, col_w - 36, draw)
        for li, l in enumerate(d_lines[:3]):
            draw.text((bx + 18, by + 62 + li * 24), l, font=f_pil_d, fill=(71, 85, 105, 255))

        # Flow Arrow between Card 1 -> Card 2, Card 2 -> Card 3, and Card 4 -> Card 5, Card 5 -> Card 6
        if col < num_cols - 1:
            ax = bx + col_w + (col_gap_x - arrow_size) // 2
            ay = by + (row_h - arrow_size) // 2
            canvas.paste(arrow_right, (ax, ay), arrow_right)

    out_slide = os.path.join(SLIDES_DIR, "Part E - Settle screen (payment, split, food voucher, gift card).jpg")
    out_export = os.path.join(EXPORT_DIR, "Part E - Settle screen (payment, split, food voucher, gift card).jpg")

    canvas.convert("RGB").save(out_slide, "JPEG", quality=96, optimize=True)
    canvas.convert("RGB").save(out_export, "JPEG", quality=96, optimize=True)

    print("Generated Part E overview slider:")
    print("1.", out_slide)
    print("2.", out_export)

if __name__ == "__main__":
    render_part_e_slider()
