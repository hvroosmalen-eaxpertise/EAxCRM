"""Rule modules.  Each import here triggers the rule's engine.register() call."""
from . import ea001_no_direct_ea_query  # noqa: F401
from . import ea002_generate_needs_sync  # noqa: F401
from . import ea003_no_existing_diagram_writes  # noqa: F401
