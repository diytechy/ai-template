+++
id = "WI-595"
title = "LLR-207/TC-205 return and LLR-208/TC-206 amendment: the verdict rows describe every mechanism that now holds them"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
priority = 2
safety_class = "spine"
bar = "DevStg-Tests"
+++

## Context

Drafted by WI-590 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

VERDICT THIS CONTINUES:
`docs/reviews/wi-590-adjudicate-llr-207-llr-208/004-ADJUDICATE-774ef35.md`,
governing line `OUTCOME: RETURN rows=4`. `LLR-208` and `TC-206` were APPROVED by
that act; they enter this scope as an AMENDMENT (round 011 MAJOR, below), not
as a return. NO OVERLAPPING ADJUDICATION REMAINS: `WI-594` (minted at
`09193fea` for the out-of-band trunk range) was minted naming these four rows
as well as LLR-209 and TC-207; round 012 drove its first-approval brief and
found it would put LLR-207 and TC-205 in front of a fourth adjudicator as
awaiting first approval, with none of this lane's three returns in the brief.
WI-594 was therefore NARROWED on the trunk to LLR-209 and TC-207 — the two
rows only that range authored — so this successor is the one next author of
LLR-207/TC-205 and the one amender of LLR-208/TC-206, and needs no ordering
against it. Its merge mints the amendment adjudication over the two Approved
rows it amends (§A5.2), which is where the approval act is taken.

ROUND 011's MAJOR, the amendment half of this scope. `LLR-208.detail` says
membership in the trunk regen set "is the only thing that makes the
exclusive-writer clause above true"; since `7ea3cce7` that is false in the
tree — `gen_verdict_rollup._off_trunk_refusal` refuses a direct write on any
branch other than the trunk (exit 2), and `trunk_step` passes `--trunk-step`
as the one allowed off-trunk caller — so the Approved cell now under-describes
its own module, and the snapshot copied it whole. Amend `LLR-208.detail` to
state BOTH mechanisms (the refusal is what enforces the clause; the regen
membership is what keeps the artifact fresh), add `_off_trunk_refusal` to
`LLR-208.code_symbol`, and state the refusal arm in `TC-206.method` with
`tests/test_verdict_record.py::test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`
cited in `TC-206.evidence`. Those are amendments to Approved cells: intake
mints their amendment adjudication at this successor's merge (§A5.2), and
the act stays the adjudicator's.

`LLR-207` and `TC-205` return together
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
