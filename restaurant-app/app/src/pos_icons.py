"""
Restaurant POS Domain Vector Badges:
Generates custom, pixel-perfect, 4x-supersampled antialiased vector icons for every POS card topic.
Pure in-memory Pillow generation with zero external asset dependencies.
"""
import math
from typing import Dict
from PIL import Image, ImageDraw

COLOR_GREEN = (3, 142, 65, 255)
BG_FILL = (238, 248, 242, 255)
BG_OUTLINE = (180, 226, 202, 255)

_ICON_CACHE: Dict[str, Image.Image] = {}

def draw_star(draw: ImageDraw.ImageDraw, cx: float, cy: float, r_out: float, r_in: float, fill: tuple, outline: tuple = None, width: int = 1):
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * (math.pi / 5)
        r = r_out if i % 2 == 0 else r_in
        points.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
    draw.polygon(points, fill=fill, outline=outline)

def create_pos_vector_icon(name: str, size: int = 64, color: tuple = COLOR_GREEN) -> Image.Image:
    """Renders a 4x supersampled, antialiased 64x64 vector icon badge."""
    scale = 4
    big_size = size * scale
    im = Image.new("RGBA", (big_size, big_size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # 1. Container Badge
    pad = 4 * scale
    d.rounded_rectangle(
        (pad, pad, big_size - pad, big_size - pad),
        radius=16 * scale,
        fill=BG_FILL,
        outline=BG_OUTLINE,
        width=int(2.2 * scale)
    )

    lw = int(2.6 * scale)
    lw_thin = int(2.0 * scale)
    lw_thick = int(3.5 * scale)

    # 2. Draw Specific Domain Vector Icon inside the badge
    if name == "monitor":
        # PC / Monitor Terminal
        d.rounded_rectangle((66, 62, 190, 150), radius=10, outline=color, width=lw)
        d.line([(128, 150), (128, 186)], fill=color, width=lw)
        d.line([(96, 186), (160, 186)], fill=color, width=lw)
        d.line([(86, 134), (170, 134)], fill=color, width=lw_thin)
        d.ellipse((124, 140, 132, 148), fill=color)

    elif name == "key":
        # Security Key / Admin Credentials
        d.ellipse((68, 94, 126, 152), outline=color, width=lw)
        d.ellipse((84, 110, 110, 136), outline=color, width=lw_thin)
        d.line([(126, 123), (188, 123)], fill=color, width=lw)
        d.line([(162, 123), (162, 146)], fill=color, width=lw)
        d.line([(178, 123), (178, 142)], fill=color, width=lw)

    elif name == "doc_tax":
        # Legal Business Document / VAT Tax
        d.rounded_rectangle((76, 58, 180, 198), radius=10, outline=color, width=lw)
        # Folded corner
        d.line([(148, 58), (180, 90)], fill=color, width=lw)
        d.line([(148, 58), (148, 90), (180, 90)], fill=color, width=lw_thin)
        # Text lines
        d.line([(96, 106), (160, 106)], fill=color, width=lw)
        d.line([(96, 128), (160, 128)], fill=color, width=lw)
        d.line([(96, 150), (136, 150)], fill=color, width=lw)
        # Stamp badge
        d.ellipse((142, 156, 168, 182), outline=color, width=lw_thin)

    elif name == "shield_lock":
        # Security & Offline Shield
        # Shield curve
        d.line([(80, 78), (176, 78)], fill=color, width=lw)
        d.line([(80, 78), (80, 124)], fill=color, width=lw)
        d.line([(176, 78), (176, 124)], fill=color, width=lw)
        d.arc((80, 84, 176, 194), start=0, end=90, fill=color, width=lw)
        d.arc((80, 84, 176, 194), start=90, end=180, fill=color, width=lw)
        # Lock inside
        d.rounded_rectangle((110, 122, 146, 154), radius=6, outline=color, width=lw)
        d.arc((116, 102, 140, 130), start=180, end=360, fill=color, width=lw)
        d.ellipse((125, 134, 131, 142), fill=color)

    elif name == "power":
        # Hardware Power On Symbol
        d.arc((78, 76, 178, 176), start=305, end=235, fill=color, width=lw_thick)
        d.line([(128, 58), (128, 124)], fill=color, width=lw_thick)

    elif name == "storefront":
        # Restaurant Storefront / Branch Head Office
        # Awning
        d.polygon([(64, 106), (128, 64), (192, 106)], outline=color)
        d.line([(64, 106), (192, 106)], fill=color, width=lw)
        # Store body
        d.rectangle((76, 106, 180, 192), outline=color, width=lw)
        # Door
        d.rounded_rectangle((112, 136, 144, 192), radius=6, outline=color, width=lw)
        # Windows
        d.rectangle((86, 124, 104, 150), outline=color, width=lw_thin)
        d.rectangle((152, 124, 170, 150), outline=color, width=lw_thin)

    elif name == "wifi":
        # Wi-Fi Network Health
        d.ellipse((123, 175, 133, 185), fill=color)
        d.arc((108, 148, 148, 188), start=215, end=325, fill=color, width=lw_thick)
        d.arc((90, 124, 166, 200), start=215, end=325, fill=color, width=lw_thick)
        d.arc((72, 100, 184, 212), start=215, end=325, fill=color, width=lw_thick)

    elif name == "cash_money":
        # Opening Cash Float / Banknote & Coins
        d.rounded_rectangle((68, 82, 172, 152), radius=10, outline=color, width=lw)
        d.ellipse((106, 103, 134, 131), outline=color, width=lw)
        d.line([(78, 94), (78, 140)], fill=color, width=lw_thin)
        d.line([(162, 94), (162, 140)], fill=color, width=lw_thin)
        # Coin at bottom right
        d.ellipse((136, 134, 188, 186), fill=BG_FILL, outline=color, width=lw)
        d.ellipse((146, 144, 178, 176), outline=color, width=lw_thin)

    elif name == "save_disk":
        # Save Order / Order Ticket Storage
        d.rounded_rectangle((74, 66, 182, 190), radius=12, outline=color, width=lw)
        # Top slider
        d.rounded_rectangle((94, 66, 162, 114), radius=6, outline=color, width=lw_thin)
        d.rectangle((106, 76, 122, 102), fill=color)
        # Bottom label
        d.rounded_rectangle((90, 136, 166, 180), radius=6, outline=color, width=lw_thin)
        d.line([(102, 150), (154, 150)], fill=color, width=lw_thin)
        d.line([(102, 164), (142, 164)], fill=color, width=lw_thin)

    elif name == "kds_screen":
        # Kitchen Display Screen (KDS)
        d.rounded_rectangle((66, 68, 190, 162), radius=12, outline=color, width=lw)
        d.line([(128, 162), (128, 188)], fill=color, width=lw)
        d.line([(98, 188), (158, 188)], fill=color, width=lw)
        # 3 KDS order ticket columns inside
        d.rounded_rectangle((78, 82, 108, 148), radius=4, outline=color, width=lw_thin)
        d.rounded_rectangle((113, 82, 143, 148), radius=4, outline=color, width=lw_thin)
        d.rounded_rectangle((148, 82, 178, 148), radius=4, outline=color, width=lw_thin)

    elif name == "thermal_printer":
        # Thermal POS Printer
        d.rounded_rectangle((72, 108, 184, 192), radius=14, outline=color, width=lw)
        d.line([(88, 108), (168, 108)], fill=color, width=lw_thick)
        # Paper ticket exiting printer
        d.rectangle((94, 62, 162, 108), fill=BG_FILL, outline=color, width=lw)
        d.line([(106, 76), (150, 76)], fill=color, width=lw_thin)
        d.line([(106, 88), (138, 88)], fill=color, width=lw_thin)
        d.ellipse((162, 134, 172, 144), fill=color)

    elif name == "bill_preview":
        # Bill Preview / Guest Check Slip
        d.rounded_rectangle((78, 60, 158, 194), radius=8, outline=color, width=lw)
        d.line([(92, 82), (144, 82)], fill=color, width=lw)
        d.line([(92, 102), (144, 102)], fill=color, width=lw_thin)
        d.line([(92, 118), (144, 118)], fill=color, width=lw_thin)
        d.line([(92, 134), (130, 134)], fill=color, width=lw_thin)
        # Eye / Magnifier badge
        d.ellipse((136, 136, 180, 180), fill=BG_FILL, outline=color, width=lw)
        d.line([(168, 168), (188, 188)], fill=color, width=lw_thick)

    elif name == "table_move":
        # Table Transfer (Change Table)
        # Source table
        d.ellipse((68, 108, 116, 156), outline=color, width=lw)
        # Destination table
        d.ellipse((140, 108, 188, 156), outline=color, width=lw)
        # Transfer arrow above
        d.arc((92, 60, 164, 120), start=200, end=340, fill=color, width=lw_thick)
        d.polygon([(162, 88), (174, 94), (166, 108)], fill=color)

    elif name == "table_merge":
        # Merge Dining Tables
        d.rounded_rectangle((64, 100, 114, 160), radius=10, outline=color, width=lw)
        d.rounded_rectangle((142, 100, 192, 160), radius=10, outline=color, width=lw)
        # Merge link / double arrow
        d.line([(114, 130), (142, 130)], fill=color, width=lw_thick)
        d.polygon([(118, 122), (110, 130), (118, 138)], fill=color)
        d.polygon([(138, 122), (146, 130), (138, 138)], fill=color)

    elif name == "bill_split":
        # Split Covers or Bill (Divided ticket)
        d.rounded_rectangle((86, 60, 170, 120), radius=8, outline=color, width=lw)
        d.line([(100, 80), (156, 80)], fill=color, width=lw_thin)
        # Split downward paths
        d.line([(112, 120), (94, 152)], fill=color, width=lw)
        d.line([(144, 120), (162, 152)], fill=color, width=lw)
        # Two mini bills at bottom
        d.rounded_rectangle((70, 152, 118, 196), radius=6, outline=color, width=lw)
        d.rounded_rectangle((138, 152, 186, 196), radius=6, outline=color, width=lw)

    elif name == "floor_zones":
        # Table Area Switch (Dining Zones Map)
        d.rounded_rectangle((68, 68, 120, 120), radius=8, fill=color)
        d.rounded_rectangle((136, 68, 188, 120), radius=8, outline=color, width=lw)
        d.rounded_rectangle((68, 136, 120, 188), radius=8, outline=color, width=lw)
        d.rounded_rectangle((136, 136, 188, 188), radius=8, outline=color, width=lw)

    elif name == "coupon_percent":
        # Food Vouchers / Coupons
        d.rounded_rectangle((66, 84, 190, 172), radius=12, outline=color, width=lw)
        # Semicircle ticket notches
        d.arc((52, 114, 80, 142), start=270, end=90, fill=color, width=lw)
        d.arc((176, 114, 204, 142), start=90, end=270, fill=color, width=lw)
        # Percentage % symbol
        d.line([(146, 104), (110, 152)], fill=color, width=lw)
        d.ellipse((108, 106, 122, 120), fill=color)
        d.ellipse((134, 136, 148, 150), fill=color)

    elif name == "gift_card":
        # Prepaid Gift Cards
        d.rounded_rectangle((64, 82, 192, 174), radius=14, outline=color, width=lw)
        d.line([(64, 110), (192, 110)], fill=color, width=lw_thick)
        # Gift Ribbon bow
        d.line([(128, 82), (128, 174)], fill=color, width=lw)
        d.ellipse((116, 68, 128, 84), outline=color, width=lw_thin)
        d.ellipse((128, 68, 140, 84), outline=color, width=lw_thin)

    elif name == "loyalty_star":
        # CRM Loyalty Points
        draw_star(d, 128, 114, 46, 22, fill=color)
        # Ribbon tails
        d.line([(106, 146), (92, 192), (114, 180), (126, 194)], fill=color, width=lw)
        d.line([(150, 146), (164, 192), (142, 180), (130, 194)], fill=color, width=lw)

    elif name == "pos_terminal":
        # SoftPOS Terminal / Handheld Contactless Card Tap
        d.rounded_rectangle((82, 60, 174, 196), radius=14, outline=color, width=lw)
        d.rounded_rectangle((94, 76, 162, 118), radius=6, outline=color, width=lw_thin)
        # Keypad dots
        for rx in [106, 128, 150]:
            for ry in [136, 154, 172]:
                d.ellipse((rx - 4, ry - 4, rx + 4, ry + 4), fill=color)
        # NFC waves on top right
        d.arc((156, 44, 196, 84), start=270, end=360, fill=color, width=lw)
        d.arc((168, 32, 208, 72), start=270, end=360, fill=color, width=lw)

    elif name == "receipt_printer":
        # Receipt Printers (Counter)
        d.rounded_rectangle((72, 100, 184, 192), radius=14, outline=color, width=lw)
        d.rounded_rectangle((92, 58, 164, 100), radius=6, fill=BG_FILL, outline=color, width=lw)
        d.line([(104, 72), (152, 72)], fill=color, width=lw_thin)
        d.line([(104, 84), (140, 84)], fill=color, width=lw_thin)
        d.line([(86, 100), (170, 100)], fill=color, width=lw_thick)
        d.ellipse((158, 130, 170, 142), fill=color)

    elif name == "kitchen_printer":
        # Kitchen Station Printers (with Chef Cloche)
        d.rounded_rectangle((72, 104, 184, 192), radius=14, outline=color, width=lw)
        d.rounded_rectangle((92, 64, 164, 104), radius=6, fill=BG_FILL, outline=color, width=lw)
        # Chef Cloche icon on front
        d.arc((106, 126, 150, 166), start=180, end=360, fill=color, width=lw)
        d.line([(102, 166), (154, 166)], fill=color, width=lw)
        d.ellipse((124, 122, 132, 130), fill=color)

    elif name == "network_routing":
        # Network Mapping / Router & Nodes
        d.rounded_rectangle((104, 104, 152, 152), radius=8, fill=color)
        # Lines radiating to printer endpoints
        d.line([(128, 104), (128, 68)], fill=color, width=lw)
        d.line([(104, 128), (68, 128)], fill=color, width=lw)
        d.line([(152, 128), (188, 128)], fill=color, width=lw)
        d.line([(128, 152), (128, 188)], fill=color, width=lw)
        # Peripheral nodes
        d.ellipse((118, 58, 138, 78), outline=color, width=lw)
        d.ellipse((58, 118, 78, 138), outline=color, width=lw)
        d.ellipse((178, 118, 198, 138), outline=color, width=lw)
        d.ellipse((118, 178, 138, 198), outline=color, width=lw)

    elif name == "slip_template":
        # Receipt Header & Footer Configuration
        d.rounded_rectangle((80, 56, 176, 200), radius=8, outline=color, width=lw)
        # Header block
        d.rounded_rectangle((92, 68, 164, 94), radius=4, fill=color)
        # Body lines
        d.line([(92, 112), (164, 112)], fill=color, width=lw_thin)
        d.line([(92, 126), (164, 126)], fill=color, width=lw_thin)
        d.line([(92, 140), (140, 140)], fill=color, width=lw_thin)
        # Footer block (e.g. QR code)
        d.rectangle((120, 158, 152, 190), outline=color, width=lw_thin)
        d.rectangle((128, 166, 144, 182), fill=color)

    elif name == "export_arrow":
        # Catalog Export (Box + Arrow Out)
        d.rounded_rectangle((70, 116, 186, 192), radius=10, outline=color, width=lw)
        d.line([(70, 144), (186, 144)], fill=color, width=lw_thin)
        # Arrow pointing UP and OUT
        d.line([(128, 154), (128, 64)], fill=color, width=lw_thick)
        d.polygon([(128, 56), (112, 82), (144, 82)], fill=color)

    elif name == "import_arrow":
        # Catalog Import (Box + Arrow In)
        d.rounded_rectangle((70, 116, 186, 192), radius=10, outline=color, width=lw)
        d.line([(70, 144), (186, 144)], fill=color, width=lw_thin)
        # Arrow pointing DOWN and IN
        d.line([(128, 64), (128, 146)], fill=color, width=lw_thick)
        d.polygon([(128, 156), (112, 130), (144, 130)], fill=color)

    elif name == "cloud_sync":
        # Cloud Sync Backups
        # Cloud arcs
        d.arc((76, 88, 132, 144), start=140, end=330, fill=color, width=lw)
        d.arc((110, 68, 174, 132), start=190, end=360, fill=color, width=lw)
        d.arc((148, 88, 188, 144), start=230, end=40, fill=color, width=lw)
        d.line([(86, 144), (180, 144)], fill=color, width=lw)
        # Circular sync arrows below cloud
        d.arc((106, 146, 150, 190), start=30, end=150, fill=color, width=lw)
        d.arc((106, 146, 150, 190), start=210, end=330, fill=color, width=lw)
        d.polygon([(148, 160), (156, 168), (142, 172)], fill=color)
        d.polygon([(108, 176), (100, 168), (114, 164)], fill=color)

    elif name == "db_clean":
        # Database Shield / Safe Data Cleaning
        # Database cylinders
        d.ellipse((82, 70, 174, 98), outline=color, width=lw)
        d.line([(82, 84), (82, 136)], fill=color, width=lw)
        d.line([(174, 84), (174, 136)], fill=color, width=lw)
        d.arc((82, 108, 174, 136), start=0, end=180, fill=color, width=lw)
        d.line([(82, 136), (82, 186)], fill=color, width=lw)
        d.line([(174, 136), (174, 186)], fill=color, width=lw)
        d.arc((82, 158, 174, 186), start=0, end=180, fill=color, width=lw)
        # Sparkle / broom star at top right
        d.line([(160, 64), (188, 64)], fill=color, width=lw_thin)
        d.line([(174, 50), (174, 78)], fill=color, width=lw_thin)

    elif name == "tax_gov":
        # Company & Legal Tax (ZATCA Government Tax)
        d.rounded_rectangle((74, 60, 182, 196), radius=10, outline=color, width=lw)
        # Scale of justice / pillar top
        d.polygon([(88, 86), (128, 68), (168, 86)], fill=color)
        d.line([(88, 92), (168, 92)], fill=color, width=lw)
        # Text rows
        d.line([(94, 114), (162, 114)], fill=color, width=lw_thin)
        d.line([(94, 130), (162, 130)], fill=color, width=lw_thin)
        d.line([(94, 146), (142, 146)], fill=color, width=lw_thin)
        # Checkmark stamp
        d.ellipse((136, 150, 168, 182), outline=color, width=lw_thin)
        d.line([(144, 166), (150, 172), (160, 158)], fill=color, width=lw)

    elif name == "team_roles":
        # Users & Role Privileges (Team / Users)
        # Center user head and shoulders
        d.ellipse((112, 74, 144, 106), outline=color, width=lw)
        d.arc((94, 110, 162, 166), start=180, end=360, fill=color, width=lw)
        d.line([(94, 138), (162, 138)], fill=color, width=lw)
        # Left user
        d.ellipse((76, 92, 100, 116), outline=color, width=lw_thin)
        d.arc((66, 120, 110, 164), start=180, end=360, fill=color, width=lw_thin)
        # Right user
        d.ellipse((156, 92, 180, 116), outline=color, width=lw_thin)
        d.arc((146, 120, 190, 164), start=180, end=360, fill=color, width=lw_thin)
        # Shield badge at bottom center
        d.polygon([(120, 154), (136, 154), (136, 176), (128, 184), (120, 176)], fill=color)

    elif name == "menu_book":
        # Floor & Product Catalog (Menu Book & Fork)
        # Open book
        d.line([(128, 86), (128, 188)], fill=color, width=lw_thick)
        d.arc((72, 74, 128, 108), start=180, end=360, fill=color, width=lw)
        d.arc((128, 74, 184, 108), start=180, end=360, fill=color, width=lw)
        d.line([(72, 91), (72, 182)], fill=color, width=lw)
        d.line([(184, 91), (184, 182)], fill=color, width=lw)
        d.arc((72, 165, 128, 199), start=0, end=180, fill=color, width=lw)
        d.arc((128, 165, 184, 199), start=0, end=180, fill=color, width=lw)
        # Fork and knife on pages
        d.line([(90, 114), (110, 114)], fill=color, width=lw_thin)
        d.line([(90, 130), (110, 130)], fill=color, width=lw_thin)
        d.line([(146, 114), (166, 114)], fill=color, width=lw_thin)
        d.line([(146, 130), (166, 130)], fill=color, width=lw_thin)

    elif name == "test_checklist":
        # End-to-End Test Ticket (Checklist Clipboard)
        d.rounded_rectangle((76, 64, 180, 196), radius=10, outline=color, width=lw)
        d.rounded_rectangle((104, 52, 152, 72), radius=4, fill=color)
        # Checkmark 1
        d.line([(92, 100), (98, 106), (112, 92)], fill=color, width=lw)
        d.line([(120, 100), (164, 100)], fill=color, width=lw_thin)
        # Checkmark 2
        d.line([(92, 132), (98, 138), (112, 124)], fill=color, width=lw)
        d.line([(120, 132), (164, 132)], fill=color, width=lw_thin)
        # Checkmark 3
        d.line([(92, 164), (98, 170), (112, 156)], fill=color, width=lw)
        d.line([(120, 164), (150, 164)], fill=color, width=lw_thin)

    else:
        # Default elegant terminal
        d.rounded_rectangle((66, 62, 190, 150), radius=10, outline=color, width=lw)
        d.line([(128, 150), (128, 186)], fill=color, width=lw)
        d.line([(96, 186), (160, 186)], fill=color, width=lw)

    # 3. Downsample to target size with high-precision Lanczos
    res = im.resize((size, size), Image.Resampling.LANCZOS)
    return res

def get_matching_icon_for_card(card: dict, default_step: int = 1, size: int = 64) -> Image.Image:
    """Selects and caches the exact matching icon for a card based on explicit key or title analysis."""
    # 1. Explicit key
    if "icon" in card and card["icon"]:
        icon_name = card["icon"]
    else:
        # 2. Heuristic matcher based on title & description
        text = (card.get("title", "") + " " + card.get("description", "")).lower()
        if "security" in text or "shield" in text or "protect" in text:
            icon_name = "shield_lock"
        elif "hardware" in text or "terminal" in text or "laptop" in text:
            icon_name = "monitor"
        elif "credential" in text or "pin" in text or "password" in text or "key" in text:
            icon_name = "key"
        elif "power" in text:
            icon_name = "power"
        elif "branch" in text or "head office" in text or "store" in text:
            icon_name = "storefront"
        elif "network" in text or "wi-fi" in text or "wifi" in text or "offline" in text:
            icon_name = "wifi"
        elif "cash" in text or "float" in text or "till" in text or "drawer" in text:
            icon_name = "cash_money"
        elif "save order" in text or "save current" in text:
            icon_name = "save_disk"
        elif "kot to screen" in text or "kitchen display" in text or "kds" in text:
            icon_name = "kds_screen"
        elif "kot & print" in text or "station printer" in text:
            icon_name = "kitchen_printer"
        elif "bill preview" in text or "interim" in text or "guest check" in text:
            icon_name = "bill_preview"
        elif "change table" in text or "move active" in text:
            icon_name = "table_move"
        elif "merge table" in text or "combine" in text:
            icon_name = "table_merge"
        elif "split" in text:
            icon_name = "bill_split"
        elif "area" in text or "zone" in text or "floor" in text:
            icon_name = "floor_zones"
        elif "voucher" in text or "coupon" in text or "promotional" in text:
            icon_name = "coupon_percent"
        elif "gift card" in text or "prepaid" in text:
            icon_name = "gift_card"
        elif "loyalty" in text or "crm" in text or "points" in text or "reward" in text:
            icon_name = "loyalty_star"
        elif "softpos" in text or "countertop" in text or "contactless" in text or "nfc" in text:
            icon_name = "pos_terminal"
        elif "receipt printer" in text or "thermal" in text:
            icon_name = "receipt_printer"
        elif "mapping" in text or "router" in text or "ip" in text:
            icon_name = "network_routing"
        elif "header & footer" in text or "template" in text or "slip" in text:
            icon_name = "slip_template"
        elif "export" in text:
            icon_name = "export_arrow"
        elif "import" in text:
            icon_name = "import_arrow"
        elif "backup" in text or "cloud" in text:
            icon_name = "cloud_sync"
        elif "cleaning" in text or "safe data" in text or "maintenance" in text:
            icon_name = "db_clean"
        elif "user" in text or "role" in text or "privilege" in text:
            icon_name = "team_roles"
        elif "menu" in text or "catalog" in text or "dish" in text:
            icon_name = "menu_book"
        elif "test" in text or "checklist" in text:
            icon_name = "test_checklist"
        else:
            default_map = {1: "monitor", 2: "key", 3: "storefront", 4: "test_checklist"}
            icon_name = default_map.get(default_step, "monitor")

    cache_key = f"{icon_name}_{size}"
    if cache_key not in _ICON_CACHE:
        _ICON_CACHE[cache_key] = create_pos_vector_icon(icon_name, size)
    return _ICON_CACHE[cache_key]
