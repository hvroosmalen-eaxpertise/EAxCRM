"""Put the skill directory on sys.path so tests can `import engine`, `import rules`."""
import pathlib
import sys

_SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))
