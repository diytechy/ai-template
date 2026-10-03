+++
id = "WI-762"
title = "adjudicate: LLR-195, LLR-206 - approved/routed cell(s) amended on merged trunk 8773677..c58af7a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-195", "LLR-206"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-195 `Detail`: "measure() walks project-trajectory/scripts/**/*.py (excluding __pycache__), hashes each function's AST-dumped body (doc…" -> "measure() walks project-trajectory/scripts/**/*.py (excluding __pycache__), hashes each function's AST-dumped body (doc…"
- LLR-206 `Detail`: "cognitive() walks one function's body by recursive descent carrying a nesting level (not ast.walk, which loses depth), …" -> "cognitive() walks one function's body by recursive descent carrying a nesting level (not ast.walk, which loses depth), …"

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
