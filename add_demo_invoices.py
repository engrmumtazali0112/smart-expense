import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import User, Invoice, InvoiceItem, InvoiceStatus
from datetime import datetime
import random
import string

def generate_invoice_number():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"INV-{datetime.now().strftime('%Y%m')}-{suffix}"

def add_demo_invoices():
    db = SessionLocal()
    
    try:
        # Get your user
        user = db.query(User).filter(User.email == "engrmumtazali01@gmail.com").first()
        
        if not user:
            print("❌ User not found. Available users:")
            users = db.query(User).all()
            for u in users:
                print(f"   - {u.email}")
            return
        
        print(f"✅ Found user: {user.name} ({user.email})")
        
        demo_data = [
            {
                "client_name": "TechStart Solutions",
                "client_email": "accounts@techstart.com",
                "status": InvoiceStatus.sent,
                "due_date": datetime(2026, 5, 30),
                "notes": "Payment terms: Net 30 days\nProject includes 3 months of support",
                "items": [
                    {"description": "Website Development", "quantity": 80, "unit_price": 75},
                    {"description": "Database Design", "quantity": 30, "unit_price": 120},
                    {"description": "UI/UX Design", "quantity": 40, "unit_price": 65},
                    {"description": "Testing & QA", "quantity": 20, "unit_price": 50}
                ]
            },
            {
                "client_name": "Digital Marketing Pro",
                "client_email": "finance@digitalmarketingpro.com",
                "status": InvoiceStatus.paid,
                "due_date": datetime(2026, 5, 15),
                "notes": "Payment received via wire transfer. Thank you!",
                "items": [
                    {"description": "SEO Optimization", "quantity": 50, "unit_price": 85},
                    {"description": "Social Media Management", "quantity": 30, "unit_price": 95},
                    {"description": "Content Creation", "quantity": 20, "unit_price": 75},
                    {"description": "Email Campaign", "quantity": 15, "unit_price": 110}
                ]
            },
            {
                "client_name": "Waqas Khan",
                "client_email": "waqaskhan123@gmail.com",
                "status": InvoiceStatus.paid,
                "due_date": datetime(2026, 6, 6),
                "notes": "API Integration project completed",
                "items": [
                    {"description": "API Integration", "quantity": 15, "unit_price": 120}
                ]
            }
        ]
        
        created_count = 0
        
        for inv_data in demo_data:
            # Create invoice
            invoice = Invoice(
                invoice_number=generate_invoice_number(),
                client_name=inv_data["client_name"],
                client_email=inv_data["client_email"],
                status=inv_data["status"],
                due_date=inv_data["due_date"],
                notes=inv_data["notes"],
                user_id=user.id
            )
            db.add(invoice)
            db.flush()
            
            # Add items
            for item_data in inv_data["items"]:
                item = InvoiceItem(
                    description=item_data["description"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    invoice_id=invoice.id
                )
                db.add(item)
            
            created_count += 1
            print(f"✅ Created invoice for {inv_data['client_name']} - Total: ${invoice.total:,.2f}")
        
        db.commit()
        
        print(f"\n{'='*50}")
        print(f"✅ Successfully created {created_count} invoices!")
        
        # Show all invoices
        all_invoices = db.query(Invoice).filter(Invoice.user_id == user.id).all()
        print(f"\n📄 Total invoices now: {len(all_invoices)}")
        total_amount = sum(inv.total for inv in all_invoices)
        print(f"💰 Total revenue: ${total_amount:,.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding demo invoices...")
    add_demo_invoices()