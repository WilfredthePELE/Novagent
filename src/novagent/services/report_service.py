"""Job report service — build structured reports from milestones and deliverables."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from novagent.models.report import JobReport, Milestone, MilestoneStatus


class ReportService:
    """Handles creation and management of job reports."""

    def create_report(
        self,
        title: str,
        client_name: str,
        project_description: str,
        milestones: list[Milestone] | None = None,
        deliverables: list[str] | None = None,
    ) -> JobReport:
        """Create a new job report.

        Args:
            title: Report title.
            client_name: Name of the client.
            project_description: Description of the project.
            milestones: Optional list of milestones.
            deliverables: Optional list of deliverable descriptions.

        Returns:
            A new JobReport instance.
        """
        return JobReport(
            title=title,
            client_name=client_name,
            project_description=project_description,
            milestones=milestones or [],
            deliverables=deliverables or [],
        )

    def add_milestone(
        self,
        report: JobReport,
        title: str,
        description: str | None = None,
        due_date: datetime | None = None,
    ) -> JobReport:
        """Add a milestone to a report.

        Args:
            report: The job report to modify.
            title: Milestone title.
            description: Optional description.
            due_date: Optional due date.

        Returns:
            The updated report.
        """
        milestone = Milestone(
            title=title,
            description=description,
            due_date=due_date,
        )
        report.milestones.append(milestone)
        report.updated_at = datetime.utcnow()
        return report

    def complete_milestone(self, report: JobReport, milestone_index: int) -> JobReport:
        """Mark a milestone as completed.

        Args:
            report: The job report.
            milestone_index: Index of the milestone to complete.

        Returns:
            The updated report.
        """
        if 0 <= milestone_index < len(report.milestones):
            report.milestones[milestone_index].status = MilestoneStatus.COMPLETED
            report.milestones[milestone_index].completed_at = datetime.utcnow()
            report.updated_at = datetime.utcnow()
        return report

    def add_deliverable(self, report: JobReport, deliverable: str) -> JobReport:
        """Add a deliverable to a report.

        Args:
            report: The job report.
            deliverable: Description of the deliverable.

        Returns:
            The updated report.
        """
        report.deliverables.append(deliverable)
        report.updated_at = datetime.utcnow()
        return report

    def finalize(
        self,
        report: JobReport,
        summary: str,
        hours_worked: float | None = None,
    ) -> JobReport:
        """Finalize a report with a summary.

        Args:
            report: The job report.
            summary: Executive summary.
            hours_worked: Optional total hours worked.

        Returns:
            The finalized report.
        """
        report.summary = summary
        if hours_worked is not None:
            report.hours_worked = hours_worked
        report.updated_at = datetime.utcnow()
        return report
