from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routers import auth, dashboard, invoices, expenses


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database on startup."""
    init_db()
    yield


app = FastAPI(
    title="Smart Expense & Invoice Manager",
    version="1.0.0",
    description="A focused web application for managing invoices and expenses.",
    lifespan=lifespan,
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(invoices.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return RedirectResponse("/dashboard")


@app.exception_handler(302)
async def redirect_handler(request: Request, exc):
    return RedirectResponse(exc.headers["Location"])


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse({"detail": "Not found"}, status_code=404)
