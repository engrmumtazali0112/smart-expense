from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Invoice, InvoiceItem, InvoiceStatus
from app.services.auth import get_current_user
from app.services.pdf import generate_invoice_pdf
from datetime import datetime
from typing import Optional
import json, random, string

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def gen_invoice_number() -> str:
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"INV-{datetime.now().strftime('%Y%m')}-{suffix}"

@router.get("/invoices", response_class=HTMLResponse)
def invoices_page(request: Request, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user),
                  page: int = 1,
                  status: Optional[str] = None):
    per_page = 10
    query = db.query(Invoice).filter(Invoice.user_id == current_user.id)
    if status:
        query = query.filter(Invoice.status == status)
    total = query.count()
    invoices = query.order_by(Invoice.created_at.desc())\
        .offset((page - 1) * per_page).limit(per_page).all()
    return templates.TemplateResponse(request, "invoices/list.html", {
        "user": current_user,
        "invoices": invoices, "page": page,
        "total_pages": (total + per_page - 1) // per_page,
        "status_filter": status, "total": total
    })

@router.get("/invoices/new", response_class=HTMLResponse)
def new_invoice_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request, "invoices/form.html", {
        "user": current_user, "invoice": None
    })

@router.get("/invoices/{invoice_id}", response_class=HTMLResponse)
def invoice_detail(invoice_id: int, request: Request, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id,
                                       Invoice.user_id == current_user.id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return templates.TemplateResponse(request, "invoices/detail.html", {
        "user": current_user, "invoice": invoice
    })

@router.get("/invoices/{invoice_id}/edit", response_class=HTMLResponse)
def edit_invoice_page(invoice_id: int, request: Request, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id,
                                       Invoice.user_id == current_user.id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return templates.TemplateResponse(request, "invoices/form.html", {
        "user": current_user, "invoice": invoice
    })

# ─── API endpoints ────────────────────────────────────────────────────────────
@router.post("/api/invoices")
async def create_invoice(request: Request, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    data = await request.json()
    due_date: Optional[datetime] = (
        datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
    )
    invoice = Invoice(
        invoice_number=gen_invoice_number(),
        client_name=data["client_name"],
        client_email=data.get("client_email", ""),
        status=data.get("status", InvoiceStatus.draft),
        notes=data.get("notes", ""),
        due_date=due_date,
        user_id=current_user.id
    )
    db.add(invoice)
    db.flush()
    for item in data.get("items", []):
        db.add(InvoiceItem(
            description=item["description"],
            quantity=float(item["quantity"]),
            unit_price=float(item["unit_price"]),
            invoice_id=invoice.id
        ))
    db.commit()
    return JSONResponse({"id": invoice.id, "invoice_number": invoice.invoice_number,
                         "redirect": f"/invoices/{invoice.id}"})

@router.put("/api/invoices/{invoice_id}")
async def update_invoice(invoice_id: int, request: Request, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id,
                                       Invoice.user_id == current_user.id).first()
    if not invoice:
        raise HTTPException(status_code=404)
    data = await request.json()
    invoice.client_name = data["client_name"]
    invoice.client_email = data.get("client_email", "")
    invoice.status = data.get("status", invoice.status)
    invoice.notes = data.get("notes", "")
    invoice.due_date = (
        datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
    )
    for item in invoice.items:
        db.delete(item)
    db.flush()
    for item in data.get("items", []):
        db.add(InvoiceItem(
            description=item["description"],
            quantity=float(item["quantity"]),
            unit_price=float(item["unit_price"]),
            invoice_id=invoice.id
        ))
    db.commit()
    return JSONResponse({"id": invoice.id, "redirect": f"/invoices/{invoice.id}"})

@router.delete("/api/invoices/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id,
                                       Invoice.user_id == current_user.id).first()
    if not invoice:
        raise HTTPException(status_code=404)
    db.delete(invoice)
    db.commit()
    return JSONResponse({"message": "Deleted"})

@router.get("/api/invoices/{invoice_id}/pdf")
def download_pdf(invoice_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id,
                                       Invoice.user_id == current_user.id).first()
    if not invoice:
        raise HTTPException(status_code=404)
    pdf_bytes = generate_invoice_pdf(invoice)
    return Response(content=pdf_bytes, media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename={invoice.invoice_number}.pdf"})

@router.get("/api/invoices")
def list_invoices_api(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    invoices = db.query(Invoice).filter(Invoice.user_id == current_user.id).all()
    return [{"id": i.id, "invoice_number": i.invoice_number, "client_name": i.client_name,
             "status": i.status, "total": i.total, "created_at": str(i.created_at)} for i in invoices]