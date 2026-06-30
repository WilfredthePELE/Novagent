"""Invoice data models."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class InvoiceLineItem(BaseModel):
    """A single line item on an invoice."""

    description: str
    quantity: Decimal = Decimal("1")
    unit_price: Decimal
    total: Optional[Decimal] = None

    def model_post_init(self, __context) -> None:
        if self.total is None:
            self.total = self.quantity * self.unit_price


class Invoice(BaseModel):
    """A complete invoice document."""

    id: str = Field(default_factory=lambda: f"INV-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}")
    invoice_number: Optional[str] = None
    client_name: str
    client_address: Optional[str] = None
    status: InvoiceStatus = InvoiceStatus.DRAFT
    line_items: list[InvoiceLineItem] = []
    subtotal: Decimal = Decimal("0.00")
    tax_rate: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    total: Decimal = Decimal("0.00")
    currency: str = "USD"
    issue_date: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None

    def model_post_init(self, __context) -> None:
        if self.invoice_number is None:
            self.invoice_number = self.id

    def calculate_totals(self) -> None:
        """Recalculate subtotal, tax, and total."""
        self.subtotal = sum((item.total or Decimal("0")) for item in self.line_items)
        self.tax_amount = (self.subtotal * self.tax_rate).quantize(Decimal("0.01"))
        self.total = (self.subtotal + self.tax_amount).quantize(Decimal("0.01"))
