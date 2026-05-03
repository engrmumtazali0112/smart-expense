# app/routers/auth.py
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.services.auth import (
    hash_password, verify_password, create_access_token, 
    get_optional_user, get_current_user, require_admin
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    if get_optional_user(request, db):
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse(request, "auth/login.html")


@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request, db: Session = Depends(get_db)):
    if get_optional_user(request, db):
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse(request, "auth/signup.html")


@router.post("/api/auth/signup")
def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...),
           db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # First user becomes admin, others become regular users
    is_first_user = db.query(User).count() == 0
    role = UserRole.ADMIN if is_first_user else UserRole.USER
    
    user = User(name=name, email=email, hashed_password=hash_password(password), role=role)
    db.add(user)
    db.commit()
    
    token = create_access_token({"sub": user.email})
    response = JSONResponse({"message": "Account created", "redirect": "/dashboard"})
    response.set_cookie("access_token", token, httponly=True, max_age=86400)
    return response


@router.post("/api/auth/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if not user or not verify_password(password, str(user.hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": str(user.email)})
    response = JSONResponse({"message": "Login successful", "redirect": "/dashboard"})
    response.set_cookie("access_token", token, httponly=True, max_age=86400)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("access_token")
    return response


# Admin: User Management Routes
@router.get("/admin/users", response_class=HTMLResponse)
def admin_users_page(request: Request, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    if not require_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    users = db.query(User).all()
    return templates.TemplateResponse(request, "admin/users.html", {
        "user": current_user,
        "users": users,
        "roles": [{"value": r.value, "label": r.value.capitalize()} for r in UserRole]
    })


@router.get("/api/admin/users")
def list_users_api(db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if not require_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    users = db.query(User).all()
    return [{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "role": u.role.value,
        "is_active": u.is_active,
        "created_at": u.created_at.isoformat()
    } for u in users]


@router.put("/api/admin/users/{user_id}/role")
def update_user_role(user_id: int, request: Request, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    if not require_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    data = request.json() if hasattr(request, 'json') else {}
    if isinstance(request, Request):
        import json
        body = json.loads(request.body())
        data = body
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role")
    
    user.role = UserRole(data.get("role", user.role.value))
    db.commit()
    return JSONResponse({"message": "Role updated successfully"})


@router.put("/api/admin/users/{user_id}/toggle")
def toggle_user_active(user_id: int, request: Request, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    if not require_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    
    user.is_active = not user.is_active
    db.commit()
    return JSONResponse({"message": f"User {'activated' if user.is_active else 'deactivated'}"})


@router.delete("/api/admin/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if not require_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    db.delete(user)
    db.commit()
    return JSONResponse({"message": "User deleted successfully"})