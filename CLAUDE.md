# CLAUDE.md (Project Router)

## First, read these (source of truth)
1) `AGENTS.md`
2) `.github/` (all agent instructions live here)

If anything conflicts, prioritize `.github/` instructions.

## How to work in this repo
- Before making changes: scan repo structure and identify impacted files.
- Prefer small, reviewable diffs.
- Do not change data contracts / file I/O formats unless explicitly requested.

## Repo map (high-level)
- `.github/` : canonical agent instructions
- `src/` : core code / experiments / analysis
- `data/` : data (treat as read-only unless instructed)
- `lib/` : module
- `reports/` : outputs
