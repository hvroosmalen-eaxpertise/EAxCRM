---
title: EA Journal/WAL files to gitignore
tags: [sparx-ea, gitignore, sqlite]
summary: EA creates 3 transient SQLite journal files alongside .qea that must be gitignored
created: 2026-07-08
updated: 2026-07-08
importance: medium
---

When Sparx EA opens a `.qea` file (embedded SQLite), it creates three transient files:
- `*.qea-journal` — SQLite rollback journal
- `*.qea-wal` — SQLite Write-Ahead Log
- `*.qea-shm` — SQLite shared memory file

These are crash-recovery artifacts that appear/disappear as EA uses the file. They must be in `.gitignore` or they'll pollute the working tree.

Add to `.gitignore`:
```
*.qea-journal
*.qea-wal
*.qea-shm
```
