"""EA001 — no direct queries against the EA repository.

Fires on:
- Calls to sqlite3.connect / pyodbc.connect / sqlalchemy.create_engine.
- Raw SQL string literals in EA-touching code, unless the string is
  passed to a .SQLQuery(...) call (EA's own read-only COM method).

Known gap (v1): calls made via `from sqlite3 import connect` (or similar
`from` imports) are not detected.  The offenders in this repo have used
`import sqlite3; sqlite3.connect(...)`.  Broaden if needed.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterable

from engine import Finding, register


_DB_DRIVER_CALLS = {
    ("sqlite3", "connect"): "sqlite3.connect",
    ("pyodbc", "connect"): "pyodbc.connect",
    ("sqlalchemy", "create_engine"): "sqlalchemy.create_engine",
}

# Case-sensitive: project convention is uppercase SQL.  Requiring the
# keyword to be followed by whitespace rules out identifiers like
# "Select-Object" (PowerShell) even if they were uppercase.  Docstrings that
# say "update" or "create" in prose are lowercase and don't match.
#
# We also require the companion clause (SELECT+FROM, UPDATE+SET, etc.) to
# appear in the same string constant.  Real SQL always pairs; prose like
# "DELETE connector id=..." or "sanity SELECT first" does not.
_SQL_LEADS_TO_PAIR = {
    "SELECT": re.compile(r"\bFROM\s"),
    "INSERT": re.compile(r"\bINTO\s"),
    "UPDATE": re.compile(r"\bSET\s"),
    "DELETE": re.compile(r"\bFROM\s"),
    "CREATE": re.compile(r"\b(TABLE|INDEX|VIEW)\s"),
    "DROP":   re.compile(r"\b(TABLE|INDEX|VIEW)\s"),
    "ALTER":  re.compile(r"\b(TABLE|INDEX)\s"),
}
_SQL_LEAD_RE = re.compile(
    r"\b(" + "|".join(_SQL_LEADS_TO_PAIR) + r")\s"
)


def _looks_like_sql(text: str) -> bool:
    m = _SQL_LEAD_RE.search(text)
    if not m:
        return False
    return bool(_SQL_LEADS_TO_PAIR[m.group(1)].search(text))

# Function names that legitimately take a SQL string as their first argument
# because they route through Repository.SQLQuery internally.  The check is
# on the LAST segment of the dotted call chain, so `repo.SQLQuery(...)`,
# `ea_session.sql_rows(repo, ...)`, and `sql_rows(repo, ...)` all match.
_SQL_SINK_FUNCS = {"SQLQuery", "sql_rows"}

_MSG_DRIVER = (
    "direct EA-repo query via {label}(); use ea_session.ea_repository() + COM"
)
_MSG_SQL = (
    "raw SQL string in EA-touching code; use Repository.SQLQuery(...) for reads"
)


def _attr_chain(node: ast.AST) -> tuple[str, ...]:
    """Turn a.b.c into ('a', 'b', 'c'); bare Name → ('a',); anything else → ()."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return tuple(reversed(parts))
    return ()


def _annotate_parents(tree: ast.AST) -> None:
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child._parent = parent  # type: ignore[attr-defined]


class Rule:
    id = "EA001"
    description = (
        "No direct queries against the EA repository; "
        "use ea_session.ea_repository() + COM (Repository.SQLQuery for reads)."
    )

    def check(
        self, path: Path, source: str, tree: ast.AST
    ) -> Iterable[Finding]:
        _annotate_parents(tree)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                chain = _attr_chain(node.func)
                for key, label in _DB_DRIVER_CALLS.items():
                    if len(chain) >= len(key) and chain[-len(key):] == key:
                        yield Finding(
                            path, node.lineno, self.id,
                            _MSG_DRIVER.format(label=label),
                        )
                        break

            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if _looks_like_sql(node.value):
                    if not _is_arg_to_sql_sink(node):
                        yield Finding(
                            path, node.lineno, self.id, _MSG_SQL
                        )


def _is_arg_to_sql_sink(str_node: ast.AST) -> bool:
    """True if the string sits as an argument to a whitelisted SQL sink call.

    Walks up through ast.JoinedStr so f-string parts are recognized as
    arguments to the enclosing call.
    """
    parent = getattr(str_node, "_parent", None)
    while isinstance(parent, ast.JoinedStr):
        parent = getattr(parent, "_parent", None)
    if not isinstance(parent, ast.Call):
        return False
    chain = _attr_chain(parent.func)
    return bool(chain) and chain[-1] in _SQL_SINK_FUNCS


register(Rule())
