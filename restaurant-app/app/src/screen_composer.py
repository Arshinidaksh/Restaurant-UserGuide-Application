"""
Screen Composer: fits screenshots into hardware frames (e.g. PC-Screen.png).
Fully in-memory execution using cached frames and fast Lanczos resampling.
"""
from typing import Union
from PIL import Image
from .config import (
    PC_SCREEN_X,
    PC_SCREEN_Y,
    PC_SCREEN_WIDTH,
    PC_SCREEN_HEIGHT
)
from .cache import get_cached_image

def compose_pc_screen(
    screen_source: Union[str, Image.Image],
    pc_frame_path: str,
    crop_top_only: bool = True,
    crop_align: str = "left"
) -> Image.Image:
    """
    Fits a software screenshot into the screen area of PC-Screen.png in-memory.
    crop_align='left' preserves the left navigation sidebar when width exceeds target aspect ratio.
    Returns the composited RGBA PIL Image.
    """
    frame = get_cached_image(pc_frame_path, mode="RGBA").copy()

    if isinstance(screen_source, str):
        screen = Image.open(screen_source).convert("RGBA")
    else:
        screen = screen_source.convert("RGBA") if screen_source.mode != "RGBA" else screen_source

    target_w = PC_SCREEN_WIDTH
    target_h = PC_SCREEN_HEIGHT
    target_aspect = target_w / target_h

    screen_w, screen_h = screen.size
    screen_aspect = screen_w / screen_h

    if crop_top_only:
        if screen_aspect < target_aspect:
            crop_h = int(screen_w / target_aspect)
            cropped_screen = screen.crop((0, 0, screen_w, min(screen_h, crop_h)))
        else:
            crop_w = int(screen_h * target_aspect)
            if crop_align == "left":
                left_crop = 0
            elif crop_align == "right":
                left_crop = screen_w - crop_w
            else:
                left_crop = (screen_w - crop_w) // 2
            cropped_screen = screen.crop((left_crop, 0, left_crop + crop_w, screen_h))
    else:
        cropped_screen = screen

    # High-quality Lanczos resampling to display bounds
    fitted_screen = cropped_screen.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Paste into the frame
    frame.paste(fitted_screen, (PC_SCREEN_X, PC_SCREEN_Y))
    return frame
