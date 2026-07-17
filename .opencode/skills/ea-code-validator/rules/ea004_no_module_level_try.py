"""EA004 — no module-level ``try:`` in EA-touching files.

Any ``try/except`` block at *module* scope is flagged. The pattern
exists to swallow initialization errors from side-effectful code, so
its presence at module scope reliably signals that the module does
real work at import time — spawning EA COM, opening files, mutating
the .qea.

Motivation: on 2026-07-17, importing ``modelgen/cleanup.py`` for a
smoke test deleted 74 ArchiMate elements from the live .qea, and
importing ``modelgen/smoke_archimate.py`` (then named
``test_archimate.py``) added a Test Business Actor to the live model.
Both had the same shape — module body wrapped in ``try:`` that did
COM writes, no ``__main__`` guard.

The fix is always the same: move the body into ``def main()`` and
call it from ``if __name__ == "__main__":``. Importing then becomes a
side-effect-free operation.

Scope: this rule is intentionally narrow. It only fires on ``ast.Try``
nodes that are direct children of the module body. Try/except inside
functions, classes, or an ``if __name__ == "__main__":`` block is
fine. Assignments like ``SCRIPT_DIR = os.path.dirname(...)``,
``re.compile(...)``, ``textwrap.dedent(...)`` at module scope are
also fine — they are not the smell this rule chases.
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable

from engine import Finding, register


_MSG = (
    "module-level `try:` in EA-touching file — wrap body in `def main()` "
    "behind `if __name__ == \"__main__\":` so importing the module is "
    "side-effect free"
)


class Rule:
    id = "EA004"
    description = (
        "No module-level `try:` in EA-touching files — wrap side-effecting "
        "code in main() behind an `if __name__ == \"__main__\":` guard."
    )

    def check(
        self, path: Path, source: str, tree: ast.AST
    ) -> Iterable[Finding]:
        if not isinstance(tree, ast.Module):
            return
        for node in tree.body:
            if isinstance(node, ast.Try):
                yield Finding(path, node.lineno, self.id, _MSG)


register(Rule())
