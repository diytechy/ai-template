+++
id = "WI-971"
title = "The adoption-record step reads lane commits and work specs through the shared walk and listing"
workstream = "process"
sr_refs = ["SR-148"]
specref = "docs/decisions/wi-969.toml"
buildtier = "medium"
safety_class = "ordinary"
priority = 6
+++

## Context

Filed by hand in headless leg 11 (2026-10-22) at WI-969's landing, as
`docs/decisions/wi-969.toml` D-022 and D-027 state: every review round of
that lane raised the same consolidation MINORs (PROCESS.md §3,
"Consolidate, don't duplicate"), which never cost a round and were not
fixed after the gate.

- `adoption_record.staged_adoption_record_lines` and its `_squash_walk`
  resolve HEAD, MERGE_HEAD and the SQUASH_MSG tip, test ancestry and walk
  HEAD..tip, repeating `text_then_act.staged_text_then_act_lines` and
  `_squash_lines` (a third copy beside `plan_gate`'s), and walk commits
  outside `text_then_act.lane_commit_walk`. The stated reason, an import
  cycle, exists only because `LANE_COMMIT_RIDERS` lives in `text_then_act`
  and imports `adoption_record` to register the rider.
- `adoption_record._spec_paths` (per-id spec paths under `docs/work` and
  `docs/archive/work`, at a tree or the index) repeats in intent
  `acceptance_record._tree_specs`, differing only in that it keeps
  duplicate ids where `_tree_specs` collapses them; `tree_specs` and
  `_tree_text` in the same module are a second listing-plus-read pair.

Anchor: SR-148 (LLR-345 is the commit rule's one home). The row changes
no behaviour.

## Done-when

- One traversal owner, below both services, walks a lane's commits and a
  staged squash's HEAD..tip range for every per-commit rule (text-then-act,
  the adoption record, the plan gate where it shares the shape); each rule
  keeps its own range read, refusal text, remedy and squash policy, and no
  import cycle is needed to register a rider.
- One work-spec listing at a tree or the index serves `acceptance_record`
  and `adoption_record`, each keeping its own view (single path per id,
  or every path with the duplicate refusal).
- The existing tests of all three rules pass unchanged, and a test drives
  each rule's staged squash form through the shared walk.
- No RESYNC migration is forced; the bar is green on the landing tip.
