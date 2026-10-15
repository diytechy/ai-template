## 2026-10-15 (b) — attended coordinator: the plan gate landed

The fifth attended coordinator session under the review-churn program
(handoff-2026-10-15-attended-coordinator). It took WI-913, the plan gate,
from its checkpoint to its landing, the program's first mechanism change on
trunk.

- **WI-913, the plan gate** (landed as `b803dd019`; lane tips `d37b223df`
  and pre-rebase `b9de474d7` archived in `archive/lanes`):
  - **Rebase** onto `2025f8419` before the checkpoint; only the watermark
    conflicted (trunk's file, then `--bump-ids`).
  - **Checkpoint prep** (`3c4f079b6`): the spec's S3 list and the
    plan-decomposition rubric's coverage sentence, coordinator text; D-007.
  - **Terra's reconcile** (`76dc6746a`), from the spine change list's round
    sections, approved cells amended by addition and checked cell by cell
    against trunk. A coordinator check before the sitting found two
    obligations the tests expect but no requirement stated (a tick does not
    unbind; the second critique never meets the first verdict), which a
    second Terra turn added.
  - **Sitting 010** (combined): LLR-313 and TC-333 re-attested (act 113),
    LLR-337 and TC-367 approved (act 114), SR-154 returned (an acceptance
    clause its requirement never states; the obligation form). An advisory
    corrected TC-333's tier to Full by TC-205's rule.
  - **Owner ruling, in session:** the disposition's "shall refuse" would
    give SR-154 a second `shall`, which `trace.py --strict` reports and the
    Done-when forbids. The owner chose one `shall`, the approved sentence
    reordered so its unattended condition scopes only the routing predicate,
    over a separate SR or a waiver (D-008).
  - **Sitting 011** re-attested SR-154 and TC-333 (act 115).
  - **The uncounted post-checkpoint gate** (`012`–`014`): Sol, Fable and
    Opus all APPROVE, MINORs only (D-010). Its reading exclusion was
    extended to the lane's decisions record (D-009).
  - **Landing:** squash, RESYNC entry re-anchored at `2025f8419`, the sweep
    minted WI-919 (closed as already settled, `4cdbe977a`) and WI-920
    (TC-055's declared-trigger re-judge, queued as real work).
- **Trial tally, the gate:** Sol 1 MINOR (unique); Fable 3 MINOR (1
  unique); Opus 2 MINOR (both shared with Fable).
- **Drafted, not filed** (coordinator-2026-10-15 D-001): the hook-floor row
  for `done-when-blessed`, and D-006's landing-shapes successor.
- **Bar at landing:** smoke 2588 passed, 2 skipped (38.3 s; budget 35.8 s
  of 60); `check_trajectory --strict` clean; `trace.py --strict` only
  LLR-292's known finding.
