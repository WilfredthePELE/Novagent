"""Business logic services for Novagent."""

from __future__ import annotations

from .proposal_service import ProposalService
from .invoice_service import InvoiceService

__all__ = [
    "ProposalService",
    "InvoiceService",
]
