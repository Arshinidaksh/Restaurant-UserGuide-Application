# LLM Developer Guide: Isarva Restaurant POS Slide & Search Engine

This document is a deterministic operational guide for LLM agents working in this repository. Follow this guide strictly to generate high-quality, brand-aligned 1920x1080 slide images and to retrieve sub-millisecond knowledge for **Isarva Restaurant POS** (`ISARVA-CG-001` v1.2).

---

## 1. Core Directives & Output Rules

1. **Output Format:** Slide outputs MUST ALWAYS be **1920x1080 Full HD `.jpg` images** located in `output/` (e.g. `output/POS-1.0-isarva-restaurant-pos.jpg`). Do NOT generate `.pptx` files unless explicitly requested by the user.
2. **Execution Method:** Always use the local Python virtual environment:
   ```powershell
   & ".\app\.venv\Scripts\python.exe" app\main.py --slide <slide_id>
   ```
3. **AI Fast Knowledge Search:** Before synthesizing procedures, query the fast AI index:
   ```powershell
   & ".\app\.venv\Scripts\python.exe" app\search.py "<query>"
   ```
4. **Scrubbing Policy (Default: DO NOT SCRUB):** By default, keep all screenshot UI text and numbers intact (`"scrub_rules": []`). Only scrub when explicitly instructed by the user.
5. **Boundary Constraint:** The right-hand column content MUST NEVER overflow past the bottom curve of the background circle. Keep bullet points to **exactly 5 single-line items**.

---

## 2. File & Directory Layout

```
restaurant-app/
├── app/
│   ├── .venv/                         <-- Python 3.12 virtual environment
│   ├── content/
│   │   ├── slides_data.json           <-- Combined slide database
│   │   ├── pos_slides_data.json       <-- Dedicated POS slide definitions
│   │   ├── pos_chunks.jsonl           <-- Line-by-line semantic chunks for vector DBs
│   │   └── pos_knowledge_index.json   <-- Compiled BM25 inverted index & metadata
│   ├── fonts/                         <-- Local Google Rubik TTF font files
│   ├── src/
│   │   ├── config.py                  <-- Coordinate constants, DPI, dimensions, brand colors
│   │   ├── cache.py                   <-- In-memory LRU caching (fonts, base canvas, frames)
│   │   ├── pos_data_builder.py        <-- Master POS knowledge extractor & chunk definitions
│   │   ├── ai_indexer.py              <-- Inverted index compiler & Lucene BM25 calculation
│   │   ├── search_engine.py           <-- 0.085ms BM25 ranking, role filter & AI prompt builder
│   │   ├── info_renderer.py           <-- 1920x1080 Information Board & Flow Card renderer
│   │   ├── screen_composer.py         <-- In-memory PC frame viewport fitting & resampler
│   │   └── preview_renderer.py        <-- 1920x1080 canvas screenshot slide renderer
│   ├── brand_check_icon.png           <-- 26x26 RGBA brand checkmark icon
│   ├── main.py                        <-- CLI slide runner (--slide <id> | --all | --list)
│   └── search.py                      <-- CLI AI query tool (--role, --troubleshoot, --ai-context)
├── project/
│   ├── screens/                       <-- UI software screenshots (.jpg)
│   └── userguide/
│       └── isarva-pos-userguide.pdf   <-- Official ISARVA-CG-001 Customer User Guide v1.2
├── output/                            <-- Final generated 1920x1080 JPG slide images
├── Libraries/                         <-- Master PSD/PNG templates & PC-Screen.png
├── CLI.md                             <-- Step-by-step CLI usage guide
├── CONTEXT.md                         <-- System architecture & slide registry
└── GUIDE_TO_LLMS.md                   <-- This guide
```

---

## 3. Brand Design Guidelines & Geometry

| Element | Position / Size | Font & Weight | Size | Color | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Canvas** | `1920 x 1080` | — | — | Solid `#FFFFFF` | Background transparent overlay applied on top |
| **PC Monitor Mockup** | `x: 63, y: 180`, size `1068x790` | — | — | — | Uses `Libraries/Parts/PC-Screen.png` |
| **Screen Viewport** | `x: 31, y: 27, w: 971, h: 505` inside frame | — | — | — | Global canvas: `(94, 207)`. Left-anchored crop (`crop_align="left"`) |
| **Kicker** | `x: 1148, y: 195` | Rubik Medium | 28px | `#1271D0` (Blue) or `#038E41` (Green) | Module name (e.g. `"PART D — FLOOR TICKETS"`) |
| **Heading** | `x: 1148, y: 240` (or `205` if no kicker) | Rubik SemiBold | 64px | `#58585A` (Dark Grey) | e.g. `"Dine-In Order & Kitchen Flow"` |
| **Body Copy** | `x: 1148, y: 320–330` | Rubik Regular | 24px | `#58585A` (Dark Grey) | 1–2 sentences, wrapped at max 640px |
| **Bullets (5 items)** | `x: 1148, y: 470`, spacing `52px` | Rubik Regular | 24px | `#58585A` (Dark Grey) | Exactly 5 single-line items starting with action verbs |
| **Check Icon** | `x: 1148`, size `26x26` | — | — | Brand Blue / Green | Pre-rendered transparent RGBA icon |
| **Ending Sentence** | — | — | — | — | Keep `""` (empty) to avoid boundary overflow |

---

## 4. Standard Workflow for LLMs When Handling User Prompts

When the user asks to generate or modify a slide (e.g., *"Generate a slide for Dine-In Orders"*):

### Step 1: Query the AI Search Engine for Ground Truth
```powershell
& ".\app\.venv\Scripts\python.exe" app\search.py "dine in order floor ticket"
```
Retrieve exact steps, role permissions, and key notes directly from the indexed POS knowledge base.

### Step 2: Configure Slide Entry in `app/content/slides_data.json`
Choose the appropriate layout:
* **For Overviews / Troubleshooting / Feature Grids:** Use `layout: "info"`, `style: "board"` with 6 structured `items`.
* **For Step-by-Step Sequences:** Use `layout: "info"`, `style: "flow"` with 4 `cards`.
* **For UI Screenshots:** Provide `screen_filename`, `kicker`, `heading`, `body`, and 5 `bullets`.

### Step 3: Execute Slide Generation Engine
```powershell
& ".\app\.venv\Scripts\python.exe" app\main.py --slide "POS-X.X"
```

### Step 4: Verify and Register Output
1. Check that the output file exists in `output/<slide_id>-<name>.jpg`.
2. Update the slide registry table in `CONTEXT.md`.
3. Provide a clickable link `[output/...jpg](file:///C:/Users/ISARVA/Documents/Restaurant-UserGuide-Application/restaurant-app/output/...jpg)` to the user.

---

## 5. POS Content Templates Reference

| Module | Kicker | Recommended Heading | Action Verbs for Bullets |
| :--- | :--- | :--- | :--- |
| **Floor / Dine-In** | `PART D — FLOOR TICKETS` | `Dine-In Order & Kitchen Flow` | *Seat, Select, Add, Send, Preview* |
| **Settle Screen** | `PART E — SETTLE MODAL` | `Flexible Payment & Split Settlement` | *Select, Split, Apply, Redeem, Confirm* |
| **Kitchen KDS** | `PART H — KITCHEN KDS` | `Kitchen Manager Display & Bumping` | *Filter, Review, Bump, Alert, Route* |
| **Delivery / Online** | `PART F & G — MULTI-CHANNEL` | `Takeaway, Aggregators & QR Orders` | *Receive, Confirm, Assign, Dispatch, Complete* |
| **Day Close** | `PART J & P — BACK OFFICE` | `Day Close & Financial Reconciliation` | *Settle, Reconcile, Count, Verify, Archive* |
| **Inventory / Stock** | `PART Q & R — INVENTORY` | `Stock Receiving, Recipes & POs` | *Raise, Receive, Transfer, Deduct, Count* |
| **Printers** | `PART M — PRINTER SETTINGS` | `Station Mapping & Ticket Routing` | *Connect, Map, Assign, Format, Test* |
| **Troubleshooting** | `PART W — TROUBLESHOOTING` | `Common POS Problems & Solutions` | *Audit, Reassign, Reopen, Enable, Refresh* |

---

## 6. Golden Rules & Checklists for LLMs

- [ ] **Exact Resolution:** Must always be 1920x1080.
- [ ] **No PPTX:** Output `.jpg` only.
- [ ] **No Overflow:** 5 bullet points max; no text past the bottom curve.
- [ ] **Sub-Millisecond Search:** Use `search.py` for all ground-truth queries instead of scanning large text files.
- [ ] **Action Verbs:** Bullets should start with action verbs (*Seat, Add, Send, Settle, Verify, Configure*).
- [ ] **Scrubbing Policy:** Default is NO scrubbing (`"scrub_rules": []`); only scrub when explicitly requested by user.
- [ ] **In-Memory Caching:** Keep pipeline fast; zero intermediate disk writes.
