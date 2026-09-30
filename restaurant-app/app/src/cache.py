"""
High-Performance In-Memory Cache Utilities for waCRM Slide Generation.
Eliminates redundant disk I/O and expensive resampling by caching:
1. Pre-warmed base 1920x1080 canvas (white background + transparent brand overlay).
2. Hardware monitor frames (PC-Screen.png).
3. Pre-scaled RGBA checkmark icons.
4. Pre-parsed TrueType font instances across multiple sizes.
5. In-memory raw screenshots.
"""
import os
import hashlib
from functools import lru_cache
from typing import Tuple, Optional
from PIL import Image, ImageFont

@lru_cache(maxsize=64)
def get_cached_font(font_path: str, size: int) -> ImageFont.FreeTypeFont:
    """Caches parsed TrueType font instances in memory."""
    return ImageFont.truetype(font_path, size)

@lru_cache(maxsize=16)
def get_cached_image(image_path: str, mode: str = "RGBA") -> Image.Image:
    """Caches static assets (frames, backgrounds, icons) in memory."""
    img = Image.open(image_path)
    if mode and img.mode != mode:
        img = img.convert(mode)
    return img

@lru_cache(maxsize=16)
def get_cached_icon(icon_path: str, size: Tuple[int, int]) -> Image.Image:
    """Caches pre-resized icons to avoid repeated Lanczos downsampling."""
    base_img = get_cached_image(icon_path, mode="RGBA")
    return base_img.resize(size, Image.Resampling.LANCZOS)

@lru_cache(maxsize=2)
def get_cached_base_background(bg_trans_path: str) -> Image.Image:
    """
    Creates and caches the 1920x1080 white background with the transparent design overlay.
    Pre-composited once in RAM to eliminate per-slide compositing overhead.
    """
    canvas = Image.new("RGBA", (1920, 1080), (255, 255, 255, 255))
    overlay = Image.open(bg_trans_path).convert("RGBA")
    if overlay.size != (1920, 1080):
        overlay = overlay.resize((1920, 1080), Image.Resampling.LANCZOS)
    canvas.paste(overlay, (0, 0), overlay)
    return canvas

def is_cache_valid(source_path: str, cached_path: str) -> bool:
    """Checks if a cached target file is up-to-date relative to its source."""
    if not os.path.exists(cached_path) or not os.path.exists(source_path):
        return False
    return os.path.getmtime(cached_path) >= os.path.getmtime(source_path)
