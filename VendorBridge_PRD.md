# VendorBridge — Product Requirements Document (PRD)
## Procurement & Vendor Management ERP
**Event:** Odoo × KSV Hackathon 2026  
**Build Duration:** 8 Hours (Strict)  
**Version:** 1.0  
**Date:** June 6, 2026  
**Status:** Ready for Development

---

## 1. Executive Summary

### 1.1 Product Vision
VendorBridge is a **Procurement & Vendor Management ERP** that digitizes and automates the entire procurement lifecycle — from vendor registration and RFQ creation to quotation comparison, approval workflows, purchase order generation, invoicing, and analytics.

### 1.2 Problem Statement
Organizations currently manage procurement through fragmented tools (email, Excel, phone calls), leading to:
- Lost vendor communications and scattered records
- Manual, error-prone quotation comparison
- Delayed approvals with no audit trail
- Disconnected PO and invoice generation
- Zero visibility into spending trends

### 1.3 Solution in One Line
A centralized, role-based ERP platform built on **Odoo 17** that connects buyers, vendors, and managers in a single procurement workflow with AI-powered automation and real-time analytics.

### 1.4 Success Criteria (How We Win)
| Criteria | Target |
|----------|--------|
| **Functionality** | All 10 baseline features working end-to-end |
| **Innovation** | 3 "wow" AI features integrated and demo-ready |
| **UI/UX** | Mobile-responsive, modern design, <3s page load |
| **Odoo Leverage** | Heavy use of native modules (Purchase, Contacts, Accounting) |
| **Demo Story** | Complete narrative from RFQ → Invoice in <3 minutes |

---

## 2. User Personas & Roles

### 2.1 Role Matrix

| Role | Permissions | Primary Actions |
|------|-------------|-----------------|
| **Admin** | Full system access | Manage users, vendors, view all analytics |
| **Procurement Officer** | RFQ, Quotations, PO, Invoice | Create RFQs, compare quotes, generate POs/invoices |
| **Manager / Approver** | Read + Approval actions | Approve/reject procurement requests, monitor workflows |
| **Vendor** | External portal access | Submit quotations, track RFQ status, view POs |

### 2.2 User Persona Details

**Priya — Procurement Officer**
- Age: 28, works at a mid-size IT company
- Pain: Spends 3 hours/day copying vendor quotes into Excel
- Goal: Create RFQs in under 2 minutes and compare quotes instantly

**Rajesh — Vendor (Delhi Hardware Hub)**
- Age: 45, runs a small B2B supply business
- Pain: Receives RFQs via WhatsApp, loses track of deadlines
- Goal: Submit professional quotes quickly without creating accounts

**Manager Arun — Department Head**
- Age: 38, approves all purchases >₹50,000
- Pain: No visibility into pending approvals while traveling
- Goal: Approve or reject from mobile with full context

---

## 3. Functional Requirements

### 3.1 Feature 1: Authentication & Role Management
**Priority:** P0 (Must Have)

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| AUTH-01 | Email/password login with role-based redirect | After login, user lands on role-appropriate dashboard |
| AUTH-02 | Signup with role selection | New users select role during registration; admin approves |
| AUTH-03 | Session management & logout | Auto-logout after 30 min inactivity; secure cookie handling |
| AUTH-04 | "Magic Link" for vendors | Vendors receive time-limited (24h) secure link via email to submit quotes without registration |

**Odoo Native Leverage:** Use Odoo's built-in `res.users` and `res.groups` with custom groups for each role.

---

### 3.2 Feature 2: Dashboard (Home Screen)
**Priority:** P0

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| DASH-01 | Analytics cards | Show: Active RFQs count, Pending Approvals, Total Spend (MTD), Overdue Invoices |
| DASH-02 | Recent activity feed | Last 5 actions (RFQ created, Quote received, PO generated) with timestamps |
| DASH-03 | Quick action buttons | "+ New RFQ", "+ Add Vendor", "View Quotations" |
| DASH-04 | Role-based widgets | Managers see "Pending Approvals" first; Vendors see "Open RFQs" |

**Odoo Native Leverage:** Extend Odoo's `web.dashboard` or create custom QWeb dashboard view.

---

### 3.3 Feature 3: Vendor Management
**Priority:** P0

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| VEND-01 | Vendor registration form | Fields: Name, Category (dropdown), GST Number, Address, Contact Person, Email, Phone, Status (Active/Inactive/Blocked) |
| VEND-02 | Vendor profile view | Single page showing all details + historical performance score |
| VEND-03 | Search & filter | Search by name, GST, category; filter by status and rating |
| VEND-04 | Vendor rating (auto-calculated) | 1-5 star rating based on: on-time delivery %, price competitiveness, quote response time |
| VEND-05 | Vendor categories | Pre-seeded categories: IT Hardware, Office Supplies, Furniture, Logistics, Stationery |

**Odoo Native Leverage:** Extend `res.partner` model (Odoo's contact master) with custom fields.

---

### 3.4 Feature 4: RFQ Creation
**Priority:** P0

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| RFQ-01 | RFQ header | Fields: Title, Description, Deadline (date picker), Priority (Low/Med/High) |
| RFQ-02 | Line items | Dynamic table: Item Name, Quantity, Unit of Measure, Specifications |
| RFQ-03 | Vendor assignment | Multi-select dropdown of active vendors; "Select All" option |
| RFQ-04 | File attachments | Support PDF, DOCX, JPG (max 5MB per file, max 3 files) |
| RFQ-05 | Voice-to-RFQ (WOW) | Microphone button captures speech → auto-fills title, items, deadline via Web Speech API |
| RFQ-06 | Auto-save draft | Draft saved every 30 seconds to prevent data loss |
| RFQ-07 | Email notification | On publish, invited vendors receive email with magic link |

**Odoo Native Leverage:** Use Odoo Purchase module's `purchase.order` (RFQ state) with custom extensions.

---

### 3.5 Feature 5: Vendor Quotation Submission
**Priority:** P0

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| QUOTE-01 | External vendor portal | Clean, mobile-responsive page accessible via magic link |
| QUOTE-02 | Line-item response | Pre-filled RFQ items; vendor enters: Unit Price, Delivery Days, Notes |
| QUOTE-03 | AI Quote Reader (WOW) | Vendor uploads quotation PDF/image → Gemini API extracts data → auto-fills form |
| QUOTE-04 | Edit before submit | Vendor can modify any field before final submission |
| QUOTE-05 | Submit & confirm | Success message + email confirmation to vendor and procurement officer |
| QUOTE-06 | Deadline enforcement | Portal blocks submissions after RFQ deadline |

**Odoo Native Leverage:** Custom Odoo Website page + controller handling file uploads.

---

### 3.6 Feature 6: Quotation Comparison
**Priority:** P0

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| COMP-01 | Side-by-side table | Columns: Item, Vendor A Price, Vendor B Price, Vendor C Price, Delivery Days, Rating |
| COMP-02 | Lowest price highlighting | Cell with lowest price per item highlighted in green |
| COMP-03 | Best overall suggestion | AI badge: "Recommended: Vendor X — lowest total cost + meets deadline" |
| COMP-04 | Sorting & filtering | Sort by total price, delivery time, vendor rating |
| COMP-05 | Export view | "Download Comparison" as PDF (optional stretch goal) |

**Odoo Native Leverage:** Custom QWeb view or Owl component querying `purchase.order.line` records.

---

### 3.7 Feature 7: Approval Workflow
**Priority:** P0

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| APPR-01 | Visual workflow timeline | Stepper UI: RFQ Created → Quotes Received → Under Review → Approved/Rejected → PO Generated |
| APPR-02 | Approve/reject actions | Manager clicks Approve or Reject; required comment field for rejection |
| APPR-03 | Approval remarks | Text area for manager comments visible in audit log |
| APPR-04 | Auto-transition | On approval, status auto-updates and PO generation button appears |
| APPR-05 | Email notifications | Manager gets notified when quotes are ready; officer gets notified on approval/rejection |
| APPR-06 | Delegation support | Manager can reassign approval to another manager |

**Odoo Native Leverage:** Use Odoo's `mail.activity` and `mail.message` for notifications; custom state machine on RFQ model.

---

### 3.8 Feature 8: Purchase Order & Invoice Generation
**Priority:** P0

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| PO-01 | Auto-generated PO number | Format: `PO-2026-XXXX` (auto-incrementing) |
| PO-02 | PO document | Professional PDF with company logo, vendor details, item table, tax, total |
| PO-03 | Invoice generation | One-click "Generate Invoice" from approved PO; auto-calculates GST (18%) |
| PO-04 | Invoice actions | Download PDF, Print, Email (with pre-filled template) |
| PO-05 | One-click email | "Send Invoice via Email" button attaches PDF and sends via SMTP |
| PO-06 | Status tracking | PO/Invoice statuses: Draft → Sent → Paid → Overdue |

**Odoo Native Leverage:** Odoo Purchase → PO; Odoo Accounting → Vendor Bill/Invoice; QWeb for PDF reports.

---

### 3.9 Feature 9: Activity Logs & Notifications
**Priority:** P1 (Should Have)

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| LOG-01 | Global activity timeline | Chronological list: "RFQ created by Priya at 09:00", "Quote received from Vendor A at 09:45" |
| LOG-02 | Filter by entity | Filter logs by RFQ, Vendor, PO, or Invoice |
| LOG-03 | In-app notifications | Bell icon dropdown showing unread notifications |
| LOG-04 | Email alerts | Configurable: RFQ published, Quote received, Approval required, Invoice generated |
| LOG-05 | Audit trail immutability | Logs cannot be edited or deleted by any user (including admin) |

**Odoo Native Leverage:** Odoo's built-in `mail.message` and `mail.activity` models.

---

### 3.10 Feature 10: Reports & Analytics
**Priority:** P1

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| RPT-01 | Spending summary cards | Total spend (MTD), Active vendors, PO fulfillment rate, Overdue invoices |
| RPT-02 | Monthly trend chart | Bar chart: spend per month (last 6 months) using Chart.js |
| RPT-03 | Category breakdown | Pie/donut chart: spend by category (IT Hardware, Furniture, etc.) |
| RPT-04 | Vendor performance table | Top vendors by spend + average rating + on-time delivery % |
| RPT-05 | Export reports | "Export to CSV" button for all report views |

**Odoo Native Leverage:** Custom SQL views + Chart.js frontend; Odoo's `ir.actions.report` for CSV export.

---

### 3.11 Feature 11: Procurement Copilot (WOW)
**Priority:** P1

| Requirement ID | Description | Acceptance Criteria |
|----------------|-------------|---------------------|
| COP-01 | Chat widget | Floating chat bubble (bottom-right) on all screens |
| COP-02 | Hardcoded intents | "Show pending approvals" → queries and displays list; "Total spend this month" → shows number |
| COP-03 | Natural language fallback | Unrecognized questions sent to Groq API with system prompt + current data context |
| COP-04 | Response formatting | Answers include numbers, short lists, or "I don't have that information" |

---

## 4. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Performance** | Page load < 3 seconds; report generation < 5 seconds |
| **Security** | Role-based access control; magic links expire in 24h; password hashing (Odoo default) |
| **Scalability** | Support 50 concurrent users; 1,000 vendors; 10,000 RFQs (architected via Odoo ORM) |
| **Reliability** | Auto-save on all forms; graceful error messages; no data loss on crash |
| **Compatibility** | Chrome, Edge, Firefox (latest 2 versions); mobile responsive (iOS Safari, Android Chrome) |
| **Data Integrity** | All financial calculations use Decimal fields; GST always 18% for demo |

---

## 5. Technical Architecture

### 5.1 System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │   Officer    │ │   Manager    │ │    Vendor    │           │
│  │   (Odoo UI)  │ │   (Odoo UI)  │ │ (Web Portal) │           │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘           │
└─────────┼────────────────┼────────────────┼───────────────────┘
          │                │                │
          └────────────────┴────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    ODOO 17 APPLICATION                       │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │  Custom      │ │   Native     │ │   Custom     │       │
│  │  Modules     │ │   Modules    │ │  Controllers │       │
│  │  (vendor_    │ │  (Purchase,  │ │  (API routes,│       │
│  │   bridge)    │ │   Contacts,  │ │   portal)    │       │
│  │              │ │   Accounting)│ │              │       │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘       │
└─────────┼────────────────┼────────────────┼───────────────┘
          │                │                │
          └────────────────┴────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    DATA & SERVICES LAYER                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │  PostgreSQL  │ │  Gemini API  │ │   Groq API   │       │
│  │  (Odoo DB)   │ │  (Quote      │ │  (Copilot    │       │
│  │              │ │   Reader)    │ │   Chat)      │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Module Structure

### Root Directory Layout
```
vendorbridge-hackathon/
├── .git/                          # Git metadata
├── .gitignore                     # Ignore __pycache__, .pyc, node_modules
├── README.md                      # Setup instructions for judges
├── requirements.txt               # Python dependencies (if any extras)
├── vendorbridge/                  # MAIN ODOO MODULE (Person B owns this)
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── vendor.py              # Vendor management model
│   │   ├── rfq.py                 # RFQ model
│   │   ├── quotation.py           # Vendor quotation model
│   │   ├── approval_workflow.py   # Approval states & logic
│   │   └── activity_log.py        # Audit trail model
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── main.py                # Public routes, API endpoints
│   │   └── ai_services.py         # Gemini, Groq API wrappers
│   ├── views/
│   │   ├── vendor_views.xml       # Backend tree/form views
│   │   ├── rfq_views.xml          # RFQ backend views
│   │   ├── dashboard_views.xml    # Dashboard action/window
│   │   └── menu.xml               # Main menu items
│   ├── data/
│   │   ├── demo_data.xml          # 10 vendors, 3 RFQs, 5 POs
│   │   └── email_templates.xml    # RFQ invite, invoice email
│   ├── reports/
│   │   ├── purchase_order.xml     # QWeb PO PDF template
│   │   └── invoice_report.xml     # QWeb Invoice PDF template
│   ├── security/
│   │   ├── ir.model.access.csv    # Access rights
│   │   └── vendorbridge_security.xml  # Record rules (vendors see own quotes only)
│   └── static/
│       └── src/                   # Person A works INSIDE here for frontend assets
│           ├── css/
│           │   └── vendorbridge.css   # Custom styles (Tailwind-like utilities)
│           ├── js/
│           │   ├── voice_to_rfq.js    # Web Speech API implementation
│           │   ├── chat_copilot.js    # Procurement Copilot widget
│           │   └── quote_reader.js    # File upload + preview handler
│           └── xml/
│               └── dashboard.xml      # Owl component templates
├── vendorbridge_website/          # Person A owns this (Frontend Portal)
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── portal.py              # Vendor portal routes, magic links
│   ├── views/
│   │   ├── vendor_portal.xml      # Vendor-facing pages (quotation submission)
│   │   ├── rfq_list.xml           # Vendor RFQ list view
│   │   └── comparison_page.xml    # Public comparison page (optional)
│   └── static/
│       ├── css/
│       │   └── portal.css         # Tailwind CDN + custom portal styles
│       └── js/
│           ├── portal.js          # Portal interactions
│           └── chart_config.js    # Chart.js dashboard configs
└── config/
    └── odoo.conf                  # Odoo server config (shared)
```

## 6. Data Model Specifications

### 6.1 Entity Relationship Diagram (Simplified)

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  res.users   │       │  res.partner │       │  vendor.rating│
│  (Odoo User) │       │  (Vendor)    │       │  (Score)     │
└──────┬───────┘       └──────┬───────┘       └──────┬───────┘
       │                      │                      │
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
┌──────▼───────┐       ┌──────▼───────┐       ┌──────▼───────┐
│purchase.order│       │purchase.order│       │  approval   │
│   (RFQ)      │       │    line      │       │  workflow   │
└──────┬───────┘       └──────────────┘       └──────────────┘
       │
       │ (approved)
       │
┌──────▼───────┐       ┌──────────────┐
│  purchase    │       │  account     │
│   order      │──────▶│   move       │
│   (PO)       │       │  (Invoice)   │
└──────────────┘       └──────────────┘
```

### 6.2 Key Fields

**Vendor Extension (`res.partner`)**
| Field | Type | Description |
|-------|------|-------------|
| `x_is_vendor` | Boolean | Marks partner as vendor |
| `x_gst_number` | Char | GST registration number |
| `x_vendor_category` | Selection | IT Hardware, Furniture, etc. |
| `x_vendor_status` | Selection | Active / Inactive / Blocked |
| `x_rating` | Float | Auto-calculated 1-5 score |
| `x_on_time_rate` | Float | % of on-time deliveries |

**RFQ Extension (`purchase.order`)**
| Field | Type | Description |
|-------|------|-------------|
| `x_rfq_title` | Char | Human-readable title |
| `x_deadline` | Date | Quote submission deadline |
| `x_priority` | Selection | Low / Medium / High |
| `x_status` | Selection | Draft → Sent → Quotes Received → Under Review → Approved → Rejected |
| `x_approval_notes` | Text | Manager's comments |

**Quotation Response (`vendor.quotation`)**
| Field | Type | Description |
|-------|------|-------------|
| `rfq_id` | Many2one | Link to purchase.order |
| `vendor_id` | Many2one | Link to res.partner |
| `line_ids` | One2many | Quote line items |
| `total_amount` | Float | Sum of line items |
| `delivery_days` | Integer | Promised delivery timeline |
| `attachment` | Binary | Uploaded quotation file |

---

## 7. API Specifications

### 7.1 Internal Odoo RPC Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/web/dataset/call_kw` | POST | Standard Odoo ORM calls (search, read, create, write) |
| `/vendor_bridge/portal/rfq/<id>` | GET | Vendor portal view for specific RFQ |
| `/vendor_bridge/portal/submit_quote` | POST | Vendor submits quotation |
| `/vendor_bridge/api/voice_to_rfq` | POST | Parses speech transcript into RFQ data |
| `/vendor_bridge/api/extract_quote` | POST | Uploads file, calls Gemini, returns JSON |
| `/vendor_bridge/api/copilot` | POST | Processes chat query, returns response |

### 7.2 External API Integrations

**Google Gemini 1.5 Flash (Quote Reader)**
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=API_KEY
Body: {
  "contents": [{
    "parts": [{
      "text": "Extract from this quotation in JSON format: items, quantities, unit_prices, total, delivery_date, vendor_name."
    }, {
      "inline_data": {
        "mime_type": "application/pdf",
        "data": "base64_encoded_file"
      }
    }]
  }]
}
```

**Groq API (Copilot)**
```
POST https://api.groq.com/openai/v1/chat/completions
Headers: Authorization: Bearer API_KEY
Body: {
  "model": "llama3-8b-8192",
  "messages": [
    {"role": "system", "content": "You are a procurement assistant. Answer using this data context: {context}"},
    {"role": "user", "content": "{user_query}"}
  ]
}
```

---

## 8. UI/UX Requirements

### 8.1 Design System
- **Primary Color:** `#714B67` (Odoo brand purple)
- **Secondary Color:** `#017E84` (Teal for actions)
- **Success:** `#28A745` (Green for approvals/lowest price)
- **Danger:** `#DC3545` (Red for rejections/overdue)
- **Warning:** `#FFC107` (Yellow for pending)
- **Font:** Inter or system sans-serif
- **Border Radius:** 8px for cards, 4px for buttons
- **Shadows:** `0 2px 8px rgba(0,0,0,0.08)` for cards

### 8.2 Responsive Breakpoints
| Breakpoint | Target |
|------------|--------|
| Mobile | < 768px (single column, stacked cards) |
| Tablet | 768px - 1024px (2-column grid) |
| Desktop | > 1024px (full layout) |

### 8.3 Key Screens
1. **Login Screen:** Centered card, logo, role selector
2. **Dashboard:** 4 metric cards + recent activity + quick actions
3. **Vendor List:** Table with search, filters, rating stars
4. **RFQ Form:** Multi-section form with voice button and dynamic line items
5. **Comparison Screen:** Side-by-side table with color coding
6. **Approval Workflow:** Horizontal stepper with action buttons
7. **PO/Invoice View:** Document preview with action toolbar
8. **Reports:** Dashboard with Chart.js visualizations
9. **Vendor Portal:** Clean, minimal, mobile-first design

---

## 9. AI Integration Specifications

### 9.1 Voice-to-RFQ (Web Speech API)
- **Trigger:** Microphone button click on RFQ form
- **Flow:**
  1. User clicks mic → `webkitSpeechRecognition` starts
  2. User speaks: *"Create RFQ for 50 Dell laptops, delivery by July 15th"*
  3. Transcript captured in JavaScript
  4. Regex extraction: numbers → quantities, dates → deadline, keywords → item names
  5. Form fields auto-populated
- **Fallback:** If speech recognition fails, show manual input prompt
- **Time to build:** ~45 minutes

### 9.2 Smart Quote Reader (Gemini API)
- **Trigger:** File upload in vendor portal
- **Flow:**
  1. Vendor selects PDF/image file
  2. Frontend converts to base64
  3. POST to Odoo controller `/api/extract_quote`
  4. Controller calls Gemini API with structured prompt
  5. JSON response parsed and returned to frontend
  6. Frontend auto-fills quotation form fields
- **Error Handling:** If extraction fails, show "Please review auto-filled data" warning
- **Time to build:** ~90 minutes

### 9.3 Procurement Copilot (Groq API)
- **Trigger:** Chat widget open + user message
- **Flow:**
  1. User types query in chat widget
  2. Frontend sends to `/api/copilot`
  3. Backend checks hardcoded intents first (regex matching)
  4. If no match, sends to Groq API with data context
  5. Response formatted and displayed in chat bubble
- **Pre-built Intents:**
  - "pending approvals" → search `purchase.order` where state='waiting'
  - "total spend" → sum `account.move` where type='in_invoice'
  - "top vendor" → sort `res.partner` by `x_rating` desc
- **Time to build:** ~90 minutes

---

## 10. 8-Hour Build Timeline

### Phase 1: Foundation (Hour 0-2)
| Time | Task | Owner |
|------|------|-------|
| 0:00-0:30 | Setup Odoo 17 dev environment, install dependencies | Backend |
| 0:30-1:00 | Create `vendor_bridge` module skeleton, define manifest | Backend |
| 1:00-1:30 | Extend `res.partner` (vendor fields), create demo data (10 vendors) | Backend |
| 1:30-2:00 | Configure native Purchase module, test RFQ → PO flow | Backend |

### Phase 2: Core Features (Hour 2-5)
| Time | Task | Owner |
|------|------|-------|
| 2:00-2:45 | Build custom dashboard view (QWeb) with metric cards | Frontend |
| 2:45-3:30 | Create RFQ creation form with dynamic line items | Frontend |
| 3:30-4:15 | Build vendor portal page (magic link access, quote submission) | Full Stack |
| 4:15-5:00 | Implement quotation comparison screen (side-by-side table) | Frontend |

### Phase 3: Workflow & Documents (Hour 5-6)
| Time | Task | Owner |
|------|------|-------|
| 5:00-5:30 | Build approval workflow UI (stepper + approve/reject buttons) | Frontend |
| 5:30-6:00 | Configure PO and Invoice PDF reports (QWeb reports) | Backend |
| 6:00-6:30 | Implement email sending (RFQ invites, invoice delivery) | Backend |

### Phase 4: Wow Features (Hour 6-7.5)
| Time | Task | Owner |
|------|------|-------|
| 6:30-7:00 | Integrate Web Speech API (Voice-to-RFQ) | Frontend |
| 7:00-7:30 | Integrate Gemini API (Smart Quote Reader) | Full Stack |
| 7:30-8:00 | Integrate Groq API (Procurement Copilot) + chat widget | Full Stack |

### Phase 5: Polish & Demo Prep (Hour 7.5-8)
| Time | Task | Owner |
|------|------|-------|
| 7:30-7:45 | Add Chart.js to reports dashboard | Frontend |
| 7:45-8:00 | Final testing, fix critical bugs, prepare demo data | All |

**Buffer:** If any phase runs over, drop the Reports dashboard (P1) and focus on ensuring P0 features work.

---

## 11. Demo Script (3-Minute Presentation)

### Minute 1: The Setup & Story
- **Screen:** Login as Admin → Dashboard
- **Narrative:** *"Meet Acme Corp. They buy ₹50L worth of equipment every year. Today, they need 50 laptops and 10 standing desks. Let me show you how VendorBridge handles this in under 5 minutes."*
- **Action:** Show dashboard with pre-seeded data (12 active RFQs, 8 vendors).

### Minute 2: The Core Workflow
- **Screen:** Create RFQ → Voice-to-RFQ demo → Send to vendors
- **Narrative:** *"Instead of typing, Priya just speaks. The system understands and creates the RFQ. Vendors get an email with a magic link — no password needed."*
- **Action:** Switch to vendor portal. Upload a PDF quotation. Show Smart Quote Reader extracting data in 3 seconds.
- **Screen:** Quotation Comparison → Approve
- **Narrative:** *"All quotes side-by-side. Lowest price highlighted. One click to approve."*

### Minute 3: The Payoff & Wow
- **Screen:** Auto-generated PO → Generate Invoice → Email
- **Narrative:** *"Purchase order auto-created. Invoice with GST calculated. Emailed to vendor in one click."*
- **Screen:** Activity Logs → Reports → Copilot
- **Narrative:** *"Every action tracked. Spending trends visualized. And if the manager has a question, the AI Copilot answers instantly."*
- **Action:** Ask Copilot: *"How much did we spend on IT hardware this month?"* Show instant answer.
- **Closing:** *"VendorBridge: Procurement, simplified."*

---

## 12. Risk Register & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Gemini API rate limit / failure | Medium | High | Pre-extract 2-3 sample quotes locally; demo with those if API fails |
| Odoo module installation issues | Low | High | Pre-install Odoo 17 + PostgreSQL before hackathon; test on same laptop |
| Time overrun on custom UI | High | Medium | Use Tailwind CDN + minimal custom CSS; fallback to native Odoo forms |
| Team member unavailable | Low | High | Assign primary + backup owner for each feature; document everything |
| Demo data corruption | Medium | Medium | Keep a `demo_data_backup.sql` file; restore in 2 minutes |
| Internet failure during demo | Medium | High | Run everything on localhost; pre-download all CDN libraries |

---

## 13. Appendix

### A. Pre-Hackathon Checklist
- [ ] Odoo 17 Community installed and running locally
- [ ] PostgreSQL configured with demo database
- [ ] VS Code with Python/XML extensions
- [ ] GitHub repository created with `.gitignore`
- [ ] Gemini API key generated (free tier)
- [ ] Groq API key generated (free tier)
- [ ] SMTP credentials configured (Gmail app password or Mailgun)
- [ ] Demo data script tested (10 vendors, 3 RFQs, 5 POs)
- [ ] Sample quotation PDFs prepared for AI demo
- [ ] Laptop charger + backup USB with full project

### B. Useful Odoo Commands
```bash
# Start Odoo server
./odoo-bin -c odoo.conf --addons-path=addons,custom_addons

# Update module
./odoo-bin -c odoo.conf -u vendor_bridge -d vendor_bridge_db

# Backup database
pg_dump -U odoo vendor_bridge_db > backup.sql

# Restore database
psql -U odoo vendor_bridge_db < backup.sql
```

### C. Free API Limits
| Service | Free Tier | Hackathon Sufficiency |
|---------|-----------|----------------------|
| Gemini 1.5 Flash | 1,500 requests/day | ✅ More than enough |
| Groq (llama3-8b) | 20 requests/minute | ✅ Sufficient for demo |
| Mailgun | 5,000 emails/month | ✅ Sufficient |

---

**Document Owner:** VendorBridge Hackathon Team  
**Reviewers:** All team members (pre-hackathon)  
**Next Review:** Post-hackathon retrospective

---
*"Build the story first, the features second, and the polish third."*
