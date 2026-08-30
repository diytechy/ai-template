+++
id = "WI-543"
title = "SR-163 verification: one TC that drives the complete file-to-requirement-to-need join over the whole shipped universe"
specref = "docs/requirements/system-requirements.toml#SR-163"
workstream = "requirements"
sr_refs = ["SR-163"]
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Context

**Why this row exists, and why it is parked in `deferred/` rather than queued.**
`SR-163` (Approved, `verification = "Test"`) requires that every shipped file
map, through the declared inventory and its exclusions, to a system requirement
whose references resolve to a stakeholder need — the whole join, over the whole
shipped universe. Its two children deliver mechanisms, not that join:
`LLR-203`/`TC-199` (the inventory's missing-file and stale-entry findings, the
dogfood direction and the package direction) and `LLR-204`/`TC-200` (the
`Implements:` backlink grammar, the inverse direction over the source roots).
Both LLRs record on-row that the purpose join and the shipped-file universe
are undischarged, and after the remap program's close (review rounds 003, 011,
013 of its lane) the two TCs verify only their LLRs, so `SR-163` stands as an
honest orphan — `trace.py --strict`: `SR SR-163 has no test (TC)`.

Review round 018 of that lane made the successor a condition of the merge:
*"file a successor owning SR-163, then implement and trace a TC that drives all
of its acceptance classes before closing the owner."* This row is that owner.
It is filed under the delegated unattended run (decision file
`docs/decisions-for-review-2026-08-31.md`, decision 19) with the kit's own
allocator, and parked in `deferred/` because its scope is the owner's to weigh:
the join needs a declared purpose reference per shipped file (the `Implements:`
line, or a MAPPING-side annotation) across ~74 kit modules plus the
non-Python surface, which is authoring the owner may prefer to sequence after
the complexity-sensor and adjudicator-retention programs already queued.
Moving it to `queued/` is the owner's act; nothing else changes.

**Done-when.** A TC (new or a widened `TC-199`) whose method drives, over the
full declared inventory (`bootstrap.py::MAPPING` plus its recorded exclusions),
every acceptance class `SR-163` names: a shipped file absent from the inventory,
a stale entry, an entry whose requirement reference does not resolve to a need,
a file with no mapping, and a generated output mapping through its generator —
each reported under the declared warn-versus-gate policy; the TC `verifies`
`SR-163` directly; approval through the ordinary flow under the declared dial.
