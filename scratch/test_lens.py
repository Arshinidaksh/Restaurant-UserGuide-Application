import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "app")
FONTS_DIR = os.path.join(APP_DIR, "fonts")
SCREENS_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app", "project", "screens")

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from src.cache import get_cached_font

def build_magnifier_lens(
    screen_path: str,
    focus_x: int, # in original screen coordinates
    focus_y: int,
    lens_diameter: int = 170,
    zoom_factor: float = 2.2,
    border_color = (255, 92, 53, 255), # Brand orange
    border_width: int = 4
):
    """
    Creates a circular magnifier loupe zoomed in on (focus_x, focus_y).
    Includes a crisp circular border, glass rim effect, and drop shadow.
    """
    screen = Image.open(screen_path).convert("RGBA")
    sw, sh = screen.size
    
    # Calculate crop area on original screen
    crop_size = int(lens_diameter / zoom_factor)
    x1 = max(0, focus_x - crop_size // 2)
    y1 = max(0, focus_y - crop_size // 2)
    x2 = min(sw, x1 + crop_size)
    y2 = min(sh, y1 + crop_size)
    
    cropped = screen.crop((x1, y1, x2, y2))
    zoomed = cropped.resize((lens_diameter, lens_diameter), Image.Resampling.LANCZOS)
    
    # Create circular mask with antialiasing
    scale = 4
    mask = Image.new("L", (lens_diameter * scale, lens_diameter * scale), 0)
    d_mask = ImageDraw.Draw(mask)
    d_mask.ellipse((0, 0, lens_diameter * scale - 1, lens_diameter * scale - 1), fill=255)
    mask = mask.resize((lens_diameter, lens_diameter), Image.Resampling.LANCZOS)
    
    # Circular zoomed image
    circular_lens = Image.new("RGBA", (lens_diameter, lens_diameter), (0, 0, 0, 0))
    circular_lens.paste(zoomed, (0, 0), mask)
    
    # Draw double-ring bezel: Outer brand color, inner white highlight
    bezel = Image.new("RGBA", (lens_diameter * scale, lens_diameter * scale), (0, 0, 0, 0))
    d_bezel = ImageDraw.Draw(bezel)
    bw = border_width * scale
    # Outer ring (Brand orange/blue)
    d_bezel.ellipse((0, 0, lens_diameter * scale - 1, lens_diameter * scale - 1), outline=border_color, width=bw)
    # Inner white separator ring
    d_bezel.ellipse((bw, bw, lens_diameter * scale - 1 - bw, lens_diameter * scale - 1 - bw), outline=(255, 255, 255, 240), width=scale * 2)
    bezel = bezel.resize((lens_diameter, lens_diameter), Image.Resampling.LANCZOS)
    
    circular_lens.paste(bezel, (0, 0), bezel)
    
    # Create soft drop shadow
    pad = 20
    total_size = lens_diameter + pad * 2
    shadow_canvas = Image.new("RGBA", (total_size, total_size), (0, 0, 0, 0))
    d_shadow = ImageDraw.Draw(shadow_canvas)
    # shadow ellipse slightly offset downwards
    d_shadow.ellipse((pad + 2, pad + 6, pad + lens_diameter - 2, pad + lens_diameter + 4), fill=(0, 0, 0, 70))
    shadow_blurred = shadow_canvas.filter(ImageFilter.GaussianBlur(8))
    
    # Paste lens over shadow
    shadow_blurred.paste(circular_lens, (pad, pad), circular_lens)
    
    return shadow_blurred, pad

# Test generating magnifier
lens_img, pad = build_magnifier_lens(
    os.path.join(SCREENS_DIR, "03_main_dashboard.jpg"),
    focus_x=1740,
    focus_y=30,
    lens_diameter=160,
    zoom_factor=2.0
)
lens_img.save("scratch/test_lens.png")
print("Saved scratch/test_lens.png")
