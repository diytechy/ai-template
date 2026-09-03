# WI-586 — ADJUDICATE first approval — commit d7ffb41

Four rows awaiting a FIRST approval: `LLR-207`, `LLR-208`, `TC-205`, `TC-206`.
The question judged is the only one this act answers — is each row's TEXT ready
to be blessed as it stands. Basis: the live registries against
`docs/archive/last_approved` (copied 2026-08-30, commit `4824c0ba`).

Every load-bearing claim below was re-driven against the tree at this commit
rather than read for plausibility. Citations are what I ran or read, not what a
cell asserts. Two independent hostile readers were run over `LLR-207`/`TC-205`;
every finding they returned that appears below I re-drove myself, and the ones I
could not confirm as text defects are recorded in the closing section rather
than carried into the verdict.

## The rows

- [RETURN] LLR-207 -> obligation: ONE definition of what a governing verdict is — the record-path tree identity, the rev it is measured at, the logged-session evidence join, the declared phase span and the cycle count — so the merge slot's "may this lane merge" and the loop's "which phase does it still owe" cannot answer differently -> chain: parent `SR-156` is the right home (its seam's verdict rung is `LLR-140`'s, already Approved, and this row is that rung's shared definition, declared as the `IF-175` seam whose requestors are `integrate`, `agent_loop` and `gen_verdict_rollup`); sideways it does not overlap `LLR-140` (the refusal ladder) or `LLR-145`/`LLR-150`/`LLR-151`; downward its sole `TestRefs` is `TC-205` -> NOT READY on five counts, each driven. (1) `Detail` says `governing_identity` "composes governing_rev and tree_identity for HEAD or an explicit revision" — the contract is the BRANCH TIP, and the first argument must be a branch NAME, not `HEAD`. Driven at real refresh commit `c16246e0`: `refresh_attestation` answers the attested work sha under the branch name and `None` under `"HEAD"`, and `governing_identity` returns `ce5e2550…` vs `2c9a1840…` — two identities across exactly one refresh commit, which is the cross-refresh disagreement this row exists to eliminate. The module forbids the word by name (`kitlib/verdict.py:738-740`, "`branch` must therefore be the lane's BRANCH NAME and not `HEAD`") and records it as the original defect (`:50`). A row whose one job is to name the identity both readers key on must not name the value that silently produces a different one. (2) `Detail` says `governing_rev` "walks across commits whose non-record identity equals their first parent's UNTIL IT CAN PEEL a verified refresh" — that is not the termination condition. Driven at `0e6bad3b`, where `refresh_attestation` is `None` and no refresh exists in range: `governing_rev` still walks back to `d202c9f3`, terminating at the first commit whose identity differs from its parent's (`verdict.py:462-475`; a peel `continue`s at `:467` rather than ending the walk). A builder implementing the row's sentence returns the tip. `IF-175` states the same mechanism correctly ("to reach a refresh it would otherwise hide"), so the defect is this cell's wording and not the design. (3) `Detail` states "a joined key whose logs declare more than one review phase yields no round" and NOTHING verifies it: no fixture in the repo writes two session logs at one `(train, ordinal)` — `tests/test_verdict_record.py:401` asserts "one session log" and `add_round` writes exactly one per ordinal — and relaxing the guard at `verdict.py:608` from `len(ph) == 1` to last-wins leaves the whole suite green (98 passed, mutation driven and reverted). This is a stated fail-closed rule with no detector. (4) `Detail` states "branch_trailers verifies each carrier against its governing identity" — the anti-forgery half of the row's own claim that the trailer "cannot create an approval" — and deleting that check (`verdict.py:802-803`) also leaves the suite green: every fixture commits its trailer on a carrier whose identity already matches, so the "words rode onto a tree they do not describe" arm is unexercised repo-wide. (5) `Detail`'s `work_tip` clause and `refresh_attestation`'s refusal arms are discharged only in `tests/test_integrate_station.py`, which `TC-205` does not cite — that suite is `TC-132`'s, verifying `LLR-140`. The `Rationale`'s "Separate read-only and reset peels protect both contracts" therefore has no test under THIS row. Findings (1)-(2) are false statements of a delivered contract; (3)-(5) are stated obligations no cited test discharges. Either class alone returns the row.

- [RETURN] TC-205 -> obligation: drive the verdict record's two halves — the identity and the evidence — each beside its opposite, so the merge gate's demand and the loop's owed set are shown to come from one reader -> chain: `Verifies` `SR-156;LLR-207;IF-175` satisfies the triangle (`LLR-207.sr_refs = ["SR-156"]`, `IF-175` owned by `scripts/kitlib/verdict`); `Tier: Smoke` is right for the 36 `test_verdict_record` nodes; all 39 evidence node ids exist and collect, and the vacuity sweep is clean — every `== []` is either paired with an opposite arm or explicitly guarded against the empty-scan failure mode (`tests/test_verdict_record.py:331-333`, `1378-1381` commit a real `WI: WI-401` trailer and say so) -> NOT READY, and it moves with its parent: the three coverage gaps above (LLR-207 findings 3, 4, 5) are gaps in exactly this row's `Method` and `Evidence`, so blessing this text would record that `LLR-207` is verified when its multi-log ambiguity rule, its trailer-carrier verification refusal and its reset-peel contract are not. One further defect is this row's alone: `Method` states "a changed work blob and a changed `docs/work/` spec each fold DIFFERENT", but at `tests/test_verdict_record.py:81-90` only the `src/widget.py` entry is changed (`b"00001"` -> `b"00009"`; the spec's synthetic blob is `…0002` and its path holds no `00001`) and the second assertion DROPS the spec entry rather than changing it. Coverage is equivalent in effect, but the sentence describes an assertion that is not in the test, and a `Method` is a claim about what was driven.

- [APPROVE] LLR-208 -> obligation: the per-review-scope rollup is GENERATED — one file per review scope under `docs/reviews/rollup/<train>.md`, scope set taken from the round-file name parser's own `train` field rather than the directory layout, the generator owning that directory on both the check and the write arm, the one name collision refused rather than resolved, declared/regenerated/freshness-gated at the seam and stood down on a work branch, and stating no governing verdict -> chain: parent `SR-170` holds the exclusive-writer contract for shared authority surfaces and this is a third such surface joining the compiled log (`LLR-137`) and the generated status snapshot (`LLR-060`/`LLR-124`), with the work-branch skip signal owned separately by `LLR-141` — no overlap, one decision (the serial trunk actor is this artifact's sole writer); downward `TC-206` -> READY. I read `project-trajectory/scripts/gen_verdict_rollup.py` in full and every clause binds: the scope set is `kverdict.round_file`'s `train` over `rglob` (`:89-95`), `rollup/` excluded from its own scan (`:90`), the flat layout's reserved stem (`:55`, `:108`), the collision refused on BOTH arms before the `--check`/write split (`:176-191`), normalized-line-ending comparison (`:200`), `_extra` reported by `--check` (`:203`) AND pruned by the write path (`:219-221`), and the header carrying "**The merge gate does not read this file.**" (`:63-64`). The wiring the cell claims is real: `docs/stack.ini:988` declares `docs/reviews/rollup/ = verdictrollup`, `trunk_step.py:589` carries the `verdict-rollup` regen row, `check.py:1176` wires the step and `:1554-1556` places it in `_TRUNK_FRESHNESS_STEPS`. `Component: CMP-009` is right — the artifact is a human reading surface — and its one cross-component edge into `kitlib/verdict` (CMP-008) is declared and policed by `IF-175`, which names `scripts/gen_verdict_rollup` a requestor "for the NAME grammar only", true of the code (`:92`, `:115` are its only `kverdict` calls). Every obligation is restatable and closed; no "should", no unnamed threshold.

- [APPROVE] TC-206 -> obligation: drive the rollup as derived state — regeneration, all three `--check` answers, the extra arm proven CLEARABLE by the remedy its own failure message names, the flat pre-train layout, the collision refusal on both arms, the prune, and the honesty sentence — with the declaration side held by the wiring guard and the work-branch stand-down set asserted whole -> chain: `Verifies SR-170;LLR-208`, all four evidence nodes exist, and all three modules (`test_verdict_record`, `test_generated_freshness_wiring`, `test_check_lane`) are outside `tests/conftest.py`'s `SLOW_MODULES`, so `Tier: Smoke` is exact rather than covered-on-paper -> READY. Every `Method` clause has a driving assertion at `tests/test_verdict_record.py:1207-1285`: absent-is-stale (`:1217`), fresh (`:1225`), a new round re-staling (`:1229`), the flat layout stale -> regenerated into the reserved stem -> fresh (`:1246-1252`), the collision refused on the check AND the write arm (`:1259-1260`), the flat rollup pruned when both scopes go (`:1264`), the retired scope's rollup asserted REMOVED with the assertion placed on the CLEARING and not the reporting (`:1269-1273`), and the header sentence (`:1222`). The declaration side is `test_generated_freshness_wiring.py:108-132` (bidirectional — no unenforced `[generated]` row, and no table entry naming a row that no longer exists). The test drives one arm the `Method` does not describe — recursive pruning of a nested output (`:1279-1285`) — which is coverage beyond the claim, not a false claim.

## What this returns, and what it does not

`LLR-207` and `TC-205` go back TOGETHER: findings 3-5 are one gap seen from the
requirement and the test side, and neither row can be blessed while the other
carries it. The `## Dispositions` draft in this row's spec states the whole set.

Nothing about the DESIGN is returned. The identity fold, the two-shape peel, the
logged-session join, the phase span and the cross-check-not-accept reading of the
trailer are all correct as built and I would bless them stated accurately —
findings (1) and (2) are wording that contradicts the module, not a mechanism to
reopen. `IF-175` is untouched by this act (it is not among my rows, and it states
both mechanisms correctly).

Three observations that do NOT falsify a cell in this batch and therefore raise
no draft, recorded so the next reader need not re-derive them:

- `agent_loop.py:317` defines its own `REVIEW_PHASES = ("REVIEW-A", "REVIEW-B")`,
  an unpinned identical copy of `verdict.py:157`, and `_clamped_review_rounds`
  clamps with a magic `min(2, ...)` (`:4170`) where `verdict.py:678-679` claims
  it "clamps the dial to the same span". This does NOT falsify `LLR-207`: the
  SPAN both readers slice really is `kverdict.declared_phases` (`agent_loop.py`
  `:1211`, `:2751`; `score_reviews.py:429`), and `agent_loop`'s own tuple is used
  only for the different question of whether a phase IS a review phase
  (`:354`, `:3284`). It is a duplicated closed vocabulary of the class
  `kitlib/ladder.py` exists to end — a design finding for a separate lane.
- `IF-175`'s `requestors` omits `scripts/score_reviews`, which holds a hard
  `from kitlib.verdict import declared_phases` (`score_reviews.py:72`, used at
  `:429`). `IF-175` is not my row and is not in this batch.
- `components.toml`'s `CMP-006` note says `kitlib/station.py` "is the one package
  module NOT owned here". With `verdict.py` at `CMP-008` that enumeration is
  stale. It was already stale on the merged trunk before this act — the module
  and its row exist there — so approving or returning `LLR-207` neither creates
  nor cures it, and `CMP-006` is an Approved row outside this act's scope.

## The approval act on LLR-208/TC-206 is WITHHELD — mechanism, not content

The two APPROVE lines above are my verdict on those rows' TEXT and they stand.
The `Status` flip and its anchoring snapshot could not be TAKEN, for the reason
`WI-584` was minted to fix, and no registry cell was edited by this session.

Reproduced at this commit. I flipped `LLR-208` and `TC-206` to `Approved` — two
bytes, `git diff` confirmed nothing else moved — and ran the prescribed act:

    python3 project-trajectory/scripts/intake.py snapshot --approves \
      "docs/requirements/low-level-requirements.toml=WI-586;docs/test/test-cases.toml=WI-586"

It is REFUSED, and neither registry I flipped appears in the refusal. Every row
listed is an `SR-###` in `docs/requirements/system-requirements.toml`:
`SR-024`, `SR-033`, `SR-043`, `SR-052`, `SR-053` `Rationale` and twelve more.
`baseline_snapshot.refresh_ledger` at this commit reads `system-requirements.toml`
17 absorbed rows, `low-level-requirements.toml` 9, `test-cases.toml` 4, no flips
anywhere. `copy_live` has been scoped since `WI-571` and would not have written
`system-requirements.toml` at all; `refresh_refusal` judges the whole ledger.
This is `WI-584`'s observable, unchanged and still queued.

Neither way around it is open to me.

- Naming `system-requirements.toml` in `--approves` would re-anchor text this
  act did not bless. My own brief forbids it in as many words — "the merge
  refuses the whole commit as a snapshot WIDENED without an approved row" — and
  it would resolve `WI-584`'s open ruling (a)/(b) by fiat, from a lane whose
  scope is four rows' text. The 17 SR cells are `WI-547`'s CLARITY verdict;
  whether a CLARITY verdict authorises absorbing them is precisely the question
  `WI-584` exists to rule, and it is not mine.
- Flipping without the anchor lands a RED on the trunk. Driven both ways at this
  commit: `trace.py --approve modified --check` answers "docs/ratify/CURRENT.md
  is current" on the clean tree and "STALE against the registry and the
  docs/archive/last_approved snapshot" with the two flips in place. That step is
  in `check.py`'s `_TRUNK_FRESHNESS_STEPS`, so it SKIPS on this work branch and
  RUNS at the seam — an approved-but-unanchored row would stop the queue at the
  integration step rather than at me.

So the rows stay `Drafted` with their approval OWED and its blocker named, which
is `WI-578`'s precedent for the same mechanism (`docs/reviews/wi-578-adjudicate-llr-158-llr-203/001-ADJUDICATE-921f947.md`
— re-anchor blocked, correction drafted, no act taken) and what `WI-584:76-83`
already says happens next: once that row lands and the act is takeable, a
trunk-side adjudication takes the anchor. The second `## Dispositions` draft in
this row's spec carries `LLR-208` and `TC-206` there, so this reading is not
re-derived and the two rows are not re-judged from scratch.

What this costs is honest and bounded: two rows I would bless read as unblessed
for one more adjudication. What the alternative would cost is a false claim in
the approval record or a red at the seam.

OUTCOME: RETURN rows=4
