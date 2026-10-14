"""Where this repository's coordinator tools find things, derived from this file.

The tools live in `scripts/coordinator/` of the primary checkout. The lanes, the
review scratch root and the overnight logs live in the checkout's sibling
folder, `<checkout>.wt` (for `C:/Projects/ai-template`, that is
`C:/Projects/ai-template.wt`). Nothing here names a machine or a user, so the
tools run unchanged wherever the checkout is.
"""

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WTROOT = REPO.parent / (REPO.name + ".wt")
PYTHON = REPO / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
