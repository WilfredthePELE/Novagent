"""Receipt data model."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ReceiptStatus(str, Enum):
    ISSUED = "issued"
    CANCELLED = "cancelled"


class ReceiptLineItem(BaseModel):
    """A single item on a receipt."""

    description: str
    amount: Decimal


class Receipt(BaseModel):
    """A payment receipt."""

    receipt_number: str = Field(default_factory=lambda: f"RCT-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}")
    paid_by: str
    amount: Decimal
    currency: str = "USD"
    payment_method: str = "bank_transfer"
    status: ReceiptStatus = ReceiptStatus.ISSUED
    line_items: list[ReceiptLineItem] = []
    reference: Optional[str] = None
    notes: Optional[str] = None
    issue_date: datetime = Field(default_factory=datetime.utcnow)
    related_invoice_id: Optional[str] = None
