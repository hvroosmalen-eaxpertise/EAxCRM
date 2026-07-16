"""EA003 — heuristic: no writes to existing-diagram geometry.

Flags Attribute assignments to ``.left`` / ``.top`` / ``.right`` /
``.bottom`` on targets whose name looks like a DiagramObject variable
(``dobj``, ``diagram_object``, ``diagramobject`` — case-insensitive
substring match), unless the same name was assigned from a
``.AddNew(...)`` or ``.CreateDiagramObject(...)`` call within the last
``_JUST_CREATED_WINDOW`` lines of the same function.

The check is intentionally heuristic — a fully-general "did this
DiagramObject already exist at runtime?" answer isn't derivable from
source.  False-positive posture (per design): with no waivers,
legitimate first-time-creation code that trips this should be
restructured so the creating call sits visibly close to the geometry
write.  That constraint is itself desirable.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterable, Iterator

from engine import Finding, register


_GEOMETRY_ATTRS = frozenset({"left", "top", "right", "bottom"})
_CREATE_CALL_NAMES = frozenset({"AddNew", "CreateDiagramObject"})
_DOBJ_NAME_RE = re.compile(r"(dobj|diagram_?object)", re.IGNORECASE)
_JUST_CREATED_WINDOW = 20

_MSG = (
    "possible write to existing diagram geometry; only just-created "
    "DiagramObjects may be positioned"
)


def _is_dobj_name(name: str) -> bool:
    return bool(_DOBJ_NAME_RE.search(name))


def _attr_last_segment(node: ast.AST) -> str | None:
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _is_create_call(rhs: ast.AST) -> bool:
    if not isinstance(rhs, ast.Call):
        return False
    return _attr_last_segment(rhs.func) in _CREATE_CALL_NAMES


def _iter_functions(tree: ast.AST) -> Iterator[ast.AST]:
    yielded = False
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node
            yielded = True
    if not yielded and isinstance(tree, ast.Module):
        yield tree


def _check_function(path: Path, rule_id: str, func: ast.AST) -> Iterator[Finding]:
    """One create-tracker per function, statements walked in source order."""
    created_at: dict[str, int] = {}

    assigns = sorted(
        (n for n in ast.walk(func) if isinstance(n, ast.Assign)),
        key=lambda n: (n.lineno, n.col_offset),
    )

    for node in assigns:
        # Track "just-created" targets.
        if _is_create_call(node.value):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    created_at[tgt.id] = node.lineno

        # Flag geometry writes on dobj-shaped targets not recently created.
        if len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Attribute):
            continue
        if target.attr not in _GEOMETRY_ATTRS:
            continue
        base = target.value
        if not isinstance(base, ast.Name):
            continue
        if not _is_dobj_name(base.id):
            continue

        created_line = created_at.get(base.id)
        if created_line is None or node.lineno - created_line > _JUST_CREATED_WINDOW:
            yield Finding(path, node.lineno, rule_id, _MSG)


class Rule:
    id = "EA003"
    description = (
        "Heuristic: no writes to existing-diagram geometry; only "
        "just-created DiagramObjects may be positioned."
    )

    def check(
        self, path: Path, source: str, tree: ast.AST
    ) -> Iterable[Finding]:
        for func in _iter_functions(tree):
            yield from _check_function(path, self.id, func)


register(Rule())
