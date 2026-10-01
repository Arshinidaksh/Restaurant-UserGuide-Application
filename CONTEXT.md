# Isarva Restaurant POS — System Context, Architecture & Slide Generation Engine

## 1. Project Overview & Objectives
This repository is an automated, high-fidelity slide generation engine, multi-agent workflow framework, and sub-millisecond AI search & knowledge retrieval system built for **Isarva Restaurant POS**.

The project directly models and automates the official customer user guide:
- **Document ID:** `ISARVA-CG-001` (Version 1.2, ISO/IEC 27001:2022 compliant)
- **Product:** Isarva Restaurant POS
- **Live Application URL:** `https://app.restaurant-pos.isarva.in`
- **Reference Manual:** `ISARVA-CG-001-Customer-User-Guide.pdf` (covering Parts A through Y + Support)
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
       scripts/pipeline/ & worker-offload/                 restaurant-app/app/src/search_engine.py
                    │                                                   │
     - Specification parser (JSON spec)                  - Pre-computed BM25 Inverted Index
     - Distributed Cloud Worker Fleet (DigitalOcean)     - Latency: 0.085ms per query
     - Headless Playwright screen capture (10 workers)   - Throughput: 11,700+ Queries/Sec
     - Brand PC monitor mockup compositing (16 workers)  - Role Filtering (Admin, Cashier, etc.)
     - Clean Info & Checklist Slide Stitcher             - 19-scenario instant troubleshooting
     - Session state reuse for instant navigation        - LLM prompt context generator
     - 1920x1080 Full HD slide outputs                  
     - Exports to Slides/ and export/                    
```

---

## 3. Brand & Slide Design System

All generated slides adhere strictly to the brand design specifications defined in `.agents/rules/slide-design-system.md`:

### Canvas & Layout (1920 x 1080 Full HD)
- **Base Background:** `restaurant-app/Libraries/complete-design-format/Only-background-transparent.png` composited over solid pure white (`#FFFFFF`).
- **Footer Branding:** `www.isarvait.com` with dark green and vibrant orange brand accent curves.

### Layout 1: Monitor Hardware Screen Slides
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

### Layout 2: Information & Checklist Slides (Non-Monitor)
- **Header:** Blue section kicker (font size 18, bold uppercase) + dark slate heading (font size 38, bold) + description subtitle (font size 18, muted).
- **Grid Layout:** Supports either 1-column or 2-column configurations (`columns: 1` or `columns: 2`).
- **Items & Sub-items:**
  - Blue numbered circle badges (`#1271D0`, 28px diameter) with bold white index numbers.
  - Bold item titles with indented or inline secondary descriptions.
- **Footnote / Milestone Banner:** Light blue informational callout at the bottom left (`Complete each milestone before accepting live paying customers`).

### Strict Visual Constraints
- **Clean Screenshots (No Annotations):** Screenshots inside the PC monitor mockup must be 100% authentic, live application screens without bounding boxes, highlight borders, or arrows.
- **Glyph Compatibility:** Rubik font does not support Unicode arrows (`→`, `←`). The pipeline automatically replaces arrows with `>` or `<` to prevent broken square glyph boxes (``).
- **Decoupled Slide Kickers:** Each slide uses its own specific kicker (e.g. `PART V — ONBOARDING & SETUP`, `PART W — TROUBLESHOOTING & SOLUTIONS`) rather than inheriting collective batch prefixes.
- **Alternative Wording:** For sections like Part M, subheadings use `Location:` instead of `Where:` (e.g. `Location: Settings > Printer > Receipt Printer`).

---

## 4. Pipeline & Generator Engines

The repository provides two execution pipelines:

### 1. Local Pipeline (`scripts/pipeline/`)
- **`schema.py`**: Pydantic/dataclass schema for structured slide definitions (`PartSpecification`, `SlideDefinition`, `BrowserAction`).
- **`capture_screens.py`**: Headless Playwright script that authenticates with the POS (`C001`, `admin`, `0000`), navigates to target routes, waits for toast banners to fade, and captures pristine 1080p screens.
- **`compose_slides.py`**: Compositing engine that mounts PC frames, lays out typography, and saves to `Slides/` and `export/`.
- **`orchestrator.py`**: CLI coordinator executing both capture and rendering locally.

### 2. Distributed Cloud Worker Pipeline (`worker-offload/`)
- Asynchronous orchestration engine connecting to remote cloud workers via `httpx`.
- High-concurrency client (`worker-offload/client/async_slide_generator.py`) capable of generating batches of slides at **3.8 to 6.6+ slides/second**.
- Dual API endpoint support:
  - `POST /compose`: Monitor mockup frame composition.
  - `POST /compose-info`: High-fidelity multi-column informational slide stitching.

---

## 5. Module Map & Knowledge Coverage (Parts A–Y + Support)

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
| **Part N** | Catalog & Master Data (N1–N7) | Department lists, Menu categories, Dishes & pricing, Custom modifiers, Addons mapping, Barcode scanner catalog, Menu timetable scheduling. |
| **Part O** | Inventory & Stock Control (O1–O5) | Raw material ingredients, Recipes & portion cost, Storage locations & warehouses, Purchase orders & stock receiving, Inter-branch stock transfers. |
| **Part P** | Cash & Shift Operations (P1–P4) | Cash drawer balance, Mid-day cash drops, Shift handover audit, Financial end-of-shift reconciliation. |
| **Part Q** | Kitchen Display System (Q1–Q4) | Station routing (Kitchen, Bar, Grill, Expo), Item bump controls, Order prep timer alerts, Completed order dispatch. |
| **Part R** | Delivery Fleet & Online Channels (R1–R4) | In-house delivery riders, Aggregator live order queue, Courier handover dispatch, COD cash settlement. |
| **Part S** | User Accounts & Security (S1–S3) | Staff profile creation, Role-based privilege matrix, Cashier PIN authorization rules. |
| **Part T** | Reports & Business Analytics (T1–T5) | Daily Sales Summary, Hourly Sales Trends, Product Mix & Popular Dishes, Payment Breakdown, Tax & VAT Audit Ledger. |
| **Part U** | System Maintenance & Database (U1–U3) | Cloud sync status, Manual database backup snapshot, Audit trail & security logs. |
| **Part V** | 16-Step Go-Live Roadmap | Sequential restaurant onboarding milestone sequence preventing missing dependencies. |
| **Part W** | Troubleshooting Matrix (W1–W2) | Frontline diagnosis & remediation protocols: floor tickets, discounts, taxes, hardware, stock receipts, card terminals, aggregators. |
| **Part X** | Daily Closing Checklist | Mandatory 5-step end-of-day shutdown routine ensuring tamper-proof financial reconciliation. |
| **Part Y** | Security & Compliance Rules | Mandatory ISO/IEC 27001:2022 security policies: individual logins, terminal lock, credential secrecy, card data privacy. |
| **Quick Start** | Opening Day Summary | Chronological 9-step go-live roadmap for the opening day team. |
| **Support** | Technical Support & Audit History | Official support channels, onboarding assistance, version changelog, and document control. |

---

## 6. Generated Presentation Slides Registry

Slides are mirrored in both `Slides/` and `export/` directories:

### Part L — Settings → Business (17 Slides)
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

### Part M — Settings → Printer (4 Slides)
- `M1 - Receipt Printer.jpg` (`Location: Settings > Printer > Receipt Printer`)
- `M2 - KOT Printer.jpg` (`Location: Settings > Printer > KOT Printer`)
- `M3 - Printer Mapping.jpg` (`Location: Settings > Printer > Printer Mapping`)
- `M4 - Print designs - templates.jpg` (`Location: Settings > Printer > Print designs`)

### Parts N through U — Products, Inventory, KDS, Reports (28 Slides)
- `Part N (N1–N7)`: Department lists, Menu categories, Dishes & pricing, Custom modifiers, Addons mapping, Barcodes, Timetables.
- `Part O (O1–O5)`: Raw ingredients, Recipes, Storage locations, PO & Stock receiving, Inter-branch transfers.
- `Part P (P1–P4)`: Cash drawer float, Cash drops, Shift audit, Drawer reconciliation.
- `Part Q (Q1–Q4)`: Station routing, Item bump controls, Order timer alerts, Order dispatch.
- `Part R (R1–R4)`: Rider accounts, Aggregator queue, Courier handover, COD settlement.
- `Part S (S1–S3)`: Staff profiles, Role privileges, Cashier PIN setup.
- `Part T (T1–T5)`: Daily Sales, Hourly Trends, Dish Popularity, Payments Received, Tax / VAT Ledger.
- `Part U (U1–U3)`: Cloud sync, Database backup, Audit logs.

### V to Support — Checklists, Troubleshooting, Security & Support (7 Dedicated Slides)
Located in `Slides/V to Support/` and `export/V to Support/`:
- `Part V - Full Setup Order Checklist.jpg` (Kicker: `PART V — ONBOARDING & SETUP`)
- `Part W1 - Common Problems Floor Orders and Tax.jpg` (Kicker: `PART W — TROUBLESHOOTING & SOLUTIONS`)
- `Part W2 - Common Problems Hardware Stock Delivery.jpg` (Kicker: `PART W — TROUBLESHOOTING & SOLUTIONS`)
- `Part X - Daily Closing Checklist.jpg` (Kicker: `PART X — OPERATIONS & END-OF-DAY`)
- `Part Y - Customer Security Rules.jpg` (Kicker: `PART Y — SECURITY & COMPLIANCE`)
- `Quick Start Summary.jpg` (Kicker: `QUICK START — GO-LIVE GUIDE`)
- `Support and Document Control.jpg` (Kicker: `SUPPORT & DOCUMENT CONTROL`)

---

## 7. AI Search Engine Benchmarks
- **Engine Location:** `restaurant-app/app/src/search_engine.py` & `search.py`
- **Indexed Chunks:** 26 full semantic sections covering Parts A–Y
- **Vocabulary Size:** 1,033 distinct indexed terms
- **Average Query Latency:** **0.085 ms**
- **Throughput:** **11,739+ Queries/Second**
- **Capabilities:** Keyword search, role-based filtering, instant troubleshooting retrieval, LLM context generation.

---

## 8. Distributed Cloud Worker Offload Architecture (`worker-offload/`)

To maximize slide throughput and offload compute-intensive workloads, the repository includes a distributed worker subsystem provisioned via DigitalOcean `doctl` with Dockerized microservices.

### Infrastructure-as-Code (IaC) & Cloud Provisioning
The cluster is fully automated and can be spun up, torn down, or re-created with identical specs via scripts:
- **Droplet Specs:** `s-4vcpu-8gb` (8 GB RAM / 4 vCPUs per worker) in region `blr1`.
- **Operating System:** Ubuntu 22.04 LTS x64.
- **Port 2222 SSH Configuration:** Cloud-init scripts reconfigure OpenSSH to listen on **Port 2222** (`sshd_config.d/port.conf`), bypassing corporate firewalls and ISP blocks on Port 22.
- **Automated IP Discovery:** Upon boot, `provision_vms.ps1` retrieves public IPs and automatically writes them to `worker-offload/client/config.json`.

### Worker Microservices
1. **`screenshot-vm` (`screenshot-worker`)**:
   - **Engine:** Playwright Chromium headless in Docker.
   - **Worker Concurrency:** **10 concurrent browser sessions** (`WORKER_CONCURRENCY=10`).
   - **Shared Memory:** `shm_size: 2gb` allocated for headless Chromium stability.
   - **Session Reuse:** Persists `storage_state.json` after initial POS terminal activation (`C001`) and admin authentication (`0000`), allowing subsequent screenshots to load in <1 second without re-logging in.
   - **API:** `POST /capture` (accepts route, query params, actions, output format, quality).

2. **`image-stitcher-vm` (`stitcher-worker`)**:
   - **Engine:** FastAPI + Pillow with ThreadPool execution in Docker.
   - **Worker Concurrency:** **16 concurrent render threads** (`WORKER_CONCURRENCY=16`).
   - **Rendering Engine:**
     - Monitor slide composition: Fits screenshots into hardware frames, applies anti-aliased step badges, wraps typography, and renders 1920x1080 slides.
     - Info slide composition: Multi-column grid layout, circle badges, bullet lists, note banners, and custom kickers.
   - **API:** `POST /compose` (monitor slides) and `POST /compose-info` (informational slides).

### Automation Lifecycle Commands
```powershell
# 1. Provision VMs from scratch (8GB RAM, 10 screenshot / 16 stitcher workers)
powershell -ExecutionPolicy Bypass -File worker-offload\provisioning\provision_vms.ps1

# 2. Verify worker health and Port 2222 connectivity
powershell -ExecutionPolicy Bypass -File worker-offload\provisioning\verify_workers.ps1

# 3. Dispatch batch slide generation jobs
uv run --with httpx python worker-offload\client\async_slide_generator.py --spec specs\v_to_support_spec.json

# 4. Teardown VMs to stop cloud billing
powershell -ExecutionPolicy Bypass -File worker-offload\provisioning\teardown_vms.ps1 -Force
```
