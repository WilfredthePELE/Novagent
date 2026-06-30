# Novagent — Intelligence That Delivers

[![License](https://img.shields.io/badge/License-Apache%202.0-indigo)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-cyan?logo=python)](https://python.org)

**Novagent** is an autonomous AI agency — 54+ skills across 12 service categories, delivering ~116 distinct services. From proposal generation and invoicing to job reporting and audit certification, Novagent handles end-to-end business workflows autonomously.

Built for the **Hermes Agent Accelerated Business Hackathon (June 2026)**.

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/WilfredthePELE/Novagent.git
cd Novagent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# Install
pip install -e .

# Run
novagent
```

## 📁 Project Structure

```
Novagent/
├── src/
│   └── novagent/
│       ├── __init__.py       # Version 0.1.0
│       ├── config.py         # NovagentConfig dataclass
│       ├── main.py           # CLI entry point (16 subcommands)
│       ├── models/           # Pydantic v2 data models
│       │   ├── proposal.py   # Proposal, ProposalSection
│       │   ├── invoice.py    # Invoice, InvoiceLineItem
│       │   ├── receipt.py    # Receipt, ReceiptLineItem
│       │   └── report.py     # JobReport, Milestone
│       ├── services/         # Business logic
│       │   ├── proposal_service.py
│       │   ├── invoice_service.py
│       │   ├── receipt_service.py
│       │   └── report_service.py
│       ├── templates/        # Jinja2 templates (4 files)
│       │   └── files/
│       │       ├── proposal.md.j2
│       │       ├── invoice.html.j2
│       │       ├── receipt.md.j2
│       │       └── report.md.j2
│       └── output/           # DocumentBuilder — MD + HTML generation
├── tests/                    # pytest suite
├── docs/
│   └── roadmap.md
├── AGENTS.md
├── pyproject.toml
└── README.md
```

## 🧠 Capabilities

| Category | Services |
|---|---|
| **Proposals** | Generation, review, versioning, client-ready output |
| **Invoicing** | Create, send, track, reconcile |
| **Receipts** | Generate, categorize, archive |
| **Job Reports** | Structured reporting, milestone tracking |
| **User Manuals** | Auto-documentation, technical writing |
| **Audit Certificates** | Compliance checks, certification generation |
| *And more…* | 54+ skills, 116+ services |

## 🎨 Brand

- **Tagline:** *Intelligence That Delivers*
- **Primary:** Indigo `#6366F1`
- **Accent:** Cyan `#22D3EE`

## 📄 License

Apache License 2.0 — see [LICENSE](LICENSE).
