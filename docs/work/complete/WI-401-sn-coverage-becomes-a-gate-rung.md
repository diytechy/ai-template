+++
id = "WI-401"
title = "SN coverage becomes a gate rung: an SN with no covering SR caps the derived gate (owner ruling 2026-08-01, dispatcher-flow review Q2; log.md Decisions references the session). TODAY derive_gate.py reads SNs only as draft-or-not (sn_draft_ids) and SN->SR linkage is NOT a gate input at all - an unanswered ratified need leaves the gate untouched, while its orphanhood is only a trace.py finding at G2 strictness. THE RUNG: in _raw_level, a ratified SN id cited by zero SR SN-Refs caps the raw level at G0 (a ratified-but-unanswered need means G1 is not earned; a draft SN already caps at G0 via the existing rung, so the new rung bites only the ratified-and-uncovered case). MEASURED SAFE 2026-08-01: census on this repo reads 25/25 SNs covered, zero ghost SN-Refs, so the rung lands green here - the test fixture must construct the uncovered case, not find it. KEEP THE DOUBLE-COUNTING SEAM the current design manages deliberately: a Draft row is EXEMPT from the orphan rule yet drops the gate - one fact must not fire two findings at once, so document the split (this rung = the gate input on ratified SNs; the trace.py orphan finding = the itemized listing at strictness) and verify the pair does not contradict on the same registry state. F5 RULE APPLIES: derive_gate.py stays self-contained - the SN-Refs parse is duplicated, not imported, and pinned equal to trace.py's by tests/test_rule_sync.py exactly like phase_num and LLR_EXEMPT already are. Update docs/registry-machinery-reference.md's gate-computation section, and the basis-line documentation if the counts change shape (the basis line is compared whole by --check, so any new field is a cache-format change downstream repos regenerate through). Tests: an uncovered ratified SN caps at G0/G1; covering it restores the prior level; a draft SN still reads G0; -000 example rows are ignored; the ex-draft counterfactual treats the rung consistently."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

The rung (2026-08-02, work commit 38091685): `derive_gate.sn_gate` now takes
the cited set and reads, in order — Draft SN => G0 (the existing rung, and the
only one that fires on a draft); ratified SN in the cited set => G3 (never
caps); ratified SN cited by zero SR `SN-Refs` => G0 (a ratified-but-unanswered
need has not earned G1; the runnable value still floors to G1). The cited set
is `sn_cited_ids(srs)` — the SN-Refs parse duplicated from trace.py per F5,
never imported, now a NAMED function on both sides (trace's inline
`sr_sn_refs` comprehension became the same function) and pinned equal by
`tests/test_rule_sync.py::test_sn_cited_ids_agrees`, the phase_num/LLR_EXEMPT
pattern. `_raw_level` rebuilds the set from the rows in scope, so the ex-draft
counterfactual drops a Draft SR's citation with its row — removing a draft
answer never fabricates coverage. The double-counting seam holds and is
documented on both code sides plus the reference doc (§2.1/§6/§8.1/§8.3/§8.4):
this rung is the gate input on ratified SNs; trace.py's `SN … has no SR` stays
the itemized orphan listing at G2 strictness; a Draft SN is exempt from both
(one fact, one rung); and both surfaces read the same cited set, so the gate
and the listing cannot contradict on one registry state.

Cache format: the compared basis line gains `uncovered=N` between `modified=`
and `computed=` — the spec's counts-change-shape branch was exercised, so this
is a cache-format change (`--check` compares the line whole) handled
coherently: docs/gate recommitted in the work commit, the dogfood cache test
red on the old format and green after regen. Census on this repo at close:
SN=25, uncovered=0 — 25/25 covered, the rung lands green here exactly as the
spec measured
<!-- fig: cmd="python project-trajectory/scripts/derive_gate.py --print --root ." rev=38091685 -->.

Tests, watched red first — 8 failed on the claim tree (the rung fixtures, the
sn_gate signature, the rule-sync pin; the uncovered fixture read raw G3 where
the rung demands G0), then green: uncovered-ratified caps at G0/G1 with
uncovered=1 on the basis; covering via SN-Refs restores G3; a Draft SN stays
on the draft rung with uncovered=0; -000 rows are ignored on both sides of the
join (an example SR cannot fake coverage); the ex-draft consistency case; the
sync-pin battery. Registration per the WI-393 precedent: LLR-147 + TC-141
(CMP-001, under SR-049, Phase 4) — SR-049's Verified row untouched, no
Modified flip owed. Bookkeeping re-stamps, reasons in place: trace.py size
baseline 2895->2909 (+14: the named parse + seam comments); dupes census
5a474f5d87b5 -> e933a42ec7f5 (the spine-loader block grew to span
sn_draft_ids + sn_cited_ids, class count 20 unchanged). Deliberately NOT
built: window_open does not read `uncovered` (its signals stay
drafts/modified) — recorded as an honest gap in §8.4, not scope.

Watched at close: smoke 616 passed / 6 skipped in 9.73s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=38091685 -->;
full suite 1866 passed / 10 skipped in 0:04:51
<!-- fig: cmd="python -m pytest -q -n auto" rev=38091685 -->;
check_trajectory / check_doc_refs / check_figures all rc=0 under --strict, and
derive_gate --check rc=0 on the recommitted cache.
