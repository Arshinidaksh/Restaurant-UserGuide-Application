# Isarva Restaurant POS — Documentation-to-Slide Mapping & Live Application Stitching

> **Document ID:** `ISARVA-CG-001` (Version 1.2, ISO/IEC 27001:2022 Compliant)  
> **Source User Guide:** `restaurant-app/project/userguide/isarva-pos-userguide.pdf` (22 Pages, Parts A through Y)  
> **Target Application URL:** [https://app.restaurant-pos.isarva.in](https://app.restaurant-pos.isarva.in)  
> **Output Format:** Pure 1920x1080 Full HD JPEG Images (`.jpg`) — **No PPTX files**  
> **Slide Output Directory:** `export/`  
> **Execution Runtime:** Python 3.12+ via `uv` on Windows  

---

## 1. Executive System Overview & Visual Archetypes

The **Isarva Restaurant POS** presentation engine generates pixel-perfect Full HD (`1920x1080`) **JPEG (.jpg)** presentation slides adhering strictly to the official brand guidelines. The engine executes 100% in-memory compositing with zero PPTX overhead. The system supports two primary visual formats:

### Slide Archetype 1: Informational Slides
* **Sub-type A: 4-Step Process Flow** (`restaurant-app/examples/information-slide-1.jpg`)
  - **Structure:** 4 horizontal connected step cards ("01", "02", "03", "04") with directional arrows, category kicker, and strong action-oriented titles.
  - **Best For:** Sequential user journeys, first-time till setup, morning checklists, dine-in kitchen dispatch, and go-live phases.
* **Sub-type B: 6-Card Information Board / Feature Grid** (`restaurant-app/examples/information-slide-2.jpg`)
  - **Structure:** 2×3 grid layout with color-coded status badges (`SETUP`, `FLOOR`, `PAYMENTS`, `KITCHEN`, `INVENTORY`, `ZATCA`), header kicker, subtitle, and bottom `TIP` pill.
  - **Best For:** Architecture overviews, module directories, troubleshooting diagnosis matrices, and security directives.

### Slide Archetype 2: Slides with Screenshot and Steps (`restaurant-app/examples/slide-whtscreen-and-steps.jpg`)
* **Left Column (Hardware Monitor Frame):**
  - Frame asset: `restaurant-app/Libraries/Parts/PC-Screen.png` (dimensions `1068x790` placed at `x: 63, y: 180`).
  - Screen Viewport: Inner dimensions `971x505` at canvas coordinate `(x: 94, y: 207)`.
  - Content: Authentic live UI screenshot captured from the active POS web application (`https://app.restaurant-pos.isarva.in`), anchored with left-menu alignment (`crop_align="left"`).
* **Right Column (Brand Typography & Action Steps):**
  - **Kicker:** Rubik Medium 28px in `#1271D0` (Brand Blue) or `#038E41` (Brand Green).
  - **Heading:** Rubik SemiBold 64px in `#58585A` (Dark Grey).
  - **Body Description:** Rubik Regular 24px in `#58585A` (max width 640px).
  - **Action Bullets:** Exactly 5 single-line action items starting with imperative verbs, preceded by `restaurant-app/app/brand_check_icon.png` (26×26px RGBA icon).

---

## 2. Live Application Navigation & Authentication Context

All screenshot captures are authenticated and bound using the environment variables configured in `.env`:

```ini
APPLICATION_URL: https://app.restaurant-pos.isarva.in/
COMAPNY_CODE: C001
USERNAME: admin
PASSWORD: 0000
Switch to: H001 - Head Office
```

### Authentication & Initialization Sequence:
1. **Navigate:** Load `https://app.restaurant-pos.isarva.in/` in Microsoft Edge / Chromium.
2. **Till Activation:** Enter Company Code `C001` and click **Activate POS**.
3. **Staff Login:** Enter Username `admin` and PIN/Password `0000`, then click **OK**.
4. **Till & Branch Verification:** Select or verify branch `H001 - Head Office` from the top navigation bar.

---

## 3. Comprehensive Documentation-to-Slide Mapping (Parts A through Y)

The 22 pages of `isarva-pos-userguide.pdf` are mapped below into individual slides, stitching each user guide paragraph to its live application screen, action steps, and target screenshot.

```
====================================================================================================
SLIDE 01: POS-A01 — System Architecture & Prerequisites
====================================================================================================
```
* **PDF Reference:** Page 1, *Part A — Before you start*
* **Slide Type:** Informational Slide (Sub-type B: Information Board)
* **Kicker:** `CUSTOMER USER GUIDE`
* **Heading:** `Isarva Restaurant POS`
* **Subheading:** `ISO/IEC 27001:2022 Certified Architecture · Version 1.2 · Complete System Overview`
* **Theme Color:** `green`
* **Source Paragraph:**
  > "Before you start: Prepare computer, laptop, or tablet with internet. Google Chrome or Microsoft Edge browser (recommended). Your Company Code (given by Isarva). Your Admin username and password / PIN (given by Isarva). Your restaurant name, VAT / tax details, and branch address ready."
* **Slide Structure (6 Grid Cards):**
  1. `[SETUP]` **Complete Setup & Activation:** First-time till activation via Company Code, multi-branch configuration, and bilingual EN/AR interface.
  2. `[FLOOR]` **Floor & Dine-In Operations:** Interactive table seating, order tickets, KOT dispatch, item customizers, bill split, table change & merge.
  3. `[PAYMENTS]` **Smart Settle & Payment Hub:** Equal & custom split, food vouchers, gift cards, loyalty points, SoftPOS, mada, Apple Pay, STC Pay.
  4. `[KITCHEN]` **Kitchen KDS & Delivery:** Multi-station KDS, bump flow, 86 item alerts, delivery aggregator APIs (HungerStation, Jahez, Keeta), and rider app.
  5. `[INVENTORY]` **Inventory, Recipes & POs:** Yield conversions, recipe food costing, storage transfers, vendor POs, receiving, and Stock Master counts.
  6. `[ZATCA]` **ZATCA e-Invoicing & Reports:** KSA ZATCA Phase 2 compliance, sales P&L, void audits, discount logs, and branch-specific Day Close.
* **Tip Pill:** `Application URL: https://app.restaurant-pos.isarva.in · ISO 27001 compliant restaurant operations.`
* **Screenshot Required:** None (Informational Board Layout).

---

```
====================================================================================================
SLIDE 02: POS-B01 — First-Time Till Activation
====================================================================================================
```
* **PDF Reference:** Page 1–2, *Part B — First-time setup: Step 1 & 2*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART B — FIRST-TIME SETUP`
* **Heading:** `Activate This POS Till`
* **Body:** `Permanently bind this browser terminal to your restaurant using the authorized company code.`
* **Source Paragraph:**
  > "Step 1 — Open the POS website: 1. Open your browser. 2. Go to: https://app.restaurant-pos.isarva.in. 3. Wait for the login / activate screen to open. Step 2 — Activate this POS for your restaurant: 1. On the screen, find Activate POS (or company code box). 2. Type your Company Code given by Isarva (e.g. C001). 3. Company code must be at least 3 characters. 4. Tap or click Activate POS. 5. Wait until the screen shows your restaurant name."
* **5 Action Step Bullets:**
  - `Navigate to official application URL in Chrome or Edge`
  - `Locate Activate POS card on the initial landing screen`
  - `Enter registered Company Code C001 in the input box`
  - `Tap Activate POS button to bind hardware to restaurant`
  - `Confirm restaurant legal name is displayed on screen`
* **Live App Navigation Path:**
  1. Open `https://app.restaurant-pos.isarva.in/`
  2. Focus input placeholder `C001`
  3. Screenshot target: Initial "Activate this POS" card with green header badge
* **Screenshot File:** `project/screens/01_activate_pos.jpg`

---

```
====================================================================================================
SLIDE 03: POS-B02 — Staff & Admin Authentication
====================================================================================================
```
* **PDF Reference:** Page 2, *Part B — First-time setup: Step 3*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART B — FIRST-TIME SETUP`
* **Heading:** `Sign In with Admin PIN`
* **Body:** `Authenticate staff and manager credentials using the on-screen numeric keypad or keyboard.`
* **Source Paragraph:**
  > "Step 3 — Sign in as Admin: 1. Enter your Admin username. 2. Enter your PIN or password. 3. Tap Sign in. 4. You should see the Home / main menu. If you cannot sign in: Check Caps Lock. Tap Refresh on the login screen and try again. Ask Isarva if your user is active."
* **5 Action Step Bullets:**
  - `Enter designated staff username into the Username field`
  - `Type security PIN or password using physical or touch keypad`
  - `Tap Show PIN button if password verification is required`
  - `Tap orange OK button to authenticate and unlock system`
  - `Access role-authorized POS dashboard and till controls`
* **Live App Navigation Path:**
  1. Complete POS activation with `C001`
  2. Wait for "Sign in" screen with PIN pad
  3. Screenshot target: Sign in modal with keypad (1–9, Clear, 0, OK)
* **Screenshot File:** `project/screens/02_admin_login.jpg`

---

```
====================================================================================================
SLIDE 04: POS-B03 — Main POS Operations Hub
====================================================================================================
```
* **PDF Reference:** Page 2, *Part B — Step 4 & 5 (Language switch & Branch selection)*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `CORE DASHBOARD`
* **Heading:** `Main Restaurant Dashboard`
* **Body:** `Central command center displaying live till sales, kitchen queues, and quick order launch pads.`
* **Source Paragraph:**
  > "Step 4 — Choose language (optional): Use the language switch (EN / AR) if you need Arabic. You can change language anytime later. Step 5 — Set company and branches: Open Settings → Company & Branches... On the top bar, select the correct branch for this till."
* **5 Action Step Bullets:**
  - `Verify assigned till branch H001 - Head Office at top bar`
  - `Monitor live metrics: Open Tables, Billing, and Kitchen Queue`
  - `Switch bilingual interface between English and Arabic`
  - `Launch front-of-house services: Dine In, Takeaway, Drive Thru`
  - `Access back-office tools: Day Close, Expenses, and Settings`
* **Live App Navigation Path:**
  1. Authenticate with `admin` / `0000`
  2. Land on default HOME dashboard
  3. Screenshot target: Full 1920x1080 dashboard view with top bar, KPI cards, and service buttons
* **Screenshot File:** `project/screens/03_main_dashboard.jpg`

---

```
====================================================================================================
SLIDE 05: POS-C01 — Daily Morning Opening Routine
====================================================================================================
```
* **PDF Reference:** Page 3, *Part C — Daily opening checklist (morning)*
* **Slide Type:** Informational Slide (Sub-type A: 4-Step Process Flow)
* **Kicker:** `PART C — DAILY OPERATIONS`
* **Heading:** `Morning Opening Checklist`
* **Source Paragraph:**
  > "Part C — Daily opening checklist (morning): 1. Turn on computer, printer, and internet router. 2. Open browser, go to POS URL. 3. Check top bar: Is the branch correct? 4. Check green indicator: Connected (if Offline, check Wi-Fi/cable). 5. Open Day Open (if drawer tracking enabled) — type starting float cash."
* **Cards (4 Step Flow):**
  - **Card 01:** `Hardware Check` — Turn on computer, receipt printer, thermal KOT printers, and verify router connectivity.
  - **Card 02:** `Launch & Verify` — Open Google Chrome, launch POS app, and verify top branch reads H001 - Head Office.
  - **Card 03:** `Network Status` — Confirm the green Connected status badge; check LAN cables if Offline appears.
  - **Card 04:** `Opening Cash Float` — Tap Day Open, count till drawer float cash, enter starting SAR amount, and begin service.
* **Screenshot Required:** None (4-Card Process Flow).

---

```
====================================================================================================
SLIDE 06: POS-D01 — Dine-In Floor & Table Seating
====================================================================================================
```
* **PDF Reference:** Page 3–4, *Part D — Floor tickets: Step 1 & 2*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART D — FLOOR TICKETS`
* **Heading:** `Interactive Table Seating & Menu`
* **Body:** `Select dining zones, seat guests on interactive floor tables, and build order tickets.`
* **Source Paragraph:**
  > "Part D — Floor tickets (Dine-in / table orders): Step 1 — Start a ticket: Tap Floor (or Dine In). You see the floor plan with tables. Green / empty table = free. Orange / red table = occupied / has open order. Tap an empty table (e.g. Table 5). Order screen opens for Table 5. Step 2 — Add food items: Tap a category on the left (e.g. Burgers, Drinks, Desserts). Tap an item to add it to the ticket."
* **5 Action Step Bullets:**
  - `Open Floor or Dine In service from dashboard or sidebar`
  - `View floor map with color-coded table occupancy status`
  - `Tap empty table to launch new dine-in guest order ticket`
  - `Select menu categories on left to browse dishes and beverages`
  - `Tap food items to add to ticket with custom kitchen modifiers`
* **Live App Navigation Path:**
  1. Click `Dine In` on Dashboard or `FLOOR` on sidebar
  2. Select active floor area (Ground Floor / Dining Hall)
  3. Screenshot target: Interactive table layout and ticket builder
* **Screenshot File:** `project/screens/04_floor_tickets.jpg`

---

```
====================================================================================================
SLIDE 07: POS-D02 — Kitchen Order Ticket (KOT) Dispatch
====================================================================================================
```
* **PDF Reference:** Page 4–5, *Part D — Floor tickets: Step 7*
* **Slide Type:** Informational Slide (Sub-type A: 4-Step Process Flow)
* **Kicker:** `PART D — FLOOR TICKETS`
* **Heading:** `Dine-In Order & Kitchen Flow`
* **Source Paragraph:**
  > "Step 7 — Send to kitchen: KOT and KOT & Print: KOT = sends items to kitchen display screen (KDS) without printing paper. KOT & Print = sends to kitchen screen AND prints a paper ticket in the kitchen printer. Once sent, items change status (e.g. Cooking / Sent). You cannot easily delete items without manager void."
* **Cards (4 Step Flow):**
  - **Card 01:** `Seat & Add Dishes` — Select guest table from floor map, pick categories, add dishes with custom kitchen preparation notes.
  - **Card 02:** `Send KOT to Kitchen` — Tap KOT (or KOT & Print) to route items instantly to kitchen display stations and KOT printers.
  - **Card 03:** `Discounts & Charges` — Apply discount percentage pills (0%, 7%, 10%) or toggle extra charges (service fee, parking) as authorized.
  - **Card 04:** `Save & Bill Preview` — Tap Save & Bill to generate interim guest check slip for review before proceeding to final settlement.
* **Screenshot Required:** None (4-Card Process Flow).

---

```
====================================================================================================
SLIDE 08: POS-E01 — Smart Settle & Payment Workflows
====================================================================================================
```
* **PDF Reference:** Page 6–8, *Part E — Settle screen and payments*
* **Slide Type:** Informational Slide (Sub-type B: Information Board)
* **Kicker:** `PART E — SETTLE MODAL`
* **Heading:** `Flexible Payment & Split Settlement`
* **Subheading:** `ISO/IEC 27001:2022 Compliant Financial Reconciliation & Multi-Tender Workflows`
* **Theme Color:** `blue`
* **Source Paragraph:**
  > "Part E — Settle screen and payments: Single payment (full bill): Cash, mada / Visa / Mastercard, Apple Pay / STC Pay. Equal split (same amount each): Tap Split, select number of guests (2, 3, 4...). Custom split (different items or amounts). Food vouchers, Gift cards, Loyalty points, and Card machine integration (SoftPOS)."
* **Slide Structure (6 Grid Cards):**
  1. `[CASH]` **Full Single Payment:** Settle entire bill instantly via Cash, mada debit, Apple Pay, or credit card with automatic change return.
  2. `[SPLIT]` **Equal Split Settlement:** Divide total bill evenly across 2 to 6+ guests, allowing each guest to settle via distinct tender.
  3. `[CUSTOM]` **Custom Item Split:** Allocate specific food dishes or custom amounts to separate payers before issuing fiscal receipts.
  4. `[VOUCHER]` **Voucher & Gift Cards:** Redeem promotional food vouchers and prepaid gift card serial numbers with automatic balance deduction.
  5. `[LOYALTY]` **Loyalty Redemption:** Apply earned customer points to discount bill subtotals based on configured loyalty campaigns.
  6. `[SOFTPOS]` **Integrated SoftPOS:** Send transaction total directly to network payment terminal, eliminating manual cashier entry errors.
* **Tip Pill:** `ZATCA Phase 2 compliant QR code is generated instantly upon invoice settlement.`
* **Screenshot Required:** None (Informational Board Layout).

---

```
====================================================================================================
SLIDE 09: POS-E02 — Settle Modal UI & Tender Capture
====================================================================================================
```
* **PDF Reference:** Page 6, *Part E — Step 11: Settle (full payment)*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART E — PAYMENTS`
* **Heading:** `Order Settlement & Tender Screen`
* **Body:** `Finalize customer tickets with multi-tender payment methods and instant invoice generation.`
* **Source Paragraph:**
  > "Step 11 — Settle (full payment): 1. When guests want to pay the full bill, tap Settle on the ticket. 2. Settle window opens: Settle — Table XX. 3. Total amount is shown clearly at the top. 4. Choose payment type: Cash, Card, Apple Pay, Voucher. 5. Enter received amount; system shows change. 6. Tap Settle / Print Final Invoice."
* **5 Action Step Bullets:**
  - `Tap Settle button on active ticket to open settlement modal`
  - `Select payment method: Cash, mada Card, or Digital Wallet`
  - `Enter cash received to automatically calculate customer change`
  - `Split ticket into equal parts or custom amounts if requested`
  - `Tap Complete Settlement to generate ZATCA fiscal receipt`
* **Live App Navigation Path:**
  1. Open active order or click `PAYMENTS` from sidebar
  2. Open Settle dialog for Table/Order
  3. Screenshot target: Payment settle modal with tender buttons and keypad
* **Screenshot File:** `project/screens/05_payments_settle.jpg`

---

```
====================================================================================================
SLIDE 10: POS-F01 — Takeaway & Drive-Thru Channels
====================================================================================================
```
* **PDF Reference:** Page 8, *Part F — Takeaway / drive-thru*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART F — QUICK SERVICE`
* **Heading:** `Takeaway & Drive-Thru Operations`
* **Body:** `Fast order capture for counter takeaway and drive-thru vehicle queues without table seating.`
* **Source Paragraph:**
  > "Part F — Takeaway / drive-thru: 1. From Home, tap Takeaway or Drive-thru. 2. Takeaway creates a ticket without a table number. 3. Enter customer name or token / buzzer number. 4. Add items and tap Settle immediately (or KOT if pay later). 5. Hand token to customer. When food is ready, call token."
* **5 Action Step Bullets:**
  - `Select Takeaway or Drive Thru directly from service launchpad`
  - `Assign customer name, phone number, or token buzzer ID`
  - `Add fast-food items and combo modifiers to quick ticket`
  - `Process immediate payment via Cash or contactless mada card`
  - `Hand pickup token to guest and dispatch preparation to kitchen`
* **Live App Navigation Path:**
  1. Click `TAKEAWAY` or `DRIVE` from sidebar/dashboard
  2. Screenshot target: Takeaway order screen with token queue
* **Screenshot File:** `project/screens/06_takeaway.jpg`

---

```
====================================================================================================
SLIDE 11: POS-H01 — Kitchen Display System (KDS)
====================================================================================================
```
* **PDF Reference:** Page 9, *Part H — Kitchen screen (Kitchen Manager)*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART H — KITCHEN OPERATIONS`
* **Heading:** `Kitchen Display & Station Routing`
* **Body:** `Live paperless kitchen order manager with ticket bumping, station filters, and 86 stock-outs.`
* **Source Paragraph:**
  > "Part H — Kitchen screen (Kitchen Manager / KDS): 1. Open Kitchen (KDS). 2. Orders appear as cards sorted by time (oldest first). 3. Filter by station: All, Kitchen, Grill, Bar / Drinks, Expo. 4. Tap an item or ticket to mark Started / Cooking. 5. Tap Ready / Done to bump the ticket off screen. 6. 86 / Out of stock: Kitchen Manager marks sold out items instantly."
* **5 Action Step Bullets:**
  - `Open KDS module to view incoming kitchen tickets in real time`
  - `Filter tickets by prep station: Grill, Fryer, Salad, or Bar`
  - `Monitor elapsed cook timers color-coded for fast SLA fulfillment`
  - `Tap ticket card to bump status from Cooking to Ready for Expo`
  - `Toggle 86 Out of Stock to instantly hide unavailable items on POS`
* **Live App Navigation Path:**
  1. Click `KOT` from sidebar or `Kitchen Display` card on Home
  2. Screenshot target: Kitchen display screen with live order cards
* **Screenshot File:** `project/screens/10_kitchen_kot.jpg`

---

```
====================================================================================================
SLIDE 12: POS-J01 — Day Close & Cash Drawer Reconciliation
====================================================================================================
```
* **PDF Reference:** Page 9, *Part J — Day close (Admin / authorised user)*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART J — FINANCIAL RECONCILIATION`
* **Heading:** `Daily Till Shift & Day Close`
* **Body:** `Mandatory end-of-day audit reconciling actual drawer cash against recorded POS ledger sales.`
* **Source Paragraph:**
  > "Part J — Day close (Admin / authorised user): 1. Ensure all open tables and delivery orders are settled. 2. Tap Day Close from Home. 3. Count physical cash in till drawer (SAR 500, SAR 100, SAR 50...). 4. Enter actual cash count in drawer reconciliation box. 5. System compares actual cash vs expected sales and highlights variance. 6. Tap Confirm Day Close to seal financial records and print Z-Report."
* **5 Action Step Bullets:**
  - `Verify all floor tables and delivery tickets are fully settled`
  - `Open Day Close module to initiate end-of-shift cash audit`
  - `Count drawer bank notes and coins by denomination into till count`
  - `Review automated variance between counted cash and POS ledger`
  - `Confirm Day Close to lock sales shift and generate Z-Report`
* **Live App Navigation Path:**
  1. Click `Day Close` button on Dashboard or sidebar
  2. Screenshot target: Day Close cash reconciliation dialog
* **Screenshot File:** `project/screens/03_main_dashboard.jpg` (or dedicated day close dialog)

---

```
====================================================================================================
SLIDE 13: POS-L01 — Settings: Business, Branches & ZATCA
====================================================================================================
```
* **PDF Reference:** Page 10, *Part L — Settings → Business (L1 to L4)*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART L — SETTINGS & COMPLIANCE`
* **Heading:** `Business Profile & ZATCA Phase 2`
* **Body:** `Configure legal entity details, restaurant branches, tax rates, and KSA e-invoicing compliance.`
* **Source Paragraph:**
  > "Part L — Settings → Business: L1. Company Details: Legal name, trade name, tax / VAT number (15 digits), branch address, commercial registration (CR). L2. ZATCA Settings: CSID cryptographic certificate, OTP from Fatoora portal, production mode toggle. L3. ZATCA invoices (queue): Monitor reported and cleared B2B/B2C invoices."
* **5 Action Step Bullets:**
  - `Open Settings module to configure restaurant business profile`
  - `Enter legal trade name, 15-digit VAT number, and CR number`
  - `Set branch addresses and contact information for receipt headers`
  - `Upload ZATCA CSID certificate and enter compliance OTP token`
  - `Monitor live ZATCA invoice queue for accepted B2B and B2C bills`
* **Live App Navigation Path:**
  1. Click `SETTINGS` on sidebar or `Settings` button on Dashboard
  2. Open `Company Details` / `Business` tab
  3. Screenshot target: Settings business configuration panel
* **Screenshot File:** `project/screens/15_settings.jpg`

---

```
====================================================================================================
SLIDE 14: POS-N01 — Settings: Products, Menu & Tax
====================================================================================================
```
* **PDF Reference:** Page 13–14, *Part N — Settings → Products (Catalog and pricing)*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART N — MENU MANAGEMENT`
* **Heading:** `Product Catalog & Menu Pricing`
* **Body:** `Manage restaurant menu categories, dish pricing, modifier groups, and 15% VAT tax application.`
* **Source Paragraph:**
  > "Part N — Settings → Products: 1. Food Categories: Starters, Main Course, Beverages, Desserts. 2. Products / Dishes: Name (English/Arabic), sales price, category, printer station. 3. Item Modifiers: Extras, spice levels, sugar levels. 4. Bulk Tax Update: Apply 15% VAT across all items in one click."
* **5 Action Step Bullets:**
  - `Navigate to Settings → Products to manage food catalog`
  - `Create menu categories with English and Arabic display names`
  - `Add dishes with selling prices, barcodes, and kitchen stations`
  - `Configure modifier groups for sizes, add-ons, and prep instructions`
  - `Execute Bulk Tax Update to ensure universal 15% VAT compliance`
* **Live App Navigation Path:**
  1. Click `MASTERS` or `SETTINGS` on sidebar
  2. Open Products catalog
  3. Screenshot target: Menu items and pricing catalog table
* **Screenshot File:** `project/screens/15_settings.jpg`

---

```
====================================================================================================
SLIDE 15: POS-R01 — Inventory, Recipes & Storage Transfers
====================================================================================================
```
* **PDF Reference:** Page 17–18, *Part R — Settings → Inventory (Stock modules)*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART R — STOCK MANAGEMENT`
* **Heading:** `Inventory, Recipes & Storage Transfers`
* **Body:** `Track raw ingredient stocks, vendor purchase orders, recipe yield deductions, and internal transfers.`
* **Source Paragraph:**
  > "Part R — Settings → Inventory: Open Settings → tab Inventory, or menu Stock. 1. Storage locations: Main Warehouse, Kitchen Store, Bar Store. 2. Purchase Orders (PO): Order ingredients from suppliers. 3. Receiving: Enter delivered quantities and unit costs. 4. Recipe deduction: Automatically subtract raw meat, vegetables, and oil upon dish sale. 5. Stock Master: Periodic physical count vs digital balance."
* **5 Action Step Bullets:**
  - `Access Stock module from sidebar to monitor ingredient counts`
  - `Define storage locations: Main Storage, Cold Room, Kitchen Prep`
  - `Create Purchase Orders and record supplier ingredient receiving`
  - `Link recipe BOM ingredients to automatically deduct upon sales`
  - `Perform weekly physical stock counts to track wastage variance`
* **Live App Navigation Path:**
  1. Click `STOCK` from left sidebar
  2. Screenshot target: Stock inventory master table and storage locations
* **Screenshot File:** `project/screens/11_stock_inventory.jpg`

---

```
====================================================================================================
SLIDE 16: POS-T01 — Business Intelligence & Financial Reports
====================================================================================================
```
* **PDF Reference:** Page 19, *Part T — Reports module (complete list)*
* **Slide Type:** Slide with Screenshot and Steps (Archetype 2)
* **Kicker:** `PART T — REPORTING & ANALYTICS`
* **Heading:** `Business Intelligence & Audit Reports`
* **Body:** `Comprehensive operational analytics, sales summaries, void audits, and tax liability reports.`
* **Source Paragraph:**
  > "Part T — Reports module: Open Menu → Reports. 1. Sales Summary: Total revenue, VAT collected, net sales by day/week/month. 2. Hourly Sales: Peak dining hours analysis. 3. Void / Cancel Audit: Trace cancelled items and manager authorizations. 4. Product Sales Ranking: Top-selling vs slow-moving menu items. 5. Payment Tender Report: Cash vs mada vs credit vs aggregator delivery revenue."
* **5 Action Step Bullets:**
  - `Open Reports module from sidebar for complete business analytics`
  - `Generate Daily Sales Summary with gross revenue and VAT totals`
  - `Analyze peak rush hours using the Hourly Sales Distribution chart`
  - `Inspect Void & Discount Audit logs to prevent cashier leakage`
  - `Export tender reconciliation reports for accounting and tax filing`
* **Live App Navigation Path:**
  1. Click `REPORTS` from left sidebar
  2. Screenshot target: Reports dashboard with date filter and sales summaries
* **Screenshot File:** `project/screens/14_reports.jpg`

---

```
====================================================================================================
SLIDE 17: POS-V01 — New Restaurant Go-Live Checklist
====================================================================================================
```
* **PDF Reference:** Page 20, *Part V — Full setup order checklist (recommended)*
* **Slide Type:** Informational Slide (Sub-type A: 4-Step Process Flow)
* **Kicker:** `PART V — IMPLEMENTATION`
* **Heading:** `New Restaurant Go-Live Checklist`
* **Source Paragraph:**
  > "Part V — Full setup order checklist (recommended): Follow this order to avoid missing dependencies: 1. Company & Tax (VAT / ZATCA). 2. Users & Roles (give passwords). 3. Tables & Floor areas. 4. Menu categories & Dishes. 5. Printers & KDS mapping. 6. Test order end-to-end: seat table, add item, send KOT, split bill, settle payment, print invoice."
* **Cards (4 Step Flow):**
  - **Card 01:** `Company & Legal Tax` — Register restaurant legal name, 15-digit VAT number, branch locations, and ZATCA Phase 2 credentials.
  - **Card 02:** `Users & Role Privileges` — Create staff user accounts, configure PIN passwords, and assign cashier/server role permissions.
  - **Card 03:** `Floor & Product Catalog` — Build floor layout zones, create table numbers, import food categories, dishes, and 15% VAT.
  - **Card 04:** `End-to-End Test Ticket` — Run test order: seat table, add food, route KOT, execute split payment, and verify invoice QR.
* **Screenshot Required:** None (4-Card Process Flow).

---

```
====================================================================================================
SLIDE 18: POS-W01 — Operational Troubleshooting Matrix
====================================================================================================
```
* **PDF Reference:** Page 20–21, *Part W — Common problems (all modules)*
* **Slide Type:** Informational Slide (Sub-type B: Information Board)
* **Kicker:** `PART W — TROUBLESHOOTING`
* **Heading:** `Common POS Problems & Solutions`
* **Subheading:** `Instant Remediation Protocols for Front-Line Restaurant Operations`
* **Theme Color:** `green`
* **Source Paragraph:**
  > "Part W — Common problems (all modules): 1. Screen shows Offline: check Wi-Fi, reboot router, orders still save locally. 2. Printer not printing: check paper roll, IP address in Settings. 3. Cannot settle bill: ensure total equals sum of tenders. 4. Void button disabled: requires manager PIN privilege. 5. Card payment declined: check SoftPOS reader pairing. 6. Report empty: verify date range filter."
* **Slide Structure (6 Grid Cards):**
  1. `[NETWORK]` **Offline Mode Notice:** Verify Wi-Fi or LAN cable. POS continues taking local orders; offline cache syncs automatically upon reconnect.
  2. `[PRINTER]` **KOT / Bill Not Printing:** Check thermal paper roll orientation, power switch, and verify printer IP mapping in Settings.
  3. `[SETTLE]` **Cannot Settle Bill:** Ensure tendered payment amount exactly matches or exceeds remaining balance before tapping OK.
  4. `[SECURITY]` **Void / Discount Disabled:** Front-line servers require Admin or Manager authorization PIN to cancel sent kitchen tickets.
  5. `[PAYMENTS]` **Card SoftPOS Declined:** Reconnect Bluetooth terminal, verify POS network bridge, or switch to manual card tender.
  6. `[REPORTS]` **Sales Report Shows Zero:** Check date/time range filter and ensure current cashier shift Day Open has completed sales.
* **Tip Pill:** `Contact Isarva 24/7 technical hotline for urgent on-site hardware or ZATCA gateway assistance.`
* **Screenshot Required:** None (Informational Board Layout).

---

## 4. Automated Next Steps: Generation Engine Architecture

The automated generation pipeline will run seamlessly via `uv` without requiring repetitive user intervention:

### Architecture Components:
1. **Automated Screen Grabber (`scripts/capture_all_screens.py`):**
   - Headless Edge automation via Playwright.
   - Automatically navigates `https://app.restaurant-pos.isarva.in/`, enters `C001`, logs in with `admin` / `0000`, switches to `H001 - Head Office`, and grabs all required UI screens in Full HD.
2. **Master Content Registry (`restaurant-app/app/content/slides_data.json`):**
   - Populated with the full slide definitions mapped above (POS-A01 through POS-W01).
3. **Batch Slide Compiler (`restaurant-app/app/main.py`):**
   - Enhanced with `--export-dir export/` flag.
   - Includes a visual progress bar (e.g. `[=================> ] 18/18 Slides (100%)`) displaying real-time slide compilation.
   - Generates Full HD `.jpg` slide frames directly into `export/`. Zero PPTX overhead.

### Windows Execution Commands:
```powershell
# 1. Capture all live application screenshots automatically
uv run --with playwright python scripts/capture_all_screens.py

# 2. Compile all slides with progress bar to export/ folder
uv run python restaurant-app/app/main.py --all --export-dir export
```
