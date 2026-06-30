"""Phase 2 tests — template rendering, receipt service, report service, document builder, CLI."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pathlib import Path
import tempfile


# ── Receipt Model & Service ───────────────────────────────────

def test_receipt_model():
    """Verify receipt model creation and defaults."""
    from novagent.models.receipt import Receipt, ReceiptLineItem, ReceiptStatus

    r = Receipt(paid_by="Acme Corp", amount=Decimal("1500.00"))
    assert r.receipt_number.startswith("RCT-")
    assert r.status == ReceiptStatus.ISSUED
    assert r.currency == "USD"
    assert r.payment_method == "bank_transfer"

    # With line items
    r2 = Receipt(
        paid_by="Client Inc.",
        amount=Decimal("500.00"),
        line_items=[
            ReceiptLineItem(description="Consulting", amount=Decimal("300.00")),
            ReceiptLineItem(description="Expenses", amount=Decimal("200.00")),
        ],
    )
    assert len(r2.line_items) == 2
    assert r2.line_items[0].description == "Consulting"


def test_receipt_service():
    """Verify receipt service can issue and cancel receipts."""
    from novagent.services import ReceiptService
    from novagent.models.receipt import ReceiptStatus

    svc = ReceiptService()
    r = svc.create_receipt(
        paid_by="Client Inc.",
        amount=Decimal("2500.00"),
        payment_method="credit_card",
        reference="PAY-12345",
        notes="Full payment",
    )
    assert r.amount == Decimal("2500.00")
    assert r.reference == "PAY-12345"

    svc.cancel(r)
    assert r.status == ReceiptStatus.CANCELLED


# ── Report Service ────────────────────────────────────────────

def test_report_service():
    """Verify report service can create, add milestones, and finalize."""
    from novagent.services import ReportService
    from novagent.models.report import Milestone

    svc = ReportService()
    r = svc.create_report(
        title="Website Redesign",
        client_name="Acme Corp",
        project_description="Complete redesign of corporate website.",
    )
    assert r.id.startswith("JR-")

    svc.add_milestone(r, "Discovery Phase", "Initial client meetings")
    svc.add_milestone(r, "Design Phase", "Wireframes and mockups")
    assert len(r.milestones) == 2

    svc.complete_milestone(r, 0)
    assert r.milestones[0].status.value == "completed"
    assert r.milestones[0].completed_at is not None

    svc.add_deliverable(r, "Source code")
    svc.add_deliverable(r, "Documentation")
    assert len(r.deliverables) == 2

    svc.finalize(r, "Project completed successfully.", hours_worked=80.5)
    assert r.summary == "Project completed successfully."
    assert r.hours_worked == 80.5


# ── Template Renderer ─────────────────────────────────────────

def test_template_renderer():
    """Verify template renderer loads and renders templates."""
    from novagent.templates import TemplateRenderer
    from novagent.models.proposal import Proposal, ProposalSection

    renderer = TemplateRenderer()
    p = Proposal(
        title="Test",
        client_name="Client",
        sections=[ProposalSection(title="Scope", content="Work", order=1)],
    )
    output = renderer.render("proposal.md.j2", proposal=p)
    assert "Test" in output
    assert "Client" in output
    assert "Intelligence That Delivers" in output
    assert "Scope" in output


def test_template_renderer_to_file():
    """Verify template renderer writes files correctly."""
    from novagent.templates import TemplateRenderer
    from novagent.models.proposal import Proposal

    renderer = TemplateRenderer()
    p = Proposal(title="File Test", client_name="Client")

    with tempfile.TemporaryDirectory() as tmpdir:
        path = renderer.render_to_file("proposal.md.j2", Path(tmpdir) / "test.md", proposal=p)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "File Test" in content
        assert "Client" in content


# ── Document Builder ──────────────────────────────────────────

def test_document_builder_proposal():
    """Verify document builder produces proposal markdown."""
    from novagent.output import DocumentBuilder
    from novagent.models.proposal import Proposal

    builder = DocumentBuilder()
    p = Proposal(title="Build Test", client_name="Client")

    with tempfile.TemporaryDirectory() as tmpdir:
        path = builder.build_proposal_md(p, tmpdir)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "Build Test" in content


def test_document_builder_proposal_html():
    """Verify document builder produces proposal HTML."""
    from novagent.output import DocumentBuilder
    from novagent.models.proposal import Proposal

    builder = DocumentBuilder()
    p = Proposal(title="HTML Test", client_name="Client")

    with tempfile.TemporaryDirectory() as tmpdir:
        path = builder.build_proposal_html(p, tmpdir)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "HTML Test" in content


def test_document_builder_invoice_md():
    """Verify document builder produces invoice markdown."""
    from novagent.output import DocumentBuilder
    from novagent.models.invoice import Invoice, InvoiceLineItem

    builder = DocumentBuilder()
    inv = Invoice(
        client_name="Client",
        line_items=[InvoiceLineItem(description="Work", quantity=Decimal("1"), unit_price=Decimal("500"))],
    )
    inv.calculate_totals()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = builder.build_invoice_md(inv, tmpdir)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "Invoice" in content
        assert "$500.00" in content


def test_document_builder_invoice_html():
    """Verify document builder produces invoice HTML."""
    from novagent.output import DocumentBuilder
    from novagent.models.invoice import Invoice, InvoiceLineItem

    builder = DocumentBuilder()
    inv = Invoice(
        client_name="Client",
        line_items=[InvoiceLineItem(description="Work", quantity=Decimal("1"), unit_price=Decimal("500"))],
    )
    inv.calculate_totals()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = builder.build_invoice_html(inv, tmpdir)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "$500.00" in content


def test_document_builder_receipt():
    """Verify document builder produces receipt markdown."""
    from novagent.output import DocumentBuilder
    from novagent.models.receipt import Receipt

    builder = DocumentBuilder()
    r = Receipt(paid_by="Client", amount=Decimal("1000.00"))

    with tempfile.TemporaryDirectory() as tmpdir:
        path = builder.build_receipt_md(r, tmpdir)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "Receipt" in content
        assert "$1,000.00" in content


def test_document_builder_report():
    """Verify document builder produces report markdown and HTML."""
    from novagent.output import DocumentBuilder
    from novagent.models.report import JobReport

    builder = DocumentBuilder()
    r = JobReport(title="Project X", client_name="Client", project_description="Work")

    with tempfile.TemporaryDirectory() as tmpdir:
        path = builder.build_report_md(r, tmpdir)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "Project X" in content

    with tempfile.TemporaryDirectory() as tmpdir:
        path = builder.build_report_html(r, tmpdir)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content


# ── CLI Smoke Tests ───────────────────────────────────────────

def test_cli_version():
    """Verify CLI version command works."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "Novagent" in result.output
    assert "0.1.0" in result.output


def test_cli_info():
    """Verify CLI info command works."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "System Info" in result.output


def test_cli_config_show():
    """Verify CLI config show command works."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["config", "show"])
    assert result.exit_code == 0, f"Exit code {result.exit_code}: {result.output}"
    assert "Brand" in result.output


def test_cli_proposal_create():
    """Verify CLI proposal create works."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["proposal", "create", "Test Proposal", "Acme Corp"])
    assert result.exit_code == 0, f"Exit code {result.exit_code}: {result.output}"
    assert "PROP-" in result.output
    assert "Acme Corp" in result.output


def test_cli_proposal_render():
    """Verify CLI proposal render works."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(cli, ["proposal", "render", "PROP-DEMO", "--output", tmpdir])
        assert result.exit_code == 0, f"Exit code {result.exit_code}: {result.output}"
        assert "rendered to" in result.output.lower()


def test_cli_invoice_create():
    """Verify CLI invoice create works (non-interactive — skip prompts)."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    # Provide empty input to skip interactive line items
    result = runner.invoke(cli, ["invoice", "create", "Acme Corp", "--tax-rate", "0.10"], input="\n")
    assert result.exit_code == 0, f"Exit code {result.exit_code}: {result.output}"
    assert "INV-" in result.output


def test_cli_invoice_render():
    """Verify CLI invoice render works."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(cli, ["invoice", "render", "INV-DEMO", "--output", tmpdir])
        assert result.exit_code == 0, f"Exit code {result.exit_code}: {result.output}"
        assert "rendered to" in result.output.lower()


def test_cli_receipt_issue():
    """Verify CLI receipt issue works."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["receipt", "issue", "Acme Corp", "1500", "--method", "wire"])
    assert result.exit_code == 0, f"Exit code {result.exit_code}: {result.output}"
    assert "RCT-" in result.output


def test_cli_report_create():
    """Verify CLI report create works (non-interactive — skip prompts)."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    result = runner.invoke(
        cli, ["report", "create", "Project Report", "Acme Corp", "Website work"],
        input="\n\n",  # skip milestones, skip deliverables
    )
    assert result.exit_code == 0, f"Exit code {result.exit_code}: {result.output}"
    assert "JR-" in result.output


def test_cli_report_render():
    """Verify CLI report render works."""
    from click.testing import CliRunner
    from novagent.main import cli

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(cli, ["report", "render", "JR-DEMO", "--output", tmpdir])
        assert result.exit_code == 0, f"Exit code {result.exit_code}: {result.output}"
        assert "rendered to" in result.output.lower()
