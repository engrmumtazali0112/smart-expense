from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.auth import hash_password, verify_password, create_access_token, get_optional_user

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
    user = User(name=name, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    token = create_access_token({"sub": user.email})
    response = JSONResponse({"message": "Account created", "redirect": "/dashboard"})
    response.set_cookie("access_token", token, httponly=True, max_age=86400)
    return response

@router.post("/api/auth/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.email})
    response = JSONResponse({"message": "Login successful", "redirect": "/dashboard"})
    response.set_cookie("access_token", token, httponly=True, max_age=86400)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("access_token")
    return response