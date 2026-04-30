# Smart Expense & Invoice Management System

A focused, production-quality web application for managing invoices and expenses — built with **FastAPI**, **SQLAlchemy**, **Jinja2**, and **jQuery**.

> **Assessment submission for: Python Developer Role @ Times TX GmbH**

---

## Quick Start

**Prerequisites:** Python 3.10+, pip

```bash
# 1. Clone / unzip the repository
cd smart-expense

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (SQLite works out of the box — no DB setup needed)
cp .env.example .env

# 5. Run the server
python main.py

# 6. Open http://localhost:8000
```

### Docker (one command)
```bash
docker-compose up --build
# → http://localhost:8000
```

---

## Features

### ✅ Authentication
- Secure signup and login
- Passwords hashed with **bcrypt** (via direct `bcrypt` library — avoids passlib backend errors on Python 3.12+)
- JWT stored in **HttpOnly cookie** (24-hour expiry, XSS-safe)
- All protected routes auto-redirect to `/login`

### ✅ Invoice Management
- Create invoices with **multiple line items**
- Auto-generated invoice numbers (`INV-YYYYMM-XXXXXX`)
- Status workflow: **Draft → Sent → Paid**
- Edit, delete, and detailed invoice view
- **PDF export** — professional layout generated with ReportLab
- Pagination (10/page) with status filter tabs

### ✅ Expense Tracking
- Add, edit, and delete expenses via **AJAX modal** (no full page reloads)
- 8 categories: Food, Travel, Utilities, Software, Hardware, Marketing, Salary, Other
- Filter by **category** and **date range**
- Running total shown in the list header

### ✅ Dashboard
- Summary stats: total invoices, invoice revenue, total expenses, combined total
- **Donut chart** — expense breakdown by category (Chart.js)
- Recent invoices and expenses at a glance
- Quick-action links to create new records

### ✅ REST API
Full JSON CRUD API alongside the HTML views:

| Method   | Endpoint                     | Description               |
|----------|------------------------------|---------------------------|
| `POST`   | `/api/auth/signup`           | Create account            |
| `POST`   | `/api/auth/login`            | Login → JWT cookie        |
| `GET`    | `/api/invoices`              | List all invoices (JSON)  |
| `POST`   | `/api/invoices`              | Create invoice            |
| `PUT`    | `/api/invoices/{id}`         | Update invoice            |
| `DELETE` | `/api/invoices/{id}`         | Delete invoice            |
| `GET`    | `/api/invoices/{id}/pdf`     | Download PDF export       |
| `GET`    | `/api/expenses`              | List expenses (filterable)|
| `POST`   | `/api/expenses`              | Create expense            |
| `PUT`    | `/api/expenses/{id}`         | Update expense            |
| `DELETE` | `/api/expenses/{id}`         | Delete expense            |

Interactive API docs auto-generated at: **http://localhost:8000/docs**

### ✅ Bonus Features
- **PDF export** for invoices (ReportLab, branded layout)
- **Pagination** on both invoice and expense list views
- **Docker** setup with `Dockerfile` + `docker-compose.yml`

---

## Project Structure

```
smart-expense/
├── app/
│   ├── main.py              # FastAPI app factory, router registration
│   ├── database.py          # SQLAlchemy engine, session factory, init_db
│   ├── models.py            # User, Invoice, InvoiceItem, Expense ORM models
│   ├── routers/
│   │   ├── auth.py          # Signup, login, logout (HTML + JSON)
│   │   ├── dashboard.py     # Aggregated stats + chart data
│   │   ├── invoices.py      # Invoice CRUD, PDF download
│   │   └── expenses.py      # Expense CRUD with date/category filters
│   ├── services/
│   │   ├── auth.py          # JWT creation, bcrypt hashing, auth dependencies
│   │   └── pdf.py           # ReportLab invoice PDF generator
│   ├── static/
│   │   ├── css/app.css      # Custom styles, animations, print styles
│   │   └── js/app.js        # Shared utilities (toasts, AJAX helpers)
│   └── templates/
│       ├── base.html        # Responsive sidebar layout, toast system
│       ├── auth/            # login.html, signup.html
│       ├── dashboard/       # index.html (stats + chart)
│       ├── invoices/        # list.html, form.html, detail.html
│       └── expenses/        # list.html (AJAX modal)
├── main.py                  # Entry point: uvicorn with reload
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## Database Schema

| Table           | Key Columns                                                    |
|-----------------|----------------------------------------------------------------|
| `users`         | id, name, email (unique), hashed_password, created_at         |
| `invoices`      | id, invoice_number (unique), client_name, client_email, status, due_date, notes, user_id |
| `invoice_items` | id, description, quantity, unit_price, invoice_id             |
| `expenses`      | id, title, amount, category (enum), description, date, user_id|

SQLite is used by default — zero configuration needed. Switch to PostgreSQL by setting `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/smart_expense
```

---

## Key Technical Decisions

**FastAPI over Django/Flask** — Async-ready, clean dependency injection for auth and DB sessions, and automatic OpenAPI docs make it the best fit for an API-first app where the same endpoints serve HTML views and JSON consumers.

**Bcrypt via direct library** — `passlib[bcrypt]` has a known backend-loading issue on Python 3.12+ (the error in the bug report). The fix is to import `bcrypt` directly and bypass passlib's backend discovery entirely. `bcrypt==4.1.3` is added explicitly to `requirements.txt`.

**JWT in HttpOnly cookie** — More secure than localStorage. Automatic with every request; inaccessible to JavaScript, preventing XSS token theft.

**jQuery AJAX for key interactions** — Expense create/edit/delete happens without page reloads. Invoice save POSTs JSON and redirects on success. Regular navigation used for page transitions where AJAX adds no UX value.

**SQLite default, PostgreSQL-ready** — A single env var makes switching effortless. Removes all setup friction for reviewers.

**No frontend framework** — Jinja2 + Tailwind CDN + jQuery keeps the stack simple, loads fast, and requires zero build tooling. Tailwind CDN is acceptable for an assessment; a production build would use PostCSS.

---

## Tradeoffs & Notes

- **SQLite** by default for zero-setup. Production: set `DATABASE_URL` to PostgreSQL.
- **No Alembic migrations** — `init_db()` creates tables at startup. With more time, Alembic would be used to version schema changes safely.
- **No email verification** — Out of scope for the 72-hour timeframe.
- **Tailwind CDN** — Fine for demo/assessment. Production would use PostCSS + PurgeCSS build.
- The API is authenticated via cookie; a proper API-key or Bearer-token flow would be added for headless consumers in production.

---

## What I'd Add With More Time

1. Alembic migrations for schema versioning
2. Email notifications when invoice status changes (SendGrid/Mailgun)
3. CSV export for expense reports
4. Multi-currency with live exchange rates
5. Role-based access (admin, accountant, viewer)
6. Proper test suite (pytest + httpx)

---

## Bugs Fixed

**Root cause:** `passlib[bcrypt]` uses a lazy backend discovery system that fails on Python 3.12+ because of changes in how `importlib` finds submodules. The `MissingBackendError` appears even when `bcrypt` is installed.

**Fix applied:**
1. Added `bcrypt==4.1.3` explicitly to `requirements.txt`
2. Replaced `passlib.context.CryptContext` with direct `bcrypt` library calls in `app/services/auth.py` — bypassing passlib's broken discovery entirely
3. `hash_password()` now calls `bcrypt.hashpw()` directly; `verify_password()` calls `bcrypt.checkpw()` directly


---

## Bug Fixes Applied

### Bug 1 — bcrypt / passlib MissingBackendError
**Root cause:** `passlib[bcrypt]` lazy backend discovery breaks on Python 3.12+.
**Fix:** Replaced `passlib.context.CryptContext` with direct `bcrypt` library calls in `app/services/auth.py`. Added `bcrypt==4.1.3` explicitly to `requirements.txt`.

### Bug 2 — SQLAlchemy 2.0.30 TypeError on Python 3.14
**Error:** `TypeError: Can't replace canonical symbol for '__firstlineno__'`
**Root cause:** SQLAlchemy 2.0.30 uses `FastIntFlag` in a way that conflicts with Python 3.14's stricter `__firstlineno__` attribute handling in `enum`/`IntFlag`.
**Fix:** Upgraded to `sqlalchemy==2.0.49` which includes the Python 3.14 compatibility patch.

### Other Modernizations
- `app/main.py`: Replaced deprecated `@app.on_event("startup")` with the modern `lifespan` context manager (required in FastAPI 0.115+)
- `app/models.py`: Replaced `from sqlalchemy.ext.declarative import declarative_base` + `Base = declarative_base()` with the modern `class Base(DeclarativeBase): pass` pattern
- All package versions bumped to latest stable (FastAPI 0.136.1, uvicorn 0.46.0, reportlab 4.5.0)
