"""
Configuration constants for Isarva Restaurant POS Slide Generator.
Brand Guidelines based on Libraries/Fonts.md and complete-design-format.
Pure JPEG 1920x1080 Full HD Slide Generation (Zero PPTX dependency).
"""

# Product Metadata
PRODUCT_NAME = "Isarva Restaurant POS"
PRODUCT_URL = "https://app.restaurant-pos.isarva.in"
DOCUMENT_ID = "ISARVA-CG-001"
DOCUMENT_VERSION = "1.2"
ORGANISATION = "Isarva"

# Slide Dimensions (16:9 Full HD standard)
SLIDE_WIDTH_PX = 1920
SLIDE_HEIGHT_PX = 1080

# Brand Hex Colors
HEX_GREEN = "038e41"
HEX_BLUE = "1271d0"
HEX_GREEN_HOME = "039645"
HEX_ORANGE = "ff5c35"
HEX_GRAY = "58585a"

# RGB Colors (Tuples for Pillow rendering)
COLOR_BLUE = (18, 113, 208)    # #1271D0
COLOR_GRAY = (88, 88, 90)      # #58585A
COLOR_GREEN = (3, 142, 65)     # #038E41
COLOR_ORANGE = (255, 92, 53)   # #FF5C35

# Typography
FONT_FAMILY = "Rubik"

# Layout Coordinates (in 1920x1080 pixels)
# Left Monitor Placement
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
BULLETS_START_Y = 460
BULLET_SPACING_Y = 48
CHECK_ICON_SIZE = 28
ENDING_Y = 725
MAX_TEXT_WIDTH_PX = 660
