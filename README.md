<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=30&duration=2800&pause=2000&color=7C3AED&center=true&vCenter=true&width=960&lines=💸+Smart+Expense+%26+Invoice+Manager;⚡+FastAPI+%2B+SQLAlchemy+%2B+jQuery;👑+Role-Based+Access+Control+(RBAC);🚀+Python+Developer+Assessment+—+Times+TX+GmbH" alt="Typing SVG" />

<br/>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=python&logoColor=white)](https://sqlalchemy.org)
[![jQuery](https://img.shields.io/badge/jQuery-3.7-0769AD?style=for-the-badge&logo=jquery&logoColor=white)](https://jquery.com)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CDN-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

> **🏢 Assessment Submission — Python Developer Role @ Times TX GmbH**
>
> Submitted by **Mumtaz Ali** · [📧 engrmumtazali01@gmail.com](mailto:engrmumtazali01@gmail.com) · [🐙 github.com/engrmumtazali0112](https://github.com/engrmumtazali0112)

<br/>

```
⚡ 3 Bugs Fixed  ·  ✅ All Core Features Delivered  ·  👑 RBAC with 3 Roles  ·  🎁 All 3 Bonus Features Included
```

</div>

---

## 📋 Table of Contents

- [✨ Features Overview](#-features-overview)
- [👥 Role-Based Access Control](#-role-based-access-control)
- [🖼️ Screenshots](#️-screenshots)
- [⚡ Quick Start](#-quick-start)
- [🔐 Demo Credentials](#-demo-credentials)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🗄️ Database Schema](#️-database-schema)
- [🔌 API Documentation](#-api-documentation)
- [🧠 Key Technical Decisions](#-key-technical-decisions)
- [⚖️ Tradeoffs & Honest Notes](#️-tradeoffs--honest-notes)
- [🐛 Bugs Fixed](#-bugs-fixed)
- [🐳 Docker Setup](#-docker-setup)

---

## ✨ Features Overview

<table>
<tr>
<td width="50%">

### 🔐 Authentication & Security
- **Role-Based Access Control (RBAC)** — 3 distinct roles
- JWT stored in **HttpOnly cookies** (XSS-safe, 24-hour expiry)
- **bcrypt** password hashing — direct library (bypasses passlib Python 3.12+ bug)
- Protected routes with automatic redirects

</td>
<td width="50%">

### 🧾 Invoice Management
- Multi-line-item invoices with live subtotal preview
- Auto-generated invoice numbers (`INV-YYYYMM-XXXXXX`)
- Status workflow: `Draft` → `Sent` → `Paid`
- Filter tabs · Full CRUD · **PDF Export** · Pagination

</td>
</tr>
<tr>
<td width="50%">

### 💸 Expense Tracking
- Add/Edit/Delete via **AJAX modal** (zero page reloads)
- **8 Categories**: Food · Travel · Utilities · Software · Hardware · Marketing · Salary · Other
- Filter by **category** and **date range**
- Running total in list header · Pagination

</td>
<td width="50%">

### 📊 Dashboard
- **4 Stat Cards**: Total Invoices · Revenue · Expenses · Combined
- **Donut Chart** — expense breakdown by category (Chart.js)
- Recent invoices and expenses panels
- Role-specific quick actions & personalized greeting

</td>
</tr>
</table>

---

## 👥 Role-Based Access Control

### Permission Matrix

| Feature | 👑 Admin | 📊 Manager | 👁️ Viewer |
|---------|:--------:|:---------:|:--------:|
| **Dashboard** | ✅ Full | ✅ Own | ✅ Own |
| **Create Invoice** | ✅ | ✅ | ❌ |
| **Edit Invoice** | ✅ All | ✅ Own | ❌ |
| **Delete Invoice** | ✅ All | ✅ Own | ❌ |
| **View Invoices** | ✅ All | ✅ Own | ✅ Own |
| **Create Expense** | ✅ | ✅ | ❌ |
| **Edit Expense** | ✅ All | ✅ Own | ❌ |
| **Delete Expense** | ✅ All | ✅ Own | ❌ |
| **View Expenses** | ✅ All | ✅ Own | ✅ Own |
| **User Management** | ✅ | ❌ | ❌ |
| **PDF Export** | ✅ All | ✅ Own | ✅ Own |

### Role Badges
| Role | Badge | Permissions Summary |
|------|-------|---------------------|
| **Admin** | 👑 Purple Crown | Full system access + User Management |
| **Manager** | 📊 Blue Chart | View all, create/edit/delete own data |
| **Viewer** | 👁️ Green Eye | Read-only access to own data |

---

## 🖼️ Screenshots

### 👑 Admin Role — Full Access

<table>
<tr>
<td align="center" width="50%">

**Figure 1 — Admin Dashboard**

![Admin Dashboard](Demo/a1.PNG)

*Full-access dashboard showing 8 invoices, $29,725 revenue, 21 expenses across all categories. Includes User Management in sidebar.*

</td>
<td align="center" width="50%">

**Figure 2 — Admin Invoice List**

![Admin Invoices](Demo/a2.PNG)

*Admin can view, edit, delete, and download PDFs for all invoices system-wide. Status badges: Draft / Sent / Paid.*

</td>
</tr>
<tr>
<td align="center" width="50%">

**Figure 3 — Admin Expense Tracker**

![Admin Expenses](Demo/a3.PNG)

*Admin expense view with $24,401.25 total across 10 expenses. Full edit/delete controls per row.*

</td>
<td align="center" width="50%">

**Figure 4 — User Management Panel**

![User Management](Demo/a4.PNG)

*Admin-only panel to manage users, change roles (Admin / Manager / Viewer), activate/deactivate accounts, and delete users.*

</td>
</tr>
</table>

---

### 📊 Manager Role — View All, Manage Own

<table>
<tr>
<td align="center" width="50%">

**Figure 5 — Manager Dashboard**

![Manager Dashboard](Demo/m1.PNG)

*Manager dashboard showing own stats only. Donut chart and recent panels with full action buttons (+ New, + Add).*

</td>
<td align="center" width="50%">

**Figure 6 — Manager Invoice List**

![Manager Invoices](Demo/m2.PNG)

*Manager sees own invoices with create/edit/delete access. "No invoices yet" state with prompt to create first invoice.*

</td>
</tr>
<tr>
<td align="center" width="50%" colspan="2">

**Figure 7 — Manager Expense List**

![Manager Expenses](Demo/m3.PNG)

*Manager expense list with 7 expenses totalling $587.79. Category filter, date range filter, and full CRUD action icons per row.*

</td>
</tr>
</table>

---

### 👁️ Viewer Role — Read-Only Access

<table>
<tr>
<td align="center" width="50%">

**Figure 8 — Viewer Dashboard**

![Viewer Dashboard](Demo/Viwver.PNG)

*Viewer dashboard shows own data with "Read Only — Cannot Create/Edit/Delete" label. Recent panels show "Read Only" badge instead of action buttons.*

</td>
<td align="center" width="50%">

**Figure 9 — Viewer Invoice List (Read Only)**

![Viewer Invoices](Demo/v2.PNG)

*Viewer sees invoices in read-only mode. "Read Only Mode" button replaces the "+ New Invoice" button. Empty state prompts user to contact admin.*

</td>
</tr>
<tr>
<td align="center" width="50%" colspan="2">

**Figure 10 — Viewer Expense List (Read Only)**

![Viewer Expenses](Demo/v3.PNG)

*Viewer can see 4 expenses totalling $68.74 but all action columns show "Read only" text — no edit or delete icons rendered.*

</td>
</tr>
</table>

---

### 🔌 REST API — Swagger UI

<table>
<tr>
<td align="center">

**Figure 11 — Interactive API Documentation**

![Swagger API Docs](Demo/api.PNG)

*FastAPI auto-generates OpenAPI 3.1 documentation at `/docs`. All endpoints are testable directly in the browser — authentication, invoices, expenses, and admin routes.*

</td>
</tr>
</table>

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

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

# 🌱 4. Seed demo data (creates 3 users + sample invoices & expenses)
python add_demo_data.py

# 🚀 5. Start the server
python run.py

# 🌐 6. Open in browser
#  → http://127.0.0.1:8000
```

### 🐳 Docker (One Command)
```bash
docker-compose up --build
# → http://localhost:8000
```

---

## 🔐 Demo Credentials

After running `python add_demo_data.py`, use these credentials:

| Role | Email | Password | Access Level |
|------|-------|----------|-------------|
| 👑 **Admin** | `admin@demo.com` | `admin123` | Full system access + User Management |
| 📊 **Manager** | `manager@demo.com` | `manager123` | View all, manage own data |
| 👁️ **Viewer** | `viewer@demo.com` | `viewer123` | Read-only access |

**Demo Data Includes:**
- Admin: 5 invoices + 10 expenses
- Manager: 3 invoices + 6 expenses
- Viewer: 0 invoices + 4 expenses

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| 🐍 Backend | FastAPI | 0.104.1 | REST API + HTML routing |
| 🗄️ ORM | SQLAlchemy | 2.0.23 | Database models & queries |
| 🎨 Frontend | Jinja2 + Tailwind | 3.1.2 | Server-side templates |
| ⚡ AJAX | jQuery | 3.7.1 | No-reload interactions |
| 📊 Charts | Chart.js | Latest | Donut chart on dashboard |
| 🔐 Auth | bcrypt + JWT | 4.0.1 | Secure password hashing |
| 📄 PDF | ReportLab | 4.0.4 | Invoice PDF generation |
| 🗃️ Database | SQLite / PostgreSQL | — | Zero-config default |
| 🐳 Container | Docker | — | One-command deployment |

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
│   │   ├── auth.py              # Signup, login, logout + Admin user management
│   │   ├── dashboard.py         # Stats aggregation + chart data (role-aware)
│   │   ├── invoices.py          # Invoice CRUD + PDF download (role-aware)
│   │   └── expenses.py          # Expense CRUD + filters (role-aware)
│   │
│   ├── 📂 services/
│   │   ├── auth.py              # JWT creation, bcrypt, RBAC helpers
│   │   └── pdf.py               # ReportLab branded PDF generator
│   │
│   ├── 📂 static/
│   │   ├── css/app.css          # Custom styles, animations, print styles
│   │   └── js/app.js            # Toast notifications, AJAX helpers
│   │
│   └── 📂 templates/
│       ├── base.html            # Responsive sidebar + role-based menu
│       ├── 📂 auth/             # login.html (role selection), signup.html
│       ├── 📂 dashboard/        # index.html (role-aware stats + chart)
│       ├── 📂 invoices/         # list.html, form.html, detail.html
│       ├── 📂 expenses/         # list.html (role-based AJAX modal)
│       └── 📂 admin/            # users.html (Admin only)
│
├── 📂 Demo/                     # Screenshot images (11 screenshots across all roles)
├── add_demo_data.py             # 🌱 Demo data seeder (3 users + sample data)
├── run.py                       # Entry point — uvicorn with hot reload
├── requirements.txt             # Pinned Python dependencies
├── Dockerfile                   # Container build
├── docker-compose.yml           # One-command deployment
└── .env.example                 # Environment variable template
```

---

## 🗄️ Database Schema

```sql
┌─────────────────────────────────────────────────────────────────┐
│  users          id · name · email(unique) · hashed_password     │
│                 role(admin/manager/user) · is_active            │
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

## 🔌 API Documentation

Interactive API docs available at **[http://localhost:8000/docs](http://localhost:8000/docs)** after starting the server.

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/signup` | Register new user |
| `POST` | `/api/auth/login` | Login → JWT cookie |
| `GET` | `/logout` | Logout → clear cookie |

### Invoice Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/invoices` | List invoices (role-filtered) |
| `GET` | `/api/invoices/{id}` | Get invoice details |
| `POST` | `/api/invoices` | Create invoice + line items |
| `PUT` | `/api/invoices/{id}` | Update invoice |
| `DELETE` | `/api/invoices/{id}` | Delete invoice |
| `GET` | `/api/invoices/{id}/pdf` | Download PDF |

### Expense Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/expenses` | List expenses (filterable) |
| `POST` | `/api/expenses` | Create expense |
| `PUT` | `/api/expenses/{id}` | Update expense |
| `DELETE` | `/api/expenses/{id}` | Delete expense |

### Admin Endpoints *(Admin role only)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/admin/users` | List all users |
| `PUT` | `/api/admin/users/{id}/role` | Update user role |
| `PUT` | `/api/admin/users/{id}/toggle` | Activate/Deactivate user |
| `DELETE` | `/api/admin/users/{id}` | Delete user |

---

## 🧠 Key Technical Decisions

**🚀 FastAPI over Django/Flask** — Chosen for async support, automatic OpenAPI/Swagger UI (free at `/docs`), and clean dependency injection. The same routes serve both HTML templates (for browser) and JSON (for API clients) with no duplication.

**🔐 bcrypt via direct library** — `passlib[bcrypt]` has a known backend-loading bug on Python 3.12+ where `importlib` changes cause `MissingBackendError` even when `bcrypt` is installed. Fixed by calling `bcrypt.hashpw()` and `bcrypt.checkpw()` directly, bypassing passlib entirely.

**🍪 JWT in HttpOnly Cookie** — More secure than localStorage. The token is sent automatically with every request and is invisible to JavaScript, eliminating XSS-based token theft.

**⚡ jQuery AJAX for key interactions** — Expense CRUD runs through modals with zero page reloads. Invoice form POSTs JSON and redirects server-side. Standard navigation is used where AJAX adds no real UX benefit.

**🗃️ SQLite default, PostgreSQL-ready** — Zero setup friction for the reviewer. One env var switches the database engine completely.

---

## ⚖️ Tradeoffs & Honest Notes

| Decision | Reason | Production Alternative |
|----------|--------|----------------------|
| SQLite default | Zero reviewer setup friction | PostgreSQL via `DATABASE_URL` |
| No Alembic | `init_db()` sufficient for assessment scope | Alembic with versioned migrations |
| Tailwind CDN | No build tooling needed | PostCSS + PurgeCSS pipeline |
| Cookie-based API auth | Works perfectly for browser clients | Bearer token for headless consumers |
| No email verification | Out of scope | SendGrid / Mailgun integration |

---

## 🐛 Bugs Fixed

> Three Python 3.12+ / 3.14 compatibility issues were identified and resolved during development:

| # | Error | Root Cause | Fix Applied |
|---|-------|-----------|-------------|
| 1 | `passlib MissingBackendError` | passlib lazy backend discovery breaks on Python 3.12+ | Direct `bcrypt` library calls — bypass passlib entirely |
| 2 | `SQLAlchemy TypeError __firstlineno__` | SQLAlchemy 2.0.30 `FastIntFlag` conflicts with Python 3.14 enum changes | Upgraded to `sqlalchemy==2.0.23` (stable) |
| 3 | `no such column: users.role` | Database missing role column after RBAC addition | Updated models and re-ran `init_db()` |
| 4 | `AttributeError: 'str' has no attribute 'value'` | Category enum handling in expense router | Fixed expense router to use string categories directly |

---

## 🐳 Docker Setup

### Using Docker Compose (Recommended)
```bash
# Build and run
docker-compose up --build

# Stop containers
docker-compose down
```

### Using Docker Directly
```bash
# Build image
docker build -t smart-expense .

# Run container
docker run -p 8000:8000 smart-expense
```

Then open **[http://localhost:8000](http://localhost:8000)**

---

## 🔮 What I'd Add With More Time

- [ ] 🗄️ Alembic migrations for safe schema versioning
- [ ] 📧 Email notifications on invoice status changes (SendGrid)
- [ ] 📤 CSV export for expense reports
- [ ] 💱 Multi-currency with live exchange rates
- [ ] 🧪 Full test suite with pytest + httpx
- [ ] 📱 PWA support for mobile installation

---

<div align="center">

### Built with ❤️ by Mumtaz Ali

[![GitHub](https://img.shields.io/badge/GitHub-engrmumtazali0112-181717?style=for-the-badge&logo=github)](https://github.com/engrmumtazali0112)
[![Email](https://img.shields.io/badge/Email-engrmumtazali01%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:engrmumtazali01@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mumtaz%20Ali-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/mumtazali)

<br/>

*"A smaller scope done well will always score higher than a rushed implementation that covers everything."*
*— Times TX GmbH Assessment Brief*

<br/>

⭐ **Star this repo if you found it helpful!**

</div>