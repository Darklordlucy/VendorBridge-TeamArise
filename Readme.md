# VendorBridge 🤝
## Procurement & Vendor Management ERP


> **Built for Odoo × KSV Hackathon 2026** — A production-ready procurement ERP that digitizes vendor management, RFQs, quotations, approvals, purchase orders, and invoices with AI-powered enhancements.

---

## 🎯 Problem Statement

Organizations still manage procurement through emails, phone calls, and Excel sheets. This creates chaos:
- Vendors are scattered across different contact lists
- Price quotes arrive in random formats (PDFs, emails, WhatsApp)
- Managers lose track of approvals and purchase status
- Purchase orders and invoices are created manually, causing delays and errors

**VendorBridge solves this** with a centralized ERP platform that connects vendors, buyers, and managers in one seamless workflow.

---

## ✨ Key Features

### Core ERP Modules
- 🔐 **Role-Based Authentication** — 4 user roles: Admin, Procurement Officer, Vendor, Manager/Approver
- 📋 **Vendor Management** — Register vendors with GST, categories, contact details, and performance ratings
- 📄 **RFQ Creation** — Create and send Request for Quotations to multiple vendors
- 💰 **Quotation Comparison** — Side-by-side vendor comparison with lowest-price auto-highlighting
- ✅ **Approval Workflow** — Visual step-by-step approval process with status tracking
- 📑 **PO & Invoice Generation** — Auto-generated Purchase Orders and Invoices with tax calculations
- 📧 **Email Integration** — Send RFQ invites and invoices directly from the system
- 📊 **Reports & Analytics** — Spending trends, vendor performance, and procurement insights
- 📝 **Activity Logs** — Complete audit trail of every procurement action

### 🚀 AI-Powered "Wow" Features

| Feature | Description | Tech Used |
|---------|-------------|-----------|
| **🤖 Smart Quote Reader** | Upload a vendor quotation PDF/image → AI auto-extracts items, quantities, prices, and delivery dates in 3 seconds | Google Gemini 1.5 Flash API |
| **🎙️ Voice-to-RFQ** | Click the mic button, speak your procurement need (e.g., *"50 laptops by next week"*), and the form auto-fills | Web Speech API (Browser Native) |
| **💬 Procurement Copilot** | AI chat assistant in the bottom-right corner. Ask *"How much did we spend?"* or *"Who is cheapest?"* and get instant answers | Groq LLM API + Hardcoded Intents |

---

## 🛠️ Tech Stack

### Backend
- **Odoo 17 Community** — ERP framework with native Purchase, Accounting, and Mail modules
- **Python 3.10+** — Business logic and custom controllers
- **PostgreSQL 14+** — Database (bundled with Odoo)
- **Google Gemini API** — Document extraction and OCR
- **Groq API** — Fast LLM inference for the Copilot chatbot

### Frontend
- **Odoo QWeb & Owl** — Native Odoo templating and component framework
- **Tailwind CSS (CDN)** — Modern utility-first styling
- **Chart.js (CDN)** — Analytics dashboards and reports
- **FontAwesome (CDN)** — Professional icons
- **Web Speech API** — Browser-native voice recognition

---

## 📁 Project Structure

```
vendorbridge-hackathon/
├── vendorbridge/                  # Main Odoo module (Backend)
│   ├── models/                    # Python business logic
│   │   ├── vendor.py
│   │   ├── rfq.py
│   │   ├── quotation.py
│   │   ├── approval_workflow.py
│   │   └── activity_log.py
│   ├── controllers/               # API routes & AI services
│   │   ├── main.py
│   │   └── ai_services.py
│   ├── views/                     # Backend XML views
│   ├── data/                      # Demo data & email templates
│   ├── reports/                   # QWeb PDF templates (PO, Invoice)
│   ├── security/                  # Access rights & record rules
│   └── static/src/                # Frontend assets (JS, CSS, XML)
│       ├── js/
│       │   ├── voice_to_rfq.js
│       │   ├── chat_copilot.js
│       │   └── quote_reader.js
│       └── css/
│           └── vendorbridge.css
├── vendorbridge_website/          # Vendor Portal (Frontend)
│   ├── controllers/portal.py      # Public vendor routes
│   ├── views/                     # Portal pages (quotation submission)
│   └── static/                    # Portal CSS & JS
└── config/
    └── odoo.conf                  # Odoo server configuration
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 14 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/vendorbridge-hackathon.git
cd vendorbridge-hackathon
```

### Step 2: Install Odoo 17 Community
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Odoo dependencies
pip install -r requirements.txt
```

### Step 3: Configure PostgreSQL
```bash
# Create database user
sudo -u postgres createuser -s $USER

# Create Odoo database
createdb vendorbridge_db
```

### Step 4: Configure Odoo
Edit `config/odoo.conf`:
```ini
[options]
addons_path = /path/to/vendorbridge-hackathon
db_host = localhost
db_port = 5432
db_user = your_username
db_password = your_password
db_name = vendorbridge_db
http_port = 8069
```

### Step 5: Run Odoo
```bash
python3 /path/to/odoo/odoo-bin -c config/odoo.conf
```

### Step 6: Install the Module
1. Open browser: `http://localhost:8069`
2. Create admin account (first time only)
3. Go to **Apps** → Enable **Developer Mode**
4. Click **Update Apps List**
5. Search **VendorBridge** → Click **Install**

### Step 7: Load Demo Data
The module automatically loads demo data on install:
- 10 realistic vendors with GST numbers
- 3 active RFQs
- 5 historical purchase orders
- Sample quotations and approvals

---

## 🔑 API Keys Setup (For AI Features)

### Google Gemini (Smart Quote Reader)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a free API key
3. Replace `YOUR_GEMINI_API_KEY` in `vendorbridge/controllers/ai_services.py`

### Groq (Procurement Copilot)
1. Visit [Groq Console](https://console.groq.com/keys)
2. Create a free API key
3. Replace `YOUR_GROQ_API_KEY` in `vendorbridge/controllers/ai_services.py`

> **Note:** Both services offer generous free tiers sufficient for hackathon demos.

---


## 📸 Screenshots

> *(Add screenshots here after deployment)*

| Dashboard | Quotation Comparison | Approval Workflow |
|-----------|---------------------|-------------------|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Comparison](docs/screenshots/comparison.png) | ![Approval](docs/screenshots/approval.png) |

| Vendor Portal | AI Quote Reader | Procurement Copilot |
|---------------|-----------------|---------------------|
| ![Portal](docs/screenshots/portal.png) | ![AI Reader](docs/screenshots/ai_reader.png) | ![Copilot](docs/screenshots/copilot.png) |

---

## 🤝 Contributing

This project was built for a hackathon. For improvements or issues:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open-sourced under the **MIT License**.

---
