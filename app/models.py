from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime
import enum


class Base(DeclarativeBase):
    pass


class ExpenseCategory(str, enum.Enum):
    food = "food"
    travel = "travel"
    utilities = "utilities"
    software = "software"
    hardware = "hardware"
    marketing = "marketing"
    salary = "salary"
    other = "other"


class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    invoices = relationship("Invoice", back_populates="owner", cascade="all, delete")
    expenses = relationship("Expense", back_populates="owner", cascade="all, delete")


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    client_name = Column(String(150), nullable=False)
    client_email = Column(String(150))
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.draft)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete")

    @property
    def total(self):
        return sum(item.quantity * item.unit_price for item in self.items)


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    invoice = relationship("Invoice", back_populates="items")

    @property
    def subtotal(self):
        return self.quantity * self.unit_price


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(ExpenseCategory), default=ExpenseCategory.other)
    description = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="expenses")
