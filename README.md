<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=7C3AED&center=true&vCenter=true&width=940&lines=💸+Smart+Expense+%26+Invoice+Manager;⚡+FastAPI+%2B+SQLAlchemy+%2B+jQuery;🚀+Python+Developer+Assessment+—+Times+TX+GmbH" alt="Typing SVG" />

<br/>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=python&logoColor=white)](https://sqlalchemy.org)
[![jQuery](https://img.shields.io/badge/jQuery-3.7-0769AD?style=for-the-badge&logo=jquery&logoColor=white)](https://jquery.com)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CDN-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **🏢 Assessment Submission — Python Developer Role @ Times TX GmbH**
> Submitted by **Mumtaz Ali** · [📧 engrmumtazali01@gmail.com](mailto:engrmumtazali01@gmail.com) · [🐙 github.com/engrmumtazali0112](https://github.com/engrmumtazali0112)

<br/>

```
⚡ 3 bugs fixed  ·  ✅ All features delivered  ·  🎁 All 3 bonus features included
```

</div>

---

## 🖼️ Live Demo Screenshots

<div align="center">

### 📊 Dashboard
![Dashboard](Demo/Dashboard.PNG)

### 🧾 Invoices
![Invoices](Demo/Invoices.PNG)

### 💸 Expenses
![Expenses](Demo/Expensive.PNG)

### 🔌 API Docs (Swagger UI)
![API](Demo/api.PNG)

</div>

---

## ⚡ Quick Start

```bash
# 📦 1. Clone the repository
git clone https://github.com/engrmumtazali0112/smart-expense.git
cd smart-expense

# 🐍 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac / Linux

# 📥 3. Install dependencies
pip install -r requirements.txt

# 🌱 4. Load demo data (optional but recommended)
python seed_demo.py

# 🚀 5. Start the server
python main.py

# 🌐 6. Open in browser
#  → http://localhost:8000
```

### 🐳 Docker (one command)
```bash
docker-compose up --build
# → http://localhost:8000
```

### 🔐 Demo Login Credentials
| Field | Value |
|-------|-------|
| 📧 Email | `demo@smartexpense.com` |
| 🔑 Password | `demo1234` |

> Run `python seed_demo.py` first to populate 5 invoices + 18 expenses across all categories.

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| 🐍 Backend | FastAPI | 0.136.1 | REST API + HTML routing |
| 🗄️ ORM | SQLAlchemy | 2.0.49 | Database models & queries |
| 🎨 Frontend | Jinja2 + Tailwind | 3.1.6 | Server-side templates |
| ⚡ AJAX | jQuery | 3.7.1 | No-reload interactions |
| 📊 Charts | Chart.js | Latest | Donut chart on dashboard |
| 🔐 Auth | bcrypt + JWT | 4.1.3 | Secure password hashing |
| 📄 PDF | ReportLab | 4.5.0 | Invoice PDF generation |
| 🗃️ Database | SQLite / PostgreSQL | — | Zero-config default |
| 🐳 Container | Docker | — | One-command deployment |

---

## ✅ Features

<details open>
<summary><b>🔐 Authentication</b></summary>

- Signup and login forms with validation
- Passwords hashed with **bcrypt** (direct library — bypasses passlib's Python 3.12+ backend bug)
- JWT stored in **HttpOnly cookie** — XSS-safe, 24-hour expiry
- All protected routes auto-redirect to `/login`

</details>

<details open>
<summary><b>🧾 Invoice Management</b></summary>

- Create invoices with **multiple line items** — live subtotal preview as you type
- Auto-generated invoice numbers (`INV-YYYYMM-XXXXXX`)
- Status workflow: `Draft` → `Sent` → `Paid` with color-coded badges
- Invoice list with **filter tabs** (All / Draft / Sent / Paid)
- Full invoice detail page with line item breakdown
- Edit and delete with confirmation
- **PDF export** — professional branded layout (ReportLab)
- **Pagination** — 10 per page

</details>

<details open>
<summary><b>💸 Expense Tracking</b></summary>

- Add, edit, delete via **AJAX modal** — zero page reloads
- **8 categories**: Food · Travel · Utilities · Software · Hardware · Marketing · Salary · Other
- Filter by **category** and **date range**
- Running total displayed in the list header
- **Pagination** — 10 per page

</details>

<details open>
<summary><b>📊 Dashboard</b></summary>

- **4 stat cards**: Total Invoices · Invoice Revenue · Total Expenses · Combined Total
- **Donut chart** — expense breakdown by category (Chart.js)
- Recent invoices and recent expenses panels
- Quick-action buttons (+ New Invoice, + Add Expense)
- Personalized greeting with user's name

</details>

<details open>
<summary><b>🔌 REST API</b></summary>

Full JSON CRUD API — all endpoints documented in Swagger UI at `/docs`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/signup` | Create account |
| `POST` | `/api/auth/login` | Login → JWT cookie |
| `GET` | `/api/invoices` | List invoices (JSON) |
| `POST` | `/api/invoices` | Create invoice + line items |
| `PUT` | `/api/invoices/{id}` | Update invoice |
| `DELETE` | `/api/invoices/{id}` | Delete invoice |
| `GET` | `/api/invoices/{id}/pdf` | Download PDF |
| `GET` | `/api/expenses` | List expenses (filterable) |
| `POST` | `/api/expenses` | Create expense |
| `PUT` | `/api/expenses/{id}` | Update expense |
| `DELETE` | `/api/expenses/{id}` | Delete expense |

🔗 **Interactive docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

</details>

<details open>
<summary><b>🎁 Bonus Features (all 3 delivered)</b></summary>

- ✅ **PDF export** for invoices — branded, professional layout
- ✅ **Pagination** on both invoice and expense list views
- ✅ **Docker** — `Dockerfile` + `docker-compose.yml` included

</details>

---

## 📁 Project Structure

```
smart-expense/
│
├── 📂 app/
│   ├── main.py                  # FastAPI app, lifespan, router registration
│   ├── database.py              # SQLAlchemy engine, session factory, init_db
│   ├── models.py                # User, Invoice, InvoiceItem, Expense ORM models
│   │
│   ├── 📂 routers/
│   │   ├── auth.py              # Signup, login, logout (HTML + JSON)
│   │   ├── dashboard.py         # Stats aggregation + chart data
│   │   ├── invoices.py          # Invoice CRUD + PDF download
│   │   └── expenses.py          # Expense CRUD + date/category filters
│   │
│   ├── 📂 services/
│   │   ├── auth.py              # JWT creation, bcrypt hashing, auth dependency
│   │   └── pdf.py               # ReportLab branded PDF generator
│   │
│   ├── 📂 static/
│   │   ├── css/app.css          # Custom styles, animations, print styles
│   │   └── js/app.js            # Toast notifications, AJAX helpers
│   │
│   └── 📂 templates/
│       ├── base.html            # Responsive sidebar layout + toast system
│       ├── 📂 auth/             # login.html, signup.html
│       ├── 📂 dashboard/        # index.html (stats + chart)
│       ├── 📂 invoices/         # list.html, form.html, detail.html
│       └── 📂 expenses/         # list.html (AJAX modal)
│
├── 📂 Demo/                     # Screenshot images for README
├── seed_demo.py                 # 🌱 Demo data seeder (5 invoices + 18 expenses)
├── main.py                      # Entry point — uvicorn with hot reload
├── requirements.txt             # Pinned Python 3.14-compatible versions
├── Dockerfile                   # Container build
├── docker-compose.yml           # One-command deployment
└── .env.example                 # Environment variable template
```

---

## 🗄️ Database Schema

```sql
┌─────────────────────────────────────────────────────────────────┐
│  users          id · name · email(unique) · hashed_password     │
│                 created_at                                       │
├─────────────────────────────────────────────────────────────────┤
│  invoices       id · invoice_number(unique) · client_name       │
│                 client_email · status(draft/sent/paid)          │
│                 due_date · notes · user_id(FK→users)            │
├─────────────────────────────────────────────────────────────────┤
│  invoice_items  id · description · quantity · unit_price        │
│                 invoice_id(FK→invoices)                         │
├─────────────────────────────────────────────────────────────────┤
│  expenses       id · title · amount · category(enum)            │
│                 description · date · user_id(FK→users)          │
└─────────────────────────────────────────────────────────────────┘
```

**Switch to PostgreSQL** with a single env var in `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost/smart_expense
```

---

## 🧠 Key Technical Decisions

**🚀 FastAPI over Django/Flask** — Chosen for async support, automatic OpenAPI/Swagger UI (free at `/docs`), and clean dependency injection. The same routes serve both HTML templates (for browser) and JSON (for API clients) with no duplication.

**🔐 bcrypt via direct library** — `passlib[bcrypt]` has a known backend-loading bug on Python 3.12+ where `importlib` changes cause `MissingBackendError` even when `bcrypt` is installed. Fixed by calling `bcrypt.hashpw()` and `bcrypt.checkpw()` directly, bypassing passlib entirely.

**🍪 JWT in HttpOnly cookie** — More secure than localStorage. The token is sent automatically with every request and is invisible to JavaScript, eliminating XSS-based token theft.

**⚡ jQuery AJAX for key interactions** — Expense CRUD (create, edit, delete) runs through modals with zero page reloads. Invoice form POSTs JSON and redirects server-side. Standard navigation is used where AJAX adds no real UX benefit.

**🗃️ SQLite default, PostgreSQL-ready** — Zero setup friction for the reviewer. One env var switches the database engine completely.

---

## ⚖️ Tradeoffs & Honest Notes

| Decision | Reason | Production Alternative |
|----------|--------|----------------------|
| SQLite default | Zero reviewer setup friction | PostgreSQL via `DATABASE_URL` |
| No Alembic | `init_db()` sufficient for assessment scope | Alembic with versioned migrations |
| Tailwind CDN | No build tooling needed | PostCSS + PurgeCSS pipeline |
| Cookie-based API auth | Works perfectly for browser clients | Bearer token for headless consumers |
| No email verification | Out of scope for 72 hours | SendGrid / Mailgun integration |

---

## 🔮 What I'd Add With More Time

- [ ] 🗄️ Alembic migrations for safe schema versioning
- [ ] 📧 Email notifications on invoice status changes (SendGrid)
- [ ] 📤 CSV export for expense reports
- [ ] 💱 Multi-currency with live exchange rates
- [ ] 👥 Role-based access (admin / accountant / viewer)
- [ ] 🧪 Full test suite with pytest + httpx
- [ ] 📱 PWA support for mobile installation

---

## 🐛 Bugs Fixed During Development

> Three Python 3.14 compatibility issues were identified and resolved:

| # | Error | Root Cause | Fix Applied |
|---|-------|-----------|-------------|
| 1 | `passlib MissingBackendError` | passlib lazy backend discovery breaks on Python 3.12+ | Direct `bcrypt` library calls — bypass passlib entirely |
| 2 | `SQLAlchemy TypeError __firstlineno__` | SQLAlchemy 2.0.30 `FastIntFlag` conflicts with Python 3.14 enum changes | Upgraded to `sqlalchemy==2.0.49` (official fix) |
| 3 | `Jinja2 TypeError unhashable dict` | Starlette 1.0 changed `TemplateResponse` signature; `request` in context dict breaks LRU cache key | Updated all calls to `TemplateResponse(request, name, ctx)` |

---

<div align="center">

### Built with ❤️ by Mumtaz Ali

[![GitHub](https://img.shields.io/badge/GitHub-engrmumtazali0112-181717?style=for-the-badge&logo=github)](https://github.com/engrmumtazali0112)
[![Email](https://img.shields.io/badge/Email-engrmumtazali01%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:engrmumtazali01@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mumtaz%20Ali-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/mumtazali)

<br/>

*"A smaller scope done well will always score higher than a rushed implementation that covers everything."*
*— Times TX GmbH Assessment Brief*

⭐ **Star this repo if you found it helpful!**

</div>
