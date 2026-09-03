# WI-586 REVIEW-A round 012 — 51fb3e8

Independent review of `git diff contract_split...HEAD` (excluding records and
generated artifacts). Reading scope resolves to ONE work file:
`docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md`
(+219). No code, test or registry file is touched by this lane.

## Worst failure classes this change admits, hunted first

1. **Silent wrong content in a disposition** — a factual claim about the tree
   that is false sends a successor lane to fix a non-defect, or leaves a real
   one. Every measured claim was re-driven below.
2. **A disposition that cannot land** — a block that will not parse, or a
   remedy the lane rung refuses, drops a ruled follow-up at the mint.
3. **Fail-open on the act** — the lane performing the approval it is only
   allowed to draft.

## Instruments, run here

- `python project-trajectory/scripts/check.py --jobs 0` →
  `RESULT: PASS` (`registry-integrity`, `vocabulary`, `need-form`, `privacy`,
  `doc-navigability`, `skills-index`, `prompt-catalog`, `staged-divergence`,
  `approval-immutable` PASS; `derived-stage`/`approval-fresh`/`verdict-rollup`
  SKIP as trunk-owned on a work branch).
- `python project-trajectory/scripts/trace.py --strict-integrity` →
  `Traceability: SN=27 SR=76 LLR=190 TC=189 orphans=2 integrity=0 ... provenance-findings=1`
  (the one provenance finding is the pre-existing `LLR-197` Detail `WI-448`
  citation, untouched by this diff).

## Done-when mapping (the `## Context` Outcomes contract)

- *RETURN with findings over the adjudicated set* — COVERED. `adjudicates`
  lists LLR-207/LLR-208/TC-205/TC-206; draft 1 scopes LLR-207+TC-205, draft 2
  scopes LLR-208+TC-206. All four dispositioned, none orphaned.
- *Follow-up drafted in a `## Dispositions` section of THIS spec* — COVERED,
  driven through the shipped reader rather than read: `intake.parse_dispositions`
  on the real file returns `refusal=None`, `3` drafts, each `kind='spine'`,
  `bar='DevStg-Tests'`, with `scope` prose correctly aligned to its own block
  (8183 / 2884 / 1746 chars, each opening `VERDICT THIS CONTINUES:`).
- *The approval act is NOT this lane's* — COVERED. `ac.lane_approval_refusal(".", "contract_split", "HEAD")`
  → `None`; `ac.staged_drafted_rows(...)` → `[]`; the delta touches no path
  under `docs/archive/last_approved`, `docs/requirements` or `docs/test`. The
  four rows are still `Drafted`, matching both "NOT ON THIS LANE" paragraphs.

## Re-driven evidence (nothing below is inherited from the spec's own text)

Baseline over the three cited modules: `134 passed in 67.63s` — the number the
spec's mutation arms are measured against.

- Draft 1 finding 3 (multi-log ambiguity has no detector): relaxed
  `verdict.py:608` to `sorted(ph)[-1] ... if ph` → `134 passed in 68.87s`.
  CONFIRMED: the fail-closed guard is unexercised.
- Draft 1 finding 4 (`branch_trailers` carrier verification has no detector):
  deleted `verdict.py:802-803` → `134 passed in 69.37s`. CONFIRMED.
- Draft 2 (the trunk regen step is unasserted): deleted the
  `("verdict-rollup", _has("docs/reviews"), _cmd("gen_verdict_rollup.py"), "docs/reviews/ absent")`
  tuple from `trunk_step.py:588-593` → `0` `verdict-rollup` occurrences remain,
  and `tests/test_trunk_step.py` plus all four TC-206 evidence nodes give
  `20 passed in 2.80s`. CONFIRMED, and the `27 -> 20` correction this round
  makes is the honest number. Working tree restored (`git status --porcelain`
  empty) after each arm.
- Draft 1 findings 1/2 (Detail contradicts the module): `governing_rev` seats
  `rev = rev or branch` and its docstring says "`rev` (default: the tip)";
  `governing_identity`'s says "`rev` defaults to the branch tip";
  `format_branch_trailer` forbids `HEAD` by name at `:738-740`. A peel at
  `:465` re-seats and `continue`s — it does not terminate; the walk ends at
  `:473` (identity differs), `:470` (absent parent) or `_MAX_GOVERNING_WALK`
  (`:398`). Every line citation in the spec is byte-exact.
- Draft 1 finding 5: `work_tip` occurs 0 times in `tests/test_verdict_record.py`;
  `refresh_attestation` appears there only as the positive assertion at `:608`;
  the 26 reset-peel/refusal occurrences are all in `tests/test_integrate_station.py`,
  which TC-205 does not cite and TC-132 does. The named refusal arms genuinely
  exist there (`test_a_forged_bar_green_trailer_...`,
  `test_amending_a_refresh_commit_revokes_its_attestation`,
  `test_a_work_commit_that_quotes_the_trailer_is_never_peeled_away`), so the
  "citing is the smaller change and is honest" recommendation holds. The
  Smoke/`SLOW_MODULES` parenthetical also holds: `test_integrate_admission` is
  already both, and `docs/registry-machinery-reference.md:359`/§12.2 records the
  Tier/marker split as deliberate.
- Draft 1 finding 6: `_listing` numbers blobs `{:040x}` at `:60-64`, so only
  `src/widget.py`'s sha contains `00001`; the second assertion at `:89` compares
  against `_listing("src/widget.py")`, which DROPS the spec entry. The
  `Method`'s "each fold DIFFERENT" is a misstatement of its own fixture.
  CONFIRMED.
- Draft 1 finding 7: `CMP-006.notes` still reads "kitlib/station.py (LLR-182) is
  the one package module NOT owned here: it stays CMP-008", while
  `LLR-207.component = "CMP-008"` with `module = ".../kitlib/verdict.py"`. The
  sentence is falsified BY this row, so re-pointing it in-lane is right; and
  `lane_approval_refusal`'s own docstring permits a lane to AMEND "cell text on
  any such row, including approved ones", so the remedy can land.
- Draft 2's stranding argument: `staged_drafted_rows`' docstring is explicit —
  "Every `Drafted` spine row a delta ADDS or AMENDS" — so a successor that
  edited TC-206 alone would leave LLR-208 with no queued approver. The demand to
  amend `LLR-208.detail` is load-bearing, not decorative.
- Draft 3: `agent_loop.py:317` is a byte-identical duplicate of
  `verdict.py:157`; `_clamped_review_rounds` at `:4163-4170` returns
  `max(0, min(2, rp_int))`. `IF-175.requestors` omits `scripts/score_reviews`
  while `score_reviews.py:72` imports `declared_phases` and calls it at `:429`.
  Both defects CONFIRMED.

I tried to break this and could not, on the material that governs a successor's
work. One wording point remains.

## Findings

- [MINOR] docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md:246 -> for clarity: draft 3's second defect justifies itself with IF-175's sentence "a second reader of round evidence anywhere else is a finding against this row", but `score_reviews.py` reads `declared_phases` — the phase span, not round evidence — which the very next sentence of the draft concedes; the quoted clause therefore does not establish the omission, and a successor could read "a finding against this row" as licensing REMOVAL of the legitimate import rather than addition of the requestor -> rest the finding on the requestors-completeness rule instead (a hard `from kitlib.verdict import ...` that no `requestors` entry names is an undeclared seam), and keep the quoted round-evidence clause only where the draft already uses it correctly, in the "so the addition does not read as a fourth reader" remedy -> @owner

VERDICT: APPROVE findings=1
