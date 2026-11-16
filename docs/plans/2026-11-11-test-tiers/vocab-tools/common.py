"""Shared scope facts for every concept's rule file."""

# Paths check_vocab scans as live but which are records or generated views.
# Records keep the words they were written in; a stored value a current script
# still reads is rewritten by the migrator, not by a prose sweep.
RECORDS = [
    "docs/decisions/*",
    "docs/decisions-for-review-*.md",
    "docs/ai-template-redesign-2026-09-05-codex/*",
    "docs/ai-template-redesign-2026-09-05 - claude/*",
    "docs/spine-restructure-2026-08-08.md",
    "docs/concurrency-v2.md",
    "docs/concurrency-restructure.md",
    "docs/status.md",
    # a ledger of rulings, each quoted as it was made
    "docs/repo-lock.md",
    "docs/work/*",
    # generated: regenerate at the trunk step
    "docs/iteration_index.md",
    "docs/interface-reference.md",
    "docs/cli-reference.md",
]

# Spans a sweep must never rewrite: names of dated records and work items
# (citations), and other tools' own flags.
PROTECT = [
    r"\b20\d\d-\d\d-\d\d[a-z]?-[A-Za-z0-9_.-]+",  # dated record file names
    r"\bWI-\d+-[A-Za-z0-9_-]+",  # work-item file slugs
    r"dangerously-bypass-approvals-and-sandbox",
    r"--ask-for-approval",
    r"approval[-_]policy",  # the Codex CLI's own setting
    r"docs/ratify/[A-Za-z0-9_./-]*",  # immutable dated briefs
]

# Edited by hand only: the glossary names earlier words on purpose ("Formerly ...").
HAND_ONLY = ["project-trajectory/GLOSSARY.md"]
