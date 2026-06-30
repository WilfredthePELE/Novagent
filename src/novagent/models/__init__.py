"""Data models for Novagent services."""

from __future__ import annotations

from .proposal import Proposal, ProposalSection
from .invoice import Invoice, InvoiceLineItem
from .report import JobReport, Milestone

__all__ = [
    "Proposal",
    "ProposalSection",
    "Invoice",
    "InvoiceLineItem",
    "JobReport",
    "Milestone",
]
