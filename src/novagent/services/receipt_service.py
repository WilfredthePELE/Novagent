"""Receipt management service."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from novagent.models.receipt import Receipt, ReceiptLineItem, ReceiptStatus


class ReceiptService:
    """Handles creation and management of receipts."""

    def create_receipt(
        self,
        paid_by: str,
        amount: Decimal,
        payment_method: str = "bank_transfer",
        line_items: list[ReceiptLineItem] | None = None,
        reference: str | None = None,
        notes: str | None = None,
        related_invoice_id: str | None = None,
    ) -> Receipt:
        """Issue a receipt for a payment.

        Args:
            paid_by: Name of the person/entity that paid.
            amount: Total amount paid.
            payment_method: How the payment was made.
            line_items: Optional breakdown of what was paid for.
            reference: Optional payment reference number.
            notes: Optional notes.
            related_invoice_id: Optional ID of the related invoice.

        Returns:
            A new Receipt instance.
        """
        return Receipt(
            paid_by=paid_by,
            amount=amount,
            payment_method=payment_method,
            line_items=line_items or [],
            reference=reference,
            notes=notes,
            related_invoice_id=related_invoice_id,
        )

    def cancel(self, receipt: Receipt) -> Receipt:
        """Cancel a previously issued receipt."""
        receipt.status = ReceiptStatus.CANCELLED
        return receipt
