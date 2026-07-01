---
title: Set up cross-session memory with opencode-memory
tags: [opencode, memory, setup]
summary: Installed opencode-memory plugin, memory dir in EAxCRM repo, tracked on GitHub
created: 2026-07-01
updated: 2026-07-01
importance: high
source: Session with user
source_date: 2026-07-01
---

Installed `@mathew-cf/opencode-memory@1.0.1` plugin for persistent cross-session memory.

## Setup details
- **Config**: Added to `~\.config\opencode\opencode.jsonc`
- **Memory dir**: `_opencode_memory/` in EAxCRM repo root (pushed to GitHub)
- **Env var**: `OPENCODE_MEMORY_DIR` = `C:\Users\hanva\source\repos\EAxCRM\_opencode_memory`
- **Skill**: Auto-registered at `~/.agents/skills/opencode-memory/`
- **Bun**: Installed via winget (Oven-sh.Bun) for running init commands

## Notes
- Semantic search (rag-cli) unavailable on Windows — no prebuilt binary
- Keyword search via ripgrep works (supported on Windows)
- If re-bootstrapping, remove nested `.git` after init so main repo tracks the files
- `.gitignore` excludes `_opencode_memory/.git/`

## Memory tools available
- `memory_search`, `memory_list`, `memory_save`, `memory_access`, `memory_setup`
- `session_search`, `session_read`, `session_list`
