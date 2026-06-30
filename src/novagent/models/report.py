"""Job report data models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MilestoneStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class Milestone(BaseModel):
    """A project milestone tracked in a job report."""

    title: str
    description: Optional[str] = None
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: list[str] = []


class JobReport(BaseModel):
    """A structured report for a completed or ongoing job."""

    id: str = Field(default_factory=lambda: f"JR-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}")
    title: str
    client_name: str
    project_description: str
    milestones: list[Milestone] = []
    summary: Optional[str] = None
    deliverables: list[str] = []
    hours_worked: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
