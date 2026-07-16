"""EA002 — every generate_*.py must have a companion sync_*.py.

Repo-level rule.  For each directory that contains at least one
generate_*.py, extract the pairing key (stem after `generate_` with any
trailing `_from_md`/`_from_ea` suffix removed) and require a matching
sync_<key>_*.py in the same directory.  Orphan sync scripts (no
generate) are NOT flagged; sync-only extractors are legitimate.
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


class Rule:
    id = "EA002"
    description = (
        "Every generate_*.py must have a companion sync_*.py in the "
        "same directory."
    )

    def check(self, files: list[Path]) -> Iterable[Finding]:
        by_dir_generates: dict[Path, list[tuple[Path, str]]] = defaultdict(list)
        by_dir_sync_keys: dict[Path, set[str]] = defaultdict(set)

        for f in files:
            g = _GENERATE_RE.match(f.name)
            if g:
                by_dir_generates[f.parent].append((f, _pairing_key(g["stem"])))
                continue
            s = _SYNC_RE.match(f.name)
            if s:
                by_dir_sync_keys[f.parent].add(_pairing_key(s["stem"]))

        for directory, entries in by_dir_generates.items():
            keys_here = by_dir_sync_keys.get(directory, set())
            for gen_path, key in entries:
                if key not in keys_here:
                    yield Finding(
                        gen_path, 1, self.id,
                        f"no companion sync_{key}_from_ea.py "
                        f"found in {directory.name}/",
                    )


register(Rule())
