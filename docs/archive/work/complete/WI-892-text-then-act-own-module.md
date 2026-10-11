+++
id = "WI-892"
title = "The lane-commit walk and its text-then-act rider move to their own module, shared and unchanged"
workstream = "process"
sr_refs = ["SR-140"]
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Landed 2026-10-10. The text-then-act section moved byte-identical from `acceptance_record.py` (999 -> 920 SLOC) to `project-trajectory/scripts/text_then_act.py`, which also holds `lane_commit_walk` and its rider tuple `LANE_COMMIT_RIDERS`; the hook's squash path and the merge slot's per-commit rungs (text-then-act, and ruling sync with its own riders) walk the same commits through it. Every refusal, its wording and its order are unchanged; the walk takes its commit list from the caller because the two paths list the range differently today (D-002). `_commit_parents` keeps one home in `acceptance_record`. Callers import the new home with no shim; the script is registered for scaffolds; RESYNC entry. Trace upkeep: LLR-298 and LLR-302 module and code_symbol, IF-102 requestors. The Done-when's size bullet was amended to match the ratchet (both modules under its threshold) and blessed at sitting 002. Gates: full 001 (one MINOR, the size bullet), full 003 APPROVE, 0 findings (Codex gpt-6-luna for gpt-6.1-sol, D-001).

## Context

Filed by the coordinator on 2026-10-10 from WI-828's first build round (see
OI-113). `project-trajectory/scripts/acceptance_record.py` sits at 999 of the
size ratchet's 1000 SLOC, so any growth of its text-then-act section reads
as a new monolith. WI-828's round grew it to 1023 and stopped. The section
`# --- TEXT THEN ACT` (`TEXT_THEN_ACT_REMEDY`, `SQUASH_REBASE_HINT`,
`text_then_act_lines`, `commit_text_then_act_lines`, `_squash_lines`,
`staged_text_then_act_lines` and their private helpers) is a separate
judgement that shares only the parent reader with the ruling sync.

This is a structural move (`project-trajectory/PROCESS.md` §3, "A structural
move is its own commit"): it changes no behaviour, so the unchanged tests
review it.

Anchor: SR-140, through LLR-302 (whose module and code_symbol cells move
with the code).

The same row makes the lane-commit walk shared, still without changing
behaviour: WI-828's round 1 showed the shape (one walk, `HEAD..tip` with each
commit judged against its own parents, carrying a tuple of riders with
text-then-act first), and WI-833, WI-850 and WI-851 each add a rider to that
one walk. Today the merge slot walks lane commits in `integrate.py`
`_each_lane_commit` and the hook's squash path walks them in
`acceptance_record.py` `_squash_lines`; after this row both read one walk.
The hand-merge path is not built here: that is WI-893, after OI-113.

Landing order: one deliverable, the module and its one walk. It lands before
WI-893 (whatever OI-113 rules) and before WI-833, WI-850 and WI-851.

## Done-when

- The text-then-act section lives in its own module under
  `project-trajectory/scripts/`; `acceptance_record.py` keeps the shared
  parent reader it needs or both import it from one home (no duplicate).
- One lane-commit walk with a rider tuple (text-then-act its first rider)
  serves both the hook's squash path and the merge slot's per-lane-commit
  check; the ruling-sync judge rides the same walk in the merge slot. Each
  path's refusals, their wording and their order are unchanged.
- Every caller (`check.py`, `integrate.py`, the tests) imports the new home;
  no re-export shim is left behind.
- The existing text-then-act and acceptance-record tests pass unchanged
  (beyond import lines), and the module-size ratchet passes with both modules
  measured: `acceptance_record.py` and the new module each stay under its SLOC
  threshold, so neither carries a baseline entry (the ratchet admits none
  under it).
- LLR-302's module and code_symbol cells and the Implements tags follow the
  move (traced cells only; no row text changes, so no sitting is owed).
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (an adopter who imports
  the moved names updates the import).
