import sys
import os
from datetime import datetime, timedelta
import random
import string

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# First, initialize the database tables
from app.database import init_db, SessionLocal
from app.models import User, Invoice, InvoiceItem, Expense, Base
from app.services.auth import hash_password

def add_demo_data():
    print("\n" + "="*60)
    print("🚀 STARTING DEMO DATA SETUP")
    print("="*60)
    
    # STEP 1: Initialize database (create tables)
    print("\n📁 STEP 1: Initializing database...")
    init_db()
    print("   ✅ Database tables created successfully!")
    
    db = SessionLocal()
    
    try:
        # ============================================================
        # STEP 2: Create users with different roles
        # ============================================================
        print("\n📝 STEP 2: Creating users...")
        
        users = {}
        demo_users = [
            ("Admin User", "admin@demo.com", "admin123", "admin"),
            ("Manager User", "manager@demo.com", "manager123", "manager"),
            ("Viewer User", "viewer@demo.com", "viewer123", "user"),
        ]
        
        for name, email, password, role in demo_users:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    name=name,
                    email=email,
                    hashed_password=hash_password(password),
                    role=role,
                    is_active=True
                )
                db.add(user)
                db.flush()
                print(f"   ✅ Created user: {email} (Role: {role})")
            else:
                print(f"   ⚠️ User already exists: {email} (Role: {user.role})")
            users[role] = user
        
        db.commit()
        
        # ============================================================
        # STEP 3: Add Demo Invoices for ADMIN
        # ============================================================
        print("\n📄 STEP 3: Adding invoices for ADMIN...")
        
        def generate_invoice_number(prefix="INV"):
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            return f"{prefix}-{datetime.now().strftime('%Y%m')}-{suffix}"
        
        admin_invoices = [
            {
                "client_name": "TechCorp Solutions",
                "client_email": "billing@techcorp.com",
                "status": "paid",
                "notes": "Payment received via wire transfer. Thank you!",
                "due_date": datetime.now() - timedelta(days=5),
                "items": [
                    {"description": "Web Development Services", "quantity": 40, "unit_price": 75},
                    {"description": "SEO Optimization", "quantity": 1, "unit_price": 500},
                    {"description": "Database Setup", "quantity": 1, "unit_price": 300},
                ]
            },
            {
                "client_name": "Creative Agency LLC",
                "client_email": "accounts@creative.com",
                "status": "sent",
                "notes": "Please pay within 15 days",
                "due_date": datetime.now() + timedelta(days=10),
                "items": [
                    {"description": "Logo Design", "quantity": 2, "unit_price": 250},
                    {"description": "Brand Guidelines", "quantity": 1, "unit_price": 400},
                    {"description": "Business Cards", "quantity": 500, "unit_price": 0.50},
                ]
            },
            {
                "client_name": "Startup Ventures",
                "client_email": "finance@startup.com",
                "status": "draft",
                "notes": "Awaiting client approval for the proposal",
                "due_date": datetime.now() + timedelta(days=20),
                "items": [
                    {"description": "Mobile App Development", "quantity": 60, "unit_price": 85},
                    {"description": "UI/UX Design", "quantity": 30, "unit_price": 65},
                    {"description": "API Integration", "quantity": 20, "unit_price": 95},
                ]
            },
            {
                "client_name": "Global Retail Group",
                "client_email": "accounting@globalretail.com",
                "status": "paid",
                "notes": "Thank you for your business!",
                "due_date": datetime.now() - timedelta(days=2),
                "items": [
                    {"description": "E-commerce Platform", "quantity": 1, "unit_price": 3500},
                    {"description": "Payment Gateway Integration", "quantity": 1, "unit_price": 800},
                    {"description": "Inventory System", "quantity": 1, "unit_price": 1200},
                ]
            },
            {
                "client_name": "Digital Marketing Inc",
                "client_email": "billing@digitalmarketing.com",
                "status": "sent",
                "notes": "Net 30 payment terms",
                "due_date": datetime.now() + timedelta(days=15),
                "items": [
                    {"description": "Social Media Management", "quantity": 3, "unit_price": 350},
                    {"description": "Content Creation", "quantity": 10, "unit_price": 120},
                    {"description": "PPC Campaign", "quantity": 1, "unit_price": 1500},
                ]
            },
        ]
        
        for inv_data in admin_invoices:
            invoice = Invoice(
                invoice_number=generate_invoice_number("INV-ADM"),
                client_name=inv_data["client_name"],
                client_email=inv_data["client_email"],
                status=inv_data["status"],
                notes=inv_data["notes"],
                due_date=inv_data["due_date"],
                user_id=users["admin"].id
            )
            db.add(invoice)
            db.flush()
            
            for item_data in inv_data["items"]:
                item = InvoiceItem(
                    description=item_data["description"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    invoice_id=invoice.id
                )
                db.add(item)
            
            total = sum(i["quantity"] * i["unit_price"] for i in inv_data["items"])
            print(f"   📄 {inv_data['client_name']}: ${total:,.2f} ({inv_data['status']})")
        
        # ============================================================
        # STEP 4: Add Demo Invoices for MANAGER
        # ============================================================
        print("\n📄 STEP 4: Adding invoices for MANAGER...")
        
        manager_invoices = [
            {
                "client_name": "Freelance Hub",
                "client_email": "payments@freelancehub.com",
                "status": "paid",
                "notes": "Payment confirmed. Great working with you!",
                "due_date": datetime.now() - timedelta(days=3),
                "items": [
                    {"description": "Consulting Services", "quantity": 15, "unit_price": 100},
                    {"description": "Training Session", "quantity": 5, "unit_price": 75},
                ]
            },
            {
                "client_name": "Small Business Co",
                "client_email": "finance@smallbiz.com",
                "status": "sent",
                "notes": "Quote pending approval",
                "due_date": datetime.now() + timedelta(days=25),
                "items": [
                    {"description": "Website Maintenance", "quantity": 6, "unit_price": 150},
                    {"description": "Hosting Services", "quantity": 12, "unit_price": 25},
                    {"description": "Email Support", "quantity": 3, "unit_price": 100},
                ]
            },
            {
                "client_name": "Local Restaurant Chain",
                "client_email": "owner@restaurant.com",
                "status": "draft",
                "notes": "Proposal for digital menu system",
                "due_date": datetime.now() + timedelta(days=30),
                "items": [
                    {"description": "Digital Menu Boards", "quantity": 4, "unit_price": 500},
                    {"description": "Software License", "quantity": 1, "unit_price": 1200},
                ]
            },
        ]
        
        for inv_data in manager_invoices:
            invoice = Invoice(
                invoice_number=generate_invoice_number("INV-MGR"),
                client_name=inv_data["client_name"],
                client_email=inv_data["client_email"],
                status=inv_data["status"],
                notes=inv_data["notes"],
                due_date=inv_data["due_date"],
                user_id=users["manager"].id
            )
            db.add(invoice)
            db.flush()
            
            for item_data in inv_data["items"]:
                item = InvoiceItem(
                    description=item_data["description"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    invoice_id=invoice.id
                )
                db.add(item)
            
            total = sum(i["quantity"] * i["unit_price"] for i in inv_data["items"])
            print(f"   📄 {inv_data['client_name']}: ${total:,.2f} ({inv_data['status']})")
        
        # ============================================================
        # STEP 5: Add Demo Expenses for ADMIN
        # ============================================================
        print("\n💰 STEP 5: Adding expenses for ADMIN...")
        
        admin_expenses = [
            {"title": "Office Rent - Downtown", "amount": 2500.00, "category": "utilities", "date": datetime.now() - timedelta(days=5)},
            {"title": "AWS Cloud Services", "amount": 450.00, "category": "software", "date": datetime.now() - timedelta(days=2)},
            {"title": "Team Lunch Meeting", "amount": 320.50, "category": "food", "date": datetime.now() - timedelta(days=1)},
            {"title": "Flight to Tech Conference", "amount": 850.00, "category": "travel", "date": datetime.now() - timedelta(days=7)},
            {"title": "Google Ads Campaign", "amount": 1200.00, "category": "marketing", "date": datetime.now() - timedelta(days=3)},
            {"title": "New MacBook Pro", "amount": 3200.00, "category": "hardware", "date": datetime.now() - timedelta(days=10)},
            {"title": "Employee Salaries - May", "amount": 15000.00, "category": "salary", "date": datetime.now() - timedelta(days=1)},
            {"title": "Office Supplies", "amount": 180.75, "category": "other", "date": datetime.now() - timedelta(days=4)},
            {"title": "LinkedIn Ads", "amount": 500.00, "category": "marketing", "date": datetime.now() - timedelta(days=6)},
            {"title": "Internet & Phone", "amount": 200.00, "category": "utilities", "date": datetime.now() - timedelta(days=8)},
        ]
        
        for exp_data in admin_expenses:
            expense = Expense(
                title=exp_data["title"],
                amount=exp_data["amount"],
                category=exp_data["category"],
                description=f"Auto-generated expense: {exp_data['title']}",
                date=exp_data["date"],
                user_id=users["admin"].id
            )
            db.add(expense)
            print(f"   💰 {exp_data['title']}: ${exp_data['amount']:,.2f}")
        
        # ============================================================
        # STEP 6: Add Demo Expenses for MANAGER
        # ============================================================
        print("\n💰 STEP 6: Adding expenses for MANAGER...")
        
        manager_expenses = [
            {"title": "Client Dinner at Steakhouse", "amount": 245.30, "category": "food", "date": datetime.now() - timedelta(days=3)},
            {"title": "Uber to Client Meeting", "amount": 45.00, "category": "travel", "date": datetime.now() - timedelta(days=2)},
            {"title": "Zoom Pro Subscription", "amount": 60.00, "category": "software", "date": datetime.now() - timedelta(days=5)},
            {"title": "Printing Services", "amount": 89.99, "category": "other", "date": datetime.now() - timedelta(days=1)},
            {"title": "Coffee with Client", "amount": 12.50, "category": "food", "date": datetime.now() - timedelta(days=4)},
            {"title": "Dropbox Storage", "amount": 15.00, "category": "software", "date": datetime.now() - timedelta(days=6)},
        ]
        
        for exp_data in manager_expenses:
            expense = Expense(
                title=exp_data["title"],
                amount=exp_data["amount"],
                category=exp_data["category"],
                description=f"Auto-generated expense: {exp_data['title']}",
                date=exp_data["date"],
                user_id=users["manager"].id
            )
            db.add(expense)
            print(f"   💰 {exp_data['title']}: ${exp_data['amount']:,.2f}")
        
        # ============================================================
        # STEP 7: Add Demo Expenses for VIEWER
        # ============================================================
        print("\n💰 STEP 7: Adding expenses for VIEWER...")
        
        viewer_expenses = [
            {"title": "Coffee Meeting with Client", "amount": 25.50, "category": "food", "date": datetime.now() - timedelta(days=4)},
            {"title": "USB Drive 64GB", "amount": 15.99, "category": "hardware", "date": datetime.now() - timedelta(days=2)},
            {"title": "Notebooks & Pens", "amount": 8.50, "category": "other", "date": datetime.now() - timedelta(days=1)},
            {"title": "Lunch with Team", "amount": 18.75, "category": "food", "date": datetime.now() - timedelta(days=3)},
        ]
        
        for exp_data in viewer_expenses:
            expense = Expense(
                title=exp_data["title"],
                amount=exp_data["amount"],
                category=exp_data["category"],
                description=f"Auto-generated expense: {exp_data['title']}",
                date=exp_data["date"],
                user_id=users["user"].id
            )
            db.add(expense)
            print(f"   💰 {exp_data['title']}: ${exp_data['amount']:,.2f}")
        
        # ============================================================
        # STEP 8: Commit all changes
        # ============================================================
        db.commit()
        
        # ============================================================
        # STEP 9: Print Summary
        # ============================================================
        print("\n" + "="*60)
        print("🎉 DEMO DATA ADDED SUCCESSFULLY!")
        print("="*60)
        
        # Calculate totals
        total_invoices = db.query(Invoice).count()
        total_expenses = db.query(Expense).count()
        total_revenue = sum(i.total for i in db.query(Invoice).all())
        total_cost = sum(e.amount for e in db.query(Expense).all())
        
        print(f"\n📊 OVERALL SUMMARY:")
        print(f"   ├─ Total Invoices: {total_invoices}")
        print(f"   ├─ Total Revenue: ${total_revenue:,.2f}")
        print(f"   ├─ Total Expenses: {total_expenses}")
        print(f"   ├─ Total Cost: ${total_cost:,.2f}")
        print(f"   └─ Net Profit: ${(total_revenue - total_cost):,.2f}")
        
        print(f"\n👥 USERS SUMMARY:")
        for role, user in users.items():
            inv_count = db.query(Invoice).filter(Invoice.user_id == user.id).count()
            exp_count = db.query(Expense).filter(Expense.user_id == user.id).count()
            inv_total = sum(i.total for i in db.query(Invoice).filter(Invoice.user_id == user.id).all())
            exp_total = sum(e.amount for e in db.query(Expense).filter(Expense.user_id == user.id).all())
            print(f"\n   📌 {role.upper()}:")
            print(f"      ├─ Email: {user.email}")
            print(f"      ├─ Password: {role}123")
            print(f"      ├─ Invoices: {inv_count} (${inv_total:,.2f})")
            print(f"      └─ Expenses: {exp_count} (${exp_total:,.2f})")
        
        print("\n" + "="*60)
        print("🔑 LOGIN CREDENTIALS:")
        print("   Admin:   admin@demo.com / admin123")
        print("   Manager: manager@demo.com / manager123")
        print("   Viewer:  viewer@demo.com / viewer123")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_demo_data()