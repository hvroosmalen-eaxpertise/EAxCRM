"""Command-line entry point for the EA code validator."""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

_SKILL_DIR = pathlib.Path(__file__).resolve().parent
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))

import engine  # noqa: E402


def _changed_files() -> list[pathlib.Path]:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "--cached", "HEAD"],
            capture_output=True, check=True, text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [pathlib.Path(line) for line in out.stdout.splitlines() if line]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ea-code-validator")
    ap.add_argument("paths", nargs="*", type=pathlib.Path)
    ap.add_argument("--only", help="comma-separated rule ids to run")
    ap.add_argument("--list", action="store_true", dest="do_list",
                    help="list registered rules and exit")
    ap.add_argument("--changed", action="store_true",
                    help="validate only git-staged files")
    args = ap.parse_args(argv)

    engine.load_rules()

    if args.do_list:
        for r in engine.registered_rules():
            print(f"{r.id}\t{r.description}")
        return 0

    if args.changed:
        paths = _changed_files()
        if not paths:
            return 0
    elif args.paths:
        paths = args.paths
    else:
        paths = [pathlib.Path.cwd()]

    only = set(args.only.split(",")) if args.only else None
    findings, errors = engine.run(paths, only=only)

    root = pathlib.Path.cwd().resolve()
    for f in findings:
        print(f.format(root=root))
    for e in errors:
        print(f"error: {e}", file=sys.stderr)

    if errors:
        return 2
    if findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
