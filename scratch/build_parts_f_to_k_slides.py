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

def create_number_badge(num: int, size: int = 28, bg_color = (18, 113, 208, 255), fg_color = (255, 255, 255, 255)):
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

def draw_highlight_box(draw: ImageDraw.ImageDraw, box: tuple, color=(18, 113, 208, 255), width=3, radius=6):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=color, width=width)

def render_part_slide(kicker: str, heading: str, body: str, steps: list, screen_img: Image.Image, output_paths: list):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")

    canvas = get_cached_base_background(bg_trans_path).copy()

    # 1. Compose PC monitor mockup with the screen - full height visible
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

    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    f_kicker = get_cached_font(font_semibold, 20)
    f_heading = get_cached_font(font_semibold, 40)
    f_body = get_cached_font(font_regular, 19)
    f_step_text = get_cached_font(font_regular, 19)

    # Kicker
    draw.text((TEXT_COL_X, KICKER_Y), kicker, font=f_kicker, fill=c_blue)

    # Heading (wrapped)
    head_lines = wrap_text(heading, f_heading, MAX_TEXT_WIDTH_PX, draw)
    curr_y = HEADING_Y
    for hl in head_lines:
        draw.text((TEXT_COL_X, curr_y), hl, font=f_heading, fill=c_dark)
        curr_y += 48

    # Body
    curr_y += 8
    body_lines = wrap_text(body, f_body, MAX_TEXT_WIDTH_PX, draw)
    for bl in body_lines:
        draw.text((TEXT_COL_X, curr_y), bl, font=f_body, fill=c_gray)
        curr_y += 28

    curr_y += 20

    # Steps list
    step_badge_size = 28
    for idx, st_text in enumerate(steps, 1):
        badge = create_number_badge(idx, size=step_badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, curr_y + 2), badge)

        text_x = TEXT_COL_X + step_badge_size + 16
        text_max_w = MAX_TEXT_WIDTH_PX - (step_badge_size + 16)
        s_lines = wrap_text(st_text, f_step_text, text_max_w, draw)
        for sli, sl in enumerate(s_lines):
            draw.text((text_x, curr_y + sli * 27), sl, font=f_step_text, fill=c_dark)
        curr_y += max(len(s_lines) * 27 + 12, 36)

    final_img = canvas.convert("RGB")
    for out_p in output_paths:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        final_img.save(out_p, "JPEG", quality=96, optimize=True)
        print(f"Generated: {out_p}")

    return final_img

# --- SCREEN OVERLAYS BUILDERS ---

def prepare_screen_part_f():
    # Base: Takeaway ticket open (Clean screenshot from app without highlight markings)
    base_path = os.path.join(WORKSPACE_DIR, "project", "screens_parts_fk", "F_takeaway_ticket_open.jpg")
    return Image.open(base_path).convert("RGBA")

def prepare_screen_part_g():
    # Base: Online aggregator orders (Clean screen without highlight markings)
    base_path = os.path.join(WORKSPACE_DIR, "project", "screens_parts_fk", "G_online.jpg")
    return Image.open(base_path).convert("RGBA")

def prepare_screen_part_h():
    # Base: Kitchen KOT board
    base_path = os.path.join(WORKSPACE_DIR, "project", "screens_parts_fk", "H_kitchen_kot_live.jpg")
    img = Image.open(base_path).convert("RGBA")
    d = ImageDraw.Draw(img)

    # Cover empty placeholder area with clean white canvas inside the Board frame
    d.rectangle([395, 245, 1885, 920], fill=(255, 255, 255, 255))
    d.rounded_rectangle([395, 245, 1885, 920], radius=8, outline=(229, 231, 235, 255), width=1)

    font_bold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_reg = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")
    f_card_title = ImageFont.truetype(font_bold, 17)
    f_card_sub = ImageFont.truetype(font_reg, 13)
    f_card_item = ImageFont.truetype(font_bold, 15)
    f_card_note = ImageFont.truetype(font_reg, 12)
    f_card_btn = ImageFont.truetype(font_bold, 14)

    # --- CARD 1: Table 04 (Cooking) ---
    cx0, cy0, cx1, cy1 = 430, 270, 930, 680
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=10, fill=(255, 255, 255, 255), outline=(220, 224, 230, 255), width=2)
    # Header bar (Kitchen Orange)
    d.rounded_rectangle([cx0, cy0, cx1, cy0 + 60], radius=10, fill=(234, 88, 12, 255))
    d.rectangle([cx0, cy0 + 44, cx1, cy0 + 60], fill=(234, 88, 12, 255))
    d.text((cx0 + 16, cy0 + 10), "KOT #104  ·  Table 04 (Main Hall)", font=f_card_title, fill=(255, 255, 255, 255))
    d.text((cx0 + 16, cy0 + 34), "Server: Tariq  ·  Elapsed: 06m 24s  ·  Station: Kitchen", font=f_card_sub, fill=(254, 215, 170, 255))

    iy = cy0 + 76
    items1 = [
        ("1x Chicken Kabsa Full", "Note: Spice level Medium · Extra garlic sauce", (3, 142, 65, 255)),
        ("2x Roti & Curry", "Note: Well cooked, serve piping hot", (18, 113, 208, 255)),
        ("1x Onion Rings (Starter)", "Note: Priority fire first for guest", (234, 88, 12, 255)),
    ]
    for iname, inote, dot_color in items1:
        d.ellipse([cx0 + 16, iy + 4, cx0 + 26, iy + 14], fill=dot_color)
        d.text((cx0 + 36, iy), iname, font=f_card_item, fill=(30, 30, 30, 255))
        d.text((cx0 + 36, iy + 20), inote, font=f_card_note, fill=(100, 100, 100, 255))
        iy += 56
        d.line([cx0 + 16, iy - 8, cx1 - 16, iy - 8], fill=(240, 240, 240, 255), width=1)

    by0 = cy1 - 56
    d.rounded_rectangle([cx0 + 16, by0, cx0 + 150, by0 + 38], radius=6, fill=(254, 243, 199, 255), outline=(245, 158, 11, 255), width=1)
    d.text((cx0 + 28, by0 + 10), "Status: Cooking", font=f_card_btn, fill=(180, 83, 9, 255))
    d.rounded_rectangle([cx1 - 180, by0, cx1 - 16, by0 + 38], radius=6, fill=(3, 142, 65, 255))
    d.text((cx1 - 158, by0 + 10), "[ Bump / Done ]", font=f_card_btn, fill=(255, 255, 255, 255))

    # --- CARD 2: Takeaway #5 (Queued) ---
    dx0, dy0, dx1, dy1 = 970, 270, 1470, 680
    d.rounded_rectangle([dx0, dy0, dx1, dy1], radius=10, fill=(255, 255, 255, 255), outline=(220, 224, 230, 255), width=2)
    # Header bar (Blue)
    d.rounded_rectangle([dx0, dy0, dx1, dy0 + 60], radius=10, fill=(18, 113, 208, 255))
    d.rectangle([dx0, dy0 + 44, dx1, dy0 + 60], fill=(18, 113, 208, 255))
    d.text((dx0 + 16, dy0 + 10), "KOT #105  ·  Takeaway #5 (Walk-in)", font=f_card_title, fill=(255, 255, 255, 255))
    d.text((dx0 + 16, dy0 + 34), "Cashier: Admin  ·  Elapsed: 02m 10s  ·  Station: Kitchen", font=f_card_sub, fill=(219, 234, 254, 255))

    iy2 = dy0 + 76
    items2 = [
        ("1x Classic Pizza (Small)", "Note: Extra cheese, crispy crust", (234, 88, 12, 255)),
        ("1x Mixed Fruit Juice", "Note: Less sugar, chilled", (3, 142, 65, 255)),
        ("1x Chicken Strips (4 pcs)", "Note: Pack with garlic dip", (18, 113, 208, 255)),
    ]
    for iname, inote, dot_color in items2:
        d.ellipse([dx0 + 16, iy2 + 4, dx0 + 26, iy2 + 14], fill=dot_color)
        d.text((dx0 + 36, iy2), iname, font=f_card_item, fill=(30, 30, 30, 255))
        d.text((dx0 + 36, iy2 + 20), inote, font=f_card_note, fill=(100, 100, 100, 255))
        iy2 += 56
        d.line([dx0 + 16, iy2 - 8, dx1 - 16, iy2 - 8], fill=(240, 240, 240, 255), width=1)

    by1 = dy1 - 56
    d.rounded_rectangle([dx0 + 16, by1, dx0 + 150, by1 + 38], radius=6, fill=(239, 246, 255, 255), outline=(147, 197, 253, 255), width=1)
    d.text((dx0 + 30, by1 + 10), "Status: Queued", font=f_card_btn, fill=(29, 78, 216, 255))
    d.rounded_rectangle([dx1 - 180, by1, dx1 - 16, by1 + 38], radius=6, fill=(18, 113, 208, 255))
    d.text((dx1 - 164, by1 + 10), "[ Start Cooking ]", font=f_card_btn, fill=(255, 255, 255, 255))

    return img

def prepare_screen_part_i():
    # Base: Delivery Fleet
    base_path = os.path.join(WORKSPACE_DIR, "project", "screens_parts_fk", "I_delivery_riders_view.jpg")
    img = Image.open(base_path).convert("RGBA")
    d = ImageDraw.Draw(img)

    # Render an active assigned delivery order card in the Ready / Out column (x=825 to 1160)
    font_bold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_reg = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")
    f_card_title = ImageFont.truetype(font_bold, 17)
    f_card_sub = ImageFont.truetype(font_reg, 13)
    f_card_text = ImageFont.truetype(font_reg, 14)
    f_card_bold = ImageFont.truetype(font_bold, 14)

    cx0, cy0, cx1, cy1 = 825, 255, 1160, 580
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=10, fill=(255, 255, 255, 255), outline=(220, 224, 230, 255), width=1)

    # Order header
    d.rounded_rectangle([cx0, cy0, cx1, cy0 + 52], radius=10, fill=(18, 113, 208, 255))
    d.rectangle([cx0, cy0 + 38, cx1, cy0 + 52], fill=(18, 113, 208, 255))
    d.text((cx0 + 14, cy0 + 8), "ORD-049  ·  Direct Fleet", font=f_card_title, fill=(255, 255, 255, 255))
    d.text((cx0 + 14, cy0 + 30), "Rider: Arun  ·  COD SAR 185.00", font=f_card_sub, fill=(219, 234, 254, 255))

    # Guest details
    d.text((cx0 + 14, cy0 + 64), "Guest: Fahad Al-Otaibi", font=f_card_bold, fill=(30, 30, 30, 255))
    d.text((cx0 + 14, cy0 + 84), "Phone: +966 50 123 4567", font=f_card_text, fill=(70, 70, 70, 255))
    d.text((cx0 + 14, cy0 + 104), "Area: Al-Malqa, Riyadh · Villa 14", font=f_card_text, fill=(70, 70, 70, 255))

    d.line([cx0 + 14, cy0 + 128, cx1 - 14, cy0 + 128], fill=(230, 230, 230, 255), width=1)

    # Items preview
    d.text((cx0 + 14, cy0 + 138), "Items: 2x Kabsa, 1x Mixed Grill", font=f_card_text, fill=(50, 50, 50, 255))
    d.text((cx0 + 14, cy0 + 160), "Payment: Cash on Delivery (COD)", font=f_card_bold, fill=(234, 88, 12, 255))

    # Action buttons
    d.rounded_rectangle([cx0 + 14, cy0 + 200, cx1 - 14, cy0 + 242], radius=6, fill=(18, 113, 208, 255))
    d.text((cx0 + 80, cy0 + 212), "[ Start Delivery ]", font=f_card_bold, fill=(255, 255, 255, 255))

    d.rounded_rectangle([cx0 + 14, cy0 + 252, cx1 - 14, cy0 + 294], radius=6, fill=(3, 142, 65, 255))
    d.text((cx0 + 80, cy0 + 264), "[ Mark Delivered ]", font=f_card_bold, fill=(255, 255, 255, 255))

    return img

def prepare_screen_part_j():
    # Base: Accounts screen
    base_path = os.path.join(WORKSPACE_DIR, "project", "screens_parts_fk", "J_accounts.jpg")
    img = Image.open(base_path).convert("RGBA")


    # Render a centered Day Close Reconciliation dialog
    font_bold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_reg = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")
    f_dlg_title = ImageFont.truetype(font_bold, 20)
    f_dlg_sub = ImageFont.truetype(font_reg, 14)
    f_dlg_label = ImageFont.truetype(font_bold, 15)
    f_dlg_val = ImageFont.truetype(font_reg, 15)
    f_dlg_btn = ImageFont.truetype(font_bold, 15)

    pw, ph = 640, 390
    px = (1920 - pw) // 2
    py = (1080 - ph) // 2

    # Dim overlay
    dim = Image.new("RGBA", (1920, 1080), (0, 0, 0, 95))
    img.alpha_composite(dim)
    d = ImageDraw.Draw(img)

    # Modal container
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=14, fill=(255, 255, 255, 255), outline=(210, 215, 222, 255), width=2)

    # Modal Header
    d.rounded_rectangle([px, py, px + pw, py + 68], radius=14, fill=(3, 142, 65, 255))
    d.rectangle([px, py + 52, px + pw, py + 68], fill=(3, 142, 65, 255))
    d.text((px + 24, py + 14), "Day Close  ·  Branch: H001 (Head Office)", font=f_dlg_title, fill=(255, 255, 255, 255))
    d.text((px + 24, py + 42), "Audit Date: 30-Sep-2026  ·  Authorised User: Admin", font=f_dlg_sub, fill=(209, 250, 229, 255))

    # Audit rows
    rows = [
        ("System Cash Sales Total:", "SAR 2,500.00", (50, 50, 50, 255)),
        ("System Card / Mada Total:", "SAR 4,850.00", (50, 50, 50, 255)),
        ("Physical Drawer Cash Counted:", "SAR 2,500.00  [Exact Match]", (3, 142, 65, 255)),
        ("Cash Drawer Variance:", "SAR 0.00  [OK - Balanced]", (3, 142, 65, 255)),
        ("Total Day Net Revenue:", "SAR 7,350.00 incl. VAT", (18, 113, 208, 255))
    ]
    ry = py + 90
    for lbl, val, val_col in rows:
        d.text((px + 24, ry), lbl, font=f_dlg_label, fill=(40, 40, 40, 255))
        d.text((px + 330, ry), val, font=f_dlg_val, fill=val_col)
        ry += 42
        d.line([px + 24, ry - 12, px + pw - 24, ry - 12], fill=(240, 240, 240, 255), width=1)

    # Action buttons
    d.rounded_rectangle([px + 24, py + ph - 62, px + 180, py + ph - 18], radius=8, fill=(243, 244, 246, 255), outline=(209, 213, 219, 255), width=1)
    d.text((px + 68, py + ph - 48), "Cancel", font=f_dlg_btn, fill=(100, 100, 100, 255))

    d.rounded_rectangle([px + 200, py + ph - 62, px + pw - 24, py + ph - 18], radius=8, fill=(3, 142, 65, 255))
    d.text((px + 235, py + ph - 48), "[ Confirm Day Close & Lock Shift ]", font=f_dlg_btn, fill=(255, 255, 255, 255))

    return img

def prepare_screen_part_k():
    # Base: Settings screen (Clean screen without highlight markings)
    base_path = os.path.join(WORKSPACE_DIR, "project", "screens_parts_fk", "K_settings_live.jpg")
    return Image.open(base_path).convert("RGBA")

def main():
    print("=== Re-generating Slides for Part F through Part K with Precise Bounding Boxes ===")

    slides_config = [
        {
            "part_code": "Part F",
            "kicker": "PART F — TAKEAWAY & DRIVE-THRU",
            "heading": "Part F — Takeaway / drive-thru",
            "body": "Fast order entry, token buzzer tracking, and takeaway food handover.",
            "steps": [
                "Open Takeaway or Drive-thru.",
                "Create a new order.",
                "Add items and notes.",
                "Send to kitchen if required.",
                "Take payment as per your shop rule (before or at handover).",
                "Mark order completed when guest collects food."
            ],
            "img_func": prepare_screen_part_f,
            "filename": "Part F - Takeaway - drive-thru.jpg"
        },
        {
            "part_code": "Part G",
            "kicker": "PART G — AGGREGATORS & ONLINE ORDERS",
            "heading": "Part G — Delivery and online orders",
            "body": "Manage delivery apps (HungerStation, Jahez, Keeta) and guest QR menu orders.",
            "steps": [
                "Open Delivery or Online orders from the main navigation.",
                "Review new incoming orders from food apps (HungerStation, Jahez).",
                "Confirm item quantities, modifiers, and delivery destination.",
                "Tap Accept to send the ticket directly to the kitchen (KOT).",
                "Hand food to courier or assign rider when order is packed.",
                "Guest QR menu: share unique QR link (?co=) for direct mobile ordering."
            ],
            "img_func": prepare_screen_part_g,
            "filename": "Part G - Delivery and online orders.jpg"
        },
        {
            "part_code": "Part H",
            "kicker": "PART H — KITCHEN DISPLAY SYSTEM (KDS)",
            "heading": "Part H — Kitchen screen (Kitchen Manager)",
            "body": "Real-time digital ticket management for kitchen chefs and station managers.",
            "steps": [
                "Sign in with Kitchen Manager PIN credentials.",
                "Open Kitchen (KOT) from the left menu or Home dashboard.",
                "Choose station board view: All, Kitchen, Bar, or Expo.",
                "Read item notes carefully (spice levels, allergies, special requests).",
                "Tap item to mark Cooking, and Bump / Done when prepared.",
                "Do not bump wrong station items; keep tickets in order.",
                "If an ingredient is finished (86), inform Admin and floor immediately."
            ],
            "img_func": prepare_screen_part_h,
            "filename": "Part H - Kitchen screen (Kitchen Manager).jpg"
        },
        {
            "part_code": "Part I",
            "kicker": "PART I — RIDER DISPATCH & FLEET",
            "heading": "Part I — Delivery rider",
            "body": "Managing delivery riders, dispatch assignments, and cash on delivery.",
            "steps": [
                "Sign in on phone or tablet at /rider with assigned 4-digit PIN.",
                "Open Delivery to view your assigned delivery orders.",
                "Check guest name, delivery address, and contact phone number.",
                "Tap Start delivery when departing from the restaurant.",
                "Tap Mark delivered once the guest receives the food order.",
                "If Cash on Delivery (COD), collect exact cash and remit to Cashier.",
                "If guest is unreachable, call restaurant; never discard food."
            ],
            "img_func": prepare_screen_part_i,
            "filename": "Part I - Delivery rider.jpg"
        },
        {
            "part_code": "Part J",
            "kicker": "PART J — END OF DAY & CASH AUDIT",
            "heading": "Part J — Day close (Admin / authorised user)",
            "body": "Drawer cash audit, sales reconciliation, and shift locking procedure.",
            "steps": [
                "Make sure open tables and takeaway tickets are settled.",
                "Open Back Office / Accounts and select Day Close.",
                "Count physical cash in the till drawer.",
                "Compare counted cash against system recorded cash sales.",
                "Enter counted cash amount into the Day Close screen.",
                "Confirm day close to lock business day and generate Z-Report.",
                "Remember: Day close is performed separately for each branch."
            ],
            "img_func": prepare_screen_part_j,
            "filename": "Part J - Day close (Admin - authorised user).jpg"
        },
        {
            "part_code": "Part K",
            "kicker": "PART K — BACK-OFFICE SYSTEM SETTINGS",
            "heading": "Part K — How to open Settings (all modules)",
            "body": "Access configuration modules, hardware setup, catalogs, and user permissions.",
            "steps": [
                "Sign in with Admin PIN credentials.",
                "From Home dashboard or left menu, open Settings.",
                "Browse module tabs: Business, Printer, Catalog, User, Accounts, Ingredients, Inventory, Database.",
                "Tap any configuration tile to manage that system module.",
                "If a tile displays 'Coming later', that feature is not active.",
                "Always click Save after updating hardware, tax, or store settings."
            ],
            "img_func": prepare_screen_part_k,
            "filename": "Part K - How to open Settings (all modules).jpg"
        },
    ]

    for item in slides_config:
        print(f"\nProcessing {item['part_code']}: {item['filename']}...")
        screen = item["img_func"]()

        out_paths = [
            os.path.join(WORKSPACE_DIR, "Slides", item["part_code"], item["filename"]),
            os.path.join(WORKSPACE_DIR, "export", item["part_code"], item["filename"]),
            os.path.join(WORKSPACE_DIR, "Slides", item["filename"]),
            os.path.join(WORKSPACE_DIR, "export", item["filename"]),
        ]

        render_part_slide(
            kicker=item["kicker"],
            heading=item["heading"],
            body=item["body"],
            steps=item["steps"],
            screen_img=screen,
            output_paths=out_paths
        )

    print("\n=== All Parts F through K Slides Successfully Generated! ===")

if __name__ == "__main__":
    main()
