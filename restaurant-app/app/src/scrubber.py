"""
Screen Scrubber: Programmatically censors and replaces sensitive API keys, 
tokens, emails, and usernames in UI screenshots with clean dummy placeholders.
Fully in-memory execution with auto background color sampling and fast UI font matching.
"""
import os
import hashlib
from typing import Optional, Dict, Any, List, Union
from PIL import Image, ImageDraw, ImageFont

from .cache import get_cached_font

# Default UI fonts to attempt (Windows system fonts -> local fonts)
SYSTEM_FONT_PATHS = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "Rubik-Regular.ttf")
]

def get_ui_font(size: int) -> ImageFont.FreeTypeFont:
    for path in SYSTEM_FONT_PATHS:
        if os.path.exists(path):
            try:
                return get_cached_font(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def auto_sample_background(img: Image.Image, bbox: List[int]) -> tuple:
    """Samples the background color immediately outside the bbox boundary using Pillow."""
    x1, y1, x2, y2 = bbox
    w, h = img.size
    samples = []
    if y1 > 2:
        samples.append(img.getpixel(((x1 + x2) // 2, y1 - 2)))
    if x1 > 2:
        samples.append(img.getpixel((x1 - 2, (y1 + y2) // 2)))
    if x2 < w - 2:
        samples.append(img.getpixel((x2 + 2, (y1 + y2) // 2)))
    if len(samples) > 0:
        r = sum(s[0] for s in samples) // len(samples)
        g = sum(s[1] for s in samples) // len(samples)
        b = sum(s[2] for s in samples) // len(samples)
        return (r, g, b)
    return (245, 247, 250)

def scrub_image(img: Image.Image, rules: List[Dict[str, Any]]) -> Image.Image:
    """
    Applies dynamic scrubbing rules directly to a PIL Image in memory.
    Features:
    - Auto background color detection if fill is omitted or 'auto'
    - Auto text positioning if text_pos is omitted
    - Clean typography matching UI
    """
    if not rules:
        return img

    scrubbed = img.copy()
    draw = ImageDraw.Draw(scrubbed)

    for rule in rules:
        bbox = rule.get("bbox")
        if not bbox or len(bbox) < 4:
            continue

        fill = rule.get("fill")
        if fill is None or fill == "auto":
            fill = auto_sample_background(scrubbed, bbox)
        elif isinstance(fill, list):
            fill = tuple(fill)

        text = rule.get("text", "")
        font_size = rule.get("font_size", 14)
        text_color = rule.get("text_color", (107, 114, 128))
        if isinstance(text_color, list):
            text_color = tuple(text_color)

        text_pos = rule.get("text_pos")
        if not text_pos:
            box_h = bbox[3] - bbox[1]
            y_offset = max(1, (box_h - font_size) // 2)
            text_pos = (bbox[0] + 4, bbox[1] + y_offset - 1)
        elif isinstance(text_pos, list):
            text_pos = tuple(text_pos)

        # 1. Fill over the target region
        draw.rectangle(bbox, fill=fill)

        # 2. Draw dummy placeholder text
        if text:
            font = get_ui_font(font_size)
            draw.text(text_pos, text, font=font, fill=text_color)

    return scrubbed

def scrub_screenshot(
    input_source: Union[str, Image.Image],
    rules: Optional[List[Dict[str, Any]]] = None
) -> Image.Image:
    """
    Scrubs sensitive credentials in memory without disk writes.
    """
    rules = rules or []
    if isinstance(input_source, str):
        img = Image.open(input_source).convert("RGB")
    else:
        img = input_source

    return scrub_image(img, rules)
