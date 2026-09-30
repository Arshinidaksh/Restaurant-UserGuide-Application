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

def clean_unicode_arrows(text: str) -> str:
    """Replace Unicode arrows that do not exist in Rubik font to avoid missing glyph boxes."""
    return text.replace("→", ">").replace("←", "<")

def render_part_l_slide(kicker: str, heading: str, where_text: str, steps: list, note_text: str, screen_img: Image.Image, output_paths: list):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")

    canvas = get_cached_base_background(bg_trans_path).copy()

    # 1. Compose PC monitor mockup with the screen - completely clean, unannotated
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
    f_heading = get_cached_font(font_semibold, 38)
    f_where = get_cached_font(font_regular, 20)
    f_step_text = get_cached_font(font_regular, 19)
    f_note = get_cached_font(font_regular, 18)

    # Clean text of missing arrow glyphs
    kicker = clean_unicode_arrows(kicker)
    heading = clean_unicode_arrows(heading)
    where_text = clean_unicode_arrows(where_text)
    note_text = clean_unicode_arrows(note_text) if note_text else ""
    cleaned_steps = [clean_unicode_arrows(s) for s in steps]

    # Kicker
    draw.text((TEXT_COL_X, KICKER_Y), kicker, font=f_kicker, fill=c_blue)

    # Heading (wrapped)
    head_lines = wrap_text(heading, f_heading, MAX_TEXT_WIDTH_PX, draw)
    curr_y = HEADING_Y
    for hl in head_lines:
        draw.text((TEXT_COL_X, curr_y), hl, font=f_heading, fill=c_dark)
        curr_y += 46

    # Where location
    if where_text:
        curr_y += 6
        draw.text((TEXT_COL_X, curr_y), where_text, font=f_where, fill=c_gray)
        curr_y += 30

    curr_y += 18

    # Steps list
    step_badge_size = 28
    n_steps = len(cleaned_steps)
    step_gap = 40 if n_steps <= 5 else 34

    for idx, st_text in enumerate(cleaned_steps, 1):
        badge = create_number_badge(idx, size=step_badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, curr_y + 2), badge)

        text_x = TEXT_COL_X + step_badge_size + 16
        text_max_w = MAX_TEXT_WIDTH_PX - (step_badge_size + 16)
        s_lines = wrap_text(st_text, f_step_text, text_max_w, draw)
        for sli, sl in enumerate(s_lines):
            draw.text((text_x, curr_y + sli * 26), sl, font=f_step_text, fill=c_dark)
        curr_y += max(len(s_lines) * 26 + 10, step_gap)

    # Note / Tip
    if note_text:
        curr_y += 8
        note_lines = wrap_text(note_text, f_note, MAX_TEXT_WIDTH_PX, draw)
        for nli, nl in enumerate(note_lines):
            draw.text((TEXT_COL_X, curr_y + nli * 25), nl, font=f_note, fill=c_blue)
        curr_y += len(note_lines) * 25

    final_img = canvas.convert("RGB")
    for out_p in output_paths:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        final_img.save(out_p, "JPEG", quality=96, optimize=True)
        print(f"Generated: {out_p}")

    return final_img

SLIDES_DATA = [
    {
        "filename": "L1 - Company Details.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L1 — Company Details",
        "where": "Where: Settings > Company Details",
        "note": "Do this first after you Activate POS.",
        "steps": [
            "Open Company Details.",
            "Enter restaurant brand name and legal name.",
            "Enter VAT / tax number and address carefully.",
            "Add or edit Branches (each outlet).",
            "Save.",
            "On the till top bar, select the branch you are working on."
        ],
        "screen_img_rel": "L1_company_details.jpg"
    },
    {
        "filename": "L2 - ZATCA e-invoice setup.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L2 — ZATCA e-invoice setup",
        "where": "Where: Settings > Company Details (ZATCA section)",
        "note": "",
        "steps": [
            "Open company tax / ZATCA area.",
            "Fill seller details needed for KSA e-invoice.",
            "For Phase 2 onboarding (OTP, CSID), do only with Isarva support.",
            "Do not share private keys on WhatsApp or email."
        ],
        "screen_img_rel": "L2_zatca_setup.jpg"
    },
    {
        "filename": "L3 - ZATCA invoice queue.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L3 — ZATCA invoice queue",
        "where": "Where: Settings > ZATCA invoices (queue)",
        "note": "",
        "steps": [
            "Open the invoice queue.",
            "Check status: pending, failed, reported.",
            "Retry failed invoices if the button is available.",
            "If many invoices keep failing, call Isarva support."
        ],
        "screen_img_rel": "L3_zatca_queue.jpg"
    },
    {
        "filename": "L4 - Customers (CRM).jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L4 — Customers (CRM)",
        "where": "Where: Settings > Customers, or menu CRM",
        "note": "",
        "steps": [
            "Search guest by phone or name.",
            "Add new customer if needed.",
            "Check loyalty points.",
            "Save changes."
        ],
        "screen_img_rel": "L4_customers.jpg"
    },
    {
        "filename": "L5 - Gift cards.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L5 — Gift cards",
        "where": "Where: Settings > Gift cards",
        "note": "",
        "steps": [
            "Open Gift cards.",
            "Create or issue a gift card with value.",
            "Note the card number for the guest.",
            "At payment time, Cashier can redeem the gift card.",
            "Always check balance before redeem."
        ],
        "screen_img_rel": "L5_gift_cards.jpg"
    },
    {
        "filename": "L6 - Food vouchers.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L6 — Food vouchers",
        "where": "Where: Settings > Food vouchers",
        "note": "",
        "steps": [
            "Create food voucher as per your offer.",
            "Set value and rules as shown on screen.",
            "Redeem at settle when guest shows voucher.",
            "Do not issue too many vouchers without control."
        ],
        "screen_img_rel": "L6_food_vouchers.jpg"
    },
    {
        "filename": "L7 - Loyalty campaigns.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L7 — Loyalty campaigns",
        "where": "Where: Settings > Loyalty campaigns",
        "note": "",
        "steps": [
            "Open Loyalty campaigns.",
            "Set birthday bonus if you want.",
            "Set visit punch-card rules (Example: after 5 visits, give reward).",
            "Save.",
            "Train Cashiers to search guest phone at bill time."
        ],
        "screen_img_rel": "L7_loyalty_campaigns.jpg"
    },
    {
        "filename": "L8 - Vendors (suppliers).jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L8 — Vendors (suppliers)",
        "where": "Where: Settings > Vendor, or menu Vendors / Suppliers",
        "note": "",
        "steps": [
            "Add supplier name, phone, and details.",
            "Save vendor.",
            "Use this vendor later in Purchase Orders and Stock receiving."
        ],
        "screen_img_rel": "L8_vendor.jpg"
    },
    {
        "filename": "L9 - Delivery Boy (riders).jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L9 — Delivery Boy (riders)",
        "where": "Where: Settings > Delivery Boy",
        "note": "",
        "steps": [
            "Add rider name and phone.",
            "Save.",
            "On Delivery orders, assign this rider.",
            "Rider login may use last 4 digits of phone (as configured)."
        ],
        "screen_img_rel": "L9_delivery_boy.jpg"
    },
    {
        "filename": "L10 - Notification settings.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L10 — Notification settings",
        "where": "Where: Settings > Notification Settings (with Delivery Integrations)",
        "note": "",
        "steps": [
            "Open notifications / alerts section.",
            "Turn on the alerts you need.",
            "Save.",
            "Check notify log if alert did not come."
        ],
        "screen_img_rel": "L10_notifications.jpg"
    },
    {
        "filename": "L11 - Delivery APIs (aggregators).jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L11 — Delivery APIs (aggregators)",
        "where": "Where: Settings > Delivery APIs / Delivery Integrations",
        "note": "",
        "steps": [
            "Open Delivery Integrations.",
            "Select channel (Example: HungerStation, Jahez, Keeta).",
            "Enter API credentials from the platform.",
            "Tap Test connection.",
            "Use live orders only after test success.",
            "If test fails, do not guess keys — call support."
        ],
        "screen_img_rel": "L11_delivery_apis.jpg"
    },
    {
        "filename": "L12 - Table Area.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L12 — Table Area",
        "where": "Where: Settings > Table Area (Floor)",
        "note": "",
        "steps": [
            "Create areas: Indoor, Outdoor, Family, and so on.",
            "Set active / order if the screen shows it.",
            "Save.",
            "Areas appear in Dine-in floor filter."
        ],
        "screen_img_rel": "L12_table_area.jpg"
    },
    {
        "filename": "L13 - Table Management.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L13 — Table Management",
        "where": "Where: Settings > Table Management",
        "note": "",
        "steps": [
            "Add tables (Table 1, Table 2…).",
            "Set seats and area.",
            "Save.",
            "Open Dine-in and confirm tables show on floor map or list."
        ],
        "screen_img_rel": "L13_table_management.jpg"
    },
    {
        "filename": "L14 - Menu timetable.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L14 — Menu timetable",
        "where": "Where: Settings > Menu timetable",
        "note": "",
        "steps": [
            "Open Menu timetable.",
            "Set which menu or items are available at which time (breakfast, lunch, dinner).",
            "Save.",
            "At that time, check that only correct items show."
        ],
        "screen_img_rel": "L14_menu_timetable.jpg"
    },
    {
        "filename": "L15 - Addons.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L15 — Addons",
        "where": "Where: Settings > Addons",
        "note": "",
        "steps": [
            "Create addon groups (Example: Extra toppings, Cooking style).",
            "Add options and prices.",
            "Go to Masters > dish > attach addon to the dish.",
            "If you do not attach, addon will not show while ordering."
        ],
        "screen_img_rel": "L15_addons.jpg"
    },
    {
        "filename": "L16 - Card - SoftPOS terminal.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L16 — Card / SoftPOS terminal",
        "where": "Where: Settings > Card / SoftPOS",
        "note": "",
        "steps": [
            "Open Card terminal settings.",
            "Check bridge / terminal status.",
            "Use demo simulate only for training. Turn it off for live sales.",
            "Live card payment needs a working bridge. Otherwise payment will not approve."
        ],
        "screen_img_rel": "L16_card_terminal.jpg"
    },
    {
        "filename": "L17 - Counter - Quick serve.jpg",
        "kicker": "PART L — SETTINGS > BUSINESS",
        "heading": "L17 — Counter / Quick serve",
        "where": "Where: Settings > Counter, or menu Quick Serve",
        "note": "",
        "steps": [
            "Use for fast counter orders without table.",
            "Add items > take payment > finish."
        ],
        "screen_img_rel": "L17_counter.jpg"
    }
]

def main():
    screens_dir = os.path.join(WORKSPACE_DIR, "project", "screens_part_l")
    slides_out_dir = os.path.join(WORKSPACE_DIR, "Slides", "Part L")
    export_out_dir = os.path.join(WORKSPACE_DIR, "export", "Part L")

    os.makedirs(slides_out_dir, exist_ok=True)
    os.makedirs(export_out_dir, exist_ok=True)

    print(f"Building {len(SLIDES_DATA)} individual slides for Part L...")

    for i, item in enumerate(SLIDES_DATA, 1):
        screen_path = os.path.join(screens_dir, item["screen_img_rel"])
        if not os.path.exists(screen_path):
            print(f"ERROR: Screenshot not found: {screen_path}")
            continue

        screen_img = Image.open(screen_path)
        out_paths = [
            os.path.join(slides_out_dir, item["filename"]),
            os.path.join(export_out_dir, item["filename"])
        ]

        render_part_l_slide(
            kicker=item["kicker"],
            heading=item["heading"],
            where_text=item["where"],
            steps=item["steps"],
            note_text=item["note"],
            screen_img=screen_img,
            output_paths=out_paths
        )

    print("All Part L slides generated successfully!")

if __name__ == "__main__":
    main()
