# AGENTS.md

## Read these first (mandatory)
- Always follow `github-instructions.md`.
- If relevant, also follow instructions under `.github/instructions/` (e.g., `*.instructions.md`).

## Non-negotiable workflow
- Never push directly to `main`. All changes must go through PRs.
- Branch flow: `develop/* -> stage -> main`.

## Commit rules
- Use Conventional Commits: `<type>(<scope>): <description>`.

## Safety constraints
- Do not make breaking changes to APIs/interfaces without prior agreement.
- Do not make disruptive environment/dependency changes without prior agreement.
- Never commit secrets, personal data, or credentials (keep `.env` untracked).
- Avoid large binary files; use Git LFS/external storage if needed.

## Execution environment
- Use this repo’s `.venv` interpreter for Python runs (e.g., `.venv/bin/python`).
- Use `uv` for environment management; adding libraries requires approval.
