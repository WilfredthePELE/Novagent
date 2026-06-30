"""Data models for Novagent services."""

from __future__ import annotations

from .invoice import Invoice, InvoiceLineItem, InvoiceStatus
from .proposal import Proposal, ProposalSection, ProposalStatus
from .receipt import Receipt, ReceiptLineItem, ReceiptStatus
from .report import JobReport, Milestone, MilestoneStatus

__all__ = [
    "Invoice",
    "InvoiceLineItem",
    "InvoiceStatus",
    "Proposal",
    "ProposalSection",
    "ProposalStatus",
    "Receipt",
    "ReceiptLineItem",
    "ReceiptStatus",
    "JobReport",
    "Milestone",
    "MilestoneStatus",
]
