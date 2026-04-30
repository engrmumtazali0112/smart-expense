from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Expense, ExpenseCategory
from app.services.auth import get_current_user
from datetime import datetime
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/expenses", response_class=HTMLResponse)
def expenses_page(request: Request, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user),
                  page: int = 1,
                  category: Optional[str] = None,
                  date_from: Optional[str] = None,
                  date_to: Optional[str] = None):
    per_page = 10
    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    if category:
        query = query.filter(Expense.category == category)
    if date_from:
        query = query.filter(Expense.date >= datetime.fromisoformat(date_from))
    if date_to:
        query = query.filter(Expense.date <= datetime.fromisoformat(date_to))
    total = query.count()
    expenses = query.order_by(Expense.date.desc())\
        .offset((page - 1) * per_page).limit(per_page).all()
    total_amount = query.with_entities(func.sum(Expense.amount)).scalar() or 0
    return templates.TemplateResponse(request, "expenses/list.html", {
        "user": current_user,
        "expenses": expenses, "page": page,
        "total_pages": (total + per_page - 1) // per_page,
        "category_filter": category, "date_from": date_from, "date_to": date_to,
        "categories": [c.value for c in ExpenseCategory],
        "total": total, "total_amount": round(float(total_amount), 2)
    })

@router.post("/api/expenses")
async def create_expense(request: Request, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    data = await request.json()
    expense = Expense(
        title=data["title"],
        amount=float(data["amount"]),
        category=data.get("category", ExpenseCategory.other),
        description=data.get("description", ""),
        date=datetime.fromisoformat(data["date"]) if data.get("date") else datetime.utcnow(),
        user_id=current_user.id
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return JSONResponse({
        "id": expense.id,
        "title": str(expense.title),
        "amount": float(expense.amount),
        "category": expense.category.value,
        "date": expense.date.strftime("%Y-%m-%d")
    })

@router.put("/api/expenses/{expense_id}")
async def update_expense(expense_id: int, request: Request, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == expense_id,
                                       Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404)
    data = await request.json()
    expense.title = data["title"]
    expense.amount = float(data["amount"])
    expense.category = data.get("category", expense.category)
    expense.description = data.get("description", "")
    expense.date = datetime.fromisoformat(data["date"]) if data.get("date") else expense.date
    db.commit()
    return JSONResponse({"id": expense.id, "message": "Updated"})

@router.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == expense_id,
                                       Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404)
    db.delete(expense)
    db.commit()
    return JSONResponse({"message": "Deleted"})

@router.get("/api/expenses")
def list_expenses_api(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user),
                      category: Optional[str] = None,
                      date_from: Optional[str] = None,
                      date_to: Optional[str] = None):
    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    if category:
        query = query.filter(Expense.category == category)
    if date_from:
        query = query.filter(Expense.date >= datetime.fromisoformat(date_from))
    if date_to:
        query = query.filter(Expense.date <= datetime.fromisoformat(date_to))
    expenses = query.order_by(Expense.date.desc()).all()
    return [{"id": e.id, "title": e.title, "amount": float(e.amount),
             "category": e.category.value, "date": str(e.date)} for e in expenses]