"""Make the repository root importable when tests run as `pytest tests/`.

Without this, `from <client_module> import ...` in tests/ fails: pytest puts the
test file's directory on `sys.path`, not the repository root, so the client module
sitting next to this file is not found. Keeping the root importable means the tests
run with a plain `pytest tests/` and no PYTHONPATH fiddling.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
