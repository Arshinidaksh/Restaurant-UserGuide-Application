"""
Information Slide Renderer: Generates 1920x1080 pixel-perfect informational JPG slides.
Supports:
1. "board" / "notice": Whiteboard notice card based on user sketch (information-design.png)
   - Variant A: Disclaimer & Link Notice (Slide 5)
   - Variant B: Structured Grid Cards (e.g. 6 non-charged rule items for Slide 5.1)
2. "flow" / "cards": Multi-step horizontal process cards (as in PPT References/4-What-You-Need.jpg).
Pure in-memory execution, zero intermediate disk I/O, cached TrueType fonts, brand colors.
"""
import os
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont

from .cache import get_cached_font, get_cached_image, get_cached_icon

# Brand Colors
COLOR_ORANGE = (255, 92, 53, 255)       # #FF5C35 Brand Orange
COLOR_GREEN = (3, 142, 65, 255)         # #038E41 Brand Green
COLOR_BLUE = (18, 113, 208, 255)        # #1271D0 Brand Blue
COLOR_GRAY_DARK = (30, 41, 59, 255)     # Deep dark title
COLOR_GRAY_TEXT = (88, 88, 90, 255)     # Body text
COLOR_CARD_BORDER = (218, 226, 236, 255)# Card border
COLOR_STEP_NUM = (200, 228, 218, 255)   # Mint green numeral

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
    """Wraps text within a maximum pixel width."""
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

def render_board_slide(content: Dict[str, Any], fonts_dir: str, output_path: str) -> str:
    """
    Renders an informational notice board slide based directly on user's sketch (information-design.png).
    Supports either disclaimer/link format or 2x3 structured items grid.
    """
    app_dir = os.path.dirname(fonts_dir)
    base_dir = os.path.dirname(app_dir)

    # 1. Base 1920x1080 canvas with brand background
    bg_p = os.path.join(base_dir, "Libraries", "complete-design-format", "Only-background-transparent.png")
    canvas = Image.new("RGBA", (1920, 1080), (255, 255, 255, 255))
    if os.path.exists(bg_p):
        bg = get_cached_image(bg_p)
        canvas.paste(bg, (0, 0), bg)

    draw = ImageDraw.Draw(canvas)

    # 2. Fonts
    font_semibold = os.path.join(fonts_dir, "Rubik-SemiBold.ttf")
    font_medium = os.path.join(fonts_dir, "Rubik-Medium.ttf")
    font_regular = os.path.join(fonts_dir, "Rubik-Regular.ttf")

    f_kicker = get_cached_font(font_semibold, 30)
    f_heading = get_cached_font(font_semibold, 52)
    f_sub = get_cached_font(font_regular, 24)
    f_disc = get_cached_font(font_semibold, 26)
    f_text = get_cached_font(font_regular, 26)
    f_bold = get_cached_font(font_medium, 26)
    f_link = get_cached_font(font_medium, 24)
    f_pil_t = get_cached_font(font_semibold, 22)
    f_pil_d = get_cached_font(font_regular, 18)

    # Accent color for kicker/ribbon
    theme_color = content.get("theme_color", "green" if "NOT" in content.get("heading", "") else "orange")
    if theme_color == "green":
        accent_rgb = COLOR_GREEN
    elif theme_color == "blue":
        accent_rgb = COLOR_BLUE
    else:
        accent_rgb = COLOR_ORANGE

    # 3. Kicker
    kicker_text = content.get("kicker", "PRICING & BILLING").strip()
    bar_x = 90
    bar_y = 135
    draw.rectangle((bar_x, bar_y + 3, bar_x + 8, bar_y + 37), fill=accent_rgb)
    draw.text((bar_x + 22, bar_y), kicker_text, font=f_kicker, fill=accent_rgb)

    # 4. Notice Board Card (Matching the user's sketch)
    cx1, cy1, cx2, cy2 = 90, 220, 1830, 905

    # Drop shadow
    draw.rounded_rectangle((cx1 - 2, cy1 + 6, cx2 + 2, cy2 + 10), radius=22, fill=(232, 237, 244, 150))
    # White card
    draw.rounded_rectangle((cx1, cy1, cx2, cy2), radius=20, fill=(255, 255, 255, 255), outline=COLOR_CARD_BORDER, width=2)

    # Top pin (from user sketch)
    pin_x = cx1 + 90
    draw.rectangle((pin_x - 3, cy1 - 32, pin_x + 3, cy1), fill=(100, 116, 139, 255))
    draw.ellipse((pin_x - 15, cy1 - 46, pin_x + 15, cy1 - 18), fill=accent_rgb, outline=(255, 255, 255, 255), width=3)
    draw.ellipse((pin_x - 5, cy1 - 37, pin_x + 5, cy1 - 27), fill=(255, 255, 255, 255))

    # Top brand ribbon
    ribbon_rgb = accent_rgb if ("theme_color" in content or content.get("items") or content.get("table")) else (COLOR_GREEN if theme_color == "green" else COLOR_BLUE)
    draw.rounded_rectangle((cx1, cy1, cx2, cy1 + 6), radius=4, fill=ribbon_rgb)

    pad_x = cx1 + 80

    # A. Heading inside board
    heading_text = content.get("heading", "").strip()
    heading_y = cy1 + 40 if content.get("table") else cy1 + 55
    draw.text((pad_x, heading_y), heading_text, font=f_heading, fill=COLOR_GRAY_DARK)

    # Check if this board has a disclaimer banner, structured items grid, or comparison table
    banner = content.get("banner", {})
    items = content.get("items", [])
    table = content.get("table", {})

    if banner:
        # B. Disclaimer Text
        disc_label = banner.get("label", "*Disclaimer:**")
        disc_text = banner.get("text", "Meta changes pricing by country and over time. Always check the official page:")
        draw.text((pad_x, cy1 + 160), disc_label, font=f_disc, fill=COLOR_ORANGE)
        lbl_w = draw.textbbox((0, 0), disc_label, font=f_disc)[2] - draw.textbbox((0, 0), disc_label, font=f_disc)[0]
        draw.text((pad_x + lbl_w + 14, cy1 + 160), disc_text, font=f_text, fill=COLOR_GRAY_TEXT)

        # C. Clean URL Box (No button)
        url_link = banner.get("link", "https://developers.facebook.com/docs/whatsapp/pricing")
        url_y = cy1 + 220
        url_w = cx2 - 80 - pad_x
        draw.rounded_rectangle((pad_x, url_y, pad_x + url_w, url_y + 70), radius=12, fill=(244, 248, 254, 255), outline=(205, 224, 248, 255), width=2)
        draw.text((pad_x + 28, url_y + 19), url_link, font=f_link, fill=COLOR_BLUE)

        # D. Planning Note Below
        note_text = banner.get("note", "Below is a practical guide for planning, not a legal quote.")
        draw.text((pad_x, cy1 + 340), note_text, font=f_bold, fill=(51, 65, 85, 255))

        # E. Highlight Cards inside Board
        cards = content.get("cards", [])
        if cards:
            num_cards = len(cards)
            pil_gap = 42
            avail_pil_w = cx2 - 80 - pad_x
            pil_w = int((avail_pil_w - (num_cards - 1) * pil_gap) / num_cards)
            pil_h = 145
            pil_y = cy1 + 415

            color_palette = [
                (COLOR_GREEN, (238, 250, 243, 255)),
                (COLOR_BLUE, (243, 248, 255, 255)),
                (COLOR_ORANGE, (255, 246, 243, 255)),
                (COLOR_GRAY_DARK, (245, 247, 250, 255))
            ]

            for i, card in enumerate(cards):
                p_color, p_bg = color_palette[i % len(color_palette)]
                px = pad_x + i * (pil_w + pil_gap)
                draw.rounded_rectangle((px, pil_y, px + pil_w, pil_y + pil_h), radius=12, fill=p_bg, outline=p_color, width=1)
                draw.text((px + 22, pil_y + 22), card.get("title", ""), font=f_pil_t, fill=p_color)

                d_lines = wrap_text(card.get("description", ""), f_pil_d, pil_w - 44, draw)
                for li, l in enumerate(d_lines[:3]):
                    draw.text((px + 22, pil_y + 58 + li * 26), l, font=f_pil_d, fill=(71, 85, 105, 255))

    elif items:
        # Dynamic Grid Layout: 2x2 for 4 items, 3x2 for 6 items
        num_items = len(items)
        num_cols = 2 if num_items <= 4 else 3

        sub_text = content.get("subheading", "")
        if sub_text:
            draw.text((pad_x, cy1 + 130), sub_text, font=f_sub, fill=COLOR_GRAY_TEXT)

        if theme_color == "green":
            card_fill = (246, 250, 248, 255)
            card_border = (200, 230, 215, 255)
            icon_file = "brand_check_green.png"
        elif theme_color == "blue":
            card_fill = (244, 248, 254, 255)
            card_border = (205, 224, 248, 255)
            icon_file = "brand_blue_icon.png"
        else:
            card_fill = (255, 250, 248, 255)
            card_border = (255, 224, 215, 255)
            icon_file = "brand_charge_icon.png"

        icon_path = os.path.join(app_dir, icon_file)
        if not os.path.exists(icon_path):
            icon_path = os.path.join(app_dir, "brand_check_green.png")
        icon_26 = get_cached_icon(icon_path, (26, 26)) if os.path.exists(icon_path) else None

        if num_items == 3:
            # 3 Horizontal Cards (1 column x 3 rows)
            card_w = 1580
            card_h = 118
            gap_y = 20
            start_y = cy1 + 175
            f_code = get_cached_font(font_medium, 16)
            f_card_tag = get_cached_font(font_semibold, 14)

            for i, c in enumerate(items):
                cy = start_y + i * (card_h + gap_y)
                c_bg = tuple(c["card_bg"]) if isinstance(c.get("card_bg"), list) else c.get("card_bg", (248, 252, 249, 255) if i == 0 else ((247, 250, 254, 255) if i == 1 else (255, 249, 247, 255)))
                c_bd = tuple(c["card_bd"]) if isinstance(c.get("card_bd"), list) else c.get("card_bd", (205, 235, 218, 255) if i == 0 else ((210, 228, 250, 255) if i == 1 else (255, 222, 212, 255)))
                badge_bg = tuple(c["badge_bg"]) if isinstance(c.get("badge_bg"), list) else c.get("badge_bg", (238, 250, 243, 255) if i == 0 else ((243, 248, 255, 255) if i == 1 else (255, 246, 243, 255)))
                badge_col = tuple(c["badge_col"]) if isinstance(c.get("badge_col"), list) else c.get("badge_col", COLOR_GREEN if i == 0 else (COLOR_BLUE if i == 1 else COLOR_ORANGE))

                draw.rounded_rectangle((pad_x, cy, pad_x + card_w, cy + card_h), radius=12, fill=c_bg, outline=c_bd, width=1)

                # Icon
                if icon_26:
                    canvas.paste(icon_26, (pad_x + 24, cy + 24), icon_26)
                else:
                    draw.ellipse((pad_x + 24, cy + 24, pad_x + 50, cy + 50), fill=accent_rgb)

                # Title
                title_text = c.get("title", "")
                draw.text((pad_x + 64, cy + 22), title_text, font=f_pil_t, fill=(20, 30, 45, 255))

                # Tag badge next to title
                tag = c.get("tag", "")
                if tag:
                    tb_bbox = draw.textbbox((0, 0), tag, font=f_card_tag)
                    tb_w = tb_bbox[2] - tb_bbox[0] + 16
                    t_bbox = draw.textbbox((0, 0), title_text, font=f_pil_t)
                    tx_end = pad_x + 64 + (t_bbox[2] - t_bbox[0]) + 16
                    draw.rounded_rectangle((tx_end, cy + 23, tx_end + tb_w, cy + 47), radius=5, fill=badge_bg, outline=badge_col, width=1)
                    draw.text((tx_end + 8, cy + 26), tag, font=f_card_tag, fill=badge_col)

                # Description lines
                desc = c.get("description", "")
                d_lines = desc.split("\n") if "\n" in desc else wrap_text(desc, f_pil_d, card_w - 440, draw)
                for li, dl in enumerate(d_lines[:2]):
                    draw.text((pad_x + 64, cy + 58 + li * 24), dl, font=f_pil_d, fill=(71, 85, 105, 255))

                # Right-side highlight box
                hl = c.get("highlight", "")
                if hl:
                    hl_w = 340
                    hl_h = 44
                    hl_x = pad_x + card_w - hl_w - 24
                    hl_y = cy + (card_h - hl_h) // 2
                    draw.rounded_rectangle((hl_x, hl_y, hl_x + hl_w, hl_y + hl_h), radius=8, fill=(255, 255, 255, 255), outline=badge_col, width=1)
                    draw.text((hl_x + 18, hl_y + 11), hl, font=f_code, fill=badge_col)

        else:
            has_links = any(bool(item.get("link")) for item in items)
            if num_cols == 2:
                col_w = 760
                row_h = 172 if has_links else 160
                gap_x = 60
                gap_y = 22 if has_links else 30
                start_grid_y = cy1 + 175 if has_links else cy1 + 190
            else:
                col_w = 500
                row_h = 155
                gap_x = 40
                gap_y = 25
                start_grid_y = cy1 + 185

            for idx, item in enumerate(items):
                col = idx % num_cols
                row = idx // num_cols
                bx = pad_x + col * (col_w + gap_x)
                by = start_grid_y + row * (row_h + gap_y)

                # Card Colors
                c_bg = tuple(item["card_bg"]) if isinstance(item.get("card_bg"), list) else item.get("card_bg", card_fill)
                c_bd = tuple(item["card_bd"]) if isinstance(item.get("card_bd"), list) else item.get("card_bd", card_border)
                b_bg = tuple(item["badge_bg"]) if isinstance(item.get("badge_bg"), list) else item.get("badge_bg", (255, 255, 255, 255))
                b_col = tuple(item["badge_col"]) if isinstance(item.get("badge_col"), list) else item.get("badge_col", accent_rgb)

                # Box
                draw.rounded_rectangle((bx, by, bx + col_w, by + row_h), radius=12, fill=c_bg, outline=c_bd, width=1)

                # Icon
                cur_icon = icon_26
                if item.get("icon"):
                    icon_f = os.path.join(app_dir, item["icon"])
                    if os.path.exists(icon_f):
                        cur_icon = get_cached_icon(icon_f, (26, 26))

                if cur_icon:
                    canvas.paste(cur_icon, (bx + 18, by + 18), cur_icon)
                else:
                    draw.ellipse((bx + 18, by + 18, bx + 44, by + 44), fill=b_col)

                # Title
                draw.text((bx + 54, by + 19), item.get("title", ""), font=f_pil_t, fill=(20, 30, 45, 255))

                # Optional Tag badge
                tag = item.get("tag", "")
                if tag:
                    f_card_tag = get_cached_font(font_semibold, 13)
                    tb_bbox = draw.textbbox((0, 0), tag, font=f_card_tag)
                    tb_w = tb_bbox[2] - tb_bbox[0] + 16
                    tb_x = bx + col_w - tb_w - 18
                    tb_y = by + 18
                    draw.rounded_rectangle((tb_x, tb_y, tb_x + tb_w, tb_y + 24), radius=5, fill=b_bg, outline=b_col, width=1)
                    draw.text((tb_x + 8, tb_y + 3), tag, font=f_card_tag, fill=b_col)

                # Description & Link
                if has_links:
                    d_lines = wrap_text(item.get("description", ""), f_pil_d, col_w - 36, draw)
                    for li, l in enumerate(d_lines[:2]):
                        draw.text((bx + 18, by + 56 + li * 22), l, font=f_pil_d, fill=(71, 85, 105, 255))

                    link_val = item.get("link", "")
                    if link_val:
                        f_link_text = get_cached_font(font_medium, 13)
                        f_tag_lbl = get_cached_font(font_semibold, 11)
                        is_url = link_val.startswith("http")
                        tag_lbl = "URL" if is_url else "FILE"
                        tag_w = 42
                        bar_x = bx + 18
                        bar_y = by + 116
                        bar_w = col_w - 36
                        bar_h = 32

                        draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=6, fill=(255, 255, 255, 255), outline=c_bd, width=1)
                        draw.rounded_rectangle((bar_x + 1, bar_y + 1, bar_x + tag_w, bar_y + bar_h - 1), radius=5, fill=b_col)

                        tl_bbox = draw.textbbox((0, 0), tag_lbl, font=f_tag_lbl)
                        tl_w = tl_bbox[2] - tl_bbox[0]
                        tl_h = tl_bbox[3] - tl_bbox[1]
                        tl_x = bar_x + 1 + (tag_w - 1 - tl_w) // 2
                        tl_y = bar_y + (bar_h - tl_h) // 2 - 1
                        draw.text((tl_x, tl_y), tag_lbl, font=f_tag_lbl, fill=(255, 255, 255, 255))

                        available_w = bar_w - tag_w - 24
                        txt_bbox = draw.textbbox((0, 0), link_val, font=f_link_text)
                        if (txt_bbox[2] - txt_bbox[0]) > available_w:
                            f_link_text = get_cached_font(font_medium, 12)

                        draw.text((bar_x + tag_w + 12, bar_y + 7), link_val, font=f_link_text, fill=(30, 41, 59, 255))
                else:
                    d_lines = wrap_text(item.get("description", ""), f_pil_d, col_w - 36, draw)
                    for li, l in enumerate(d_lines[:3]):
                        draw.text((bx + 18, by + 58 + li * 24), l, font=f_pil_d, fill=(71, 85, 105, 255))

        # Bottom Tip Note
        bot_note = content.get("tip_note", "waCRM Tip: Maintaining documented customer opt-in protects your business sender reputation.")
        f_bot = get_cached_font(font_medium, 19)
        f_bot_bold = get_cached_font(font_semibold, 15)

        tip_badge_x = pad_x
        tip_badge_y = cy1 + 595 if num_items == 3 else (cy1 + 585 if num_cols == 2 else cy1 + 575)
        tip_badge_w = 46
        tip_badge_h = 26
        draw.rounded_rectangle((tip_badge_x, tip_badge_y, tip_badge_x + tip_badge_w, tip_badge_y + tip_badge_h), radius=6, fill=accent_rgb)
        draw.text((tip_badge_x + 9, tip_badge_y + 4), "TIP", font=f_bot_bold, fill=(255, 255, 255, 255))
        draw.text((tip_badge_x + tip_badge_w + 14, tip_badge_y + 3), bot_note, font=f_bot, fill=(51, 65, 85, 255))

    elif table:
        # Tabular Comparison Slide (e.g. Slide 5.3)
        sub_text = content.get("subheading", "Meta conversation pricing varies by category. Illustrative baseline rates for planning:")
        draw.text((pad_x, cy1 + 96), sub_text, font=f_sub, fill=COLOR_GRAY_TEXT)

        # 1. Rate Benchmark Cards
        rate_cards = content.get("rate_cards", [])
        if rate_cards:
            rc_y = cy1 + 136
            rc_h = 66
            gap_rc = 25
            w_rc = (1580 - (len(rate_cards) - 1) * gap_rc) // len(rate_cards)
            f_card_t = get_cached_font(font_semibold, 20)
            f_card_r = get_cached_font(font_medium, 20)
            f_card_b = get_cached_font(font_semibold, 14)

            palette = {
                "orange": (COLOR_ORANGE, (255, 246, 243, 255), (255, 218, 208, 255)),
                "blue": (COLOR_BLUE, (243, 248, 255, 255), (205, 224, 248, 255)),
                "green": (COLOR_GREEN, (238, 250, 243, 255), (195, 235, 212, 255))
            }

            for i, rc in enumerate(rate_cards):
                rx = pad_x + i * (w_rc + gap_rc)
                c_key = rc.get("color", "blue")
                p_col, p_bg, p_bd = palette.get(c_key, palette["blue"])

                draw.rounded_rectangle((rx, rc_y, rx + w_rc, rc_y + rc_h), radius=10, fill=p_bg, outline=p_bd, width=1)
                draw.text((rx + 20, rc_y + 20), rc.get("title", ""), font=f_card_t, fill=COLOR_GRAY_DARK)
                draw.text((rx + 175, rc_y + 20), rc.get("rate", ""), font=f_card_r, fill=p_col)

                tag = rc.get("badge", "")
                if tag:
                    tb_bbox = draw.textbbox((0, 0), tag, font=f_card_b)
                    tb_w = tb_bbox[2] - tb_bbox[0] + 18
                    tb_x = rx + w_rc - tb_w - 18
                    tb_y = rc_y + 19
                    draw.rounded_rectangle((tb_x, tb_y, tb_x + tb_w, tb_y + 28), radius=6, fill=p_col)
                    draw.text((tb_x + 9, tb_y + 5), tag, font=f_card_b, fill=(255, 255, 255, 255))

        # 2. Comparison Table
        tb_y = cy1 + 224
        th_h = 42
        col_w1 = 880
        col_w2 = 320
        col_w3 = 380

        rows = table.get("rows", [])
        table_total_h = th_h + len(rows) * 56
        draw.rounded_rectangle((pad_x, tb_y, pad_x + 1580, tb_y + table_total_h), radius=10, fill=(255, 255, 255, 255), outline=(218, 226, 236, 255), width=1)

        # Table Header
        draw.rounded_rectangle((pad_x, tb_y, pad_x + 1580, tb_y + th_h), radius=10, fill=(244, 247, 250, 255))
        draw.rectangle((pad_x, tb_y + th_h - 10, pad_x + 1580, tb_y + th_h), fill=(244, 247, 250, 255))
        draw.line([(pad_x, tb_y + th_h), (pad_x + 1580, tb_y + th_h)], fill=(218, 226, 236, 255), width=1)

        cols = table.get("columns", ["Action Scenario", "Category", "Approx. Charge per User"])
        f_th = get_cached_font(font_semibold, 18)
        f_td = get_cached_font(font_regular, 18)
        f_td_b = get_cached_font(font_medium, 18)
        f_pill = get_cached_font(font_semibold, 15)

        draw.text((pad_x + 25, tb_y + 11), cols[0], font=f_th, fill=(51, 65, 85, 255))
        draw.text((pad_x + col_w1 + 25, tb_y + 11), cols[1], font=f_th, fill=(51, 65, 85, 255))
        draw.text((pad_x + col_w1 + col_w2 + 25, tb_y + 11), cols[2], font=f_th, fill=(51, 65, 85, 255))

        cat_colors = {
            "orange": (COLOR_ORANGE, (255, 246, 243, 255)),
            "blue": (COLOR_BLUE, (243, 248, 255, 255)),
            "green": (COLOR_GREEN, (238, 250, 243, 255))
        }

        for ri, row in enumerate(rows):
            ry = tb_y + th_h + ri * 56
            row_bg = (255, 255, 255, 255) if ri % 2 == 0 else (249, 251, 253, 255)

            if ri == len(rows) - 1:
                draw.rounded_rectangle((pad_x + 1, ry, pad_x + 1579, ry + 55), radius=10, fill=row_bg)
                draw.rectangle((pad_x + 1, ry, pad_x + 1579, ry + 15), fill=row_bg)
            else:
                draw.rectangle((pad_x + 1, ry, pad_x + 1579, ry + 55), fill=row_bg)
                draw.line([(pad_x, ry + 56), (pad_x + 1580, ry + 56)], fill=(230, 236, 242, 255), width=1)

            # Col 1: Action
            draw.text((pad_x + 25, ry + 16), row.get("action", ""), font=f_td, fill=COLOR_GRAY_DARK)

            # Col 2: Category Pill
            cat_name = row.get("category", "")
            cat_ckey = row.get("category_color", "blue")
            cat_col, cat_bg = cat_colors.get(cat_ckey, cat_colors["blue"])

            pill_bbox = draw.textbbox((0, 0), cat_name, font=f_pill)
            pill_w = pill_bbox[2] - pill_bbox[0] + 24
            px = pad_x + col_w1 + 25
            py = ry + 12
            draw.rounded_rectangle((px, py, px + pill_w, py + 30), radius=6, fill=cat_bg, outline=cat_col, width=1)
            draw.text((px + 12, py + 6), cat_name, font=f_pill, fill=cat_col)

            # Col 3: Approx Charge
            draw.text((pad_x + col_w1 + col_w2 + 25, ry + 16), row.get("charge", ""), font=f_td_b, fill=(40, 55, 75, 255))

        for vx in [pad_x + col_w1, pad_x + col_w1 + col_w2]:
            draw.line([(vx, tb_y), (vx, tb_y + table_total_h)], fill=(225, 232, 240, 255), width=1)

        # Bottom Tip Note
        bot_note = content.get("tip_note", "One broadcast to 1,000 people ~ up to 1,000 billable conversations if each opens a new 24h window. Meta charges per window, not per waCRM message.")
        f_bot = get_cached_font(font_medium, 18)
        f_bot_bold = get_cached_font(font_semibold, 15)

        tip_badge_x = pad_x
        tip_badge_y = cy1 + 540
        tip_badge_w = 46
        tip_badge_h = 26
        draw.rounded_rectangle((tip_badge_x, tip_badge_y, tip_badge_x + tip_badge_w, tip_badge_y + tip_badge_h), radius=6, fill=accent_rgb)
        draw.text((tip_badge_x + 9, tip_badge_y + 4), "TIP", font=f_bot_bold, fill=(255, 255, 255, 255))
        draw.text((tip_badge_x + tip_badge_w + 14, tip_badge_y + 3), bot_note, font=f_bot, fill=(51, 65, 85, 255))

    # 5. Save output
    canvas.convert("RGB").save(output_path, "JPEG", quality=96, optimize=True)
    return output_path

def render_info_slide(content: Dict[str, Any], fonts_dir: str, output_path: str) -> str:
    """Main entry point for information slides: routes to board or flow template."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    style = content.get("style", "board" if (content.get("banner") or content.get("items") or content.get("table")) else "flow")
    if style == "board":
        return render_board_slide(content, fonts_dir, output_path)

    # Multi-card flow default (e.g. Slide 2.1)
    app_dir = os.path.dirname(fonts_dir)
    canvas = Image.new("RGBA", (1920, 1080), (254, 254, 254, 255))
    draw = ImageDraw.Draw(canvas)

    font_medium = os.path.join(fonts_dir, "Rubik-Medium.ttf")
    font_semibold = os.path.join(fonts_dir, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(fonts_dir, "Rubik-Regular.ttf")

    f_kicker = get_cached_font(font_semibold, 48)
    f_heading = get_cached_font(font_semibold, 78)
    f_card_num = get_cached_font(font_semibold, 40)
    f_card_title = get_cached_font(font_semibold, 26)
    f_card_body = get_cached_font(font_regular, 22)
    f_code = get_cached_font(font_medium, 16)

    kicker_text = content.get("kicker", "").strip()
    margin_left = 68
    kicker_y = 68
    if kicker_text:
        bar_x = margin_left
        bar_y = kicker_y + 4
        draw.rectangle((bar_x, bar_y, bar_x + 8, bar_y + 58), fill=COLOR_ORANGE)
        draw.text((bar_x + 22, kicker_y), kicker_text, font=f_kicker, fill=COLOR_ORANGE)
        heading_y = kicker_y + 88
    else:
        heading_y = kicker_y

    heading_text = content.get("heading", "").strip()
    draw.text((margin_left, heading_y), heading_text, font=f_heading, fill=COLOR_GREEN)

    cards: List[Dict[str, Any]] = content.get("cards", [])
    num_cards = max(1, len(cards))
    card_height = 412
    card_y = 397

    total_avail_w = 1920 - 2 * margin_left  # 1784
    if num_cards == 4:
        card_w = 380
        gap = 88
        card_spans = [(margin_left + i * (card_w + gap), margin_left + i * (card_w + gap) + card_w) for i in range(4)]
    elif num_cards > 1:
        gap = 72
        card_w = int((total_avail_w - (num_cards - 1) * gap) / num_cards)
        card_spans = [(margin_left + i * (card_w + gap), margin_left + i * (card_w + gap) + card_w) for i in range(num_cards)]
    else:
        card_spans = [(margin_left, margin_left + 600)]

    def get_flow_arrow_badge(size: int = 48) -> Image.Image:
        """Generates an ultra-crisp, antialiased vector arrow badge with zero distortion or artifacts."""
        scale = 4
        big_size = size * scale
        im = Image.new("RGBA", (big_size, big_size), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        
        pad = 3 * scale
        d.ellipse((pad, pad, big_size - pad, big_size - pad), fill=(235, 248, 241, 255), outline=(180, 226, 202, 255), width=int(2.2 * scale))
        
        cx = big_size // 2
        cy = big_size // 2
        arrow_color = COLOR_GREEN
        line_w = int(3.6 * scale)
        
        d.line([(cx - 10 * scale, cy), (cx + 8 * scale, cy)], fill=arrow_color, width=line_w)
        d.line([(cx + 1 * scale, cy - 7 * scale), (cx + 8 * scale, cy)], fill=arrow_color, width=line_w)
        d.line([(cx + 1 * scale, cy + 7 * scale), (cx + 8 * scale, cy)], fill=arrow_color, width=line_w)
        d.ellipse((cx + 8 * scale - line_w//2, cy - line_w//2, cx + 8 * scale + line_w//2, cy + line_w//2), fill=arrow_color)
        d.ellipse((cx + 1 * scale - line_w//2, cy - 7 * scale - line_w//2, cx + 1 * scale + line_w//2, cy - 7 * scale + line_w//2), fill=arrow_color)
        d.ellipse((cx + 1 * scale - line_w//2, cy + 7 * scale - line_w//2, cx + 1 * scale + line_w//2, cy + 7 * scale + line_w//2), fill=arrow_color)
        d.ellipse((cx - 10 * scale - line_w//2, cy - line_w//2, cx - 10 * scale + line_w//2, cy + line_w//2), fill=arrow_color)

        return im.resize((size, size), Image.Resampling.LANCZOS)

    arrow_img = get_flow_arrow_badge(48)

    from .pos_icons import get_matching_icon_for_card

    for idx, card in enumerate(cards):
        cx1, cx2 = card_spans[idx]
        cur_card_w = cx2 - cx1
        cy = card_y
        draw.rounded_rectangle((cx1 - 2, cy + 4, cx2 + 2, cy + card_height + 8), radius=22, fill=(236, 240, 244, 160))
        draw.rounded_rectangle((cx1, cy, cx2, cy + card_height), radius=20, fill=(255, 255, 255, 255), outline=COLOR_CARD_BORDER, width=2)

        step_num = card.get("step", f"{idx + 1:02d}")
        icon_img = get_matching_icon_for_card(card, default_step=idx + 1)
        canvas.paste(icon_img, (cx1 + 32, cy + 28), icon_img)

        num_bbox = draw.textbbox((0, 0), step_num, font=f_card_num)
        draw.text((cx2 - 34 - (num_bbox[2] - num_bbox[0]), cy + 34), step_num, font=f_card_num, fill=COLOR_STEP_NUM)

        title_lines = wrap_text(card.get("title", ""), f_card_title, cur_card_w - 64, draw)
        cur_y = cy + 165
        for t_line in title_lines:
            draw.text((cx1 + 32, cur_y), t_line, font=f_card_title, fill=COLOR_GRAY_DARK)
            cur_y += 34

        desc_lines = wrap_text(card.get("description", ""), f_card_body, cur_card_w - 64, draw)
        cur_y += 12
        for d_line in desc_lines:
            draw.text((cx1 + 32, cur_y), d_line, font=f_card_body, fill=COLOR_GRAY_TEXT)
            cur_y += 30

        pill_text = card.get("code_pill", "")
        if pill_text:
            cur_y += 14
            pill_w = min(cur_card_w - 64, draw.textbbox((0, 0), pill_text, font=f_code)[2] - draw.textbbox((0, 0), pill_text, font=f_code)[0] + 24)
            draw.rounded_rectangle((cx1 + 32, cur_y, cx1 + 32 + pill_w, cur_y + 40), radius=8, fill=(235, 248, 241, 255))
            draw.text((cx1 + 44, cur_y + 10), pill_text, font=f_code, fill=(0, 118, 46, 255))

        if idx < num_cards - 1 and arrow_img:
            next_cx1 = card_spans[idx + 1][0]
            arrow_x = cx2 + (next_cx1 - cx2 - arrow_img.width) // 2
            arrow_y = cy + (card_height - arrow_img.height) // 2
            canvas.paste(arrow_img, (arrow_x, arrow_y), arrow_img)

    canvas.convert("RGB").save(output_path, "JPEG", quality=95, optimize=True)
    return output_path
