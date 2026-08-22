+++
id = "WI-499"
title = "Retire the word 'ratification' for 'approval' across the live kit (owner-ruled 2026-08-21) - reviewed campaign, records untouched"
specref = "docs/log.d/2026-08-21-owner-session-dial-and-folds.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Owner ruling (2026-08-21, in-session): "ratification holds a weight to it
that the semantics here don't need" — the kit's vocabulary unifies on
**approval**. The ruling is the direction; this row is the reviewed
campaign, NOT a blind mass-replace, because the slice-5 recovery proved
exactly what a mechanical sweep does to records.

Scope, in the WI-498 sweep's proven shape:

- **Live prose and instructing surfaces** (PROCESS.md, PROCESS_OPTIONS.md,
  skills, templates, README, docstrings): ratification/ratify → approval/
  approve, reviewed line by line. One semantic check per site: the kit
  already uses "Approved" as a Status value and "approval" for the human
  gate — verify no site relied on a ratify-vs-approve distinction (if one
  genuinely does, keep it and record it; the owner's premise is that none
  should).
- **Code identifiers and CLI surface**: `agent_common.ratification_through`
  and friends, `trace.py --ratify` and its `ratify-fresh` step,
  `docs/ratify/` (the directory is a RECORD home — the directory may keep
  its name or move with a redirect note; decide by the records rule below),
  test names. Renames land with the same alias discipline WI-498 used
  (loud shims where an adopter-facing spelling changes).
- **The dial key `human_ratification_through`** is adopter-declared config:
  rename to `human_approval_through` with the bootstrap migration path
  (the WI-493/`migrate_legacy_config` precedent), a loud legacy-key read,
  and a RESYNC_PACK entry.
- **Records untouched**: docs/log.md, docs/log.d fragments, docs/archive/**,
  closed WI specs, ruled OI rows, ratify records under docs/ratify/ —
  history keeps its vocabulary (the slice-5 recovery's reverted-hunks
  lesson: a rename must never rewrite a record of the past). check_vocab
  gains the retired-spelling entry for LIVE surfaces only.
- Byte-capped docs measured before/after (byte-budget-guard convention).
  Scaffold-surface changes verified by BOOTSTRAPPING A REAL SCAFFOLD;
  full RESYNC entries.
