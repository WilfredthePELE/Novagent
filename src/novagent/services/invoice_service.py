"""Invoice generation and management service."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

from novagent.models.invoice import Invoice, InvoiceLineItem, InvoiceStatus


class InvoiceService:
    """Handles creation, management, and tracking of invoices."""

    def create_invoice(
        self,
        client_name: str,
        line_items: list[InvoiceLineItem] | None = None,
        tax_rate: Decimal = Decimal("0.00"),
        due_days: int = 30,
    ) -> Invoice:
        """Create a new invoice.

        Args:
            client_name: Name of the client.
            line_items: Optional list of line items.
            tax_rate: Tax rate as a decimal (e.g., 0.10 for 10%).
            due_days: Number of days until payment is due.

        Returns:
            A new Invoice instance.
        """
        invoice = Invoice(
            client_name=client_name,
            line_items=line_items or [],
            tax_rate=tax_rate,
            due_date=datetime.utcnow() + timedelta(days=due_days),
        )
        invoice.calculate_totals()
        return invoice

    def add_line_item(self, invoice: Invoice, description: str, quantity: Decimal, unit_price: Decimal) -> Invoice:
        """Add a line item to an existing invoice.

        Args:
            invoice: The invoice to modify.
            description: Description of the item/service.
            quantity: Number of units.
            unit_price: Price per unit.

        Returns:
            The updated invoice.
        """
        item = InvoiceLineItem(
            description=description,
            quantity=quantity,
            unit_price=unit_price,
        )
        invoice.line_items.append(item)
        invoice.calculate_totals()
        return invoice

    def mark_paid(self, invoice: Invoice) -> Invoice:
        """Mark an invoice as paid.

        Args:
            invoice: The invoice to mark paid.

        Returns:
            The updated invoice.
        """
        invoice.status = InvoiceStatus.PAID
        invoice.paid_date = datetime.utcnow()
        return invoice
