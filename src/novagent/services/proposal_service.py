"""Proposal generation and management service."""

from __future__ import annotations

from datetime import datetime, timedelta

from novagent.models.proposal import Proposal, ProposalSection, ProposalStatus


class ProposalService:
    """Handles creation, management, and rendering of proposals."""

    def create_proposal(
        self,
        title: str,
        client_name: str,
        sections: list[ProposalSection] | None = None,
        valid_days: int = 30,
    ) -> Proposal:
        """Create a new proposal with default settings.

        Args:
            title: The proposal title.
            client_name: Name of the client.
            sections: Optional list of proposal sections.
            valid_days: Number of days the proposal is valid for.

        Returns:
            A new Proposal instance.
        """
        proposal = Proposal(
            title=title,
            client_name=client_name,
            sections=sections or [],
            valid_until=datetime.utcnow() + timedelta(days=valid_days),
        )
        return proposal

    def add_section(self, proposal: Proposal, title: str, content: str) -> Proposal:
        """Add a section to an existing proposal.

        Args:
            proposal: The proposal to modify.
            title: Section title.
            content: Section body content.

        Returns:
            The updated proposal.
        """
        section = ProposalSection(
            title=title,
            content=content,
            order=len(proposal.sections),
        )
        proposal.sections.append(section)
        proposal.updated_at = datetime.utcnow()
        return proposal

    def submit(self, proposal: Proposal) -> Proposal:
        """Mark a proposal as sent.

        Args:
            proposal: The proposal to submit.

        Returns:
            The updated proposal.
        """
        proposal.status = ProposalStatus.SENT
        proposal.updated_at = datetime.utcnow()
        return proposal
