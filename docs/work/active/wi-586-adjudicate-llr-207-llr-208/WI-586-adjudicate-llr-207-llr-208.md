+++
id = "WI-586"
title = "adjudicate: LLR-207, LLR-208, TC-205, TC-206 - spine row(s) authored Drafted on merged trunk 273564c..b5735bb await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
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

- LLR-207 authored in `docs/requirements/low-level-requirements.toml`
- LLR-208 authored in `docs/requirements/low-level-requirements.toml`
- TC-205 authored in `docs/test/test-cases.toml`
- TC-206 authored in `docs/test/test-cases.toml`

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
title = "LLR-207/TC-205 return: two Detail clauses contradict kitlib/verdict.py, and three stated clauses have no test"
workstream = "process"
safety_class = "spine"
buildtier = "strong"
priority = 2
specref = "docs/requirements/low-level-requirements.toml"
bar = "DevStg-Reqs"
```

VERDICT THIS CONTINUES:
`docs/reviews/wi-586-adjudicate-llr-207-llr-208/001-ADJUDICATE-d7ffb41.md`,
governing line `OUTCOME: RETURN rows=4` over `LLR-207`, `LLR-208`, `TC-205`,
`TC-206`. `LLR-208` and `TC-206` were APPROVED by that act and are not this
row's business. `LLR-207` and `TC-205` stay `Drafted` and return TOGETHER: two
of the five findings are wording that contradicts the module, three are stated
obligations no cited test discharges, and the requirement and test halves of
those three are one gap seen from two sides.

IN SCOPE — two cells and two regressions.

1. `LLR-207.detail`, the `governing_identity` clause. It reads "composes
   governing_rev and tree_identity for HEAD or an explicit revision". The
   contract is the BRANCH TIP, and the first argument must be a branch NAME.
   Driven at refresh commit `c16246e0`: under the branch name
   `refresh_attestation` answers `('e2b3cf8a…', 'bar PASS (12 steps, tier
   all)')` and `governing_identity` returns `ce5e2550…`; under `"HEAD"` the
   attestation is `None` and the identity is `2c9a1840…`. Two identities across
   exactly one refresh commit — the cross-refresh disagreement this row exists
   to eliminate. `kitlib/verdict.py:738-740` forbids the word by name and `:50`
   records it as the original defect. Restate the clause as the branch tip or an
   explicit revision, and say that the branch argument is a branch NAME because
   the peel verifies a refresh commit against the branch it names.
2. `LLR-207.detail`, the `governing_rev` clause. It reads "walks across commits
   whose non-record identity equals their first parent's UNTIL IT CAN PEEL a
   verified refresh". That is not the termination condition: a peel `continue`s
   (`verdict.py:467`) and the walk ends at the first commit whose identity
   differs from its parent's (`:473`), or at the absent-parent / `_MAX_GOVERNING_WALK`
   bounds (`:470`, `:398`). Driven at `0e6bad3b`, where `refresh_attestation` is
   `None` and no refresh exists in range: `governing_rev` walks back to
   `d202c9f3` anyway. A builder implementing the sentence returns the tip.
   `IF-175` already states the mechanism correctly ("to reach a refresh it would
   otherwise hide"), so borrow that framing — purpose, not terminus.
3. The multi-log ambiguity rule has no detector. `LLR-207.detail` states "a
   joined key whose logs declare more than one review phase yields no round" and
   `verdict.py:608` implements it (`len(ph) == 1`). No fixture in the repo writes
   TWO session logs at one `(train, ordinal)` — `tests/test_verdict_record.py:401`
   asserts "one session log" and `add_round` writes exactly one per ordinal — and
   relaxing that guard to last-wins leaves the whole suite green (mutation driven
   and reverted, 98 passed). Write the regression: two `docs/iteration/<train>-<ordinal>-*.log`
   files at one key declaring `REVIEW-A` and `REVIEW-B`, asserted to yield NO
   round, beside the single-log arm that does — the fail-closed direction stated
   in the cell.
4. `branch_trailers`' carrier verification has no detector. `LLR-207.detail`
   states it "verifies each carrier against its governing identity" — the
   anti-forgery half of the row's own claim that the trailer "cannot create an
   approval" — and deleting `verdict.py:802-803` also leaves the suite green:
   every fixture commits its trailer on a carrier whose identity already matches,
   so the "words rode onto a tree they do not describe" arm is unexercised
   repo-wide (`branch_trailers`/`format_trailer`/`Review-Verdict` appear in no
   test module but `test_verdict_record.py`). Write the arm: a trailer naming a
   valid governing identity, amended onto or committed with a commit that CHANGED
   the work, asserted absent from `branch_trailers`' answer.
5. `TC-205`'s `Evidence` does not reach `work_tip` or `refresh_attestation`'s
   refusal arms. Both are named in `LLR-207.code_symbol` and described in its
   `detail`, and the `rationale` argues "Separate read-only and reset peels
   protect both contracts" — but the reset-peel contract and every attestation
   refusal (forged trailer, amend, cherry-pick, wrong subject) are driven only in
   `tests/test_integrate_station.py` (`:527`, `:690`, `:755`, `:764`, `:808`,
   `:832`, `:838`, `:964`), which `TC-132` cites for `LLR-140`. Either cite that
   module on `TC-205` and say in the `Method` which arms it holds, or drive the
   two peels' divergence directly in `tests/test_verdict_record.py`. Citing is
   the smaller change and is honest, since the arms genuinely exist.
6. `TC-205.method`'s one factual misstatement of its own driving: it says "a
   changed work blob and a changed `docs/work/` spec each fold DIFFERENT", but at
   `tests/test_verdict_record.py:81-90` only the `src/widget.py` entry is changed
   (`b"00001"` -> `b"00009"`; the spec's synthetic blob is `…0002` and its path
   holds no `00001`) and the second assertion DROPS the spec entry instead.
   Coverage is equivalent in effect because `fold_listing` folds the whole
   `<mode> <type> <sha>\t<path>` line (`verdict.py:256`), so fix the sentence to
   describe the dropped-entry assertion, or change the fixture to match the
   sentence. Do not leave a `Method` claiming an assertion the test does not make.

OUT OF SCOPE — the design. The identity fold, the two-shape peel, the
logged-session join, the declared phase span and the cross-check-not-accept
reading of the trailer are correct as built and were verified against the tree at
`d7ffb413`. Findings 1 and 2 are wording that contradicts the module, not a
mechanism to reopen; findings 3-6 add detectors and correct one sentence. No
change to `kitlib/verdict.py`'s behaviour is asked for by this row.

NOT ON THIS LANE — the approval, and three findings that belong elsewhere. This
lane corrects the text, writes the two regressions and STOPS: `LLR-207` and
`TC-205` stay `Drafted`, nothing under `docs/archive/last_approved/` is written,
and `python project-trajectory/scripts/intake.py snapshot` is not run in any
form — `lane_approval_refusal` refuses any lane merge whose delta touches
`SNAPSHOT_DIR`. The first approval of both rows is the act of the amendment
adjudication this row's own merge mints. Also NOT this lane's, each recorded in
the verdict's closing section with its evidence: `agent_loop.py:317`'s unpinned
duplicate of `verdict.REVIEW_PHASES` with its magic `min(2, ...)` clamp at
`:4170`; `IF-175.requestors` omitting `scripts/score_reviews`, which holds a hard
`from kitlib.verdict import declared_phases` (`score_reviews.py:72`); and
`components.toml`'s `CMP-006` note calling `kitlib/station.py` "the one package
module NOT owned here", stale since `verdict.py` landed at `CMP-008` and stale
before this act rather than because of it.

```toml
title = "Take the withheld first approval of LLR-208 and TC-206 once the snapshot's unscoped refusal is fixed"
workstream = "process"
safety_class = "adjudication"
buildtier = "medium"
priority = 2
specref = "docs/requirements/low-level-requirements.toml"
depends_on = ["WI-584"]
```

VERDICT THIS CONTINUES: the same file, whose `LLR-208` and `TC-206` lines are
`[APPROVE]`. Their text was judged READY and nothing about it is reopened here.
This row exists only because the ACT could not be taken.

WHY IT WAS WITHHELD, in one line so it is not re-derived: the prescribed
`intake.py snapshot --approves` naming only the two registries this act flipped
is REFUSED over 17 absorbed `SR-###` rows in `docs/requirements/system-requirements.toml`,
a registry this act neither judged nor may name — `WI-584`'s observable,
reproduced at `d7ffb413` (ledger: 17 SR / 9 LLR / 4 TC absorbed, no flips). The
verdict file's "approval act is WITHHELD" section records both blocked routes and
why each is closed, including the driven trunk red (`trace.py --approve modified
--check` goes stale with the flips in place, and that step sits in `check.py`'s
`_TRUNK_FRESHNESS_STEPS`).

IN SCOPE — the act and nothing else. Flip `LLR-208.status` and `TC-206.status`
from `Drafted` to `Approved`, every other cell byte-exact, and take
`python project-trajectory/scripts/intake.py snapshot --approves
"docs/requirements/low-level-requirements.toml=<this row>;docs/test/test-cases.toml=<this row>"`
in the SAME reviewed commit. Re-read both rows against the tree first — an
approval is a standing claim and this row's author must own it, not inherit it —
but the findings are already driven and recorded, so this is a confirmation pass
and not a fresh adjudication.

DEPENDS ON `WI-584`. That row rules whether the refusal is scoped to the writer
(reading (a)) or whether a single-registry approval act cannot exist (reading
(b)), and the two answers change this row's step: under (a) the act above
completes as written; under (b) the per-registry rung itself is being rethought
and this row waits for what replaces it. Do not attempt the act before `WI-584`
lands — the refusal is fail-closed and correct to refuse under today's gate.

NOT ON THIS LANE — `LLR-207` and `TC-205`. They return with findings under the
first `## Dispositions` draft above and are a different lane's business; this row
must not flip them, and a batch that flips all four would bless text this
verdict returned.
