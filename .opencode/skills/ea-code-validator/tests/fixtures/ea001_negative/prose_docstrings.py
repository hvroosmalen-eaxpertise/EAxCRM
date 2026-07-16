"""Re-run to update names, descriptions, or create new elements.

This module docstring mentions 'update' and 'create' in prose (lowercase);
EA001 must not fire on it.  The rule is case-sensitive on uppercase SQL
keywords followed by whitespace.
"""
from ea_session import ea_repository  # noqa: F401


def do_stuff():
    """Handles the update flow and creates a new element if needed."""
    msg = "Please update this later"
    return msg
