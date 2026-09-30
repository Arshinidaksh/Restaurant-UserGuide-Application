import os
import sys
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
FONTS_DIR = os.path.join(APP_DIR, "fonts")
sys.path.insert(0, os.path.join(WORKSPACE_DIR, "scratch"))

from part_d_slide_helper import render_part_d_step_slide

# Base source images
img_floor = Image.open(os.path.join(WORKSPACE_DIR, "project", "screens_v2", "04_dine_in_floor_map.jpg"))
img_ticket = Image.open(os.path.join(WORKSPACE_DIR, "project", "screens_v2", "05_active_order_ticket.jpg"))
img_settle_base = Image.open(os.path.join(WORKSPACE_DIR, "project", "screens", "debug_settle_open.jpg"))

f_bold = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf"), 20)
f_med = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-Medium.ttf"), 18)
f_reg = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-Regular.ttf"), 16)
f_title = ImageFont.truetype(os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf"), 24)

# ==========================================
# 1. Step 1: Open the table
# ==========================================
def make_step1_screen():
    im = img_floor.copy()
    d = ImageDraw.Draw(im)
    # Highlight Table 01 with a focused outline / callout
    # Table 01 is around x: 120, y: 700, w: 220, h: 140
    d.rounded_rectangle((120, 690, 345, 840), radius=14, outline=(18, 113, 208, 255), width=4)
    # Seat table dialog overlay
    dw, dh = 480, 240
    dx = (1920 - dw) // 2
    dy = (1080 - dh) // 2
    # Modal backdrop
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 100))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((dx, dy, dx + dw, dy + dh), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)
    d.text((dx + 30, dy + 28), "Table seat · T01-2", font=f_title, fill=(30, 41, 59, 255))
    d.text((dx + 30, dy + 70), "Main Hall · tap seats to assign guests (1 selected)", font=f_reg, fill=(100, 116, 139, 255))
    # Seat icons
    d.rounded_rectangle((dx + 190, dy + 110, dx + 235, dy + 155), radius=8, fill=(235, 248, 241, 255), outline=(3, 142, 65, 255), width=2)
    d.text((dx + 207, dy + 124), "1", font=f_bold, fill=(3, 142, 65, 255))
    d.rounded_rectangle((dx + 245, dy + 110, dx + 290, dy + 155), radius=8, fill=(245, 247, 250, 255), outline=(200, 210, 220, 255), width=1)
    d.text((dx + 262, dy + 124), "2", font=f_bold, fill=(140, 150, 160, 255))
    # Action button
    d.rounded_rectangle((dx + 30, dy + 175, dx + dw - 30, dy + 218), radius=8, fill=(217, 83, 30, 255))
    d.text((dx + 160, dy + 186), "Open with 1 guest", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# 2. Step 2: Add food items
# ==========================================
def make_step2_screen():
    im = img_ticket.copy()
    d = ImageDraw.Draw(im)
    # Highlight categories on left and dish card
    d.rounded_rectangle((115, 220, 205, 258), radius=8, fill=(235, 248, 241, 255), outline=(3, 142, 65, 255), width=2)
    d.text((135, 228), "Food (28)", font=f_med, fill=(3, 142, 65, 255))
    # Highlight Roti & Curry dish card
    d.rounded_rectangle((216, 186, 314, 272), radius=12, outline=(18, 113, 208, 255), width=3)
    # Highlight Order Items on right
    d.rounded_rectangle((1430, 135, 1880, 250), radius=10, outline=(3, 142, 65, 255), width=2)
    return im

# ==========================================
# 3. Step 3: Understand bill totals
# ==========================================
def make_step3_screen():
    im = img_ticket.copy()
    d = ImageDraw.Draw(im)
    # Highlight authentic Subtotal, Discount (0%), VAT, and Total pill strictly within modal bounds
    d.rounded_rectangle((1435, 614, 1823, 744), radius=10, outline=(3, 142, 65, 255), width=3)
    return im

# ==========================================
# 4. Step 4: How to use Discount on the floor
# ==========================================
def make_step4_screen():
    im = img_ticket.copy()
    d = ImageDraw.Draw(im)
    # Highlight DISCOUNT section: 0%, 7%, 10%
    d.rounded_rectangle((1435, 690, 1880, 755), radius=10, fill=(255, 250, 245, 255), outline=(255, 92, 53, 255), width=2)
    d.text((1450, 698), "DISCOUNT", font=f_med, fill=(217, 83, 30, 255))
    # 0% inactive pill
    d.rounded_rectangle((1450, 720, 1495, 748), radius=14, fill=(245, 247, 250, 255), outline=(200, 210, 220, 255), width=1)
    d.text((1462, 724), "0%", font=f_med, fill=(100, 116, 139, 255))
    # 7% inactive pill
    d.rounded_rectangle((1505, 720, 1550, 748), radius=14, fill=(245, 247, 250, 255), outline=(200, 210, 220, 255), width=1)
    d.text((1517, 724), "7%", font=f_med, fill=(100, 116, 139, 255))
    # 10% active pill (dark)
    d.rounded_rectangle((1560, 720, 1615, 748), radius=14, fill=(30, 41, 59, 255))
    d.text((1572, 724), "10%", font=f_bold, fill=(255, 255, 255, 255))
    # Pointer badge
    d.text((1630, 724), "Active: -SAR 27.00", font=f_med, fill=(3, 142, 65, 255))
    return im

# ==========================================
# 5. Step 5: How to use Extra Charges on the floor
# ==========================================
def make_step5_screen():
    im = img_ticket.copy()
    d = ImageDraw.Draw(im)
    # Highlight EXTRA CHARGES section
    d.rounded_rectangle((1435, 765, 1880, 865), radius=10, fill=(245, 248, 255, 255), outline=(18, 113, 208, 255), width=2)
    d.text((1450, 772), "EXTRA CHARGES (TAP TO TOGGLE)", font=f_med, fill=(18, 113, 208, 255))
    # Service charges pill (Active Green)
    d.rounded_rectangle((1450, 796, 1780, 826), radius=15, fill=(235, 248, 241, 255), outline=(3, 142, 65, 255), width=2)
    d.text((1465, 802), "✓ Service charges as per policy · SAR 150.00", font=f_med, fill=(3, 142, 65, 255))
    # Parking Charges pill (Inactive)
    d.rounded_rectangle((1450, 832, 1680, 858), radius=15, fill=(255, 255, 255, 255), outline=(200, 210, 220, 255), width=1)
    d.text((1465, 836), "+ Parking Charges · SAR 20.00", font=f_med, fill=(100, 116, 139, 255))
    return im

# ==========================================
# 6. Step 6: Save / Save & Print / Save & Bill
# ==========================================
def make_step6_screen():
    im = img_ticket.copy()
    d = ImageDraw.Draw(im)
    # Highlight authentic Save, Save & Print, Save & Bill buttons row
    d.rounded_rectangle((1438, 952, 1822, 984), radius=12, outline=(255, 92, 53, 255), width=3)
    return im

# ==========================================
# 7. Step 7: Send to kitchen: KOT and KOT & Print
# ==========================================
def make_step7_screen():
    im = img_ticket.copy()
    d = ImageDraw.Draw(im)
    # Highlight authentic KOT and KOT & Print buttons with high-contrast accent outline
    d.rounded_rectangle((1438, 986, 1694, 1023), radius=12, outline=(255, 92, 53, 255), width=3)
    return im

# ==========================================
# 8. Step 8: Change Table
# ==========================================
def make_step8_screen():
    im = img_ticket.copy()
    # Modal backdrop
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 110))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)
    # Change Table modal
    dw, dh = 560, 360
    dx = (1920 - dw) // 2
    dy = (1080 - dh) // 2
    d.rounded_rectangle((dx, dy, dx + dw, dy + dh), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)
    d.text((dx + 35, dy + 28), "Change Table · Table 01", font=f_title, fill=(30, 41, 59, 255))
    d.text((dx + 35, dy + 68), "Select new target vacant table to transfer active order:", font=f_reg, fill=(100, 116, 139, 255))
    # Table selection cards
    tables = [("Table 02", "Main Hall", "Free"), ("Table 03", "Main Hall", "Free"), ("Table 04", "Main Hall", "Free"), ("Table 07", "Outdoor", "Free")]
    for ti, (tname, tarea, tstat) in enumerate(tables):
        col = ti % 2
        row = ti // 2
        tx = dx + 35 + col * 245
        ty = dy + 110 + row * 85
        # highlight Table 02 as selected target
        is_sel = (ti == 0)
        bd = (18, 113, 208, 255) if is_sel else (218, 226, 236, 255)
        bg = (243, 248, 255, 255) if is_sel else (255, 255, 255, 255)
        d.rounded_rectangle((tx, ty, tx + 230, ty + 70), radius=10, fill=bg, outline=bd, width=2 if is_sel else 1)
        d.text((tx + 16, ty + 14), tname, font=f_bold, fill=(30, 41, 59, 255))
        d.text((tx + 16, ty + 38), tarea, font=f_reg, fill=(100, 116, 139, 255))
        d.rounded_rectangle((tx + 155, ty + 20, tx + 215, ty + 46), radius=5, fill=(235, 248, 241, 255))
        d.text((tx + 168, ty + 24), tstat, font=f_med, fill=(3, 142, 65, 255))
    # Confirm button
    d.rounded_rectangle((dx + 35, dy + 295, dx + dw - 35, dy + 338), radius=8, fill=(18, 113, 208, 255))
    d.text((dx + 185, dy + 306), "Confirm Table Transfer", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# 9. Step 9: Merge Tables
# ==========================================
def make_step9_screen():
    im = img_ticket.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 110))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)
    dw, dh = 560, 360
    dx = (1920 - dw) // 2
    dy = (1080 - dh) // 2
    d.rounded_rectangle((dx, dy, dx + dw, dy + dh), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)
    d.text((dx + 35, dy + 28), "Merge Tables · Host Table 01", font=f_title, fill=(30, 41, 59, 255))
    d.text((dx + 35, dy + 68), "Select occupied tables to combine onto this host ticket:", font=f_reg, fill=(100, 116, 139, 255))
    # Occupied tables to merge
    m_tables = [("Table 05", "Family Section · SAR 120.00", True), ("Table 09", "Private Room · SAR 85.00", False)]
    for mi, (mname, msub, mcheck) in enumerate(m_tables):
        my = dy + 115 + mi * 80
        bd = (3, 142, 65, 255) if mcheck else (218, 226, 236, 255)
        bg = (235, 248, 241, 255) if mcheck else (255, 255, 255, 255)
        d.rounded_rectangle((dx + 35, my, dx + dw - 35, my + 66), radius=10, fill=bg, outline=bd, width=2 if mcheck else 1)
        # Checkbox
        d.rounded_rectangle((dx + 55, my + 18, dx + 85, my + 48), radius=6, fill=(3, 142, 65, 255) if mcheck else (255, 255, 255, 255), outline=bd, width=1)
        if mcheck:
            d.text((dx + 62, my + 20), "✓", font=f_bold, fill=(255, 255, 255, 255))
        d.text((dx + 105, my + 14), mname, font=f_bold, fill=(30, 41, 59, 255))
        d.text((dx + 105, my + 38), msub, font=f_reg, fill=(100, 116, 139, 255))
    # Confirm merge
    d.rounded_rectangle((dx + 35, dy + 295, dx + dw - 35, dy + 338), radius=8, fill=(3, 142, 65, 255))
    d.text((dx + 195, dy + 306), "Confirm Merge Tables", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# 10. Step 10: Split (open Settle in split mode)
# ==========================================
def make_step10_screen():
    im = img_ticket.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 110))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)
    dw, dh = 620, 420
    dx = (1920 - dw) // 2
    dy = (1080 - dh) // 2
    d.rounded_rectangle((dx, dy, dx + dw, dy + dh), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)
    d.text((dx + 35, dy + 25), "Split Bill · Table 01", font=f_title, fill=(30, 41, 59, 255))
    d.text((dx + 35, dy + 62), "Total Due: SAR 270.00 incl. VAT", font=f_bold, fill=(3, 142, 65, 255))
    # Tabs: Equal Split / Custom Split
    d.rounded_rectangle((dx + 35, dy + 95, dx + 220, dy + 130), radius=6, fill=(18, 113, 208, 255))
    d.text((dx + 65, dy + 102), "Equal Split (2 Guests)", font=f_med, fill=(255, 255, 255, 255))
    d.rounded_rectangle((dx + 230, dy + 95, dx + 380, dy + 130), radius=6, fill=(245, 247, 250, 255), outline=(218, 226, 236, 255), width=1)
    d.text((dx + 255, dy + 102), "Custom Split", font=f_med, fill=(100, 116, 139, 255))
    # Guest 1 & Guest 2 tender lines
    d.rounded_rectangle((dx + 35, dy + 150, dx + dw - 35, dy + 215), radius=10, fill=(245, 248, 255, 255), outline=(200, 220, 245, 255), width=1)
    d.text((dx + 55, dy + 162), "Guest 1 · SAR 135.00", font=f_bold, fill=(30, 41, 59, 255))
    d.text((dx + 55, dy + 188), "Method: Cash · Status: Pending", font=f_reg, fill=(100, 116, 139, 255))
    d.rounded_rectangle((dx + 480, dy + 168, dx + 560, dy + 200), radius=6, fill=(3, 142, 65, 255))
    d.text((dx + 500, dy + 174), "Pay", font=f_bold, fill=(255, 255, 255, 255))
    d.rounded_rectangle((dx + 35, dy + 230, dx + dw - 35, dy + 295), radius=10, fill=(245, 248, 255, 255), outline=(200, 220, 245, 255), width=1)
    d.text((dx + 55, dy + 242), "Guest 2 · SAR 135.00", font=f_bold, fill=(30, 41, 59, 255))
    d.text((dx + 55, dy + 268), "Method: Card (mada) · Status: Pending", font=f_reg, fill=(100, 116, 139, 255))
    d.rounded_rectangle((dx + 480, dy + 248, dx + 560, dy + 280), radius=6, fill=(18, 113, 208, 255))
    d.text((dx + 500, dy + 254), "Pay", font=f_bold, fill=(255, 255, 255, 255))
    # Remaining bar & confirm button
    d.text((dx + 35, dy + 315), "Remaining to settle: SAR 0.00", font=f_bold, fill=(3, 142, 65, 255))
    d.rounded_rectangle((dx + 35, dy + 350, dx + dw - 35, dy + 395), radius=8, fill=(3, 142, 65, 255))
    d.text((dx + 230, dy + 362), "Confirm Split Settle", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# 11. Step 11: Settle (full payment)
# ==========================================
def make_step11_screen():
    im = img_ticket.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 110))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay))
    d = ImageDraw.Draw(im)
    dw, dh = 600, 390
    dx = (1920 - dw) // 2
    dy = (1080 - dh) // 2
    d.rounded_rectangle((dx, dy, dx + dw, dy + dh), radius=16, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=2)
    d.text((dx + 35, dy + 28), "Settle — Table 01", font=f_title, fill=(30, 41, 59, 255))
    d.text((dx + 35, dy + 66), "Amount due SAR 270.00 incl. VAT", font=f_bold, fill=(3, 142, 65, 255))
    # Payment tender buttons
    tenders = [("Cash", 18, 113, 208), ("Card (mada)", 3, 142, 65), ("Online", 100, 116, 139), ("Other", 100, 116, 139)]
    for ti, (tname, r, g, b) in enumerate(tenders):
        col = ti % 2
        row = ti // 2
        tx = dx + 35 + col * 270
        ty = dy + 115 + row * 60
        d.rounded_rectangle((tx, ty, tx + 250, ty + 50), radius=8, fill=(r, g, b, 255))
        d.text((tx + 75, ty + 14), tname, font=f_bold, fill=(255, 255, 255, 255))
    # Split bill and voucher options
    d.rounded_rectangle((dx + 35, dy + 250, dx + 290, dy + 295), radius=8, fill=(245, 247, 250, 255), outline=(218, 226, 236, 255), width=1)
    d.text((dx + 105, dy + 262), "Food Voucher", font=f_med, fill=(71, 85, 105, 255))
    d.rounded_rectangle((dx + 310, dy + 250, dx + dw - 35, dy + 295), radius=8, fill=(245, 247, 250, 255), outline=(218, 226, 236, 255), width=1)
    d.text((dx + 385, dy + 262), "Split Bill", font=f_med, fill=(71, 85, 105, 255))
    # Settle action
    d.rounded_rectangle((dx + 35, dy + 320, dx + dw - 35, dy + 365), radius=8, fill=(217, 83, 30, 255))
    d.text((dx + 175, dy + 332), "Settle & Print Final Receipt", font=f_bold, fill=(255, 255, 255, 255))
    return im

# ==========================================
# 12. Step 12: Add more items later
# ==========================================
def make_step12_screen():
    im = img_ticket.copy()
    d = ImageDraw.Draw(im)
    # Highlight second newly added dish Chicken Mandi
    d.rounded_rectangle((428, 186, 526, 272), radius=12, outline=(3, 142, 65, 255), width=3)
    # Highlight updated Order Items list showing new pending item
    d.rounded_rectangle((1430, 255, 1880, 365), radius=10, fill=(255, 250, 245, 255), outline=(217, 83, 30, 255), width=2)
    d.text((1445, 268), "Chicken Mandi (New)", font=f_bold, fill=(30, 41, 59, 255))
    d.text((1445, 296), "1x · SAR 25.00 · Status: Pending KOT", font=f_reg, fill=(217, 83, 30, 255))
    # Highlight KOT (1) button indicating new pending kitchen dispatch
    d.rounded_rectangle((1445, 918, 1640, 954), radius=8, fill=(217, 83, 30, 255), outline=(255, 255, 255, 255), width=2)
    d.text((1495, 926), "KOT (1)", font=f_bold, fill=(255, 255, 255, 255))
    return im

ALL_STEPS = [
    {
        "step_num": 1,
        "heading": "Step 1 — Open the table",
        "body": "Select guest dining zones and open the table for guest seating.",
        "steps": [
            "Tap Dine-in from the navigation or home dashboard.",
            "Select the guest table on the interactive floor map.",
            "Open / seat the table (enter number of guests if asked)."
        ],
        "screen_fn": make_step1_screen
    },
    {
        "step_num": 2,
        "heading": "Step 2 — Add food items",
        "body": "Select dish categories, quantities, custom notes, and modifiers.",
        "steps": [
            "Choose category on the left (e.g. Food, Sides, Drinks).",
            "Tap the dish to add to the order ticket.",
            "Select quantity using the touch counter buttons.",
            "Add notes if needed (Example: “No onion”, “Less spicy”).",
            "Select add-ons if the screen shows item customizers.",
            "Add the item to the order.",
            "Check Subtotal on the right side of the ticket."
        ],
        "screen_fn": make_step2_screen
    },
    {
        "step_num": 3,
        "heading": "Step 3 — Understand the bill totals (Tax / VAT)",
        "body": "Clear itemization of food subtotal, discounts, extra charges, and 15% VAT.",
        "steps": [
            "Subtotal: food total before any discount is applied.",
            "Discount (%): money reduced after you pick a discount %.",
            "Extra charges lines: if you switched on charges (Service, Parking).",
            "VAT / tax lines: automatically calculated by system settings.",
            "Total: final amount due (includes VAT when tax is on).",
            "Important: Admin modifies tax in Settings > Tax; floor displays live tax."
        ],
        "screen_fn": make_step3_screen
    },
    {
        "step_num": 4,
        "heading": "Step 4 — How to use Discount on the floor",
        "body": "Apply authorized percentage discounts directly to the floor ticket.",
        "steps": [
            "Open the table ticket with items already added.",
            "Find the DISCOUNT row located under the bill totals.",
            "Tap a percent button: 0%, 7%, 10% (configured by Admin).",
            "The active discount button becomes highlighted dark.",
            "Check that Discount amount and Net Total updated.",
            "Tap 0% anytime if you want to remove the discount."
        ],
        "screen_fn": make_step4_screen
    },
    {
        "step_num": 5,
        "heading": "Step 5 — How to use Extra Charges on the floor",
        "body": "Toggle active extra charges (service fee, parking, packing) on order.",
        "steps": [
            "Extra charges must first be created in Settings > Extra Charges.",
            "On the table ticket, find the EXTRA CHARGES section.",
            "Tap a charge pill to turn it ON (e.g. Service charges SAR 150.00).",
            "Tap the charge pill again anytime to turn it OFF.",
            "When ON, the charge line appears in totals and Total increases.",
            "Tax on that charge (if configured) is handled automatically."
        ],
        "screen_fn": make_step5_screen
    },
    {
        "step_num": 6,
        "heading": "Step 6 — Save / Save & Print / Save & Bill",
        "body": "Interim order storage options keeping the order active without payment.",
        "steps": [
            "Add items first (buttons stay disabled if the ticket is empty).",
            "Save: Saves the ticket when guests will order more later.",
            "Save & Print: Saves ticket and prints an interim order slip.",
            "Save & Bill: Saves and prints guest bill preview (temp bill).",
            "Confirm print came on the receipt printer if you chose print.",
            "Server tip: Use Save & Bill when guest requests bill to review."
        ],
        "screen_fn": make_step6_screen
    },
    {
        "step_num": 7,
        "heading": "Step 7 — Send to kitchen: KOT and KOT & Print",
        "body": "Dispatch pending food orders to Kitchen Display Screen or thermal printer.",
        "steps": [
            "KOT sends pending items electronically to kitchen display (KDS).",
            "Number badge on button indicates pending items e.g. KOT (2).",
            "KOT & Print sends items and prints physical paper kitchen ticket.",
            "After adding new items to ticket, tap KOT.",
            "Confirm kitchen screen or KOT printer received the order.",
            "Critical: Never only Save if kitchen must cook; always send KOT."
        ],
        "screen_fn": make_step7_screen
    },
    {
        "step_num": 8,
        "heading": "Step 8 — Change Table",
        "body": "Transfer active guest orders seamlessly when customers move dining tables.",
        "steps": [
            "Open the current active table ticket.",
            "Tap Change Table action button.",
            "Select the new empty / target vacant table.",
            "Confirm the table transfer.",
            "Original table frees up instantly; order shows on target table.",
            "Check floor map once to confirm seating change."
        ],
        "screen_fn": make_step8_screen
    },
    {
        "step_num": 9,
        "heading": "Step 9 — Merge Tables",
        "body": "Combine multiple seated tables into one unified host ticket.",
        "steps": [
            "Open the main / host table that will keep the combined bill.",
            "Tap Merge Tables action button.",
            "Select the other table(s) to merge into this host table.",
            "Confirm table merge.",
            "Items from linked tables transfer onto host bill with Merged badge.",
            "Settle payment once on the designated host table."
        ],
        "screen_fn": make_step9_screen
    },
    {
        "step_num": 10,
        "heading": "Step 10 — Split (open Settle in split mode)",
        "body": "Divide customer tickets across multiple payers and distinct tender types.",
        "steps": [
            "Open active table ticket.",
            "Check that Total is correct (discount, extra charges, VAT ok).",
            "Tap Split action button on the ticket.",
            "Settle window opens ready for Equal or Custom split mode.",
            "Add payments for each guest until Remaining balance is SAR 0.00.",
            "Tap Confirm split to finalize multi-guest payment."
        ],
        "screen_fn": make_step10_screen
    },
    {
        "step_num": 11,
        "heading": "Step 11 — Settle (full payment)",
        "body": "Collect full payment and issue compliant ZATCA fiscal receipts.",
        "steps": [
            "Open active table ticket.",
            "Tap Settle (main pay button).",
            "Settle window opens titled: Settle — Table XX.",
            "Amount due displays clearly inclusive of 15% VAT.",
            "Select payment method: Cash, Card (mada), Voucher, or Split.",
            "After successful payment, table becomes free automatically."
        ],
        "screen_fn": make_step11_screen
    },
    {
        "step_num": 12,
        "heading": "Step 12 — Add more items later",
        "body": "Update open dine-in tables with additional food courses and drinks.",
        "steps": [
            "Open the same occupied table again from the floor map.",
            "Add new dishes, appetizers, or beverages to the ticket.",
            "Tap KOT again to dispatch only the new pending items to kitchen.",
            "Update discount or extra charges if needed before final Settle."
        ],
        "screen_fn": make_step12_screen
    }
]

def build_all_part_d_slides():
    slides_dir = os.path.join(WORKSPACE_DIR, "Slides", "Part D")
    export_dir = os.path.join(WORKSPACE_DIR, "export", "Part D")
    os.makedirs(slides_dir, exist_ok=True)
    os.makedirs(export_dir, exist_ok=True)

    print("=== Starting Part D Slides Generation (Steps 1 to 12) ===")
    for item in ALL_STEPS:
        s_num = item["step_num"]
        heading = item["heading"]
        body = item["body"]
        steps = item["steps"]
        screen_img = item["screen_fn"]()

        # Filename matching project standards (hyphen without unicode issues or illegal slashes)
        clean_name = heading.replace('—', '-').replace('/', '-').replace(':', ' -')
        filename = f"{clean_name}.jpg"
        out_slide = os.path.join(slides_dir, filename)
        out_export = os.path.join(export_dir, filename)

        print(f"Rendering Step {s_num}: {filename}...")
        render_part_d_step_slide(
            step_num=s_num,
            heading=heading,
            body=body,
            steps=steps,
            screen_img=screen_img,
            output_paths=[out_slide, out_export]
        )

    print("=== All 12 Part D Step Slides Generated Successfully! ===")

if __name__ == "__main__":
    build_all_part_d_slides()
