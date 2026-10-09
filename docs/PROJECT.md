# PROJECT.md

Complete this document during **BOOTSTRAP**. Keep it concise and specific to
the project created from this template.

## Purpose

- Project name: Procurement Orchestration
- User or organisational problem: Automation of repetitive tasks, simplify processes, process order faster
- Intended users: Users in a company for fast data entry (procurement orders): easy and fast ordering process, 
- In scope: free text order and catalog order orchestration
- AI Integration where ? in Githubactiosn
- Add MCP server: Which one compatible with our project?
- User Story/Use Case:
  - User writes in natural language an order "I need 5 Lenovo Laptops"
- Out of scope: OCI Punchout

## Architecture

Describe the selected architecture, boundaries and dependency direction. If
Clean Architecture is used, keep dependencies pointing inward:

`domain ← application ← interfaces ← infrastructure`

Record important framework, data-store and integration decisions here.

## Structure

Document the meaningful source and test directories once they exist. Reuse the
existing repository structure where it is compatible with the selected stack.

## Commands

Document the commands for the selected stack:

| Activity | Command |
|---|---|
| Install | `TBD` |
| Unit tests | `TBD` |
| Integration tests | `TBD` |
| Run locally | `TBD` |
| Build/release | `TBD` |

## Dependencies

List the dependency manifest and runtime versions. Never commit credentials or
secrets; document required secret names and configuration variables only.
