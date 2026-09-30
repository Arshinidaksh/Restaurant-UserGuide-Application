import os
import sys
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
sys.path.insert(0, APP_DIR)

from src.info_renderer import render_info_slide

FONTS_DIR = os.path.join(APP_DIR, "fonts")
SLIDES_DIR = os.path.join(WORKSPACE_DIR, "Slides", "Part D")
EXPORT_DIR = os.path.join(WORKSPACE_DIR, "export", "Part D")

os.makedirs(SLIDES_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

content = {
    "style": "board",
    "theme_color": "green",
    "kicker": "PART D — DINE-IN ORDERS & FLOOR TICKETS",
    "heading": "Part D — How to take a dine-in order (Floor)",
    "subheading": "This part explains the Dine-in / Floor ticket screen — including Discount, Extra charges, Tax (VAT), Save buttons, KOT, Split, Change Table, Merge Tables, and Settle.",
    "items": [
        {
            "title": "Table Seating & Menu Selection",
            "description": "Select guest dining zones, tap vacant tables to seat guests, choose dishes with custom notes, addons, and quantities.",
            "tag": "FLOOR"
        },
        {
            "title": "Discounts & Extra Charges",
            "description": "Apply quick discount percentage pills (0%, 7%, 10%) and toggle optional service charges or parking fees directly on ticket.",
            "tag": "DISCOUNT"
        },
        {
            "title": "Tax (VAT 15%) Calculations",
            "description": "Automatic 15% VAT calculation and legal ZATCA itemization across Subtotal, Discount, Charges, and Grand Total.",
            "tag": "VAT 15%"
        },
        {
            "title": "Save, Save & Print, Save & Bill",
            "description": "Draft order storage options: save open ticket to floor map, print interim order slip, or generate customer bill preview.",
            "tag": "SAVE"
        },
        {
            "title": "KOT & KOT & Print Kitchen Flow",
            "description": "Dispatch pending food orders paperlessly to Kitchen Display Screens (KDS) or print station thermal kitchen tickets.",
            "tag": "KOT"
        },
        {
            "title": "Split, Change, Merge & Settle",
            "description": "Transfer orders to another table, merge dining parties into one check, split covers, and launch payment settlement.",
            "tag": "SETTLE"
        }
    ],
    "tip_note": "Application URL: https://app.restaurant-pos.isarva.in · Active Floor Tickets & Kitchen Flow Guide."
}

out_slide = os.path.join(SLIDES_DIR, "Part D — How to take a dine-in order (Floor).jpg")
out_export = os.path.join(EXPORT_DIR, "Part D — How to take a dine-in order (Floor).jpg")

render_info_slide(content, FONTS_DIR, out_slide)

# Copy to export
img = Image.open(out_slide)
img.save(out_export, "JPEG", quality=96, optimize=True)

print("Generated successfully:")
print("1.", out_slide)
print("2.", out_export)
