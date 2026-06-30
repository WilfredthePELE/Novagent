"""Template rendering engine for Novagent documents."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from novagent.config import NovagentConfig


class TemplateRenderer:
    """Jinja2-based template renderer for proposals, invoices, reports, and receipts."""

    def __init__(self, config: NovagentConfig | None = None) -> None:
        self.config = config or NovagentConfig()
        template_dir = Path(__file__).parent / "files"
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.env.filters["currency"] = _format_currency
        self.env.filters["date"] = _format_date
        self.env.globals["brand_name"] = self.config.brand_name
        self.env.globals["tagline"] = self.config.tagline
        self.env.globals["primary_color"] = self.config.primary_color
        self.env.globals["accent_color"] = self.config.accent_color

    def render(self, template_name: str, **context: Any) -> str:
        """Render a template with the given context.

        Args:
            template_name: Name of the template file (e.g., 'proposal.md.j2').
            **context: Variables to inject into the template.

        Returns:
            Rendered string output.
        """
        template = self.env.get_template(template_name)
        return template.render(**context)

    def render_to_file(self, template_name: str, output_path: str | Path, **context: Any) -> Path:
        """Render a template and write the output to a file.

        Args:
            template_name: Name of the template file.
            output_path: Path to write the rendered output.
            **context: Variables to inject into the template.

        Returns:
            Path to the written file.
        """
        output = self.render(template_name, **context)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        return path


def _format_currency(value: Any) -> str:
    """Format a number as currency."""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return f"${value}"


def _format_date(value: Any, fmt: str = "%B %d, %Y") -> str:
    """Format a datetime or date string."""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value
    if hasattr(value, "strftime"):
        return value.strftime(fmt)
    return str(value)
