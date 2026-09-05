+++
id = "WI-595"
title = "LLR-207/TC-205 return and LLR-208/TC-206 amendment: the verdict rows describe every mechanism that now holds them"
workstream = "process"
specref = ""
buildtier = "strong"
priority = 2
safety_class = "spine"
bar = "DevStg-Tests"
+++

## Deliverable

Four cells, no new mechanism and no regression written: every arm described
below already existed and passed, and only the record was silent. All four of
the spec's claims were re-driven on this tree before anything was edited, and
all four hold.

RETURNED (`Drafted`, this branch's merge mints their adjudication):

- `LLR-207.detail` — the `governing_rev` clause said the walk peels "any
  verified refresh it meets". `_peel_target` has peeled TWO classes since the
  second disposable-commit class entered the tree. The clause now names both
  (the station REFRESH, admitted by `refresh_attestation`; the machinery's own
  ADJUDICATION CLOSE, admitted by `mechanical_close_attestation` against the
  exact composed subject, a single parent, and a NON-EMPTY changed-path set
  wholly under `docs/work/` — the non-emptiness is the code's (`if not paths
  or …`) and a later read caught the first draft stating a clause the empty
  set satisfies vacuously, which matters because the zero-path commit is a
  real class this very test case drives elsewhere), the ONE property that
  admits them rather than two rules — both
  machine-authored, both moving the tree without the lane changing what it
  CLAIMS — and the fail-toward-review direction of every arm. The `work_tip`
  contrast is now explicit instead of implied: `work_tip` calls
  `refresh_attestation` DIRECTLY rather than through the shared disposable
  test, so a mechanical close is never removed by the destructive reset path.
- `LLR-207.code_symbol` — added `mechanical_close_attestation`, an `__all__`
  export that changes what both readers answer and that `grep` found described
  by ZERO rows in any requirements registry. `_peel_target` deliberately left
  out: private, and the two attestation readers are the named surface.
- `TC-205.method` / `.evidence` — `THE PEEL` enumerated the refresh arm alone.
  The second class is now stated in the cell's own idiom: the positive, the
  hand-written-subject refusal, the forged-middle refusal, and the
  reached-outside-`docs/work/` refusal. The positive also asserts the close
  REALLY moved the tree and drives the two peels COMPOSING. The forged-middle
  case is the rework regression; the other three already passed but no test
  case cited them.
- `TC-205.tier` — `Smoke` -> `Full`, RULED rather than left open, with the
  basis recorded in `Method`. The ruling rests on a MEMBERSHIP fact, not on a
  total, and is stated that way so a later citation cannot stale it: citations
  of this row live in `test_integrate_admission`, `test_integrate_station` and
  `test_handback`, all three in `tests/conftest.py` `SLOW_MODULES` and so
  deselected by `-m smoke` (9 of them as this row closes). `Full` is
  the cheapest tier at which the whole cited set runs; `Smoke` claimed
  commit-floor coverage for a set the commit floor only partly runs, which is
  the direction §12.2 names as the harmful one. Sibling `TC-132` already reads
  `Full` while citing the same station module.

AMENDED (Approved cells; §A5.2 mints their amendment adjudication at merge —
no `Status` was flipped and no `docs/archive/last_approved/` was written):

- `LLR-208.detail` — the cell said regen-set membership "is the only thing that
  makes the exclusive-writer clause above true". That stopped being true when
  the off-trunk refusal shipped, and the snapshot had copied the claim whole.
  It now states BOTH mechanisms and keeps them distinct, because they hold
  different halves and neither substitutes for the other:
  `_off_trunk_refusal` ENFORCES the clause (exit 2 on any branch but the trunk,
  keyed on the PRIMARY checkout, with `--trunk-step` the one exempt caller
  because the station's refresh runs the trunk step inside a lane worktree, and
  `--check` never refused), while regen-set membership keeps the artifact
  FRESH. The cell records why the refusal is load-bearing and not
  belt-and-braces: without it the generator returned 0, wrote the directory in
  a claimed lane, and the work-branch freshness stand-down HID the write.
- `LLR-208.code_symbol` — added `_off_trunk_refusal` (the row already names the
  private `_extra`, so this follows its own convention).
- `TC-206.method` / `.evidence` — stated the refusal arm, including why it had
  to be driven through a real LINKED worktree (the single-checkout fixtures
  every other arm uses are their own trunk and keep writing), and cited its
  detector.

Bar `DevStg-Tests` met: full unfiltered suite `1 failed, 3383 passed, 25
skipped`, the one red being the `docs/stage` FINGERPRINT node, caused by this
branch and benign — driven both ways (passes at the integration base, and
passes at this tip on a regenerated-stage worktree whose every other derived
field is byte-identical, `drafted` included). `docs/stage` is deliberately not
regenerated on this lane; its freshness is the trunk lane's. Numbers, the
both-ways evidence, and the re-run at the closing tip are in
`docs/log.d/WI-595-llr-207-tc-205-return-and-llr.md`, which also records the
three decisions the cells cannot carry themselves: `LLR-208.hat_refs` left
unset deliberately, and the `SR-170`/`UNATTENDED-OPS` question surfaced as a
separate finding rather than fixed inline. Nothing was widened into the
out-of-scope `work_tip` docstring defect the spec fenced off.

REWORK ROUND 1 (review A, `003-REVIEW-A-149698f.md`, one MAJOR). The finding
was right that the return had left its own new claim unevidenced and wrong
about what evidencing it would show, so it is taken in the half that holds.
A regression now exists and is cited —
`test_an_empty_close_is_refused_and_the_walk_covers_it_regardless`, real git
via `--allow-empty`, since a zero-path diff is the one close shape a
file-writing fixture cannot reach. The remedy AS SPECIFIED ("assert the merge
gate asks for review") was not written, because it asserts a behaviour the
module does not have: MEASURED by deleting the `not paths or` clause and
re-running the module — `1 failed, 57 passed`, the single red being the new
boundary assertion, with `governing_identity` and `_verdict_gate` giving
IDENTICAL answers on that fixture in both arms. An empty commit is
identity-preserving by construction, so `governing_rev`'s walk-through step
reaches the real close underneath whether or not the peel admits the empty
one; the finding's "would let it preserve an earlier approval" describes both
arms equally, and preserving it is CORRECT, because a commit that changed
nothing has invalidated no verdict. The clause is therefore a guard on a
public export's contract, not a gate defence, and the arm is asserted at
`mechanical_close_attestation` — where it is the only thing that can refuse —
together with the fact that it strands nothing. `LLR-207.detail`'s
"can only ask for more" was overstated in the same place and is now
"can never ask for LESS", with the empty arm's equality named.

REWORK ROUND 2 (review A, `005-REVIEW-A-5fd59ee.md`, one MAJOR) is complete.
The reviewer demonstrated that `mechanical_close_attestation`
accepted any non-empty, `docs/work/`-confined single-parent commit whose
subject merely had the mechanical-close prefix and suffix, although the row
claimed the subject was verified against the exact WI ids composed by the close
producer. The single owning boundary now reads the commit's no-renames diff,
requires paired same-name moves from one active branch to complete/, derives
the canonically ordered filename ids, re-composes the subject through the
writer's helper, and compares it exactly. The real-git forged-middle regression
proves both the public attestor refusal and the resulting gate refusal;
LLR-207, TC-205, and the approval brief describe and cite the strengthened
contract.

REWORK ROUND 3 (review A, `007-REVIEW-A-8fc8f44.md`, five findings) is
complete; all five are taken and the two MAJORs are fixed at the same owning
boundary, `verdict._closed_wi_ids`.

- The dead `not deleted` disjunct is DELETED, and re-measuring for its
  replacement showed the record would have been wrong a second time: removing
  the `len(branches) != 1` clause ALSO leaves the module fully green, because
  an empty diff derives no ids and the subject it composes
  (`adjudicate:  -> complete/ …`) cannot equal the one the commit carries. So
  the empty close's refusal is OVER-DETERMINED, no clause owns it, and the
  cell, the test comment and this record now say exactly that instead of
  naming a second wrong owner. The one-source-branch clause is separately
  pinned on the case it genuinely does own — a close reaching into a SECOND
  lane's `active/` — which is the single red when that clause is deleted.
- Only the MOVE may create or destroy. An `A` or `D` under `docs/work/` that
  is not half of a recognised move is now a refusal rather than an entry the
  loop skipped, so a close can no longer carry a smuggled new spec or the
  deletion of an archived judged row past the gate; `M` stays unrestricted
  because `spec_move`'s relink only ever modifies. Two real-git regressions,
  both driven RED against the pre-fix module. NO fail-closed regression: all
  nine real historical mechanical closes in this repo still peel.
- The two independently-chosen sortings are taken as the ANTIDOTE the finding
  named rather than as a test: `station.mechanical_close_order` is now the one
  key both sides use, so the writer and the attestor cannot diverge by
  construction. TC-205 gains the two-row batch arm anyway, and the
  writer↔verifier loop is now closed end to end on a REAL
  `handback.close_adjudication` close, which nothing drove before.
- The stale tier total is gone; the ruling is restated on the MEMBERSHIP fact
  it actually rests on, so a later citation cannot stale it again.
- `IF-175.notes` now says the two peel SHAPES are its subject and the
  disposable CLASS list is LLR-207's alone, so one adjudication no longer
  approves two rows describing the same peel at two widths.

SURFACED, NOT FIXED (a separate finding, per the working agreement): no spine
row's `code_symbol` names `station.mechanical_close_subject`,
`MECHANICAL_CLOSE_PREFIX/SUFFIX` or the new `mechanical_close_order` —
`LLR-182` and `LLR-189` between them describe the rest of that module. The
mechanical-close vocabulary was already undescribed before this lane; naming
it is a `LLR-182` amendment and belongs to whoever holds that row.

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

ROUND 005's MAJOR, addressed here. The reviewer constructed a
single-parent commit confined to `docs/work/` with subject
`adjudicate: NOT-A-COMPOSED-WI-ID -> complete/ (mechanical close)` and observed
`mechanical_close_attestation` return its parent. The implementation checked
only the subject's outer affixes, not the exact composed middle claimed by
`LLR-207.detail`. Construction cannot authenticate arbitrary external Git
messages; this verifier is therefore the one owning trust boundary and must
derive the moved WI ids from the diff, compare the canonical subject once, and
refuse the forged middle. That boundary, row text, and TC evidence now move as
one change; `test_a_forged_mechanical_close_middle_does_not_peel` is the
real-git detector.
