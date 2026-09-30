import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
RESTAURANT_APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app")
FONTS_DIR = os.path.join(APP_DIR, "fonts")
SCREENS_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "project", "screens")

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

def create_number_badge(num: int, size: int = 34, bg_color = (18, 113, 208, 255), fg_color = (255, 255, 255, 255)):
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

def build_magnifier_lens(
    screen_path: str,
    focus_x: int = 1740,
    focus_y: int = 30,
    lens_diameter: int = 180,
    zoom_factor: float = 2.0,
    border_color = (255, 92, 53, 255),
    border_width: int = 5
):
    screen = Image.open(screen_path).convert("RGBA")
    sw, sh = screen.size
    
    crop_size = int(lens_diameter / zoom_factor)
    x1 = max(0, focus_x - crop_size // 2)
    y1 = max(0, focus_y - crop_size // 2)
    x2 = min(sw, x1 + crop_size)
    y2 = min(sh, y1 + crop_size)
    
    cropped = screen.crop((x1, y1, x2, y2))
    zoomed = cropped.resize((lens_diameter, lens_diameter), Image.Resampling.LANCZOS)
    
    scale = 4
    mask = Image.new("L", (lens_diameter * scale, lens_diameter * scale), 0)
    d_mask = ImageDraw.Draw(mask)
    d_mask.ellipse((0, 0, lens_diameter * scale - 1, lens_diameter * scale - 1), fill=255)
    mask = mask.resize((lens_diameter, lens_diameter), Image.Resampling.LANCZOS)
    
    circular_lens = Image.new("RGBA", (lens_diameter, lens_diameter), (0, 0, 0, 0))
    circular_lens.paste(zoomed, (0, 0), mask)
    
    # Outer crisp ring
    bezel = Image.new("RGBA", (lens_diameter * scale, lens_diameter * scale), (0, 0, 0, 0))
    d_bezel = ImageDraw.Draw(bezel)
    bw = border_width * scale
    # Orange outer ring
    d_bezel.ellipse((0, 0, lens_diameter * scale - 1, lens_diameter * scale - 1), outline=border_color, width=bw)
    # White inner separator ring
    d_bezel.ellipse((bw, bw, lens_diameter * scale - 1 - bw, lens_diameter * scale - 1 - bw), outline=(255, 255, 255, 240), width=scale * 2)
    bezel = bezel.resize((lens_diameter, lens_diameter), Image.Resampling.LANCZOS)
    circular_lens.paste(bezel, (0, 0), bezel)
    
    # Soft drop shadow
    pad = 24
    total_size = lens_diameter + pad * 2
    shadow_canvas = Image.new("RGBA", (total_size, total_size), (0, 0, 0, 0))
    d_shadow = ImageDraw.Draw(shadow_canvas)
    d_shadow.ellipse((pad + 2, pad + 8, pad + lens_diameter - 2, pad + lens_diameter + 6), fill=(0, 0, 0, 90))
    shadow_blurred = shadow_canvas.filter(ImageFilter.GaussianBlur(10))
    shadow_blurred.paste(circular_lens, (pad, pad), circular_lens)
    
    return shadow_blurred, pad

def render_step4_with_magnifier(output_path: str):
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")
    screen_path = os.path.join(SCREENS_DIR, "03_main_dashboard.jpg")

    canvas = get_cached_base_background(bg_trans_path).copy()
    
    # 1. Compose PC monitor mockup with the dashboard screen
    screen_img = Image.open(screen_path).convert("RGBA")
    mockup_img = compose_pc_screen(
        screen_img,
        pc_frame_path,
        crop_top_only=True,
        crop_align="left"
    )
    canvas.paste(mockup_img, (PC_POS_X, PC_POS_Y), mockup_img)

    # 2. Add Magnifier & Button Highlight Circle
    # Coordinates of button on canvas:
    # center is around (973, 222), size is approx 46x24
    btn_cx = 973
    btn_cy = 222
    
    # Magnifier position: refined diameter 160px, zoom 2.3x
    lens_dia = 160
    lens_img, pad = build_magnifier_lens(
        screen_path,
        focus_x=1740,
        focus_y=30,
        lens_diameter=lens_dia,
        zoom_factor=2.3,
        border_color=(255, 92, 53, 255), # Brand Orange
        border_width=4
    )
    
    # Center lens at (870, 355)
    lens_cx = 870
    lens_cy = 355
    lens_x = lens_cx - lens_dia // 2 - pad
    lens_y = lens_cy - lens_dia // 2 - pad
    
    # Draw callout pointer / leader line from button to lens
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d_over = ImageDraw.Draw(overlay)
    
    c_orange = (255, 92, 53, 255) # Brand Orange
    
    # 1. Antialiased highlight ring around button on screen
    scale = 4
    ring_w = 60 * scale
    ring_h = 34 * scale
    ring_im = Image.new("RGBA", (ring_w, ring_h), (0, 0, 0, 0))
    d_ring = ImageDraw.Draw(ring_im)
    # Outer orange ring
    d_ring.ellipse((2 * scale, 2 * scale, ring_w - 2 * scale - 1, ring_h - 2 * scale - 1), outline=c_orange, width=3 * scale)
    # Inner subtle glow
    d_ring.ellipse((0, 0, ring_w - 1, ring_h - 1), outline=(255, 92, 53, 100), width=2 * scale)
    ring_fitted = ring_im.resize((60, 34), Image.Resampling.LANCZOS)
    overlay.paste(ring_fitted, (btn_cx - 30, btn_cy - 17), ring_fitted)
    
    # 2. Sleek connector line from button highlight to magnifier lens
    pt_start = (btn_cx - 10, btn_cy + 17)
    pt_end = (lens_cx + 35, lens_cy - int(lens_dia * 0.44))
    
    d_over.line([pt_start, pt_end], fill=(255, 92, 53, 230), width=3)
    # Small dot at button end
    d_over.ellipse((pt_start[0] - 3, pt_start[1] - 3, pt_start[0] + 3, pt_start[1] + 3), fill=c_orange)
    
    # Composite overlay and lens onto canvas
    canvas.paste(overlay, (0, 0), overlay)
    canvas.paste(lens_img, (lens_x, lens_y), lens_img)

    # 3. Typography
    draw = ImageDraw.Draw(canvas)
    c_blue = (18, 113, 208, 255)  # #1271D0
    c_gray = (88, 88, 90, 255)    # #58585A
    c_green = (3, 142, 65, 255)

    font_medium = os.path.join(FONTS_DIR, "Rubik-Medium.ttf")
    font_semibold = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
    font_regular = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")

    # Kicker
    kicker = "PART B — FIRST-TIME SETUP (DO THIS ONLY ONCE PER TILL)"
    f_kicker = get_cached_font(font_medium, 22)
    draw.text((TEXT_COL_X, KICKER_Y + 5), kicker, font=f_kicker, fill=c_blue)

    # Heading
    heading = "Step 4 — Choose language (optional)"
    f_heading = get_cached_font(font_semibold, 44)
    h_lines = wrap_text(heading, f_heading, MAX_TEXT_WIDTH_PX, draw)
    cur_y = HEADING_Y + 8
    for hl in h_lines:
        draw.text((TEXT_COL_X, cur_y), hl, font=f_heading, fill=c_gray)
        cur_y += 52

    # Body
    body = "The POS interface provides seamless bilingual support for English and Arabic."
    f_body = get_cached_font(font_regular, 24)
    body_lines = wrap_text(body, f_body, MAX_TEXT_WIDTH_PX, draw)
    cur_y += 10
    for bl in body_lines:
        draw.text((TEXT_COL_X, cur_y), bl, font=f_body, fill=c_gray)
        cur_y += 34

    # Steps
    steps = [
        "Use the language switch (EN / AR) if you need Arabic.",
        "You can change language anytime later."
    ]
    badge_size = 34
    f_step = get_cached_font(font_regular, 24)
    cur_y = max(cur_y + 40, 480)

    for i, text in enumerate(steps, start=1):
        badge = create_number_badge(i, size=badge_size, bg_color=c_blue)
        canvas.paste(badge, (TEXT_COL_X, cur_y), badge)
        lines = wrap_text(text, f_step, MAX_TEXT_WIDTH_PX - badge_size - 18, draw)
        for j, line in enumerate(lines):
            draw.text((TEXT_COL_X + badge_size + 18, cur_y + 3 + j * 34), line, font=f_step, fill=c_gray)
        cur_y += max(68, len(lines) * 34 + 26)

    # Feature box
    box_y = cur_y + 15
    box_w = MAX_TEXT_WIDTH_PX
    box_h = 100
    info_box = Image.new("RGBA", (box_w, box_h), (242, 248, 244, 255))
    d_box = ImageDraw.Draw(info_box)
    d_box.rectangle((0, 0, 4, box_h), fill=c_green)
    f_box_title = get_cached_font(font_semibold, 18)
    f_box_desc = get_cached_font(font_regular, 17)
    d_box.text((20, 16), "BILINGUAL INTERFACE & RTL SUPPORT", font=f_box_title, fill=c_green)
    d_box.text((20, 44), "Switching to Arabic immediately mirrors layout to Right-to-Left (RTL).", font=f_box_desc, fill=c_gray)
    d_box.text((20, 68), "Receipts and kitchen orders will print according to template rules.", font=f_box_desc, fill=c_gray)
    canvas.paste(info_box, (TEXT_COL_X, box_y))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.convert("RGB").save(output_path, "JPEG", quality=96, optimize=True)
    print(f"Generated: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(WORKSPACE_DIR, "Slides", "Part B", "Step 4 - Choose language (optional).jpg")
    render_step4_with_magnifier(out_file)
    # Also mirror to export/Part B/
    out_file2 = os.path.join(WORKSPACE_DIR, "export", "Part B", "Step 4 - Choose language (optional).jpg")
    render_step4_with_magnifier(out_file2)
