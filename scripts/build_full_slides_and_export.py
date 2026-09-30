"""
Full POS Slide Generator for Isarva Restaurant POS.
Generates 100% pure 1920x1080 Full HD JPEG slides directly into export/
Covers all Parts A through Y from isarva-pos-userguide.pdf (26 total slides).
Displays an interactive progress bar and execution timing.
"""
import os
import sys
import time
import orjson

sys.stdout.reconfigure(encoding='utf-8')

# Set paths
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESTAURANT_APP_DIR = os.path.join(WORKSPACE_DIR, "restaurant-app")
APP_DIR = os.path.join(RESTAURANT_APP_DIR, "app")
EXPORT_DIR = os.path.join(WORKSPACE_DIR, "export")
os.makedirs(EXPORT_DIR, exist_ok=True)

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from src.screen_composer import compose_pc_screen
from src.preview_renderer import render_slide_preview
from src.info_renderer import render_info_slide
from src.scrubber import scrub_screenshot

# Master 26-Slide Catalog covering Part A through Part Y
FULL_SLIDES = {
    # Part A
    "POS-A01": {
        "section": "POS-A01",
        "layout": "info",
        "kicker": "PART A — BEFORE YOU START",
        "heading": "Prerequisites & Hardware Setup",
        "cards": [
            {
                "step": "01",
                "title": "Hardware & Network",
                "description": "Prepare PC, laptop or tablet running Google Chrome or Edge with stable internet connection.",
                "icon": "monitor"
            },
            {
                "step": "02",
                "title": "Company Credentials",
                "description": "Obtain registered Company Code (e.g. C001) and Admin username/password provided by Isarva.",
                "icon": "key"
            },
            {
                "step": "03",
                "title": "Business Details",
                "description": "Have restaurant legal trade name, 15-digit VAT number, and branch address documentation ready.",
                "icon": "doc_tax"
            },
            {
                "step": "04",
                "title": "Security & Offline",
                "description": "Keep passwords confidential. System continues taking orders offline and syncs upon reconnection.",
                "icon": "shield_lock"
            }
        ]
    },

    # Part B — Step 1 & 2
    "POS-B01": {
        "section": "POS-B01",
        "screen_filename": "01_activate_pos.jpg",
        "crop_align": "left",
        "kicker": "PART B — FIRST-TIME SETUP",
        "heading": "Activate This POS Till",
        "body": "Permanently bind this browser terminal to your restaurant using the authorized company code.",
        "bullets": [
            "Navigate to official application URL in Chrome or Edge",
            "Locate Activate POS card on the initial landing screen",
            "Enter registered Company Code C001 in the input box",
            "Tap Activate POS button to bind hardware to restaurant",
            "Confirm restaurant legal name is displayed on screen"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part B — Step 3
    "POS-B02": {
        "section": "POS-B02",
        "screen_filename": "02_admin_login.jpg",
        "crop_align": "left",
        "kicker": "PART B — FIRST-TIME SETUP",
        "heading": "Sign In with Admin PIN",
        "body": "Authenticate staff and manager credentials using the on-screen numeric keypad or keyboard.",
        "bullets": [
            "Enter designated staff username into the Username field",
            "Type security PIN or password using physical or touch keypad",
            "Tap Show PIN button if password verification is required",
            "Tap orange OK button to authenticate and unlock system",
            "Access role-authorized POS dashboard and till controls"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part B — Step 4 & 5
    "POS-B03": {
        "section": "POS-B03",
        "screen_filename": "03_main_dashboard.jpg",
        "crop_align": "left",
        "kicker": "CORE DASHBOARD",
        "heading": "Main Restaurant Dashboard",
        "body": "Central command center displaying live till sales, kitchen queues, and quick order launch pads.",
        "bullets": [
            "Verify assigned till branch H001 - Head Office at top bar",
            "Monitor live metrics: Open Tables, Billing, and Kitchen Queue",
            "Switch bilingual interface between English and Arabic",
            "Launch front-of-house services: Dine In, Takeaway, Drive Thru",
            "Access back-office tools: Day Close, Expenses, and Settings"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part C
    "POS-C01": {
        "section": "POS-C01",
        "layout": "info",
        "kicker": "PART C — DAILY OPERATIONS",
        "heading": "Morning Opening Checklist",
        "cards": [
            {
                "step": "01",
                "title": "Hardware Power On",
                "description": "Power on POS terminals, receipt printers, kitchen display units, and verify router Wi-Fi.",
                "icon": "power"
            },
            {
                "step": "02",
                "title": "Branch Verification",
                "description": "Log into POS and confirm top header displays correct branch: H001 - Head Office.",
                "icon": "storefront"
            },
            {
                "step": "03",
                "title": "Network Health",
                "description": "Ensure green Connected badge is active. Offline mode activates automatically if network drops.",
                "icon": "wifi"
            },
            {
                "step": "04",
                "title": "Opening Cash Float",
                "description": "Open Day Open module, count till physical float cash, enter starting SAR amount, and begin.",
                "icon": "cash_money"
            }
        ]
    },

    # Part D — Step 1-3
    "POS-D01": {
        "section": "POS-D01",
        "screen_filename": "04_floor_tickets.jpg",
        "crop_align": "left",
        "kicker": "PART D — FLOOR TICKETS",
        "heading": "Interactive Table Seating Floor Plan",
        "body": "Select dining zones, seat guests on interactive floor tables, and build order tickets.",
        "bullets": [
            "Open Dine In or Floor service from the main dashboard",
            "Switch between Architectural Diagram and Table List view",
            "Monitor dining zones: Main Hall, Family Section, Outdoor",
            "Check real-time table status: Free, Occupied, and Billing",
            "Tap any vacant table to seat guests and launch order ticket"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part D — Step 4-5
    "POS-D02": {
        "section": "POS-D02",
        "layout": "info",
        "kicker": "PART D — FLOOR TICKETS",
        "heading": "Discounts & Extra Charges",
        "subheading": "Configurable Order Adjustments & Legal VAT Calculations",
        "theme_color": "green",
        "style": "board",
        "items": [
            {
                "title": "Preset Discount Pills",
                "description": "Apply quick percentage discounts (0%, 7%, 10%) directly on the order ticket based on staff privileges.",
                "tag": "DISCOUNT"
            },
            {
                "title": "Custom Discount SAR",
                "description": "Authorized managers can enter custom flat SAR discount values or special customer concessions.",
                "tag": "MANAGER"
            },
            {
                "title": "Extra Service Charges",
                "description": "Toggle optional service fees, valet parking, or private dining charges configured in Settings.",
                "tag": "CHARGES"
            },
            {
                "title": "15% VAT Display",
                "description": "Every ticket clearly itemizes Net Subtotal, Discount, Extra Charges, and 15% VAT breakdown.",
                "tag": "VAT 15%"
            },
            {
                "title": "Item-Level Voiding",
                "description": "Void un-sent items instantly; sent kitchen items require manager PIN authorization to delete.",
                "tag": "SECURITY"
            },
            {
                "title": "Audit Tracking",
                "description": "All discounts, voids, and waivers are permanently logged for financial audit reporting.",
                "tag": "AUDIT"
            }
        ],
        "tip_note": "Tax rates cannot be edited manually on the floor; updates are managed in Settings -> Tax."
    },

    # Part D — Step 6-7
    "POS-D03": {
        "section": "POS-D03",
        "layout": "info",
        "kicker": "PART D — FLOOR TICKETS",
        "heading": "Order Routing & Kitchen Flow",
        "cards": [
            {
                "step": "01",
                "title": "Save Order",
                "description": "Save current open ticket to floor map without sending preparation instructions to kitchen.",
                "icon": "save_disk"
            },
            {
                "step": "02",
                "title": "KOT to Screen",
                "description": "Tap KOT to dispatch items electronically to Kitchen Display Screens (KDS) paperlessly.",
                "icon": "kds_screen"
            },
            {
                "step": "03",
                "title": "KOT & Print",
                "description": "Send items to kitchen screens AND trigger thermal paper ticket printing at cooking stations.",
                "icon": "kitchen_printer"
            },
            {
                "step": "04",
                "title": "Save & Bill Preview",
                "description": "Print interim guest check slip for customer review prior to final payment settlement.",
                "icon": "bill_preview"
            }
        ]
    },

    # Part D — Step 8-10
    "POS-D04": {
        "section": "POS-D04",
        "layout": "info",
        "kicker": "PART D — FLOOR TICKETS",
        "heading": "Table Management & Order Transfers",
        "cards": [
            {
                "step": "01",
                "title": "Change Table",
                "description": "Move active guest orders to another vacant table when customers switch dining locations.",
                "icon": "table_move"
            },
            {
                "step": "02",
                "title": "Merge Tables",
                "description": "Combine multiple seated tables into a single unified ticket when guest parties join together.",
                "icon": "table_merge"
            },
            {
                "step": "03",
                "title": "Split Initiator",
                "description": "Initiate split bill directly from floor ticket to prepare multi-guest payment settlements.",
                "icon": "bill_split"
            },
            {
                "step": "04",
                "title": "Table Area Switch",
                "description": "Switch seamlessly between Main Dining Hall, Outdoor Terrace, and Family Section views.",
                "icon": "floor_zones"
            }
        ]
    },

    # Part E — Overview
    "POS-E01": {
        "section": "POS-E01",
        "layout": "info",
        "kicker": "PART E — SETTLE MODAL",
        "heading": "Flexible Payment & Settlement Hub",
        "subheading": "ISO/IEC 27001:2022 Certified Multi-Tender & Split Reconciliation",
        "theme_color": "blue",
        "style": "board",
        "items": [
            {
                "title": "One-Touch Fast Settle",
                "description": "Tap 'Rest -> Cash', 'Rest -> mada', or 'Rest -> Apple Pay' to settle entire balance in 1 click.",
                "tag": "FAST PAY"
            },
            {
                "title": "Equal Split",
                "description": "Divide ticket evenly across 2, 3, 4+ guests. Collect each portion via individual cash or card tenders.",
                "tag": "EQUAL"
            },
            {
                "title": "Custom Tender Split",
                "description": "Combine multiple tenders: e.g. SAR 150 Cash + remaining SAR 85 balance via mada debit card.",
                "tag": "CUSTOM"
            },
            {
                "title": "Food Vouchers",
                "description": "Enter promotional voucher code. System validates eligibility and deducts credit immediately.",
                "tag": "VOUCHER"
            },
            {
                "title": "Gift Cards & Loyalty",
                "description": "Redeem stored value gift cards or customer CRM loyalty points directly against amount due.",
                "tag": "LOYALTY"
            },
            {
                "title": "Integrated SoftPOS",
                "description": "Hardware bridge communicates directly with payment terminals for secure contactless processing.",
                "tag": "SOFTPOS"
            }
        ],
        "tip_note": "Confirm payment button unlocks exclusively when Remaining balance reaches exactly SAR 0.00."
    },

    # Part E — Step 11
    "POS-E02": {
        "section": "POS-E02",
        "screen_filename": "05_payments_settle.jpg",
        "crop_align": "left",
        "kicker": "PART E — PAYMENTS",
        "heading": "Order Settlement & Tender Screen",
        "body": "Finalize customer tickets with multi-tender payment methods and instant invoice generation.",
        "bullets": [
            "Tap Settle button on active ticket to open settlement modal",
            "Select payment method: Cash, mada Card, or Digital Wallet",
            "Enter cash received to automatically calculate customer change",
            "Split ticket into equal parts or custom amounts if requested",
            "Tap Complete Settlement to generate ZATCA fiscal receipt"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part E — Vouchers & Cards
    "POS-E03": {
        "section": "POS-E03",
        "layout": "info",
        "kicker": "PART E — SETTLE MODAL",
        "heading": "Vouchers, Gift Cards & Loyalty Points",
        "cards": [
            {
                "step": "01",
                "title": "Food Vouchers",
                "description": "Create promotional vouchers in Settings. Enter code at checkout for automated bill deduction.",
                "icon": "coupon_percent"
            },
            {
                "step": "02",
                "title": "Prepaid Gift Cards",
                "description": "Issue customer gift cards with balance tracking. Swipe or enter card serial number on settle.",
                "icon": "gift_card"
            },
            {
                "step": "03",
                "title": "CRM Loyalty Points",
                "description": "Look up customer profile by mobile number to redeem accumulated loyalty points for cash discounts.",
                "icon": "loyalty_star"
            },
            {
                "step": "04",
                "title": "SoftPOS Terminal",
                "description": "Push invoice totals directly to countertop or mobile SoftPOS card readers over local network.",
                "icon": "pos_terminal"
            }
        ]
    },

    # Part F & G
    "POS-FG01": {
        "section": "POS-FG01",
        "screen_filename": "06_takeaway.jpg",
        "crop_align": "left",
        "kicker": "PART F & G — CHANNELS",
        "heading": "Takeaway, Drive-Thru & Aggregators",
        "body": "Fast order capture for counter takeaway, car pickup, and integrated delivery aggregator orders.",
        "bullets": [
            "Select Takeaway or Drive Thru directly from service launchpad",
            "Assign customer name, phone number, or token buzzer ID",
            "Add fast-food items and combo modifiers to quick ticket",
            "Receive online aggregator orders (HungerStation, Jahez, Keeta)",
            "Process immediate payment and dispatch order to kitchen"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part H & I
    "POS-HI01": {
        "section": "POS-HI01",
        "screen_filename": "10_kitchen_kot.jpg",
        "crop_align": "left",
        "kicker": "PART H & I — KITCHEN & RIDERS",
        "heading": "Kitchen Display & Rider Dispatch",
        "body": "Paperless kitchen display system with order bumping, station filters, and delivery rider handoff.",
        "bullets": [
            "Open KDS module to view incoming kitchen tickets in real time",
            "Filter tickets by prep station: Grill, Fryer, Salad, or Bar",
            "Monitor elapsed cook timers color-coded for fast SLA fulfillment",
            "Tap ticket card to bump status from Cooking to Ready for Expo",
            "Assign prepared delivery parcels to active mobile delivery riders"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part J & P
    "POS-JP01": {
        "section": "POS-JP01",
        "screen_filename": "03_main_dashboard.jpg",
        "crop_align": "left",
        "kicker": "PART J & P — DAY CLOSE",
        "heading": "Daily Till Shift & Cash Reconciliation",
        "body": "Mandatory end-of-day audit reconciling actual drawer cash against recorded POS ledger sales.",
        "bullets": [
            "Verify all floor tables and delivery tickets are fully settled",
            "Open Day Close module to initiate end-of-shift cash audit",
            "Count drawer bank notes and coins by denomination into till count",
            "Review automated variance between counted cash and POS ledger",
            "Confirm Day Close to lock sales shift and generate Z-Report"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part K & L
    "POS-KL01": {
        "section": "POS-KL01",
        "screen_filename": "15_settings.jpg",
        "crop_align": "left",
        "kicker": "PART K & L — SETTINGS",
        "heading": "Business Profile & ZATCA Phase 2",
        "body": "Configure legal entity details, restaurant branches, tax rates, and KSA e-invoicing compliance.",
        "bullets": [
            "Open Settings module to configure restaurant business profile",
            "Enter legal trade name, 15-digit VAT number, and CR number",
            "Set branch addresses and contact information for receipt headers",
            "Upload ZATCA CSID certificate and enter compliance OTP token",
            "Monitor live ZATCA invoice queue for accepted B2B and B2C bills"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part M
    "POS-M01": {
        "section": "POS-M01",
        "layout": "info",
        "kicker": "PART M — SETTINGS",
        "heading": "Printer Configuration & Mapping",
        "cards": [
            {
                "step": "01",
                "title": "Receipt Printers",
                "description": "Configure counter thermal receipt printers with ESC/POS LAN IP addresses and paper cut options.",
                "icon": "receipt_printer"
            },
            {
                "step": "02",
                "title": "KOT Station Printers",
                "description": "Set up independent kitchen printers for Hot Kitchen, Cold Kitchen, Sushi Bar, and Beverage Bar.",
                "icon": "kitchen_printer"
            },
            {
                "step": "03",
                "title": "Printer Mapping",
                "description": "Map menu departments to specific printers: e.g. Burgers -> Kitchen, Drinks -> Juice Bar.",
                "icon": "network_routing"
            },
            {
                "step": "04",
                "title": "Receipt Header & Footer",
                "description": "Customize invoice headers with logo, VAT registration, Arabic notes, and ZATCA QR codes.",
                "icon": "slip_template"
            }
        ]
    },

    # Part N
    "POS-N01": {
        "section": "POS-N01",
        "screen_filename": "05_menu_catalog_ticket.jpg",
        "crop_align": "left",
        "kicker": "PART N — MENU CATALOG",
        "heading": "Food Menu & Order Ticket Builder",
        "body": "Browse dish categories, customize item add-ons, and build order tickets with live VAT breakdown.",
        "bullets": [
            "Browse menu categories: Starters, Mains, Soups, Salads",
            "Select dishes with selling prices and custom modifiers",
            "Review real-time ticket subtotals and 15% VAT calculation",
            "Dispatch food orders directly to kitchen display or printers",
            "Proceed to Settle for cash, card, or split payment processing"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part O
    "POS-O01": {
        "section": "POS-O01",
        "layout": "info",
        "kicker": "PART O — SETTINGS",
        "heading": "Staff Accounts & Role Privileges",
        "subheading": "ISO/IEC 27001:2022 Granular Access Control & Security Policies",
        "theme_color": "green",
        "style": "board",
        "items": [
            {
                "title": "Restaurant Admin",
                "description": "Full system permissions: menu pricing, tax updates, user management, day close, and Z-reports.",
                "tag": "ADMIN"
            },
            {
                "title": "Cashier",
                "description": "Order creation, tender settlement, split bills, customer receipts, and shift cash float drawer counts.",
                "tag": "CASHIER"
            },
            {
                "title": "Food Server / Waiter",
                "description": "Table seating, ticket taking, kitchen KOT dispatch, modifiers, and guest bill check printing.",
                "tag": "WAITER"
            },
            {
                "title": "Kitchen Manager",
                "description": "KDS screen access, order preparation bumping, station filters, and 86 out-of-stock item toggling.",
                "tag": "KITCHEN"
            },
            {
                "title": "Delivery Rider",
                "description": "Mobile app login with last 4 phone digits, parcel assignment, order tracking, and COD reconciliation.",
                "tag": "RIDER"
            },
            {
                "title": "Manager Authorization",
                "description": "Protected operations (order voiding, discounts > 10%, price overrides) enforce manager PIN entry.",
                "tag": "PIN LOCK"
            }
        ],
        "tip_note": "Never share admin passwords; each employee must operate under a unique staff username and PIN."
    },

    # Part Q & R
    "POS-QR01": {
        "section": "POS-QR01",
        "screen_filename": "11_stock_inventory.jpg",
        "crop_align": "left",
        "kicker": "PART Q & R — INVENTORY",
        "heading": "Inventory, Recipes & Storage Control",
        "body": "Track raw ingredient stocks, vendor purchase orders, recipe yield deductions, and internal transfers.",
        "bullets": [
            "Access Stock module from sidebar to monitor ingredient counts",
            "Define storage locations: Main Storage, Cold Room, Kitchen Prep",
            "Create Purchase Orders and record supplier ingredient receiving",
            "Link recipe BOM ingredients to automatically deduct upon sales",
            "Perform weekly physical stock counts to track wastage variance"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part S
    "POS-S01": {
        "section": "POS-S01",
        "layout": "info",
        "kicker": "PART S — SETTINGS",
        "heading": "Database Backup & Safety Directives",
        "cards": [
            {
                "step": "01",
                "title": "Catalog Export",
                "description": "Export complete menu catalog, products, and customer profiles into secure Excel/CSV files.",
                "icon": "export_arrow"
            },
            {
                "step": "02",
                "title": "Catalog Import",
                "description": "Bulk import new menu items and prices safely using official Isarva spreadsheet templates.",
                "icon": "import_arrow"
            },
            {
                "step": "03",
                "title": "Automated Backups",
                "description": "Cloud-synchronized encrypted backups secure transactional data under ISO 27001 standards.",
                "icon": "cloud_sync"
            },
            {
                "step": "04",
                "title": "Safe Data Cleaning",
                "description": "Restricted to authorized administrators. Cleaning tools permanently purge old test bills only.",
                "icon": "db_clean"
            }
        ]
    },

    # Part T
    "POS-T01": {
        "section": "POS-T01",
        "screen_filename": "14_reports.jpg",
        "crop_align": "left",
        "kicker": "PART T — REPORTING",
        "heading": "Business Intelligence & Audit Reports",
        "body": "Comprehensive operational analytics, sales summaries, void audits, and tax liability reports.",
        "bullets": [
            "Open Reports module from sidebar for complete business analytics",
            "Generate Daily Sales Summary with gross revenue and VAT totals",
            "Analyze peak rush hours using the Hourly Sales Distribution chart",
            "Inspect Void & Discount Audit logs to prevent cashier leakage",
            "Export tender reconciliation reports for accounting and tax filing"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part U
    "POS-U01": {
        "section": "POS-U01",
        "screen_filename": "03_main_dashboard.jpg",
        "crop_align": "left",
        "kicker": "PART U — DAILY MODULES",
        "heading": "Front-of-House Navigation Hub",
        "body": "Quick access across all daily operational modules, customer profiles, barcodes, and shifts.",
        "bullets": [
            "Access Customer directory for CRM profiles and contact history",
            "Use Barcode scanning mode for rapid retail packaging checkout",
            "Review Unsettled orders table to verify pending dine-in checks",
            "Monitor live queue counters for cooking tickets and open tables",
            "Track employee attendance time clock and staff working hours"
        ],
        "ending": "",
        "scrub_rules": []
    },

    # Part V
    "POS-V01": {
        "section": "POS-V01",
        "layout": "info",
        "kicker": "PART V — IMPLEMENTATION",
        "heading": "New Restaurant Go-Live Checklist",
        "cards": [
            {
                "step": "01",
                "title": "Company & Legal Tax",
                "description": "Register restaurant legal name, 15-digit VAT number, branch locations, and ZATCA Phase 2 credentials.",
                "icon": "tax_gov"
            },
            {
                "step": "02",
                "title": "Users & Role Privileges",
                "description": "Create staff user accounts, configure PIN passwords, and assign cashier/server role permissions.",
                "icon": "team_roles"
            },
            {
                "step": "03",
                "title": "Floor & Product Catalog",
                "description": "Build floor layout zones, create table numbers, import food categories, dishes, and 15% VAT.",
                "icon": "menu_book"
            },
            {
                "step": "04",
                "title": "End-to-End Test Ticket",
                "description": "Run test order: seat table, add food, route KOT, execute split payment, and verify invoice QR.",
                "icon": "test_checklist"
            }
        ]
    },

    # Part W
    "POS-W01": {
        "section": "POS-W01",
        "layout": "info",
        "kicker": "PART W — TROUBLESHOOTING",
        "heading": "Common POS Problems & Solutions",
        "subheading": "Instant Field Remediation Protocols for Front-Line Restaurant Operations",
        "theme_color": "green",
        "style": "board",
        "items": [
            {
                "title": "Offline Mode Notice",
                "description": "Verify Wi-Fi or LAN cable. POS continues taking local orders; offline cache syncs automatically.",
                "tag": "NETWORK"
            },
            {
                "title": "KOT / Bill Not Printing",
                "description": "Check thermal paper roll orientation, power switch, and verify printer IP mapping in Settings.",
                "tag": "PRINTER"
            },
            {
                "title": "Cannot Settle Bill",
                "description": "Ensure tendered payment amount exactly matches or exceeds remaining balance before tapping OK.",
                "tag": "SETTLE"
            },
            {
                "title": "Void / Discount Disabled",
                "description": "Front-line servers require Admin or Manager authorization PIN to cancel sent kitchen tickets.",
                "tag": "SECURITY"
            },
            {
                "title": "Card SoftPOS Declined",
                "description": "Reconnect Bluetooth terminal, verify POS network bridge, or switch to manual card tender.",
                "tag": "PAYMENTS"
            },
            {
                "title": "Sales Report Shows Zero",
                "description": "Check date/time range filter and ensure current cashier shift Day Open has completed sales.",
                "tag": "REPORTS"
            }
        ],
        "tip_note": "Contact Isarva 24/7 technical hotline for urgent on-site hardware or ZATCA gateway assistance."
    },

    # Part X & Y
    "POS-XY01": {
        "section": "POS-XY01",
        "layout": "info",
        "kicker": "PART X & Y — CLOSING & SECURITY",
        "heading": "Nightly Closing & Data Security Rules",
        "subheading": "Mandatory ISO/IEC 27001:2022 End-of-Day Operating Directives",
        "theme_color": "green",
        "style": "board",
        "items": [
            {
                "title": "Settle Open Orders",
                "description": "Ensure zero open tables, pending takeaway checks, or active delivery tickets remain unsettled.",
                "tag": "CLOSING"
            },
            {
                "title": "Till Drawer Audit",
                "description": "Count actual drawer currency, enter counts in Day Close, record variance, and print Z-Report.",
                "tag": "FINANCIAL"
            },
            {
                "title": "Sync & Cloud Backup",
                "description": "Verify all offline cash records are synchronized to central cloud servers before turning off till.",
                "tag": "SYNC"
            },
            {
                "title": "Cardholder Privacy",
                "description": "Strictly prohibited: Never write down or store customer payment card numbers or CVV codes.",
                "tag": "SECURITY"
            },
            {
                "title": "Hardware Shutdown",
                "description": "Log out user sessions, shut down thermal printers, and turn off terminal display safely.",
                "tag": "SHUTDOWN"
            },
            {
                "title": "Compliance Archive",
                "description": "File signed daily Z-Reports and merchant credit card transaction batches for accounting audits.",
                "tag": "AUDIT"
            }
        ],
        "tip_note": "All system activity is cryptographically logged under ISO/IEC 27001 data protection protocols."
    }
}

def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 35):
    """Draws a responsive progress bar in terminal."""
    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled_len = int(length * iteration // total)
    bar = '=' * filled_len + '>' if filled_len < length else '=' * length
    bar = bar.ljust(length, '-')
    print(f"\r{prefix} [{bar}] {percent}% {suffix}", end='', flush=True)
    if iteration == total:
        print()

def generate_all_export_slides():
    t_start = time.perf_counter()
    total_slides = len(FULL_SLIDES)
    print("=" * 80)
    print(f"ISARVA RESTAURANT POS — FULL HD (1920x1080) JPEG SLIDE BATCH GENERATOR")
    print(f"Target Output Directory: {EXPORT_DIR}")
    print(f"Total Slides to Generate: {total_slides} (Covering Parts A through Y)")
    print("=" * 80)

    # Save to slides_data.json & pos_slides_data.json for persistence
    content_dir = os.path.join(APP_DIR, "content")
    pos_file = os.path.join(content_dir, "pos_slides_data.json")
    with open(pos_file, "wb") as f:
        f.write(orjson.dumps(FULL_SLIDES, option=orjson.OPT_INDENT_2))

    # Assets
    bg_trans_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "complete-design-format", "Only-background-transparent.png")
    pc_frame_path = os.path.join(RESTAURANT_APP_DIR, "Libraries", "Parts", "PC-Screen.png")
    check_icon_path = os.path.join(APP_DIR, "brand_check_icon.png")
    fonts_dir = os.path.join(APP_DIR, "fonts")
    screens_dir = os.path.join(RESTAURANT_APP_DIR, "project", "screens")

    generated_files = []
    
    for idx, (slide_id, slide_data) in enumerate(FULL_SLIDES.items(), start=1):
        t0 = time.perf_counter()
        heading = slide_data.get("heading", slide_id).strip()
        safe_heading = heading.lower().replace(" ", "-").replace("&", "and").replace("?", "").replace(":", "").replace("(", "").replace(")", "").replace("/", "-").replace("--", "-").strip("-")
        out_filename = f"{slide_id}-{safe_heading}.jpg"
        out_path = os.path.join(EXPORT_DIR, out_filename)

        layout = slide_data.get("layout", "screenshot")

        if layout == "info" or not slide_data.get("screen_filename"):
            # Informational Slide
            render_info_slide(
                content=slide_data,
                fonts_dir=fonts_dir,
                output_path=out_path
            )
            slide_type_str = "Info Flow" if slide_data.get("cards") else "Info Board"
        else:
            # Screenshot Slide
            screen_name = slide_data.get("screen_filename")
            screen_path = os.path.join(screens_dir, screen_name)
            if not os.path.exists(screen_path):
                # Fallback to root project/screens
                screen_path = os.path.join(WORKSPACE_DIR, "project", "screens", screen_name)
                
            scrub_rules = slide_data.get("scrub_rules", [])
            scrubbed_img = scrub_screenshot(screen_path, rules=scrub_rules)
            crop_align = slide_data.get("crop_align", "left")
            mockup_img = compose_pc_screen(
                scrubbed_img,
                pc_frame_path,
                crop_top_only=True,
                crop_align=crop_align
            )
            render_slide_preview(
                content=slide_data,
                bg_path=bg_trans_path,
                pc_mockup=mockup_img,
                check_icon_path=check_icon_path,
                fonts_dir=fonts_dir,
                output_path=out_path
            )
            slide_type_str = f"Screenshot ({screen_name})"

        dur_ms = (time.perf_counter() - t0) * 1000
        generated_files.append((slide_id, heading, out_filename, out_path, dur_ms, slide_type_str))
        
        # Terminal Progress Update
        status_line = f"[{idx:02d}/{total_slides:02d}] {slide_id}: {heading[:32]} ({slide_type_str}) - {dur_ms:.0f}ms"
        print_progress_bar(idx, total_slides, prefix='Progress:', suffix=f'({idx}/{total_slides})', length=25)
        print(f"   [OK] {status_line}", flush=True)

    total_time = time.perf_counter() - t_start
    print("\n" + "=" * 80)
    print(f"BATCH GENERATION COMPLETE in {total_time:.2f}s!")
    print(f"Total Slides: {len(generated_files)} Full HD JPEG files")
    print(f"Output Location: {EXPORT_DIR}")
    print("=" * 80)
    
    for sid, h, fname, fpath, dur, stype in generated_files:
        print(f" * [{sid}] {h} -> {fname} ({dur:.0f}ms)")

if __name__ == "__main__":
    generate_all_export_slides()
