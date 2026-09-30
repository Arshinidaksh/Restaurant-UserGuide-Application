# Isarva Restaurant POS — System Context & Operational Architecture

## 1. Project Overview & Objective
This repository is an automated, high-performance slide presentation engine and **sub-millisecond AI search & knowledge retrieval system** built for **Isarva Restaurant POS**.

The project models the official customer manual:
* **Document ID:** `ISARVA-CG-001` (Version 1.2, ISO/IEC 27001:2022 compliant)
* **Product:** Isarva Restaurant POS
* **Application URL:** `https://app.restaurant-pos.isarva.in`
* **Reference Guide:** `project/userguide/isarva-pos-userguide.pdf` (22 pages covering Parts A through Y)
* **Target Audience:** Restaurant Owners, Admins, Cashiers, Food Servers, Kitchen Managers, Delivery Riders

---

## 2. Dual Capability Architecture

```
                                    ISARVA RESTAURANT POS
                                  (ISARVA-CG-001 User Guide)
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
       [ ULTRA-FAST AI SEARCH ENGINE ]                     [ 100% IN-MEMORY SLIDE GENERATOR ]
       app/src/search_engine.py & search.py                app/main.py & app/src/info_renderer.py
                    │                                                   │
     - Pre-computed BM25 Inverted Index                  - Pre-warmed 1920x1080 canvas caching
     - Latency: 0.085ms per query                        - TrueType Rubik font pre-warming
     - Throughput: 11,700+ Queries/Sec                   - In-memory screenshot monitor mockup
     - Role Filtering (Admin, Cashier, etc.)             - Info Boards, 4-step flows, grids
     - 19-scenario instant troubleshooting matrix        - Zero intermediate disk writes
     - LLM Prompt Context generator                      - Generates output/POS-*.jpg slides
```

---

## 3. Brand & Design System Specifications

### Canvas & Layout (1920 x 1080 Full HD)
- **Base Background:** `Libraries/complete-design-format/Only-background-transparent.png` composited over solid pure white (`#FFFFFF`).
- **Left Column (Hardware Monitor Frame):**
  - Frame asset: `Libraries/Parts/PC-Screen.png` (dimensions: `1068 x 790`).
  - Position on canvas: `x: 63, y: 180`.
  - Viewport inside frame: `x: 31, y: 27, width: 971, height: 505` (global coordinates: `x: 94, y: 207`).
  - Cropping logic: Left-anchored (`crop_align="left"`) to maintain left navigation menu visibility.
- **Right Column (Typography & Content):**
  - Left margin: `x: 1148`.
  - Maximum text wrap width: `620–660px`.
  - Boundary constraint: Content must strictly stay within the grey circular background element.

### Color Palette & Typography
- **Fonts:** Google Font **Rubik** (stored in `app/fonts/`).
  - **Kicker:** Rubik Medium, 28px, Color `#1271D0` (Brand Blue) or `#038E41` (Brand Green).
  - **Heading:** Rubik SemiBold, 64px, Color `#58585A` (Dark Grey).
  - **Body Description:** Rubik Regular, 24px, Color `#58585A`.
  - **Bullet Points:** Rubik Regular, 24px, Color `#58585A`. 5 single-line checkmark items.
  - **Bullet Icon:** Pre-rendered RGBA transparent blue circle check icon (`app/brand_check_icon.png`), size `26x26px` at `x: 1148`.

---

## 4. Module Map & Knowledge Coverage (Parts A–Y)

| Part | Module Name | Scope & Coverage |
| :--- | :--- | :--- |
| **Part A & B** | Prerequisites & Till Activation | Chrome/Edge, Company Code (min 3 chars), Admin PIN, branch assignment, 15% VAT, ZATCA Phase 2 (CSID/OTP). |
| **Part C & D** | Floor Tickets (Dine-In) | Opening checklist, table seating, food items, modifiers, Subtotal, Discount pills (0%, 7%, 10%), Extra charges, VAT, KOT kitchen routing, Save & Bill preview. |
| **Part E** | Settle Screen & Split | Single tender (`Rest -> Cash/mada/Apple Pay`), Equal Split (2, 3, 4+ guests), Custom Multi-Tender Split, Food Vouchers, Gift Cards, Loyalty Points, SoftPOS bridge. |
| **Part F & G** | Takeaway & Aggregators | Takeaway parcels, Drive-thru car pickup, Aggregator APIs (HungerStation, Jahez, Keeta), and Guest QR menu URL (`?co=XYZ`). |
| **Part H & I** | Kitchen KDS & Rider Dispatch | Kitchen Manager bump screen (All/Kitchen/Bar/Expo), 86 stock-outs, rider mobile login (last 4 digits), delivery tracking, COD reconciliation. |
| **Part J & P** | Day Close & Financial Hub | Drawer cash counting vs sales ledger, cashier drawer shift, employee attendance time clock. |
| **Part K to S** | Settings Modules | Business details, ZATCA invoice queue, Printer mapping, Products & Dishes, Bulk Tax Update, User Privileges, Ingredients & Yields, Inventory PO/Receiving/Transfers, Database backup. |
| **Part T & U** | Reports & Daily Modules | Sales P&L, Sales Summary, Hourly Sales, Void Audit, Food Cost Variance, Stock Summary, and daily navigation hubs. |
| **Part V** | 16-Step Go-Live Roadmap | Sequential store implementation sequence preventing broken dependency links. |
| **Part W** | Troubleshooting Matrix | 19 instant diagnosis and remediation procedures for front-line restaurant staff. |
| **Part X & Y** | Closing & Security Directives | Mandatory 5-step daily closing protocol and 6 customer data security directives. |

---

## 5. Current POS Slide Registry & Status

All slides are generated as pixel-perfect 1920x1080 Full HD JPG files in `output/`:

| Slide ID | Type | Kicker | Heading | Output File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **POS-1.0** | Board | `CUSTOMER USER GUIDE` | `Isarva Restaurant POS` | `output/POS-1.0-isarva-restaurant-pos.jpg` | ✅ Complete (Architecture Overview) |
| **POS-2.1** | Flow | `PART A & B — GETTING STARTED` | `Prerequisites & First-Time Till Setup` | `output/POS-2.1-prerequisites-and-first-time-till-setup.jpg` | ✅ Complete (4-Step Onboarding) |
| **POS-3.1** | Flow | `PART D — FLOOR TICKETS` | `Dine-In Order & Kitchen Flow` | `output/POS-3.1-dine-in-order-and-kitchen-flow.jpg` | ✅ Complete (Table Seating to KOT) |
| **POS-4.1** | Board | `PART E — SETTLE MODAL` | `Flexible Payment & Split Settlement` | `output/POS-4.1-flexible-payment-and-split-settlement.jpg` | ✅ Complete (6 Payment Workflows) |
| **POS-5.1** | Board | `PART W — TROUBLESHOOTING` | `Common POS Problems & Solutions` | `output/POS-5.1-common-pos-problems-and-solutions.jpg` | ✅ Complete (Problem Remediation Grid) |
| **POS-6.1** | Flow | `PART V — IMPLEMENTATION` | `New Restaurant Go-Live Checklist` | `output/POS-6.1-new-restaurant-go-live-checklist.jpg` | ✅ Complete (4-Phase Implementation) |

---

## 6. AI Search & Retrieval Engine

### Benchmark Statistics
- **Indexed Chunks:** 26 full semantic sections
- **Vocabulary:** 1,033 distinct indexed terms
- **Troubleshooting Rules:** 41 indexed problem-solution pairs
- **Average Query Latency:** **0.085 ms**
- **Throughput:** **11,739.6 Queries/Second**

### Key CLI Commands
```powershell
# 1. Natural Language Search
& ".\app\.venv\Scripts\python.exe" app\search.py "how to split bill"

# 2. Filter by Role (Admin, Cashier, Food Server, Kitchen Manager, Rider)
& ".\app\.venv\Scripts\python.exe" app\search.py --role "Food Server" "merge tables"

# 3. Direct Troubleshooting Diagnostic
& ".\app\.venv\Scripts\python.exe" app\search.py --troubleshoot "tax looks wrong on bill"

# 4. Generate AI Prompt Context for LLMs
& ".\app\.venv\Scripts\python.exe" app\search.py --ai-context "how to perform day close"

# 5. Run Performance Benchmark
& ".\app\.venv\Scripts\python.exe" app\search.py --benchmark
```

---

## 7. Slide Generator CLI Usage

```powershell
# Generate specific slide
& ".\app\.venv\Scripts\python.exe" app\main.py --slide "POS-1.0"

# List all available slides
& ".\app\.venv\Scripts\python.exe" app\main.py --list

# Batch generate all slides
& ".\app\.venv\Scripts\python.exe" app\main.py --all
```
