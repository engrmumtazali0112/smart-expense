from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import init_db
from app.routers import auth, dashboard, invoices, expenses
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Smart Expense Manager", version="1.0.0", lifespan=lifespan)

# Create directories
os.makedirs("app/static/css", exist_ok=True)
os.makedirs("app/static/js", exist_ok=True)
os.makedirs("app/templates/auth", exist_ok=True)
os.makedirs("app/templates/dashboard", exist_ok=True)
os.makedirs("app/templates/invoices", exist_ok=True)
os.makedirs("app/templates/expenses", exist_ok=True)
os.makedirs("app/templates/admin", exist_ok=True)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(invoices.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return RedirectResponse("/dashboard")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse({"detail": "Not found"}, status_code=404)