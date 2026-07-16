"""EA002 — every generate_*.py must have a companion sync_*.py.

Repo-level rule.  For each generate_*.py in the input file set, extract
the pairing key (stem after `generate_` with any trailing
`_from_md`/`_from_ea`/`_to_md`/`_to_ea` suffix removed) and require a
matching sync_<key>_*.py in the SAME DIRECTORY ON DISK -- not just in
the input file list.  That distinction matters for --changed runs (from
the pre-commit hook), where only staged files reach the rule: an
already-committed sync sibling is a valid companion and must still
count.

Orphan sync scripts (no generate) are NOT flagged; sync-only extractors
are legitimate.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from engine import Finding, register

_GENERATE_RE = re.compile(r"^generate_(?P<stem>.+)\.py$")
_SYNC_RE = re.compile(r"^sync_(?P<stem>.+)\.py$")
_STRIP_SUFFIX_RE = re.compile(r"_(from_md|from_ea|to_md|to_ea)$")


def _pairing_key(stem: str) -> str:
    return _STRIP_SUFFIX_RE.sub("", stem)


def _sync_keys_in_dir(directory: Path) -> set[str]:
    keys: set[str] = set()
    try:
        entries = list(directory.iterdir())
    except OSError:
        return keys
    for entry in entries:
        if not entry.is_file():
            continue
        m = _SYNC_RE.match(entry.name)
        if m:
            keys.add(_pairing_key(m["stem"]))
    return keys


class Rule:
    id = "EA002"
    description = (
        "Every generate_*.py must have a companion sync_*.py in the "
        "same directory."
    )

    def check(self, files: list[Path]) -> Iterable[Finding]:
        by_dir_generates: dict[Path, list[tuple[Path, str]]] = defaultdict(list)
        for f in files:
            g = _GENERATE_RE.match(f.name)
            if g:
                by_dir_generates[f.parent].append((f, _pairing_key(g["stem"])))

        # Look up sync siblings from the actual directory on disk (not just
        # from the input file set), cached per directory.
        sync_keys_cache: dict[Path, set[str]] = {}
        for directory, entries in by_dir_generates.items():
            if directory not in sync_keys_cache:
                sync_keys_cache[directory] = _sync_keys_in_dir(directory)
            keys_here = sync_keys_cache[directory]
            for gen_path, key in entries:
                if key not in keys_here:
                    yield Finding(
                        gen_path, 1, self.id,
                        f"no companion sync_{key}_from_ea.py "
                        f"found in {directory.name}/",
                    )


register(Rule())
