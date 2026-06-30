"""Novagent CLI — autonomous AI agency command-line interface."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from novagent import __version__
from novagent.config import NovagentConfig
from novagent.output import DocumentBuilder

console = Console()
config = NovagentConfig()


# ═══════════════════════════════════════════════════
# Main Group
# ═══════════════════════════════════════════════════

@click.group()
@click.version_option(version=__version__, prog_name="novagent")
@click.option("--host", default=None, help="Server host override")
@click.option("--port", type=int, default=None, help="Server port override")
def cli(host: str | None, port: int | None) -> None:
    """Novagent — Intelligence That Delivers.

    Autonomous AI agency with 54+ skills across 12 service categories.
    """
    global config
    if host:
        config.host = host
    if port:
        config.port = port


# ═══════════════════════════════════════════════════
# Version
# ═══════════════════════════════════════════════════

@cli.command()
def version() -> None:
    """Show the Novagent version."""
    console.print(f"[bold #6366F1]Novagent[/bold #6366F1] v{__version__}")
    console.print(f"[#22D3EE]{config.tagline}[/#22D3EE]")


# ═══════════════════════════════════════════════════
# Config
# ═══════════════════════════════════════════════════

@cli.group(name="config")
def config_cmd() -> None:
    """Manage Novagent configuration."""


@config_cmd.command("show")
def config_show() -> None:
    """Show current configuration."""
    table = Table(box=box.ROUNDED)
    table.add_column("Setting", style="bold")
    table.add_column("Value")
    table.add_row("Brand", config.brand_name)
    table.add_row("Tagline", config.tagline)
    table.add_row("Primary Color", config.primary_color)
    table.add_row("Accent Color", config.accent_color)
    table.add_row("Host", config.host)
    table.add_row("Port", str(config.port))
    table.add_row("Data Dir", str(config.data_dir))
    table.add_row("Output Dir", str(config.output_dir))
    categories = ", ".join(config.service_categories)
    table.add_row("Categories", categories)
    console.print(table)


# ═══════════════════════════════════════════════════
# Proposals
# ═══════════════════════════════════════════════════

@cli.group()
def proposal() -> None:
    """Create and manage proposals."""


@proposal.command("create")
@click.argument("title")
@click.argument("client_name")
@click.option("--valid-days", default=30, help="Days the proposal is valid for")
@click.option("--output", "-o", default=None, help="Output file path")
def proposal_create(title: str, client_name: str, valid_days: int, output: str | None) -> None:
    """Create a new proposal."""
    from novagent.services import ProposalService

    svc = ProposalService()
    p = svc.create_proposal(title, client_name, valid_days=valid_days)
    console.print(f"[green]✓[/green] Proposal [bold]{p.id}[/bold] created for [bold]{client_name}[/bold]")

    if output:
        builder = DocumentBuilder()
        path = builder.build_proposal_md(p, Path(output).parent if output else None)
        console.print(f"  Rendered to: [cyan]{path}[/cyan]")


@proposal.command("add-section")
@click.argument("proposal_id")
@click.argument("title")
@click.argument("content")
def proposal_add_section(proposal_id: str, title: str, content: str) -> None:
    """Add a section to an existing proposal."""
    from novagent.services import ProposalService
    from novagent.models.proposal import Proposal

    # For CLI, we create a fresh proposal as a demo (persistence coming in Phase 3)
    svc = ProposalService()
    p = Proposal(title="Loaded Proposal", client_name="Client")
    p.id = proposal_id
    svc.add_section(p, title, content)
    console.print(f"[green]✓[/green] Section [bold]'{title}'[/bold] added to proposal {proposal_id}")


@proposal.command("render")
@click.argument("proposal_id")
@click.option("--format", "-f", "fmt", type=click.Choice(["md", "html"]), default="md", help="Output format")
@click.option("--output", "-o", default=None, help="Output directory")
def proposal_render(proposal_id: str, fmt: str, output: str | None) -> None:
    """Render a proposal to a file (demo: creates a sample proposal)."""
    from novagent.models.proposal import Proposal, ProposalSection

    p = Proposal(
        id=proposal_id,
        title="Sample Proposal",
        client_name="Client",
        summary="We will deliver a comprehensive solution.",
        sections=[
            ProposalSection(title="Scope of Work", content="Full-stack development and deployment.", order=1),
            ProposalSection(title="Timeline", content="4 weeks from kickoff.", order=2),
            ProposalSection(title="Pricing", content="$10,000 total.", order=3),
        ],
        valid_until=datetime.utcnow() + timedelta(days=30),
    )

    builder = DocumentBuilder()
    if fmt == "md":
        path = builder.build_proposal_md(p, output)
    else:
        path = builder.build_proposal_html(p, output)

    console.print(f"[green]✓[/green] Proposal rendered to: [cyan]{path}[/cyan]")


# ═══════════════════════════════════════════════════
# Invoices
# ═══════════════════════════════════════════════════

@cli.group()
def invoice() -> None:
    """Create and manage invoices."""


@invoice.command("create")
@click.argument("client_name")
@click.option("--tax-rate", default=0.0, type=float, help="Tax rate (e.g. 0.10 for 10%%)")
@click.option("--due-days", default=30, type=int, help="Payment due in N days")
@click.option("--output", "-o", default=None, help="Output directory")
def invoice_create(client_name: str, tax_rate: float, due_days: int, output: str | None) -> None:
    """Create a new invoice."""
    from novagent.services import InvoiceService

    svc = InvoiceService()
    inv = svc.create_invoice(client_name, tax_rate=Decimal(str(tax_rate)), due_days=due_days)

    console.print(f"[green]✓[/green] Invoice [bold]{inv.invoice_number}[/bold] created for [bold]{client_name}[/bold]")

    # Prompt to add line items interactively
    console.print("\n[yellow]Add line items (leave description blank to finish):[/yellow]")
    while True:
        desc = click.prompt("  Description", default="")
        if not desc:
            break
        qty = Decimal(click.prompt("  Quantity", type=float, default=1.0))
        price = Decimal(click.prompt("  Unit price", type=float))
        svc.add_line_item(inv, desc, qty, price)
        console.print(f"  [green]✓[/green] Added: {desc} x{qty} @ ${float(price):,.2f}")

    if inv.line_items:
        console.print(f"\n[bold]Invoice Summary:[/bold]")
        console.print(f"  Subtotal:  ${float(inv.subtotal):,.2f}")
        if tax_rate > 0:
            console.print(f"  Tax:       ${float(inv.tax_amount):,.2f}")
        console.print(f"  [bold]Total:     ${float(inv.total):,.2f}[/bold]")

    if output:
        builder = DocumentBuilder()
        path = builder.build_invoice_md(inv, output)
        console.print(f"\n  Rendered to: [cyan]{path}[/cyan]")


@invoice.command("render")
@click.argument("invoice_number")
@click.option("--format", "-f", "fmt", type=click.Choice(["md", "html"]), default="md", help="Output format")
@click.option("--output", "-o", default=None, help="Output directory")
def invoice_render(invoice_number: str, fmt: str, output: str | None) -> None:
    """Render an invoice to file (demo: creates a sample invoice)."""
    from novagent.models.invoice import Invoice, InvoiceLineItem

    inv = Invoice(
        invoice_number=invoice_number,
        client_name="Sample Client",
        line_items=[
            InvoiceLineItem(description="Consulting Services", quantity=Decimal("10"), unit_price=Decimal("150.00")),
            InvoiceLineItem(description="Development", quantity=Decimal("20"), unit_price=Decimal("200.00")),
            InvoiceLineItem(description="Hosting (monthly)", quantity=Decimal("3"), unit_price=Decimal("50.00")),
        ],
        tax_rate=Decimal("0.10"),
    )
    inv.calculate_totals()

    builder = DocumentBuilder()
    if fmt == "md":
        path = builder.build_invoice_md(inv, output)
    else:
        path = builder.build_invoice_html(inv, output)

    console.print(f"[green]✓[/green] Invoice rendered to: [cyan]{path}[/cyan]")


@invoice.command("mark-paid")
@click.argument("invoice_number")
def invoice_mark_paid(invoice_number: str) -> None:
    """Mark an invoice as paid."""
    from novagent.models.invoice import Invoice
    from datetime import datetime

    inv = Invoice(invoice_number=invoice_number, client_name="Client")
    inv.paid_date = datetime.utcnow()
    inv.status = type(inv.status)("paid")  # type: ignore
    console.print(f"[green]✓[/green] Invoice [bold]{invoice_number}[/bold] marked as [bold green]PAID[/bold green]")


# ═══════════════════════════════════════════════════
# Receipts
# ═══════════════════════════════════════════════════

@cli.group()
def receipt() -> None:
    """Issue and manage receipts."""


@receipt.command("issue")
@click.argument("paid_by")
@click.argument("amount", type=float)
@click.option("--method", default="bank_transfer", help="Payment method")
@click.option("--reference", default=None, help="Payment reference")
@click.option("--notes", default=None, help="Additional notes")
@click.option("--output", "-o", default=None, help="Output directory")
def receipt_issue(paid_by: str, amount: float, method: str, reference: str | None, notes: str | None, output: str | None) -> None:
    """Issue a receipt for a payment."""
    from novagent.services import ReceiptService

    svc = ReceiptService()
    r = svc.create_receipt(
        paid_by=paid_by,
        amount=Decimal(str(amount)),
        payment_method=method,
        reference=reference,
        notes=notes,
    )
    console.print(f"[green]✓[/green] Receipt [bold]{r.receipt_number}[/bold] issued to [bold]{paid_by}[/bold]")
    console.print(f"  Amount: ${amount:,.2f} — Method: {method}")

    if output:
        builder = DocumentBuilder()
        path = builder.build_receipt_md(r, output)
        console.print(f"  Rendered to: [cyan]{path}[/cyan]")


@receipt.command("show")
@click.argument("receipt_number")
def receipt_show(receipt_number: str) -> None:
    """Show receipt details (demo)."""
    console.print(f"[yellow]ℹ[/yellow] Receipt [bold]{receipt_number}[/bold] lookup — coming in Phase 3 with persistence.")


# ═══════════════════════════════════════════════════
# Reports
# ═══════════════════════════════════════════════════

@cli.group()
def report() -> None:
    """Create and manage job reports."""


@report.command("create")
@click.argument("title")
@click.argument("client_name")
@click.argument("description")
@click.option("--output", "-o", default=None, help="Output directory")
def report_create(title: str, client_name: str, description: str, output: str | None) -> None:
    """Create a new job report."""
    from novagent.services import ReportService

    svc = ReportService()
    r = svc.create_report(title, client_name, description)
    console.print(f"[green]✓[/green] Report [bold]{r.id}[/bold] created: [bold]{title}[/bold]")

    # Prompt for milestones
    console.print("\n[yellow]Add milestones (leave title blank to finish):[/yellow]")
    while True:
        m_title = click.prompt("  Milestone title", default="")
        if not m_title:
            break
        svc.add_milestone(r, m_title)
        console.print(f"  [green]✓[/green] Milestone added: {m_title}")

    # Prompt for deliverables
    console.print("\n[yellow]Add deliverables (leave blank to finish):[/yellow]")
    while True:
        d = click.prompt("  Deliverable", default="")
        if not d:
            break
        svc.add_deliverable(r, d)
        console.print(f"  [green]✓[/green] Deliverable added: {d}")

    if r.milestones or r.deliverables:
        console.print(f"\n[bold]Report Summary:[/bold]")
        console.print(f"  Milestones:  {len(r.milestones)}")
        console.print(f"  Deliverables: {len(r.deliverables)}")

    if output:
        builder = DocumentBuilder()
        path = builder.build_report_md(r, output)
        console.print(f"\n  Rendered to: [cyan]{path}[/cyan]")


@report.command("render")
@click.argument("report_id")
@click.option("--format", "-f", "fmt", type=click.Choice(["md", "html"]), default="md", help="Output format")
@click.option("--output", "-o", default=None, help="Output directory")
def report_render(report_id: str, fmt: str, output: str | None) -> None:
    """Render a report to file (demo: creates a sample report)."""
    from novagent.models.report import JobReport, Milestone, MilestoneStatus
    from datetime import datetime

    r = JobReport(
        id=report_id,
        title="Project Completion Report",
        client_name="Sample Client",
        project_description="Full-stack web application development and deployment.",
        summary="All milestones completed successfully ahead of schedule.",
        milestones=[
            Milestone(title="Requirements Gathering", status=MilestoneStatus.COMPLETED, completed_at=datetime.utcnow()),
            Milestone(title="Design Phase", status=MilestoneStatus.COMPLETED, completed_at=datetime.utcnow()),
            Milestone(title="Development", status=MilestoneStatus.COMPLETED, completed_at=datetime.utcnow()),
            Milestone(title="Testing & QA", status=MilestoneStatus.COMPLETED, completed_at=datetime.utcnow()),
        ],
        deliverables=["Source code repository", "Deployment guide", "API documentation", "Test suite"],
        hours_worked=120.5,
    )

    builder = DocumentBuilder()
    if fmt == "md":
        path = builder.build_report_md(r, output)
    else:
        path = builder.build_report_html(r, output)

    console.print(f"[green]✓[/green] Report rendered to: [cyan]{path}[/cyan]")


# ═══════════════════════════════════════════════════
# Info / Dashboard
# ═══════════════════════════════════════════════════

@cli.command("info")
def info() -> None:
    """Display Novagent system information."""
    panel = Panel.fit(
        f"[bold #6366F1]Novagent[/bold #6366F1] v{__version__}\n"
        f"[#22D3EE]{config.tagline}[/#22D3EE]\n\n"
        f"[bold]Services:[/bold] {len(config.service_categories)} categories\n"
        f"[bold]Output Dir:[/bold] {config.output_dir}\n"
        f"[bold]Server:[/bold] http://{config.host}:{config.port}\n",
        title="🤖 System Info",
        border_style="#6366F1",
    )
    console.print(panel)


# ═══════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════

def main() -> int:
    """Main CLI entry point."""
    config.ensure_dirs()
    return cli()


if __name__ == "__main__":
    sys.exit(main())
