"""Proposal data models."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ProposalStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ProposalSection(BaseModel):
    """A single section within a proposal."""

    title: str
    content: str
    order: int = 0


class Proposal(BaseModel):
    """A complete business proposal."""

    id: str = Field(default_factory=lambda: f"PROP-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}")
    title: str
    client_name: str
    client_email: Optional[str] = None
    status: ProposalStatus = ProposalStatus.DRAFT
    sections: list[ProposalSection] = []
    total_amount: Decimal = Decimal("0.00")
    currency: str = "USD"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    valid_until: Optional[datetime] = None
