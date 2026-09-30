# Slide Design System & Standards for Agents

This document defines the strict graphical, typographic, and architectural rules for generating presentation slides across all user guide modules. Any agent creating slides must follow these constraints.

---

## 1. Golden Constraint: Clean Screenshots (No Annotations)
- **NO Highlights or Bounding Boxes**: Do NOT draw red, orange, or colored rectangular boxes on top of application screenshots.
- **NO Arrows or Pins on Screens**: Screenshots embedded into the PC monitor frame must be 100% authentic, unmodified application screens.
- **No Transient UI Artifacts**: Ensure toast messages, error banners, or temporary loading spinners have faded before taking the screenshot (wait at least 3-4 seconds after actions).

---

## 2. Dimensions & Canvas
- **Resolution**: 1920 x 1080 pixels (Full HD, 16:9).
- **Base Background**: `restaurant-app/Libraries/complete-design-format/Only-background-transparent.png`.
- **PC Monitor Frame**: `restaurant-app/Libraries/Parts/PC-Screen.png`.
- **Positioning**:
  - `PC_POS_X = 60`, `PC_POS_Y = 175`
  - Screen dimensions inside bezel: `1008 x 567` (or full aspect ratio center-aligned).
  - Use `src.screen_composer.compose_pc_screen(screen_img, pc_frame_path, crop_top_only=False, crop_align="center")`.

---

## 3. Typography & Color Palette
- **Fonts** (located in `restaurant-app/app/fonts/`):
  - Kicker: `Rubik-SemiBold.ttf` (size 20pt)
  - Heading: `Rubik-SemiBold.ttf` (size 38-40pt)
  - Where/Subhead: `Rubik-Regular.ttf` (size 20pt)
  - Step Body: `Rubik-Regular.ttf` (size 19pt)
  - Notes: `Rubik-Regular.ttf` (size 18pt)
- **Palette**:
  - Primary Brand Blue: `#1271D0` / `RGB(18, 113, 208)` (Used for Kicker, number badges, tip notes).
  - Headings / Dark Text: `#232323` / `RGB(35, 35, 35)`.
  - Secondary Gray: `#58585A` / `RGB(88, 88, 90)` (Used for "Where" location subtext).
- **Glyph Compatibility**:
  - Rubik font does NOT contain Unicode arrows (`→`, `←`). Always replace them with `>` or `<` to prevent broken square glyph boxes (``).

---

## 4. Text Column & Step Numbering
- `TEXT_COL_X = 1148`
- `KICKER_Y = 210`
- `HEADING_Y = 252`
- `MAX_TEXT_WIDTH_PX = 680`
- **Step Badges**:
  - Circular badge diameter: 28px
  - Background: `#1271D0`
  - Text: White bold number, centered with 4x anti-aliasing downsampling.
  - Spacing between badge and text: 16px.
  - Line gap between steps: 34-40px depending on step count.

---

## 5. Output Destinations
All rendered slides must be saved simultaneously to:
1. `Slides/<Part Name>/<Step Filename>.jpg`
2. `export/<Part Name>/<Step Filename>.jpg`
JPEG format, quality 96, optimized.
