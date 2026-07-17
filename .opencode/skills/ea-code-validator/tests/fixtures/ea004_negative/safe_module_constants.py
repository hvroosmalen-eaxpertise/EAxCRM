"""Module-scope Assign RHS with Call is fine — it's not the smell we chase."""
import os
import re
import textwrap
from ea_session import ea_repository  # noqa: F401 — makes this EA-touching

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NAME_RE = re.compile(r"(dobj|diagram_?object)", re.IGNORECASE)
SAMPLE_MD = textwrap.dedent("""\
    # Header
    - GUID: {abc}
    """)


def do_work() -> None:
    with ea_repository("M:\\some.qea") as repo:
        print(repo.Models.Count)


if __name__ == "__main__":
    do_work()
