+++
id = "WI-590"
title = "adjudicate: LLR-207, LLR-208, TC-205, TC-206 - spine row(s) authored Drafted on merged trunk e507b76..c5c4a8b await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-207", "LLR-208", "TC-205", "TC-206"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-207 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- LLR-208 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-205 amended in `docs/test/test-cases.toml` (Evidence, Method)
- TC-206 amended in `docs/test/test-cases.toml` (Evidence, Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Dispositions

```toml
title = "LLR-207/TC-205 return: governing_rev peels TWO disposable commit classes and both cells describe one - state the mechanical close in the row that is its only home, and cite the three tests that already prove it"
workstream = "process"
safety_class = "spine"
buildtier = "strong"
priority = 2
specref = "docs/requirements/low-level-requirements.toml"
bar = "DevStg-Tests"
```

VERDICT THIS CONTINUES:
`docs/reviews/wi-590-adjudicate-llr-207-llr-208/004-ADJUDICATE-774ef35.md`,
governing line `OUTCOME: RETURN rows=4`. `LLR-208` and `TC-206` were APPROVED by
that act and are NOT in this scope. `LLR-207` and `TC-205` return together
because the requirement half and the test half of one gap are the same gap seen
from two sides, and because `staged_drafted_rows` queues an approver only for
rows a delta actually amends — a successor that edited `TC-205` alone would
leave `LLR-207` with no queued approver.

This return does NOT inherit WI-586's findings. All of them were re-driven on
this tree and all are DISCHARGED: the `governing_identity` HEAD-vs-branch-tip
clause and the peel-terminus clause now read correctly; every one of `TC-205`'s
46 citations resolves to an existing, passing test in the file it names; the
`test_integrate_station` module is cited; the identity-fixture `Method`
misstatement is gone; `CMP-006.notes` now names `kitlib/verdict.py (LLR-207)`
as CMP-008 with `IF-175` as its declared seam; and the `TC-206` trunk-wiring
gap is closed by a real detector. The finding below is NEW, and it entered the
tree AFTER the row text was last written: `f4ca1bd5` ("four batch-lane
defects", merged at `c590637d`) added a second disposable-commit class to the
governing walk; `LLR-207.detail` was last edited at `64692ddf`.

IN SCOPE — two cells, no new mechanism, no regression to write.

1. `LLR-207.detail`, the `governing_rev` clause. It reads "peeling any verified
   refresh it meets to reach one those commits would otherwise hide". The walk
   does not peel refreshes; it peels through `_peel_target`
   (`kitlib/verdict.py:431-442`), whose docstring is explicit: "TWO commits are
   disposable and this is their one home, so `governing_rev`'s walk asks the
   question once: the station's REFRESH (which re-merges trunk and regenerates)
   and the machinery's own ADJUDICATION CLOSE (which archives a judged row
   terminal)." The second class is `mechanical_close_attestation` (`:376-428`),
   admitted by verification against git — exact subject
   (`station.MECHANICAL_CLOSE_PREFIX/SUFFIX`), exactly one parent, and every
   changed path under `docs/work/`. Restate the clause to name both classes and
   the one property that admits them: both are machine-authored and both move
   the tree without the lane changing what it claims. Keep the existing
   contrast with `work_tip` intact — `work_tip` calls `refresh_attestation`
   DIRECTLY (`:466`), not `_peel_target`, so a mechanical close is never peeled
   on the destructive reset path. That asymmetry is deliberate and is currently
   invisible in the cell, which is why the cell reads as if one rule served both.
2. `LLR-207.code_symbol`. Add `mechanical_close_attestation`. It is a public
   `__all__` export of this module that changes what `governing_rev` and
   `governing_identity` answer, and grep across every requirements registry
   returns ZERO rows describing it — so this row is not one of several possible
   homes, it is the only one. Leave `_peel_target` out: it is private, and the
   two attestation readers are the named surface.
3. `TC-205.method` and `TC-205.evidence`. The `THE PEEL` section enumerates the
   refresh class alone; neither cell contains the string "mechanical". Three
   tests for the second class already exist and pass
   (`3 passed, 53 deselected`) and are cited by NO test case anywhere in the
   registry: `tests/test_verdict_record.py::test_the_mechanical_close_does_not_stale_the_round_it_follows`
   (`:1600`, the positive — a close does not stale the round it follows),
   `::test_only_the_machinerys_own_close_subject_peels` (`:1628`, the subject
   refusal) and `::test_a_close_that_reached_outside_docs_work_does_not_peel`
   (`:1640`, the path-scope refusal). Cite all three and state the arm in
   `Method` beside the refresh arm, driven as its opposite in the same idiom the
   rest of the cell uses: the positive and BOTH refusals, so the peel reads as a
   verified admission rather than a subject match. No new test is needed for
   this item — the coverage exists and only the record is silent.
4. `TC-205.tier`, secondary and rulable either way. It declares `Smoke`, but 8
   of its 46 citations live in `test_integrate_admission` and
   `test_integrate_station`, both listed in `tests/conftest.py` `SLOW_MODULES`
   and therefore excluded from `-m smoke` (measured: `-m smoke` collects 56 of
   139; the 38 `test_verdict_record` citations are the smoke half). The Tier
   field and the pytest marker are a KNOWN unreconciled pair
   (`docs/registry-machinery-reference.md` §12.2) that no check compares, and
   sibling `TC-132` cites the same station module at `Tier = "Full"`. Either
   re-tier this row to `Full` or record in `Method` why `Smoke` is the honest
   label for a citation set the cheap gate only partly runs. Do not silently
   leave both readings available.

NOT IN SCOPE, recorded so a successor does not widen: the module's own
docstring contract paragraph and `work_tip`'s docstring (`:448-455`) also
predate `f4ca1bd5` — `work_tip`'s still claims "`governing_identity` measures
code-time here", which is false since `governing_identity` calls
`governing_rev`. That is a source-comment defect, not a spine cell, and it
belongs to a code lane rather than to this spine return.

NOT ON THIS LANE: this disposition is a DRAFT. Intake mints it at this row's
merge; the lane does not file it.
