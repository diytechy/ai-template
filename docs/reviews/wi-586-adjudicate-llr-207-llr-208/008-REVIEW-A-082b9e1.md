# REVIEW-A — WI-586 adjudicate LLR-207/LLR-208/TC-205/TC-206 @ 082b9e1

Scope read: `git diff contract_split...HEAD` minus records — one file,
`docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md`
(+148, a `## Dispositions` section drafting two follow-ups). No registry, no
`docs/archive/last_approved/`, no code. All four adjudicated rows verified still
`Status = Drafted`, so the RETURN performed no approval act and
`lane_approval_refusal` has nothing to refuse.

Worst failure classes this change admits, hunted in this order: (1) the drafted
prose rides VERBATIM into a minted WI's Context and is its spec-of-record, so a
false or under-scoped claim silently becomes a builder's instruction — silent
wrong content; (2) a `## Dispositions` block that will not mint drops a ruled
follow-up on the floor with nobody watching — fail-open/data loss; (3) a RETURN
whose continuation cannot reach approval strands a row below the gate forever.

## Instruments, run here

- `python project-trajectory/scripts/check.py --jobs 0` (via `.venv/bin/python`;
  bare `python` is not on PATH on this box) — `RESULT: PASS`; summary block:
  `PASS registry-integrity 2.3s / SKIP derived-stage (work branch) / PASS
  vocabulary / PASS need-form / PASS privacy / PASS doc-navigability / SKIP
  approval-fresh (work branch) / PASS skills-index / PASS prompt-catalog / SKIP
  verdict-rollup (work branch) / PASS staged-divergence / PASS
  approval-immutable`.
- `python project-trajectory/scripts/trace.py --strict-integrity` — final line:
  `Traceability: SN=27 SR=76 LLR=190 TC=189 orphans=2 integrity=0 ...
  provenance-findings=1 paraphrase-advisories=3. Report -> docs/test/report.md`
  (the one provenance finding is LLR-197, pre-existing, not this diff).

## Shipped code paths driven

- `intake.parse_dispositions` on the real spec: `REFUSAL: None`, `N DRAFTS: 2`,
  both carrying `kind='spine'`, `bar='DevStg-Tests'`, `priority=2` — every key
  inside `_DRAFT_KEYS`, `spine` inside `schedule.SAFETY_CLASSES`, `DevStg-Tests`
  inside `WI_BARS`. Failure class (2) is closed: both drafts mint.
- Every `LLR-207.code_symbol` symbol resolves in `kitlib/verdict.py`
  (`MISSING: []`); `LLR-208`'s five resolve in `gen_verdict_rollup.py`.
  `RECORD_PREFIXES` matches the Detail's three directories.
- Findings 1–2 re-driven against the module: `verdict.py:738-740` forbids `HEAD`
  by name ("`branch` must therefore be the lane's BRANCH NAME and not `HEAD`"),
  `:50` records it as the original defect; `governing_rev` `continue`s on a peel
  (`:467`) and terminates at `:473`/`:470`/`_MAX_GOVERNING_WALK` (`:398`). Both
  cells do contradict the module. `IF-175` does carry the borrowed phrase "to
  reach a refresh it would otherwise hide".
- Finding 3 mutation re-driven, not inherited: `logged_rounds`' `len(ph) == 1`
  relaxed to last-wins → `134 passed` across
  `test_verdict_record.py test_integrate_admission.py test_integrate_station.py`.
  Reverted; guard is genuinely undetected.
- Finding 4 mutation re-driven: `verdict.py:802-803` (the carrier check) deleted
  → `134 passed` over the same three modules. Reverted. Undetected.
- Finding 5 re-driven: `refresh_attestation` appears in `test_verdict_record.py`
  only at `:608` as a POSITIVE assertion; every refusal arm and both `_work_tip`
  peel arms are at the eight cited `test_integrate_station.py` lines, a module
  `TC-205.evidence` does not cite. (Checked and dismissed: citing that slow-tier
  module beside `TC-205`'s `Tier = Smoke` is NOT a new contradiction —
  `test_integrate_admission` is already in `conftest.SLOW_MODULES` and already
  cited, and `docs/registry-machinery-reference.md` §12.2 records `TC.Tier` and
  the pytest marker as deliberately unreconciled. No finding.)
- Finding 6 re-driven at `tests/test_verdict_record.py:81-90`: `changed_code`
  replaces `b"00001"` across both entries, but the spec entry's blob is `…0002`
  and its path holds no `00001`, so only `src/widget.py` moves; the second
  assertion compares against `_listing("src/widget.py")`, which DROPS the spec
  entry. `TC-205.method` does misstate its own driving.
- Draft 2's mutation re-driven: the `verdict-rollup` row deleted from
  `trunk_step.REGEN_STEPS` → `27 passed` covering all four of `TC-206`'s cited
  evidence nodes plus the whole of `tests/test_trunk_step.py`. Reverted. The
  wiring is genuinely unasserted; `16 tests collected` in `test_trunk_step.py`
  matches the draft's stated count exactly.
- The three "NOT ON THIS LANE" observations all verify: `agent_loop.py:317`
  duplicates `REVIEW_PHASES` and `:4170` clamps `min(2, rp_int)`;
  `IF-175.requestors` is `['scripts/integrate', 'scripts/agent_loop',
  'scripts/gen_verdict_rollup']` while `score_reviews.py:72` holds
  `from kitlib.verdict import declared_phases`; `CMP-006`'s note still calls
  `kitlib/station.py` "the one package module NOT owned here" while `LLR-207`
  places `verdict.py` at `CMP-008`.

## Outcome contract, mapped

The spec's `## Context` states the Done-when as APPROVE-or-RETURN. RETURN taken;
findings recorded; follow-up drafted in `## Dispositions` and proven mintable;
rows left `Drafted`; no snapshot. Covered — EXCEPT the continuation reaching all
four rows, which is finding 1 below and is UNCOVERED for `LLR-208`.

## Findings

- [BLOCKER] docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md:163 -> Draft 2's header claims "the two registry cells it corrects" but its enumerated remedy directs edits to `TC-206` ONLY ("cite it from `TC-206`, and state that arm in the test's `Method`"), while explicitly holding `LLR-208.detail` true-as-written; the first-approval mint is delta-driven off `acceptance_record.staged_drafted_rows` with no sweep over untouched Drafted rows, so a builder following the remedy literally strands `LLR-208`. Driven in a throwaway worktree: a commit amending only `TC-206.Evidence` yields `ROWS THE MINT WOULD SEE: TC-206 amended ['Evidence'] / LLR-208 present? False`, whereas the same simulation of draft 1 yields `[('LLR-207','amended',['Detail']), ('TC-205','amended',['Method'])]` — so the defect is specific to draft 2, not a property of the mechanism. `LLR-208` then has no queued approver, and `acceptance_record.adjudication_approval_refusal`'s `outside = [act for act in acts if act["id"] not in scope]` would REFUSE a later adjudication scoped to `TC-206` that tried to flip it anyway; WI-586 closes here, so nothing re-queues it -> amend draft 2's IN SCOPE paragraph to name `LLR-208.detail` as a cell the successor must edit (a Detail sentence stating the wiring the new regression now holds is the honest edit), so the successor's merge re-presents BOTH rows to the mint -> @owner. This adds no guard, so no antidote clause is owed; noting only that the stranding is representable because the trigger reads one merge's delta and no sweep asks "is any Drafted row live with no adjudication naming it" — making it unrepresentable is a change to `intake._released_drafted_rows`' trigger, well outside this diff's scope (the `antidote` skill's "smallest change that makes this fix unnecessary", which I cite rather than restate).
- [MAJOR] docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md:134 -> Three verified live defects (`agent_loop`'s unpinned `REVIEW_PHASES` duplicate + `min(2, …)` clamp; `IF-175.requestors` omitting `scripts/score_reviews`, which `IF-175`'s own notes call "a finding against this row"; `CMP-006`'s stale "the one package module NOT owned here") are recorded ONLY "in the verdict's closing section" — a file under `docs/reviews/`, which `gen_verdict_rollup` reads for ordinal/phase/sha/finding-COUNT and never for content, and which no minter reads at all; so three confirmed defects are parked where nothing will ever pick them up, while the adjudicator already holds the zero-cost mechanism it used twice on this same page -> add a third ```toml disposition block (or an OI) carrying these three with the evidence already written, so the return queues them instead of narrating them -> @owner.
- [MINOR] docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md:86 -> for clarity: finding 3 states the last-wins mutation "leaves the whole suite green (mutation driven and reverted, 98 passed)", but 98 is `test_verdict_record.py` (51) + `test_integrate_admission.py` (47), not the whole suite (~1000+); a builder re-driving "the whole suite" gets a different number and may read the claim as mis-stated and drop the regression. The substance holds — I measured `134 passed` over those two plus `test_integrate_station.py` -> name the two modules the number covers instead of "the whole suite" -> @owner.

VERDICT: CHANGES-REQUESTED findings=3
