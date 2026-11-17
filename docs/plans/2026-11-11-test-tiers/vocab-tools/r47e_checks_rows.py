"""HANDOFF 10.7 item 1 (4.5.5, 4.5.7, 9.10's leftover): the phrase map of
r47e_checks_prose.py over the rows of the five registries whose text holds
"bar" (accepted text: vocabulary only, absorbed into the record by the
migrator, D13). The lines whose sense the map gets wrong (a threshold, a
stage, a field of the trailer, the retired axis, a glyph) are put right by
line in h47g_rows.py, read against this file's dry run.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

_spec = importlib.util.spec_from_file_location("code_rules", HERE / "r47e_checks_prose.py")
_code = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_code)

# A passing or failing run is often the object of a clause whose verb belongs
# to another subject ("a rewrite after a green bar is undone"), so here those
# phrases write a plain "checks" that the agreement rule does not touch.
REGEX = [
    (pat, repl.replace(_code.M, "") if isinstance(repl, str) and repl.startswith(("failing ", "passing ")) else repl)
    for pat, repl in _code.REGEX
]
PROTECT = _code.PROTECT

_HAND = {
    # a threshold or a stage here, not a run of checks
    "skills/README.md",
    "skills/architecture-decomposition/SKILL.md",
    "skills/gate-advance/SKILL.md",
    "skills/llm-vision-convergence-loop/SKILL.md",
    "skills/render-compare-eval-loop/SKILL.md",
}


def _wanted(rel):
    for base in ():
        if rel.startswith(base):
            return "skills/" + rel[len(base):] not in _HAND
    return rel in {
        "docs/requirements/low-level-requirements.toml",
        "docs/requirements/system-requirements.toml",
        "docs/test/test-cases.toml",
        "docs/requirements/stakeholder-needs.toml",
        "docs/requirements/interfaces.toml",
        
        
    }


_ALL = subprocess.run(
    ["git", "-C", r"C:/Projects/ai-template-wt-vocabulary", "ls-files"],
    capture_output=True, text=True, check=True,
).stdout.splitlines()
EXTRA = sorted(rel for rel in _ALL if _wanted(rel))
# Everything else is skipped by top-level glob (vapply tries EXTRA first).
SKIP = sorted({rel.split("/", 1)[0] + "/*" for rel in _ALL} | {rel for rel in _ALL if "/" not in rel})
