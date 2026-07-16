"""Negative: uppercase SQL word in prose without its SQL companion.

Log messages and docstrings that mention DELETE / CREATE / etc. in
non-SQL context lack the paired clause (DELETE+FROM, CREATE+TABLE),
so EA001 must not fire.
"""
from ea_session import ea_repository  # noqa: F401


def log_delete(c):
    print(f"  DELETE connector id={c.id} guid={c.guid}")


def note():
    """Consider a small sanity SELECT first before running the batch."""
    return "CREATE a new element" + " " + "UPDATE it later"
