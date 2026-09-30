# Antigravity (agy) Prompt Instruction: Generate Isarva Restaurant POS Presentation Slide & Query AI Knowledge Base

## Objective
Generate brand-compliant 1920x1080 Full HD presentation slides (`.jpg`) and execute sub-millisecond AI search queries for the **Isarva Restaurant POS** system based on the official Customer User Guide `project/userguide/isarva-pos-userguide.pdf` (Document: `ISARVA-CG-001` v1.2, ISO/IEC 27001:2022 compliant).

---

## Step-by-Step Execution Workflow

### Step 1: Research Content via Fast AI Index
1. Use the pre-built sub-millisecond AI search engine instead of reading the raw 22-page PDF:
   ```powershell
   & ".\app\.venv\Scripts\python.exe" app\search.py "<TOPIC_OR_FEATURE>"
   ```
   *For role-specific context:*
   ```powershell
   & ".\app\.venv\Scripts\python.exe" app\search.py --role "Food Server" "merge tables"
   ```
   *For instant troubleshooting lookups:*
   ```powershell
   & ".\app\.venv\Scripts\python.exe" app\search.py --troubleshoot "tax looks wrong"
   ```
2. Formulate slide elements:
   - **Kicker:** Module / Part title in uppercase (e.g. `"PART D — FLOOR TICKETS"`, `"PART E — SETTLE MODAL"`, `"PART W — TROUBLESHOOTING"`).
   - **Heading:** Clean descriptive title without numerical noise (e.g. `"Dine-In Order & Kitchen Flow"`, `"Flexible Payment & Split Settlement"`).
   - **Subheading:** (For Board slides) High-level context or standard reference (e.g. `"ISO/IEC 27001:2022 Certified Architecture · Version 1.2"`).
   - **Body / Summary:** 1–2 concise sentences summarizing the workflow.
   - **Bullets:** Exactly 5 single-line action-oriented bullet points starting with strong verbs (*Seat, Add, Send, Settle, Verify*). Keep each bullet strictly within 50–65 characters.
   - **Ending:** Always `""` (empty string) to prevent circular background overflow.

---

### Step 2: Register Slide in `app/content/slides_data.json`

**Type A: Information Board Slide (Recommended for Modules, Overviews & Troubleshooting)**
```json
"POS-X.X": {
  "section": "POS-X.X",
  "layout": "info",
  "style": "board",
  "theme_color": "green",
  "kicker": "CUSTOMER USER GUIDE",
  "heading": "Isarva Restaurant POS",
  "subheading": "Complete System Architecture & Daily Operations",
  "items": [
    {
      "title": "<Card 1 Title>",
      "description": "<Card 1 Description>",
      "tag": "SETUP"
    },
    {
      "title": "<Card 2 Title>",
      "description": "<Card 2 Description>",
      "tag": "FLOOR"
    }
  ],
  "tip_note": "Application URL: https://app.restaurant-pos.isarva.in · ISO 27001 compliant."
}
```

**Type B: 4-Step Process Flow Slide (Recommended for Step-by-Step Sequences)**
```json
"POS-X.X": {
  "section": "POS-X.X",
  "layout": "info",
  "kicker": "PART D — FLOOR TICKETS",
  "heading": "Dine-In Order & Kitchen Flow",
  "cards": [
    {
      "step": "01",
      "title": "Seat & Add Dishes",
      "description": "Select guest table from floor map, pick categories, add dishes with custom kitchen preparation notes."
    },
    {
      "step": "02",
      "title": "Send KOT to Kitchen",
      "description": "Tap KOT (or KOT & Print) to route items instantly to kitchen display stations and KOT printers."
    },
    {
      "step": "03",
      "title": "Discounts & Charges",
      "description": "Apply discount percentage pills (0%, 7%, 10%) or toggle extra charges (service fee, parking) as authorized."
    },
    {
      "step": "04",
      "title": "Save & Bill Preview",
      "description": "Tap Save & Bill to generate interim guest check slip for review before proceeding to final settlement."
    }
  ]
}
```

**Type C: UI Screenshot Slide (Left Monitor Frame + Right Text)**
```json
"POS-X.X": {
  "section": "POS-X.X",
  "screen_filename": "<SCREENSHOT_NAME>.jpg",
  "crop_align": "left",
  "kicker": "FLOOR TICKETS",
  "heading": "Table Order Screen",
  "body": "Manage dine-in seating, menu selection, guest counts, and kitchen tickets.",
  "bullets": [
    "Select guest table on interactive floor map",
    "Add dish items with custom modifier notes",
    "Send pending items directly to kitchen via KOT",
    "Preview interim guest bill with Save & Bill",
    "Proceed to Settle window when dining finishes"
  ],
  "ending": "",
  "scrub_rules": []
}
```

---

### Step 3: Run the Slide Generator
Execute the Python engine using the local virtual environment:
```powershell
# Generate specific slide
& ".\app\.venv\Scripts\python.exe" app\main.py --slide "POS-1.0"

# List all available configured slides
& ".\app\.venv\Scripts\python.exe" app\main.py --list

# Batch generate all slides
& ".\app\.venv\Scripts\python.exe" app\main.py --all
```

---

### Step 4: Verify and Register Slide
1. **Output location:** Check `output/<slide_id>-<name>.jpg` (e.g. `output/POS-1.0-isarva-restaurant-pos.jpg`).
2. Update the slide registry table in `CONTEXT.md`.
3. Use `view_file` to inspect output if requested.
