"""Placeholder tests — replace as modules are built."""


def test_import():
    """Verify the package imports correctly."""
    import novagent  # noqa: F401

    assert novagent.__version__ == "0.1.0"


def test_config_defaults():
    """Verify default configuration loads."""
    from novagent.config import NovagentConfig

    cfg = NovagentConfig()
    assert cfg.brand_name == "Novagent"
    assert cfg.tagline == "Intelligence That Delivers"
    assert cfg.primary_color == "#6366F1"
    assert cfg.accent_color == "#22D3EE"
    assert len(cfg.service_categories) == 12


def test_proposal_model():
    """Verify proposal model creation and defaults."""
    from novagent.models import Proposal

    p = Proposal(title="Test Proposal", client_name="Acme Corp")
    assert p.id.startswith("PROP-")
    assert p.status.value == "draft"
    assert p.currency == "USD"


def test_invoice_model():
    """Verify invoice model creation and calculation."""
    from decimal import Decimal
    from novagent.models import Invoice, InvoiceLineItem

    inv = Invoice(
        client_name="Acme Corp",
        line_items=[
            InvoiceLineItem(description="Consulting", quantity=Decimal("10"), unit_price=Decimal("150.00")),
        ],
        tax_rate=Decimal("0.10"),
    )
    inv.calculate_totals()
    assert inv.subtotal == Decimal("1500.00")
    assert inv.tax_amount == Decimal("150.00")
    assert inv.total == Decimal("1650.00")


def test_proposal_service():
    """Verify proposal service creates and submits proposals."""
    from novagent.services import ProposalService

    svc = ProposalService()
    p = svc.create_proposal("Website Redesign", "Client Inc.")
    svc.add_section(p, "Scope", "Full redesign")
    assert len(p.sections) == 1
    svc.submit(p)
    assert p.status.value == "sent"


def test_invoice_service():
    """Verify invoice service creates and manages invoices."""
    from decimal import Decimal
    from novagent.services import InvoiceService

    svc = InvoiceService()
    inv = svc.create_invoice("Client Inc.", tax_rate=Decimal("0.08"))
    svc.add_line_item(inv, "Consulting", Decimal("5"), Decimal("200.00"))
    assert inv.subtotal == Decimal("1000.00")
    assert inv.tax_amount == Decimal("80.00")
    assert inv.total == Decimal("1080.00")
    svc.mark_paid(inv)
    assert inv.status.value == "paid"
    assert inv.paid_date is not None
