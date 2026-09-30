import os
import sys
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
FONTS_DIR = os.path.join(APP_DIR, "fonts")
sys.path.insert(0, os.path.join(WORKSPACE_DIR, "scratch"))

from part_e_slide_helper import render_part_e_step_slide

# Base source images
img_settle_main = Image.open(os.path.join(WORKSPACE_DIR, "project", "screens_part_e", "E01_settle_main.jpg"))
img_ticket = Image.open(os.path.join(WORKSPACE_DIR, "project", "screens_v2", "05_active_order_ticket.jpg"))
img_takeaway_settle = Image.open(os.path.join(WORKSPACE_DIR, "project", "screens", "debug_settle_open.jpg"))

f_bold = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf"), 20)
f_med = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-Medium.ttf"), 18)
f_reg = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-Regular.ttf"), 16)
f_title = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf"), 24)
f_small = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-Regular.ttf"), 14)

# ==========================================
# E1: What you see on Settle
# ==========================================
def make_e1_screen():
    im = img_settle_main.copy()
    d = ImageDraw.Draw(im)
    # 1. Amount due pill
    d.rounded_rectangle((615, 422, 900, 460), radius=8, outline=(18, 113, 208, 255), width=2)
    # 2. Loyalty customer dropdown
    d.rounded_rectangle((615, 468, 1304, 528), radius=8, outline=(3, 142, 65, 255), width=2)
    # 3. Row 1 Payment tenders (Cash, Card, Online, Other)
    d.rounded_rectangle((615, 567, 1304, 620), radius=10, outline=(255, 92, 53, 255), width=3)
    # 4. Row 2 Special tenders (Food Voucher, Customer Account, Split bill)
    d.rounded_rectangle((615, 620, 1132, 673), radius=10, outline=(3, 142, 65, 255), width=3)
    return im

# ==========================================
# E2: Pay full bill with one method (simple)
# ==========================================
def make_e2_screen():
    im = img_settle_main.copy()
    d = ImageDraw.Draw(im)
    # Highlight Cash button (Green)
    d.rounded_rectangle((616, 569, 801, 618), radius=8, outline=(3, 142, 65, 255), width=3)
    # Highlight Card button (Blue)
    d.rounded_rectangle((798, 569, 971, 618), radius=8, outline=(18, 113, 208, 255), width=3)
    # Highlight Online button (Orange)
    d.rounded_rectangle((968, 569, 1141, 618), radius=8, outline=(255, 92, 53, 255), width=3)
    return im

# ==========================================
# E3: Equal split (same amount to many people)
# ==========================================
def make_e3_screen():
    im = img_ticket.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 120))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)

    dw, dh = 660, 420
    dx = (1920 - dw) // 2
    dy = (1080 - dh) // 2
    d.rounded_rectangle((dx, dy, dx + dw, dy + dh), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)

    # Header
    d.text((dx + 35, dy + 25), "Settle — Table 01 (Equal Split)", font=f_title, fill=(30, 41, 59, 255))
    d.text((dx + 35, dy + 62), "Total SAR 270.00 incl. VAT · Split into 2 equal portions", font=f_reg, fill=(100, 116, 139, 255))

    # Tabs
    d.rounded_rectangle((dx + 35, dy + 95, dx + 240, dy + 130), radius=6, fill=(18, 113, 208, 255))
    d.text((dx + 55, dy + 102), "Equal Split (2 Guests)", font=f_med, fill=(255, 255, 255, 255))
    d.rounded_rectangle((dx + 250, dy + 95, dx + 390, dy + 130), radius=6, fill=(245, 247, 250, 255), outline=(218, 226, 236, 255), width=1)
    d.text((dx + 275, dy + 102), "Custom Split", font=f_med, fill=(100, 116, 139, 255))

    # Guest 1 & Guest 2
    d.rounded_rectangle((dx + 35, dy + 145, dx + dw - 35, dy + 210), radius=10, fill=(245, 248, 255, 255), outline=(200, 220, 245, 255), width=1)
    d.text((dx + 55, dy + 156), "Guest 1 · SAR 135.00", font=f_bold, fill=(30, 41, 59, 255))
    d.text((dx + 55, dy + 182), "Method: Cash · Status: Pending", font=f_reg, fill=(100, 116, 139, 255))
    d.rounded_rectangle((dx + 520, dy + 162, dx + 610, dy + 195), radius=6, fill=(3, 142, 65, 255))
    d.text((dx + 545, dy + 169), "Pay", font=f_bold, fill=(255, 255, 255, 255))

    d.rounded_rectangle((dx + 35, dy + 225, dx + dw - 35, dy + 290), radius=10, fill=(245, 248, 255, 255), outline=(200, 220, 245, 255), width=1)
    d.text((dx + 55, dy + 236), "Guest 2 · SAR 135.00", font=f_bold, fill=(30, 41, 59, 255))
    d.text((dx + 55, dy + 262), "Method: Card (mada) · Status: Pending", font=f_reg, fill=(100, 116, 139, 255))
    d.rounded_rectangle((dx + 520, dy + 242, dx + 610, dy + 275), radius=6, fill=(18, 113, 208, 255))
    d.text((dx + 545, dy + 249), "Pay", font=f_bold, fill=(255, 255, 255, 255))

    # Remaining bar & confirm button
    d.text((dx + 35, dy + 314), "Remaining to settle: SAR 0.00", font=f_bold, fill=(3, 142, 65, 255))
    d.rounded_rectangle((dx + 35, dy + 348, dx + dw - 35, dy + 395), radius=8, fill=(3, 142, 65, 255))
    d.text((dx + 240, dy + 360), "Confirm Split Settle", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# E4: Custom split (different amounts / methods)
# ==========================================
def make_e4_screen():
    im = img_ticket.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 120))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)

    dw, dh = 660, 420
    dx = (1920 - dw) // 2
    dy = (1080 - dh) // 2
    d.rounded_rectangle((dx, dy, dx + dw, dy + dh), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)

    # Header
    d.text((dx + 35, dy + 25), "Settle — Table 01 (Custom Split)", font=f_title, fill=(30, 41, 59, 255))
    d.text((dx + 35, dy + 62), "Total SAR 270.00 incl. VAT · Custom Tender Allocation", font=f_reg, fill=(100, 116, 139, 255))

    # Tabs
    d.rounded_rectangle((dx + 35, dy + 95, dx + 180, dy + 130), radius=6, fill=(245, 247, 250, 255), outline=(218, 226, 236, 255), width=1)
    d.text((dx + 55, dy + 102), "Equal Split", font=f_med, fill=(100, 116, 139, 255))
    d.rounded_rectangle((dx + 190, dy + 95, dx + 350, dy + 130), radius=6, fill=(18, 113, 208, 255))
    d.text((dx + 215, dy + 102), "Custom Split", font=f_med, fill=(255, 255, 255, 255))

    # Custom payments lines
    d.rounded_rectangle((dx + 35, dy + 145, dx + dw - 35, dy + 210), radius=10, fill=(235, 248, 241, 255), outline=(180, 226, 202, 255), width=1)
    d.text((dx + 55, dy + 156), "Tender 1: Cash · SAR 200.00", font=f_bold, fill=(3, 142, 65, 255))
    d.text((dx + 55, dy + 182), "Status: Tendered & Added [OK]", font=f_reg, fill=(100, 116, 139, 255))
    d.text((dx + 500, dy + 168), "[ Remove ]", font=f_small, fill=(217, 83, 30, 255))

    d.rounded_rectangle((dx + 35, dy + 225, dx + dw - 35, dy + 290), radius=10, fill=(235, 248, 241, 255), outline=(180, 226, 202, 255), width=1)
    d.text((dx + 55, dy + 236), "Tender 2: Card (mada) · SAR 70.00", font=f_bold, fill=(3, 142, 65, 255))
    d.text((dx + 55, dy + 262), "Status: Tendered & Added [OK]", font=f_reg, fill=(100, 116, 139, 255))
    d.text((dx + 500, dy + 248), "[ Remove ]", font=f_small, fill=(217, 83, 30, 255))

    # Remaining bar & confirm button
    d.text((dx + 35, dy + 314), "Total Tendered: SAR 270.00 · Remaining: SAR 0.00", font=f_bold, fill=(3, 142, 65, 255))
    d.rounded_rectangle((dx + 35, dy + 348, dx + dw - 35, dy + 395), radius=8, fill=(3, 142, 65, 255))
    d.text((dx + 235, dy + 360), "Confirm Custom Settle", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# E5: Food voucher on Settle
# ==========================================
def make_e5_screen():
    im = img_ticket.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 120))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)

    pw, ph = 640, 320
    px = (1920 - pw) // 2
    py = (1080 - ph) // 2
    d.rounded_rectangle((px, py, px + pw, py + ph), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)
    d.text((px + 35, py + 25), "Settle — Redeem Food Voucher", font=f_title, fill=(30, 41, 59, 255))
    d.text((px + 35, py + 62), "Enter or scan authorized customer voucher code:", font=f_reg, fill=(100, 116, 139, 255))

    # Code input box
    d.rounded_rectangle((px + 35, py + 100, px + pw - 35, py + 152), radius=8, fill=(245, 247, 250, 255), outline=(3, 142, 65, 255), width=2)
    d.text((px + 50, py + 114), "VOUCH-SAR100", font=f_bold, fill=(30, 41, 59, 255))
    d.text((px + pw - 180, py + 116), "Valid: -SAR 100.00", font=f_med, fill=(3, 142, 65, 255))

    # Calculation note
    d.rounded_rectangle((px + 35, py + 170, px + pw - 35, py + 225), radius=8, fill=(235, 248, 241, 255))
    d.text((px + 50, py + 185), "Bill Total: SAR 270.00 · Remaining Due: SAR 170.00", font=f_bold, fill=(3, 142, 65, 255))

    # Action button
    d.rounded_rectangle((px + 35, py + 248, px + pw - 35, py + 295), radius=8, fill=(3, 142, 65, 255))
    d.text((px + 210, py + 260), "Apply Voucher to Bill", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# E6: Gift card on Settle
# ==========================================
def make_e6_screen():
    im = img_ticket.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 120))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)

    pw, ph = 640, 320
    px = (1920 - pw) // 2
    py = (1080 - ph) // 2
    d.rounded_rectangle((px, py, px + pw, py + ph), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)
    d.text((px + 35, py + 25), "Settle — Gift Card Settlement", font=f_title, fill=(30, 41, 59, 255))
    d.text((px + 35, py + 62), "Scan physical card barcode or enter 16-digit card code:", font=f_reg, fill=(100, 116, 139, 255))

    # Gift card input box
    d.rounded_rectangle((px + 35, py + 100, px + pw - 35, py + 152), radius=8, fill=(245, 247, 250, 255), outline=(18, 113, 208, 255), width=2)
    d.text((px + 50, py + 114), "8492-XXXX-XXXX-1029", font=f_bold, fill=(30, 41, 59, 255))
    d.text((px + pw - 190, py + 116), "Balance: SAR 500.00", font=f_med, fill=(18, 113, 208, 255))

    # Calculation note
    d.rounded_rectangle((px + 35, py + 170, px + pw - 35, py + 225), radius=8, fill=(240, 248, 255, 255))
    d.text((px + 50, py + 185), "Charge SAR 270.00 · Remaining Card Funds: SAR 230.00", font=f_bold, fill=(18, 113, 208, 255))

    # Action button
    d.rounded_rectangle((px + 35, py + 248, px + pw - 35, py + 295), radius=8, fill=(18, 113, 208, 255))
    d.text((px + 200, py + 260), "Confirm Gift Card Settle", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# E7: Loyalty points (if guest in CRM)
# ==========================================
def make_e7_screen():
    im = img_settle_main.copy()
    d = ImageDraw.Draw(im)

    # Highlight Loyalty Customer dropdown
    d.rounded_rectangle((616, 470, 1303, 526), radius=8, outline=(3, 142, 65, 255), width=3)

    # Overlay active selected loyalty customer inside dropdown
    d.rounded_rectangle((620, 475, 1260, 522), radius=6, fill=(255, 255, 255, 255))
    d.text((635, 488), "Mohammed Al-Otaibi (+966 50 123 4567) · Gold VIP", font=f_med, fill=(30, 41, 59, 255))

    # Loyalty redemption callout card below dropdown
    cx1, cy1, cx2, cy2 = 618, 538, 1303, 610
    d.rounded_rectangle((cx1, cy1, cx2, cy2), radius=10, fill=(240, 249, 244, 255), outline=(180, 226, 202, 255), width=2)
    d.text((cx1 + 20, cy1 + 14), "Reward Available: 450 Points (SAR 45.00 Credit)", font=f_bold, fill=(3, 142, 65, 255))
    d.text((cx1 + 20, cy1 + 42), "Redeemed: 270 pts (-SAR 27.00) · Net Settle Amount: SAR 243.00", font=f_reg, fill=(71, 85, 105, 255))
    return im

# ==========================================
# E8: Card / mada / wallets
# ==========================================
def make_e8_screen():
    im = img_settle_main.copy()
    d = ImageDraw.Draw(im)

    # Highlight Card and Online buttons
    d.rounded_rectangle((798, 569, 1141, 618), radius=8, outline=(3, 142, 65, 255), width=3)

    # SoftPOS terminal prompt
    pw, ph = 540, 160
    px = (1920 - pw) // 2
    py = 695
    d.rounded_rectangle((px, py, px + pw, py + ph), radius=12, fill=(245, 248, 255, 255), outline=(18, 113, 208, 255), width=2)
    d.text((px + 25, py + 18), "SoftPOS / Card Terminal: Ready", font=f_bold, fill=(18, 113, 208, 255))
    d.text((px + 25, py + 50), "Supported: mada · Visa · Mastercard · Apple Pay · STC Pay", font=f_med, fill=(30, 41, 59, 255))
    d.text((px + 25, py + 82), "Contactless tap detected · Gateway Approval Received [OK]", font=f_reg, fill=(3, 142, 65, 255))
    d.text((px + 25, py + 114), "Transaction Ref: MADA-AUTH-92841 · Card: **** 4819", font=f_small, fill=(100, 116, 139, 255))
    return im

# ==========================================
# E9: If payment fails
# ==========================================
def make_e9_screen():
    im = img_ticket.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 120))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)

    # Alert Popup
    pw, ph = 560, 270
    px = (1920 - pw) // 2
    py = (1080 - ph) // 2
    d.rounded_rectangle((px, py, px + pw, py + ph), radius=14, fill=(255, 255, 255, 255), outline=(239, 68, 68, 255), width=2)
    d.text((px + 30, py + 22), "Notice: Payment Exception / Declined", font=f_title, fill=(217, 83, 30, 255))
    d.text((px + 30, py + 60), "Terminal response: Transaction Timed Out / Card Declined", font=f_reg, fill=(100, 116, 139, 255))
    d.text((px + 30, py + 92), "Critical Directive: Do not force-close or cancel ticket.", font=f_bold, fill=(30, 41, 59, 255))
    d.text((px + 30, py + 122), "Ask guest for alternate card, or switch tender to Cash.", font=f_reg, fill=(71, 85, 105, 255))

    # Action buttons
    d.rounded_rectangle((px + 30, py + 180, px + 265, py + 230), radius=8, fill=(18, 113, 208, 255))
    d.text((px + 85, py + 193), "Retry Payment", font=f_bold, fill=(255, 255, 255, 255))

    d.rounded_rectangle((px + 285, py + 180, px + pw - 30, py + 230), radius=8, fill=(3, 142, 65, 255))
    d.text((px + 330, py + 193), "Settle with Cash", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# E10: Same buttons on other sections
# ==========================================
def make_e10_screen():
    # Composite showing Dine-in Settle and Takeaway Settle side-by-side
    canvas = Image.new("RGB", (1920, 1080), (240, 243, 246))
    d = ImageDraw.Draw(canvas)

    # Left: Dine-in Settle crop
    crop_dine = img_settle_main.crop((550, 350, 1370, 720)).resize((880, 400), Image.Resampling.LANCZOS)
    canvas.paste(crop_dine, (60, 180))
    d.rounded_rectangle((60, 180, 940, 580), radius=12, outline=(18, 113, 208, 255), width=3)
    d.text((80, 140), "1. Dine-in (Floor) Settlement Modal", font=f_title, fill=(18, 113, 208, 255))

    # Right: Takeaway Settle crop
    crop_take = img_takeaway_settle.crop((550, 350, 1370, 720)).resize((880, 400), Image.Resampling.LANCZOS)
    canvas.paste(crop_take, (980, 180))
    d.rounded_rectangle((980, 180, 1860, 580), radius=12, outline=(3, 142, 65, 255), width=3)
    d.text((1000, 140), "2. Takeaway / Quick Serve Settle Modal", font=f_title, fill=(3, 142, 65, 255))

    # Bottom summary box
    d.rounded_rectangle((60, 620, 1860, 980), radius=14, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)
    d.text((100, 650), "Cross-Module Settlement Consistency Matrix", font=f_title, fill=(30, 41, 59, 255))
    d.text((100, 695), "All ordering modules share the exact same certified payment architecture:", font=f_reg, fill=(100, 116, 139, 255))

    rows = [
        ("Section / Module", "Discount & Extra Charges", "Order Routing (KOT)", "Settle, Split & Vouchers"),
        ("Dine-in (Floor)", "Yes (0%, 7%, 10% + Service/Parking)", "KOT & KOT & Print to KDS", "Full Pay / Equal & Custom Split"),
        ("Takeaway", "Yes (Customer-level discounts)", "Send / Kitchen Dispatch", "Settle + Food Voucher + Account"),
        ("Drive-thru & Quick Serve", "Yes (Configured by Admin)", "Fast Cart Dispatch", "1-Tap Settle & Cash Calculator"),
        ("Barcode & Aggregators", "Yes (Automated retail pricing)", "Direct Receipt Dispatch", "Immediate Payment Finalization")
    ]
    ry = 740
    for r_idx, r in enumerate(rows):
        is_h = (r_idx == 0)
        c_font = f_bold if is_h else f_reg
        c_fill = (18, 113, 208, 255) if is_h else (30, 41, 59, 255)
        d.text((100, ry), r[0], font=c_font, fill=c_fill)
        d.text((500, ry), r[1], font=c_font, fill=c_fill)
        d.text((1000, ry), r[2], font=c_font, fill=c_fill)
        d.text((1450, ry), r[3], font=c_font, fill=c_fill)
        d.line([(100, ry + 32), (1820, ry + 32)], fill=(225, 232, 240, 255), width=1)
        ry += 46

    return canvas

ALL_E_STEPS = [
    {
        "step_num": 1,
        "heading": "E1 — What you see on Settle",
        "body": "Overview of totals, loyalty customer, payment methods, and bill split.",
        "steps": [
            "Amount due … incl. VAT: total to collect (tax already included when tax is on).",
            "Loyalty Customer (optional): link CRM guest to earn or redeem points.",
            "Quick payment buttons: Cash, Card, Online, Other, and Customer Account.",
            "Food Voucher: redeem pre-configured food vouchers against the total.",
            "Split bill: open Equal or Custom split for multi-guest payments.",
            "Close (X): dismiss window anytime without losing order items."
        ],
        "screen_fn": make_e1_screen
    },
    {
        "step_num": 2,
        "heading": "E2 — Pay full bill with one method (simple)",
        "body": "Single-touch settlement for quick full payments.",
        "steps": [
            "Tap Settle from floor order ticket.",
            "Tap primary payment button: Cash, Card, or Online.",
            "Verify exact amount due matches tendered amount.",
            "Confirm payment when Remaining reaches SAR 0.00.",
            "Receipt automatically prints on receipt printer.",
            "Hand official receipt and change to the guest."
        ],
        "screen_fn": make_e2_screen
    },
    {
        "step_num": 3,
        "heading": "E3 — Equal split (same amount to many people)",
        "body": "Evenly divide total bill across multiple paying guests.",
        "steps": [
            "Open Settle (or tap Split on floor order ticket).",
            "Tap Split bill, then select Equal split tab.",
            "Choose number of parts / guests (2, 3, 4, etc.).",
            "System automatically divides the exact total among guests.",
            "Collect each guest's portion using their preferred method (Cash/Card).",
            "Confirm settle when Remaining balance is SAR 0.00."
        ],
        "screen_fn": make_e3_screen
    },
    {
        "step_num": 4,
        "heading": "E4 — Custom split (different amounts / methods)",
        "body": "Split bill by custom amounts across different payment tenders.",
        "steps": [
            "Open Settle > tap Split bill > select Custom tab.",
            "Remaining bar shows full amount due at start.",
            "Choose first method (e.g. Cash) and enter partial amount (e.g. SAR 200).",
            "Tap Add to apply partial payment — Remaining reduces instantly.",
            "Choose next method (e.g. mada card) for the remaining balance.",
            "Tap Confirm split once Remaining is exactly SAR 0.00."
        ],
        "screen_fn": make_e4_screen
    },
    {
        "step_num": 5,
        "heading": "E5 — Food voucher on Settle",
        "body": "Redeem authorized food vouchers to discount or pay order.",
        "steps": [
            "Food vouchers must first be created in Settings > Food vouchers.",
            "On Settle window, tap Food Voucher payment button.",
            "Enter or scan voucher code as prompted.",
            "Confirm voucher value applies — Amount Due reduces automatically.",
            "Collect any remaining balance by cash or card.",
            "Finish settle only when Remaining is 0; used vouchers cannot be reused."
        ],
        "screen_fn": make_e5_screen
    },
    {
        "step_num": 6,
        "heading": "E6 — Gift card on Settle",
        "body": "Apply preloaded gift cards toward customer settlement.",
        "steps": [
            "Gift cards are configured in Settings > Gift cards.",
            "On Settle window, tap Other > Gift Card.",
            "Enter gift card number or swipe/scan card barcode.",
            "System checks active card balance and applies available funds.",
            "Pay remaining balance with another method if card balance is partial.",
            "Confirm settle to finalize transaction and deduct card funds."
        ],
        "screen_fn": make_e6_screen
    },
    {
        "step_num": 7,
        "heading": "E7 — Loyalty points (if guest in CRM)",
        "body": "Redeem customer loyalty points for instant bill credits.",
        "steps": [
            "Tap Loyalty Customer dropdown on Settle window.",
            "Search and select customer by name or mobile number.",
            "View active points balance on customer card.",
            "Enter points to redeem as allowed by store policy.",
            "Due amount reduces proportionally to redeemed points value.",
            "Pay remaining balance normally and finish settlement."
        ],
        "screen_fn": make_e7_screen
    },
    {
        "step_num": 8,
        "heading": "E8 — Card / mada / wallets",
        "body": "Electronic payments via SoftPOS, physical terminals, and digital wallets.",
        "steps": [
            "Choose Card (mada, Visa, Mastercard) or Online (Apple Pay, STC Pay).",
            "Follow terminal / SoftPOS contactless prompt on device.",
            "Wait for real authorization and approval from payment gateway.",
            "If terminal shows error, check network connection or terminal battery.",
            "Receipt prints with transaction reference and masked card number.",
            "If terminal not ready, contact Admin (Settings > Card / SoftPOS)."
        ],
        "screen_fn": make_e8_screen
    },
    {
        "step_num": 9,
        "heading": "E9 — If payment fails",
        "body": "Standard procedures for declined transactions and payment exceptions.",
        "steps": [
            "Keep the order ticket open — NEVER force-close or cancel active bill.",
            "Ask guest for an alternate payment method (e.g. different card or cash).",
            "For split payments: remove the failed payment line and re-add tender.",
            "Check terminal connectivity and verify transaction didn't settle.",
            "If issue persists, contact Admin or Manager immediately.",
            "Do not clear the table until full payment is confirmed."
        ],
        "screen_fn": make_e9_screen
    },
    {
        "step_num": 10,
        "heading": "E10 — Same buttons on other sections",
        "body": "Consistent settlement workflow across all restaurant channels.",
        "steps": [
            "Dine-in (Floor): Settle opens from table order ticket or floor map.",
            "Takeaway: Settle opens directly from cart or customer queue.",
            "Drive-thru: Quick Settle button directly on active vehicle lane order.",
            "Quick Serve: Instant cash / card settlement right on fast cart.",
            "Barcode Mode: Settle opens automatically after scanning retail items.",
            "All sections share the same tax, discount, split, and voucher logic."
        ],
        "screen_fn": make_e10_screen
    }
]

def build_all_part_e_slides():
    slides_dir = os.path.join(WORKSPACE_DIR, "Slides", "Part E")
    export_dir = os.path.join(WORKSPACE_DIR, "export", "Part E")
    os.makedirs(slides_dir, exist_ok=True)
    os.makedirs(export_dir, exist_ok=True)

    print("=== Starting Part E Slides Generation (E1 to E10) ===")
    for item in ALL_E_STEPS:
        s_num = item["step_num"]
        heading = item["heading"]
        body = item["body"]
        steps = item["steps"]
        screen_img = item["screen_fn"]()

        # Sanitize filename (clean hyphens, no colons or slashes)
        clean_name = heading.replace('—', '-').replace('/', '-').replace(':', ' -')
        filename = f"{clean_name}.jpg"
        out_slide = os.path.join(slides_dir, filename)
        out_export = os.path.join(export_dir, filename)

        print(f"Rendering Step E{s_num}: {filename}...")
        render_part_e_step_slide(
            step_num=s_num,
            heading=heading,
            body=body,
            steps=steps,
            screen_img=screen_img,
            output_paths=[out_slide, out_export]
        )

    print("=== All 10 Part E Step Slides Generated Successfully! ===")

if __name__ == "__main__":
    build_all_part_e_slides()
