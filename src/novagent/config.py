"""Application configuration for Novagent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class NovagentConfig:
    """Central configuration for the Novagent system."""

    # Branding
    brand_name: str = "Novagent"
    tagline: str = "Intelligence That Delivers"
    primary_color: str = "#6366F1"  # Indigo
    accent_color: str = "#22D3EE"  # Cyan

    # Paths
    data_dir: Path = field(default_factory=lambda: Path.home() / ".novagent")
    output_dir: Path = field(default_factory=lambda: Path.home() / ".novagent" / "output")
    templates_dir: Path = field(default_factory=lambda: Path.home() / ".novagent" / "templates")

    # Server
    host: str = "0.0.0.0"
    port: int = 8080

    # Service categories
    service_categories: list[str] = field(default_factory=lambda: [
        "proposals",
        "invoicing",
        "receipts",
        "job-reports",
        "user-manuals",
        "audit-certificates",
        "consulting",
        "documentation",
        "analytics",
        "automation",
        "integration",
        "support",
    ])

    @classmethod
    def from_env(cls) -> NovagentConfig:
        """Load configuration from environment variables with sensible defaults."""
        return cls(
            host=os.getenv("NOVAGENT_HOST", "0.0.0.0"),
            port=int(os.getenv("NOVAGENT_PORT", "8080")),
            data_dir=Path(os.getenv("NOVAGENT_DATA_DIR", str(Path.home() / ".novagent"))),
        )

    def ensure_dirs(self) -> None:
        """Create all required directories."""
        for d in [self.data_dir, self.output_dir, self.templates_dir]:
            d.mkdir(parents=True, exist_ok=True)
