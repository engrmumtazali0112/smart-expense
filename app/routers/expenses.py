from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Expense
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
    
    categories = ['food', 'travel', 'utilities', 'software', 'hardware', 'marketing', 'salary', 'other']
    
    return templates.TemplateResponse(request, "expenses/list.html", {
        "request": request,
        "user": current_user,
        "expenses": expenses,
        "page": page,
        "total_pages": (total + per_page - 1) // per_page if total > 0 else 1,
        "category_filter": category,
        "date_from": date_from,
        "date_to": date_to,
        "categories": categories,
        "total": total,
        "total_amount": round(float(total_amount), 2)
    })


@router.post("/api/expenses")
async def create_expense(request: Request, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    try:
        data = await request.json()
        
        expense = Expense(
            title=data.get("title", ""),
            amount=float(data.get("amount", 0)),
            category=data.get("category", "other"),
            description=data.get("description", ""),
            date=datetime.fromisoformat(data["date"]) if data.get("date") else datetime.utcnow(),
            user_id=current_user.id
        )
        db.add(expense)
        db.commit()
        db.refresh(expense)
        
        return JSONResponse({
            "id": expense.id,
            "title": expense.title,
            "amount": float(expense.amount),
            "category": expense.category,
            "date": expense.date.strftime("%Y-%m-%d"),
            "message": "Expense created successfully"
        })
    except Exception as e:
        print(f"Error creating expense: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/api/expenses/{expense_id}")
async def update_expense(expense_id: int, request: Request, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    try:
        expense = db.query(Expense).filter(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
        ).first()
        
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        
        data = await request.json()
        expense.title = data.get("title", expense.title)
        expense.amount = float(data.get("amount", expense.amount))
        expense.category = data.get("category", expense.category)
        expense.description = data.get("description", expense.description)
        if data.get("date"):
            expense.date = datetime.fromisoformat(data["date"])
        
        db.commit()
        
        return JSONResponse({
            "id": expense.id,
            "message": "Expense updated successfully"
        })
    except Exception as e:
        print(f"Error updating expense: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return JSONResponse({"message": "Expense deleted successfully"})


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
    return [{
        "id": e.id,
        "title": e.title,
        "amount": float(e.amount),
        "category": e.category,
        "date": str(e.date)
    } for e in expenses]