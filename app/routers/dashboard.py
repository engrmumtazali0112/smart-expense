from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Invoice, Expense, ExpenseCategory
from app.services.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    total_invoices = db.query(Invoice).filter(Invoice.user_id == current_user.id).count()
    total_expenses = db.query(Expense).filter(Expense.user_id == current_user.id).count()

    invoices = db.query(Invoice).filter(Invoice.user_id == current_user.id).all()
    invoice_total = sum(inv.total for inv in invoices)

    expense_total = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id).scalar() or 0

    recent_invoices = db.query(Invoice).filter(Invoice.user_id == current_user.id)\
        .order_by(Invoice.created_at.desc()).limit(5).all()
    recent_expenses = db.query(Expense).filter(Expense.user_id == current_user.id)\
        .order_by(Expense.created_at.desc()).limit(5).all()

    category_data = {}
    for cat in ExpenseCategory:
        total = db.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            Expense.category == cat).scalar() or 0
        if total > 0:
            category_data[cat.value] = round(total, 2)

    return templates.TemplateResponse(request, "dashboard/index.html", {
        "user": current_user,
        "total_invoices": total_invoices,
        "total_expenses": total_expenses,
        "invoice_total": round(invoice_total, 2),
        "expense_total": round(expense_total, 2),
        "combined_total": round(invoice_total + expense_total, 2),
        "recent_invoices": recent_invoices,
        "recent_expenses": recent_expenses,
        "category_data": category_data,
    })