# procAi

[![AI-SDLC](https://img.shields.io/badge/AI--SDLC-v1.0.0-blue)](https://ai-sdlc.aisl.science)
[![CI](https://github.com/ElpiLab/Orchestration-Procurement-main/actions/workflows/ci.yml/badge.svg)](https://github.com/ElpiLab/Orchestration-Procurement-main/actions/workflows/ci.yml)

**From supplier quotation PDF to a reviewable internal order draft, with a human in the loop.**

A minimal FastAPI application that demonstrates Clean Architecture, spec-driven development and an AI-assisted lifecycle on a deliberately small use case.

- Capstone project of the FHNW module *AI-assisted Software Development* (BSc Business Information Technology, team of two)
- Created from the [AI-SDLC project template](https://github.com/AIaSDev/ai-sdlc-template)
- README structure follows the template and the reference implementation [BAIssue](https://github.com/AIaSDev/BAIssue)
- Method documentation: [AISL Docs](https://docs.aisl.science/learning-and-resources/ai-sdlc)

> [!NOTE]
> The process matters more than the application: specification, decisions and tests are as much part of the result as the code.

## Getting started

1. Clone this repository and open it in VS Code or GitHub Codespaces.
2. Run the [agent setup](#agent-setup) below.
3. Read `docs/PROJECT.md` (context, architecture, commands) and `AGENTS.md` (lifecycle rules).
4. Install the dependencies and start the application (see [Running locally](#running-locally)).
5. Upload one of the PDFs from `sample-data/` to create an internal order draft.
6. Continue the lifecycle with `AGENTS.md` and record progress in `docs/TASKS.md`. Use `docs/specs/UC-TEMPLATE.md` for new use-case specifications.

Automation in this repository:

- GitHub Copilot instructions: `.github/copilot-instructions.md`
- CI workflow: checks the required AI-SDLC structure and runs the tests
- Release workflow: runs the tests, builds the container and creates a GitHub Release for `v*` tags
- CD workflow: `.github/workflows/cd.yml` is still the inactive template, no deployment platform is configured yet (see [CI, releases and CD](#ci-releases-and-cd))

## Agent setup

**Codespaces**

- Creates a Python development container with Python, Pylance, debugging and GitHub Copilot extensions
- Prepares `.agents/skills` and the Python environment automatically
- Terminal locale is English; the VS Code UI uses its own display-language setting

**Other agents or a local checkout**

```bash
bash scripts/setup-skills.sh claude   # or: copilot, codex, cline, opencode, cursor, kiro, junie, devin, all
bash scripts/setup-python.sh          # recreate or refresh the Python environment
```

- The script links the agent's skills directory to the canonical `skills/` directory and falls back to copying if links are unavailable
- Existing destinations are kept; copies must be refreshed manually after skill changes
- The `claude` and `all` selections also create a missing `CLAUDE.md` containing `@AGENTS.md`; an existing file is preserved
- Shared instructions and skills are not modified
- Verify skill discovery in your agent: setup does not install or configure the agent itself

## Repository artefacts

- `AGENTS.md` — lifecycle router and guardrails
- `docs/PROJECT.md` — project context, scope, architecture and commands
- `docs/TASKS.md` — current lifecycle state
- `docs/specs/` — executable use-case specifications (`UC-001`: supplier quotation PDF to internal order draft)
- `docs/adr/` — architecture decision records (`ADR-001`: stateless first POC)
- `skills/ai-sdlc-*` — phase-specific execution guidance
- `src/app/` — application source (`domain`, `application`, `interfaces`, `infrastructure`)
- `tests/` — unit, integration and end-to-end tests
- `sample-data/` — six example quotation PDFs
- `brainstorming/` — the team's whiteboard sketches
- `.devcontainer/` — Codespaces and VS Code baseline
- `environments/python/` — Python environment profile and dependency manifest
- `scripts/setup-python.sh`, `scripts/setup-skills.sh` — Python environment and agent skill setup
- `.github/` — Copilot instructions, CI, release and CD workflow templates

Working principle: **Specification → Tests → Code → Validation → Release → Deployment**

## What is this?

procAi helps procurement users who read supplier quotations by hand and retype
