"""Output generation — HTML, and Markdown document creation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from novagent.config import NovagentConfig
from novagent.templates import TemplateRenderer


class DocumentBuilder:
    """Builds output documents (markdown, HTML) from models and templates."""

    def __init__(self, config: NovagentConfig | None = None) -> None:
        self.config = config or NovagentConfig()
        self.renderer = TemplateRenderer(self.config)

    # ── Proposals ──────────────────────────────────────────────

    def build_proposal_md(self, proposal: Any, output_dir: str | Path | None = None) -> Path:
        """Render a proposal as Markdown."""
        out_dir = Path(output_dir) if output_dir else self.config.output_dir / "proposals"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{proposal.id}.md"
        return self.renderer.render_to_file("proposal.md.j2", path, proposal=proposal)

    def build_proposal_html(self, proposal: Any, output_dir: str | Path | None = None) -> Path:
        """Render a proposal as HTML."""
        out_dir = Path(output_dir) if output_dir else self.config.output_dir / "proposals"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{proposal.id}.html"
        md_content = self.renderer.render("proposal.md.j2", proposal=proposal)
        html = _md_to_html(md_content, self.config)
        path.write_text(html, encoding="utf-8")
        return path

    # ── Invoices ───────────────────────────────────────────────

    def build_invoice_html(self, invoice: Any, output_dir: str | Path | None = None) -> Path:
        """Render an invoice as HTML."""
        out_dir = Path(output_dir) if output_dir else self.config.output_dir / "invoices"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{invoice.id}.html"
        return self.renderer.render_to_file("invoice.html.j2", path, invoice=invoice)

    def build_invoice_md(self, invoice: Any, output_dir: str | Path | None = None) -> Path:
        """Render an invoice as Markdown."""
        out_dir = Path(output_dir) if output_dir else self.config.output_dir / "invoices"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{invoice.id}.md"
        parts = [
            f"# {self.config.brand_name} — {self.config.tagline}\n",
            f"## Invoice {invoice.invoice_number}\n",
            f"**Client:** {invoice.client_name}  ",
            f"**Status:** {invoice.status.value.upper()}  ",
            f"**Issue Date:** {invoice.issue_date.strftime('%B %d, %Y') if hasattr(invoice.issue_date, 'strftime') else invoice.issue_date}  ",
            f"**Due Date:** {invoice.due_date.strftime('%B %d, %Y') if hasattr(invoice.due_date, 'strftime') and invoice.due_date else 'N/A'}\n",
            "| Description | Qty | Unit Price | Total |",
            "|---|---|---|---|",
        ]
        for item in invoice.line_items:
            parts.append(f"| {item.description} | {item.quantity} | ${float(item.unit_price):,.2f} | ${float(item.total):,.2f} |")
        parts.append("")
        parts.append(f"**Subtotal:** ${float(invoice.subtotal):,.2f}")
        if invoice.tax_rate and float(invoice.tax_rate) > 0:
            parts.append(f"**Tax ({float(invoice.tax_rate)*100:.0f}%):** ${float(invoice.tax_amount):,.2f}")
        parts.append(f"**Total:** ${float(invoice.total):,.2f} {invoice.currency}")
        if invoice.status.value == "paid" and invoice.paid_date:
            parts.append(f"\n**Paid on:** {invoice.paid_date.strftime('%B %d, %Y') if hasattr(invoice.paid_date, 'strftime') else invoice.paid_date}")
        parts.append(f"\n---\n*{self.config.brand_name} — {self.config.tagline}*")
        path.write_text("\n".join(parts), encoding="utf-8")
        return path

    # ── Receipts ───────────────────────────────────────────────

    def build_receipt_md(self, receipt: Any, output_dir: str | Path | None = None) -> Path:
        """Render a receipt as Markdown."""
        out_dir = Path(output_dir) if output_dir else self.config.output_dir / "receipts"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{receipt.receipt_number}.md"
        return self.renderer.render_to_file("receipt.md.j2", path, receipt=receipt)

    # ── Reports ────────────────────────────────────────────────

    def build_report_md(self, report: Any, output_dir: str | Path | None = None) -> Path:
        """Render a job report as Markdown."""
        out_dir = Path(output_dir) if output_dir else self.config.output_dir / "reports"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{report.id}.md"
        return self.renderer.render_to_file("report.md.j2", path, report=report)

    def build_report_html(self, report: Any, output_dir: str | Path | None = None) -> Path:
        """Render a job report as HTML."""
        out_dir = Path(output_dir) if output_dir else self.config.output_dir / "reports"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{report.id}.html"
        md_content = self.renderer.render("report.md.j2", report=report)
        html = _md_to_html(md_content, self.config)
        path.write_text(html, encoding="utf-8")
        return path


def _md_to_html(md_content: str, config: NovagentConfig) -> str:
    """Convert a markdown string to a styled HTML page."""
    import markdown
    html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">
<title>{config.brand_name}</title>
<style>
  body {{ font-family: 'Helvetica', 'Arial', sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #1f2937; line-height: 1.6; }}
  h1 {{ color: {config.primary_color}; border-bottom: 2px solid {config.primary_color}; padding-bottom: 10px; }}
  h2 {{ color: {config.primary_color}; }}
  table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
  th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }}
  th {{ background: {config.primary_color}; color: white; }}
  hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 30px 0; }}
  .footer {{ color: #9ca3af; font-size: 10pt; text-align: center; }}
</style>
</head>
<body>
{html_body}
<div class="footer"><p>{config.brand_name} — {config.tagline}</p></div>
</body>
</html>"""
