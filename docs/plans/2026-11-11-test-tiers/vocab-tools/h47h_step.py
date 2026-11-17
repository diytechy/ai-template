"""HANDOFF 12.4 (ruled 2026-11-16): "stage" names the development stage and
nothing else, so a step of a pipeline in code is a "step". PROCESS.md §3's
"extract the shared stage" is the sentence 12.4 named; CLAUDE.md quotes it,
AGENTS.template.md and the deep-module-design skill restate it, and the
census message, two docstrings and a test's comments cite it. All move
together so the rule reads the same everywhere. Mirrors are re-copied after.
"""

EDITS = [
    (
        "project-trajectory/PROCESS.md",
        "don't patch each site: extract the shared stage\n",
        "don't patch each site: extract the shared step\n",
    ),
    (
        "project-trajectory/PROCESS.md",
        "  become one shared stage feeding both (0→A→B, 0→A→D).",
        "  become one shared step feeding both (0→A→B, 0→A→D).",
    ),
    ("CLAUDE.md", "  shared stage rather than duplicate a fix", "  shared step rather than duplicate a fix"),
    (
        "project-trajectory/AGENTS.template.md",
        "consolidate duplicates into a shared stage (PROCESS.md §3, 0→A→B).",
        "consolidate duplicates into a shared step (PROCESS.md §3, 0→A→B).",
    ),
    (
        "project-trajectory/skills/deep-module-design/SKILL.md",
        "4. **Pull the shared stage out once.**",
        "4. **Pull the shared step out once.**",
    ),
    (
        "project-trajectory/scripts/check_dupes_census.py",
        '"duplicate pairs a fix that wants a shared stage (0->A->B), then "',
        '"duplicate pairs a fix that wants a shared step (0->A->B), then "',
    ),
    (
        "project-trajectory/scripts/integrate.py",
        "The reading itself is the one shared stage,",
        "The reading itself is the one shared step,",
    ),
    ("project-trajectory/scripts/kitlib/spine.py", "    THE SHARED STAGE of", "    THE SHARED STEP of", 2),
    ("tests/test_rule_sync.py", "# Each shared stage below took ONE home", "# Each shared step below took ONE home"),
    ("tests/test_rule_sync.py", "# the shared stage DOES,", "# the shared step DOES,"),
    ("tests/test_rule_sync.py", "are two rows to the shared stage: it", "are two rows to the shared step: it"),
    ("tests/test_rule_sync.py", "and the shared stage takes text", "and the shared step takes text"),
]
