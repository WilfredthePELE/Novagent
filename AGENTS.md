# Novagent — Agentic Development Guide

This file governs how AI agents (like Hermes Agent) work on this project.

## Architecture

- **Language:** Python 3.11+
- **Packaging:** `pyproject.toml` with `src/` layout
- **Testing:** pytest (configured via `pyproject.toml`)
- **Entry point:** `novagent.main:main` (CLI entry defined in `pyproject.toml`)

## Working with this repo

### Before making changes
1. Review existing code and tests thoroughly.
2. Check `docs/roadmap.md` for the current project phase.
3. Run existing tests: `pytest`

### Code style
- Follow PEP 8
- Type hints required for all public functions and methods
- Docstrings: Google-style (multi-line) for public APIs
- Keep functions focused — one responsibility per function

### Testing
- Write tests alongside new code (or before, TDD-style)
- Test file: `tests/test_<module>.py`
- Run: `pytest -v`
- Aim for >80% coverage on new code

### Committing
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Keep commits focused and atomic
- Always run tests before committing

## Project guardrails
- Do NOT commit secrets, keys, or credentials
- Do NOT modify `LICENSE` or `AGENTS.md` without explicit user direction
- Do NOT leave debug prints or `TODO` stubs in production code
- Prioritize working deliverables over architectural purity
