+++
id = "WI-402"
title = "Phase is NUMERIC ONLY, and the next phase is a derived call (owner rulings 2026-08-01, dispatcher-flow review; log.md Decisions references the session). TWO HALVES. (1) THE STRICT-SCHEMA RULE: phase_ratified_findings currently requires only that a Phase cell digit-parses, so a prefixed value like P1 or v2 does not crash - WORSE, it goes silently vacuous in the two string-keyed joins: trace.py --phase and --ratify match the cell LITERALLY (in_phase / _scope_srs), and check_trajectory's phase-drop detector joins the per-phase= label written into docs/gate against the [phase]-[gN] title anchor - a reformatted cell disarms the warn without telling anyone, which is worse than a crash. The rule: once the phase discipline is armed (any spine row phased), every non-Draft SR/LLR/TC Phase cell must be a BARE INTEGER - digits only, full-cell, no prefix - as a strict-schema finding (G3, where strict-schema already bites). Update the template prose that currently blesses 'a downstream v2 still parses' (the registry template comments and docs/registry-machinery-reference.md) and note the migration in the downstream-resync path. Legacy [v3]-style WI title anchors in complete/ are HISTORY - never rewrite them; the rule bites live registry cells only. (2) THE HELPER: derive_gate.py --next-phase prints max(phase over non-draft spine rows) + 1 - the one method every agent and the intake mint helper (WI-388) call when a confirmed scope change opens a new phase; derive_gate already computes the max for the basis line, so this is an output mode, not new derivation. THE PHASE BOUNDARY IS RULED (owner 2026-08-01) and must be recorded where the phase derivation is documented (registry-machinery-reference.md, and PROCESS.md's phase note if it speaks): a phase increments when re-opened scope is CONFIRMED - an adjudication verdict that scope moved, or a new draft-SN batch ratified into scope - NEVER on the raw derived-gate drop; a spurious Modified window must not burn a phase number (the WI-280 shape is the counterexample: 19 traced cells, no scope moved). Tests: strict-schema red on a prefixed cell once armed and green on bare integers; --next-phase prints current max + 1 on a fixture; the boundary rule text exists where the docs claim it."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

Both halves shipped (2026-08-02, work commit e0623526); the spec was
re-validated first against the WI-401-amended SpecRef doc (the standing WARN):
no conflict — WI-401's additions (sn_cited_ids, uncovered=, the seam split)
live in §2.1/§6/§8, this WI's edits land beside them in §3.3, the §3 column
table, §12.7 and §13.

**Half 1 — numeric-only.** `trace.phase_ratified_findings` (`--strict-schema`,
G3 where it already bites) now requires every ratified SR/LLR/TC `Phase`, once
any spine row is phased (digit-parse arming), to be a FULL-CELL BARE INTEGER —
`re.fullmatch("[0-9]+")` on the stripped cell; the finding names the literal
`--phase`/`--ratify` and `per-phase=`/`[phase]-[gN]` joins a prefix silently
disarms. A legacy `vN` registry arms the rule AND now fails it, per cell.
`phase_num` + its F5 copies stay digit-extract (grandfathering); legacy
`[v3]`-style title anchors in complete/ untouched. The v2-blessing prose is
updated everywhere it stood (SR template Phase comment, the reference doc,
PROCESS.md §4, process-options "Phased delivery", EXAMPLE.md), and the
ADOPTING.md §6 resync ledger carries the migration note (strip `v2` → `2` on
ratified rows; a traced cell, no re-attest window).

**Half 2 — the derived call.** `derive_gate.py --next-phase` prints max(Phase
over non-draft spine rows) + 1, bare — the basis line's `phase=N` derivation
as an output mode (docs/gate never written) for the intake mint helper to
`int()`; a Draft row's phase is not yet scope; an unphased spine is the
implicit foundation (1), so it prints 2. On this repo it prints 5
<!-- fig: cmd="python project-trajectory/scripts/derive_gate.py --next-phase --root ." rev=e0623526 -->.
The ruled boundary (increment on an adjudication-confirmed scope change or a
ratified draft-SN batch, NEVER the raw derived-gate drop) is recorded at
§3.3, PROCESS.md §4 and process-options, beside the derivation each documents.

**Evidence.** Watched red first — 4 failed on the claim tree — then green.
Totals on e0623526: full suite 1870 passed / 10 skipped in 0:04:49
<!-- fig: cmd="python -m pytest -q -n auto" rev=e0623526 -->;
smoke 616 passed / 6 skipped in 10.41s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=e0623526 -->;
trace G3 bar, `check_trajectory`/`check_doc_refs`/`check_figures` `--strict`
and `derive_gate --check` all rc=0. Registration: LLR-148 + TC-142 under
SR-049 (CMP-001, Phase 4); LLR-003 Detail + TC-003 Method amended to the built
truth (WI-392 rework precedent, no Modified flip). Byte deltas: PROCESS.md
64,319 → 64,460 (+141), PROCESS_OPTIONS.md 168,222 → 169,010 (+788), both
re-stamped in every tracked byte-budget-guard copy; trace.py ratchet
2909 → 2919, reason in place. Full session record: the WI-402 entry in
docs/log.md (compiled from this branch's log fragment).
