"""HANDOFF 10.7 item 1 (9.10's leftover): the same phrase map as
r47e_checks_prose.py, over the prose where "bar" names a run of checks in
nearly every use: the skills (with their two mirrors), the stack file's
comments, the runtime flows, the work-item specs, two prompts (with the
worker prompt's golden copy, which must stay byte-equal to its render), and
two registries. Every line of the dry run was read.

Not here, edited by hand (h47g*.py) because the senses mix (a threshold, a
stage, the retired axis): the rows of the spine tiers and the interfaces,
the glossary (its "Formerly a bar" lines name the earlier word on purpose),
README files, PROCESS*.md, CLAUDE.md, AGENTS.template.md, the rubrics, the
repository's own docs, and the skills listed in `_HAND`.
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

REGEX = _code.REGEX
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
    for base in ("project-trajectory/skills/", ".claude/skills/", ".agents/skills/"):
        if rel.startswith(base):
            return "skills/" + rel[len(base):] not in _HAND
    return rel in {
        "docs/stack.ini",
        "docs/runtime-flows.md",
        "project-trajectory/prompts/worker.template.md",
        "project-trajectory/prompts/adjudicate-disposition.template.md",
        "tests/golden/worker-prompt-one-row.txt",
        "docs/requirements/assumptions.toml",
        "docs/requirements/external.toml",
    } or rel.startswith("docs/specs/")


_ALL = subprocess.run(
    ["git", "-C", r"C:/Projects/ai-template-wt-vocabulary", "ls-files"],
    capture_output=True, text=True, check=True,
).stdout.splitlines()
EXTRA = sorted(rel for rel in _ALL if _wanted(rel))
# Everything else is skipped by top-level glob (vapply tries EXTRA first).
SKIP = sorted({rel.split("/", 1)[0] + "/*" for rel in _ALL} | {rel for rel in _ALL if "/" not in rel})
