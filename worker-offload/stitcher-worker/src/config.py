"""
Configuration and Layout Tokens for Slide Composition & Stitching
"""
import os

ASSETS_DIR = os.environ.get("ASSETS_DIR", os.path.join(os.path.dirname(__file__), "..", "assets"))
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Canvas Dimensions
SLIDE_WIDTH_PX = 1920
SLIDE_HEIGHT_PX = 1080

# Brand Colors (Tuples for Pillow RGBA rendering)
COLOR_BLUE = (18, 113, 208, 255)    # #1271D0
COLOR_GRAY = (88, 88, 90, 255)      # #58585A
COLOR_DARK = (35, 35, 35, 255)      # #232323
COLOR_WHITE = (255, 255, 255, 255)

# PC Hardware Mockup Placement
PC_POS_X = 63
PC_POS_Y = 180
PC_WIDTH = 1068
PC_HEIGHT = 790

# Screen area inside PC-Screen.png
PC_SCREEN_X = 31
PC_SCREEN_Y = 27
PC_SCREEN_WIDTH = 971
PC_SCREEN_HEIGHT = 505

# Right Column Text Coordinates
TEXT_COL_X = 1148
KICKER_Y = 225
HEADING_Y = 265
BODY_Y = 365
MAX_TEXT_WIDTH_PX = 660

# Asset filepaths
PC_FRAME_PATH = os.path.join(ASSETS_DIR, "PC-Screen.png")
BG_CANVAS_PATH = os.path.join(ASSETS_DIR, "Only-background-transparent.png")
FONT_REGULAR_PATH = os.path.join(FONTS_DIR, "Rubik-Regular.ttf")
FONT_SEMIBOLD_PATH = os.path.join(FONTS_DIR, "Rubik-SemiBold.ttf")
FONT_BOLD_PATH = os.path.join(FONTS_DIR, "Rubik-Bold.ttf")
