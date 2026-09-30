# Isarva Restaurant POS — System Context, Architecture & Slide Generation Engine

## 1. Project Overview & Objectives
This repository is an automated, high-fidelity slide generation engine, multi-agent workflow framework, and sub-millisecond AI search & knowledge retrieval system built for **Isarva Restaurant POS**.

The project directly models and automates the official customer user guide:
- **Document ID:** `ISARVA-CG-001` (Version 1.2, ISO/IEC 27001:2022 compliant)
- **Product:** Isarva Restaurant POS
- **Live Application URL:** `https://app.restaurant-pos.isarva.in`
- **Reference Manual:** `ISARVA-CG-001-Customer-User-Guide.pdf` (covering Parts A through Y)
- **Target Audience:** Restaurant Owners, System Admins, Cashiers, Food Waiters, Kitchen Managers, Delivery Riders

---

## 2. Core Capabilities & System Architecture

```
                                    ISARVA RESTAURANT POS
                                  (ISARVA-CG-001 User Guide)
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
       [ MULTI-AGENT SLIDE PIPELINE ]                      [ ULTRA-FAST AI SEARCH ENGINE ]
       scripts/pipeline/ & .agents/skills/                 restaurant-app/app/src/search_engine.py
                    │                                                   │
     - Specification parser (JSON spec)                  - Pre-computed BM25 Inverted Index
     - Headless Playwright screen capture                - Latency: 0.085ms per query
     - Brand PC monitor mockup compositing               - Throughput: 11,700+ Queries/Sec
     - Unannotated, clean live POS captures              - Role Filtering (Admin, Cashier, etc.)
     - 1920x1080 Full HD slide outputs                  - 19-scenario instant troubleshooting
     - Exports to Slides/ and export/                    - LLM prompt context generator
```

---

## 3. Brand & Slide Design System

All generated slides adhere strictly to the brand design specifications defined in `.agents/rules/slide-design-system.md`:

### Canvas & Layout (1920 x 1080 Full HD)
- **Base Background:** `restaurant-app/Libraries/complete-design-format/Only-background-transparent.png` composited over solid pure white (`#FFFFFF`).
- **Left Column (Hardware Monitor Mockup):**
  - Frame asset: `restaurant-app/Libraries/Parts/PC-Screen.png` (dimensions: `1068 x 790`).
  - Position on canvas: `x: 60, y: 175`.
  - Viewport inside frame: center-aligned unannotated screen capture (1920x1080 native resized to monitor bezel).
- **Right Column (Typography & Content):**
  - Text Column Start: `x: 1148`.
  - Kicker: `y: 210`.
  - Heading: `y: 252`.
  - Maximum text wrap width: `680px`.
  - Step Number Badges: 28px diameter circle in `#1271D0` with centered white bold text.

### Strict Visual Constraints
- **Clean Screenshots (No Annotations):** Screenshots inside the PC monitor mockup must be 100% authentic, live application screens without bounding boxes, highlight borders, or arrows.
- **Glyph Compatibility:** Rubik font does not support Unicode arrows (`→`, `←`). The pipeline automatically replaces arrows with `>` or `<` to prevent broken square glyph boxes (``).
- **Alternative Wording:** For sections like Part M, subheadings use `Location:` instead of `Where:` (e.g. `Location: Settings > Printer > Receipt Printer`).

---

## 4. Multi-Agent Pipeline (`scripts/pipeline/`)

The workspace provides an end-to-end multi-agent pipeline for processing any section of the user guide:

1. **`schema.py`**: Pydantic/dataclass schema for structured slide definitions (`PartSpecification`, `SlideDefinition`, `BrowserAction`).
2. **`capture_screens.py`**: Headless Playwright script that authenticates with the POS (`C001`, `admin`, `0000`), navigates to target routes, prepares clean application state, waits for toast banners to fade, and captures pristine 1080p screens into `project/screens_part_<id>/`.
3. **`compose_slides.py`**: Compositing engine that renders slides, mounts PC frames, lays out typography, and saves to `Slides/<Part>/` and `export/<Part>/`.
4. **`orchestrator.py`**: Master CLI coordinator executing both capture and rendering stages from a single command:
   ```powershell
   uv run --with playwright --with pillow python scripts/pipeline/orchestrator.py --spec specs/part_l_spec.json
   ```

---

## 5. Module Map & Knowledge Coverage (Parts A–Y)

| Part | Module Name | Scope & Coverage |
| :--- | :--- | :--- |
| **Part A & B** | Prerequisites & Till Activation | Chrome/Edge, Company Code (min 3 chars), Admin PIN, branch assignment, 15% VAT, ZATCA Phase 2 (CSID/OTP). |
| **Part C & D** | Floor Tickets (Dine-In) | Opening checklist, table seating, food items, modifiers, Subtotal, Discount pills, Extra charges, VAT, KOT kitchen routing, Save & Bill preview. |
| **Part E** | Settle Screen & Split | Single tender (`Cash / mada / Apple Pay`), Equal Split (2, 3, 4+ guests), Custom Multi-Tender Split, Food Vouchers, Gift Cards, Loyalty Points, SoftPOS bridge. |
| **Part F & G** | Takeaway & Aggregators | Takeaway parcels, Drive-thru car pickup, Aggregator APIs (HungerStation, Jahez, Keeta), and Guest QR menu URL. |
| **Part H & I** | Kitchen KDS & Rider Dispatch | Kitchen Manager bump screen (All/Kitchen/Bar/Expo), 86 stock-outs, rider mobile login (last 4 digits), delivery tracking, COD reconciliation. |
| **Part J & P** | Day Close & Financial Hub | Drawer cash counting vs sales ledger, cashier drawer shift, employee attendance time clock. |
| **Part K & L** | Settings → Business (L1–L17) | Company details, ZATCA Phase 1 & 2 CSID/OTP, ZATCA queue, CRM customers, Gift cards, Food vouchers, Loyalty campaigns, Vendors, Delivery riders, Notifications, Delivery APIs, Table areas, Table management, Menu timetables, Addons, SoftPOS card terminals, Counter quick serve. |
| **Part M** | Settings → Printer (M1–M4) | Receipt printer (paper width 58/80mm, layout, header/footer), KOT printers & kitchen stations, Printer department mapping, Print template styles. |
| **Part N to S** | Products, Catalog, Database | Department lists, Menu dishes, Recipe yields, Inventory PO/Receiving/Transfers, Database backup and restore. |
| **Part T & U** | Reports & Daily Modules | Sales P&L, Sales Summary, Hourly Sales, Void Audit, Food Cost Variance, Stock Summary, and daily navigation hubs. |
| **Part V** | 16-Step Go-Live Roadmap | Sequential restaurant implementation sequence preventing broken dependency links. |
| **Part W** | Troubleshooting Matrix | 19 instant diagnosis and remediation procedures for front-line restaurant staff. |
| **Part X & Y** | Closing & Security Directives | Mandatory 5-step daily closing protocol and 6 customer data security directives. |

---

## 6. Generated Presentation Slides Registry

### Part L — Settings → Business (17 Individual Slides)
All 17 slides generated with authentic, unannotated screenshots in `Slides/Part L/` and `export/Part L/`:
- `L1 - Company Details.jpg` (`/settings/company`)
- `L2 - ZATCA e-invoice setup.jpg` (`/settings/company?focus=zatca`)
- `L3 - ZATCA invoice queue.jpg` (`/settings/zatca/invoices`)
- `L4 - Customers (CRM).jpg` (`/crm`)
- `L5 - Gift cards.jpg` (`/settings/gift-cards`)
- `L6 - Food vouchers.jpg` (`/settings/food-vouchers`)
- `L7 - Loyalty campaigns.jpg` (`/settings/loyalty-campaigns`)
- `L8 - Vendors (suppliers).jpg` (`/settings/vendors`)
- `L9 - Delivery Boy (riders).jpg` (`/settings/delivery-riders`)
- `L10 - Notification settings.jpg` (`/settings/notifications`)
- `L11 - Delivery APIs (aggregators).jpg` (`/settings/delivery-integrations`)
- `L12 - Table Area.jpg` (`/settings/floor`)
- `L13 - Table Management.jpg` (`/settings/floor?tab=tables`)
- `L14 - Menu timetable.jpg` (`/settings/menu-timetable`)
- `L15 - Addons.jpg` (`/settings/addons`)
- `L16 - Card - SoftPOS terminal.jpg` (`/payments`)
- `L17 - Counter - Quick serve.jpg` (`/quick-serve`)

### Part M — Settings → Printer (4 Individual Slides)
All 4 slides generated with `Location:` phrasing and unannotated screenshots in `Slides/Part M/` and `export/Part M/`:
- `M1 - Receipt Printer.jpg` (`Location: Settings > Printer > Receipt Printer`)
- `M2 - KOT Printer.jpg` (`Location: Settings > Printer > KOT Printer`)
- `M3 - Printer Mapping.jpg` (`Location: Settings > Printer > Printer Mapping`)
- `M4 - Print designs - templates.jpg` (`Location: Settings > Printer > Print designs`)

### Summary & Flow Slides
- Parts A, B, C, D (Steps 1–12), E (Steps 1–10), F, G, H, I, J, K, V, W overview and step-by-step slides in `Slides/` and `export/`.

---

## 7. AI Search Engine Benchmarks
- **Engine Location:** `restaurant-app/app/src/search_engine.py` & `search.py`
- **Indexed Chunks:** 26 full semantic sections covering Parts A–Y
- **Vocabulary Size:** 1,033 distinct indexed terms
- **Average Query Latency:** **0.085 ms**
- **Throughput:** **11,739+ Queries/Second**
- **Capabilities:** Keyword search, role-based filtering, instant troubleshooting retrieval, LLM context generation.
