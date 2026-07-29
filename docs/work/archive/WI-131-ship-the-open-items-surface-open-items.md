+++
id = "WI-131"
title = "Ship the open-items surface - OPEN_ITEMS template + scaffold"
workstream = "templates"
needs = ["WI-130"]
order = 130
+++

## Deliverable

WI-131 (2026-07-13, open-items-surface slice 2): the owner decision surface ships. New OPEN_ITEMS.template.md (header states the lifecycle - a section lives only while pending; the ruling appends to log.md Decisions and the section is deleted; content quality stays reviewer-class - check_docs warns on structure only - plus an OI-1 example brief matching STATUS.template.md's OI-1 example so a fresh scaffold is coherent for the WI-132 S-3 check). bootstrap.py MAPPING gains (OPEN_ITEMS.template.md -> docs/open-items.md); STATUS.template.md gains the header Owner-decision-briefs link line + the Needs-<human> guidance (gate/ratification blockers FIRST; one-liners here; depth in open-items.md); project-trajectory/README.md kit-contents gains the row; tests/test_bootstrap.py scaffold file list gains docs/open-items.md; test_clean_scaffold_passes pins the scaffolded status.md -> open-items.md link resolving. No script-logic change beyond MAPPING; no byte-budgeted file touched.
