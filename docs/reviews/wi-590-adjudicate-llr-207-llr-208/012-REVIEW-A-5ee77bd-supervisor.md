# WI-590 REVIEW-A — round 012, tree `5ee77bdf`

Model: claude-opus-5 (supervisor-drawn). Base trunk `e410d030` (= this lane's
merge base).

Scope: `git -C <lane> diff e410d030...HEAD -- . ':!docs/reviews' ':!docs/log.d'
':!docs/iteration'` — 13 files, of which PROJECT_STATE.html, docs/stage,
docs/status.md, docs/ratify/CURRENT.md and docs/open-items.html are generated
and noted, not read for bytes. Product content: the approval act `a1d80c6f`
(LLR-208 + TC-206 `Drafted` -> `Approved` with the whole-file anchoring copy)
and the mechanically closed adjudication spec carrying TWO `## Dispositions`
drafts.

Worst failure classes hunted, in order: (1) a remedy that reads correct on the
page but cannot execute in the order the scheduler will actually run it;
(2) an Approved+anchored cell still false against its module (round 011's
MAJOR); (3) a draft that will not mint or mints a wrong successor.

## Instruments (each run once)

- `intake.parse_dispositions` on the spec -> `refusal=None`, **2** drafts,
  `kind='spine'` (with `needs=['WI-594']`, `bar='DevStg-Tests'`, priority 2) and
  `kind='ordinary'`; `_mint_shape_refusal` -> `None` for both.
- REAL MINT DRIVEN: scratch clone, merged the lane onto `contract_split`
  (`e410d030` -> `d47a56b6`), `intake.intake_after_merge(root, e410d030,
  d47a56b6, outcomes={'WI-590':'merged'})` -> `refusal=None`, minted
  **WI-595** `docs/work/queued/WI-595-llr-207-tc-205-return-and-llr.md` and
  **WI-596** `.../WI-596-the-anchoring-copy-s-absorb-le.md` (commit `3aa84e20`).
  WI-595 carries `needs = ["WI-594"]` and `safety_class = "spine"`; both draft
  prose blocks ride verbatim into the minted `## Context`.
- `integrate._approval_act_refusal(root, 'wi-590-…')` at the pre-merge state ->
  `None`: the act survives the mechanical close that drained `active/`.
- `schedule.py --root . ready --explain` on the merged+minted tree ->
  `WI-595 waiting ['waiting:hard-preds-not-done:WI-594']`,
  `WI-594 ready ['exclusive:adjudication','ready']`. The `needs` edge is a real
  ordering mechanism — and it orders WI-594 FIRST (finding 1).
- `adjudicate_brief.first_approval_values` for **WI-594** on that same merged
  tree -> `refusal=None`; chain renders `LLR-207 [AWAITING FIRST APPROVAL]`,
  `TC-205 [AWAITING FIRST APPROVAL]`, `LLR-209`, `TC-207`; LLR-208/TC-206
  correctly DROP (no longer `Drafted`); `registries` =
  `…low-level-requirements.toml=WI-594;…test-cases.toml=WI-594`, `approves_rows`
  covers `LLR-207, LLR-209` / `TC-205, TC-207`.
- Cell classification re-derived: `SPINE_APPROVED_CELLS` has LLR `Detail` and TC
  `Method`, so draft 1's prescribed edits DO fire `staged_spine_amendments` ->
  intake trigger (a); `CodeSymbol`/`Evidence` are traced-silent and ride along.
  The amendment classification in draft 1 is correct.
- `gen_verdict_rollup.py --root .` on the lane -> `REFUSED — … is a work branch
  (trunk is contract_split) …`, exit 2; `git status --porcelain` EMPTY before and
  after. Sole `--trunk-step` caller is `trunk_step.py:591`; the cited test exists
  at `tests/test_verdict_record.py:1381`. `7ea3cce7` is an ancestor of both the
  trunk base and the lane tip.
- `baseline_snapshot.refresh_ledger` at `e410d030`: LLR = 045, 058, 136, 140,
  144, 158, 197, 198, 203, 204; TC = 082, 138, 147, 194; `flips=[]` — exactly
  draft 2's 10+4 set. Attribution re-derived independently by grepping
  `docs/reviews/` for `- [MEANING|CLARITY|APPROVE|RETURN] <id>`: WI-585 ->
  LLR-045/LLR-140/TC-082; WI-566 -> LLR-058/LLR-144/LLR-198/TC-138/TC-147/TC-194;
  WI-573 -> LLR-136/LLR-158; WI-578 -> LLR-158/LLR-203/LLR-204; LLR-197 ZERO
  hits. Draft 2's ledger is honest row for row; `WI-593` and `WI-594` exist in
  `docs/work/queued/`, both minted at `09193fea`.
- `check.py --jobs 0` on the merged+minted clone -> `RESULT: PASS`, all twelve
  steps including `approval-fresh` and `approval-immutable`;
  `Traceability: SN=27 SR=76 LLR=191 TC=190 orphans=0 integrity=0 …
  interface-findings=0 paraphrase-advisories=3`.
- Scope: `git diff e410d030...HEAD -- docs/requirements docs/test` is exactly two
  lines (`status = "Drafted"` -> `"Approved"`); only `a1d80c6f` touches
  `docs/archive/last_approved/`; the mechanical close `f0528530` touches one file
  under `docs/work/`; the only non-`docs/` path is `PROJECT_STATE.html` — no
  product code on the lane. `WI-590` is scrubbed from `docs/status.md`.
  Draft titles: 113 chars (draft 1) and 155 (draft 2, the known unenforced WARN).
- Round 011's MAJOR HAS A REAL REMEDY: LLR-208's live `detail`
  (`low-level-requirements.toml:2199`) still reads "it is the only thing that
  makes the exclusive-writer clause above true", `code_symbol` still omits
  `_off_trunk_refusal`, TC-206's `evidence` still cites five tests and not the
  refusal test — and draft 1 now names all four cells, the symbol and the test by
  path. Verified accurate against the tree.

## Findings

- [MAJOR] docs/work/complete/WI-590-adjudicate-llr-207-llr-208.md:53 -> the ORDERING paragraph is false where it is load-bearing, and the mechanism it declares points the wrong way. It claims WI-594 "finds returned and Drafted with this row queued as their next author — and cannot produce a fourth return on unchanged text". Driven on the post-merge tree: `schedule` makes WI-594 `ready` and WI-595 `waiting`, so WI-594 runs FIRST on unchanged text, and `adjudicate_brief.first_approval_values(WI-594)` composes `LLR-207 [AWAITING FIRST APPROVAL]` / `TC-205 [AWAITING FIRST APPROVAL]` — this session's to flip — with a `--approves` argument covering both; the composed brief carries NO prior verdict, no mention of WI-590's three returns and no mention of WI-595 (the first-approval template's only not-yours labels are HELD-for-owner and another-act's-row, and the row is squarely in WI-594's own `Adjudicates`). So both open branches are bad: WI-594 APPROVES the text this lane returned three times, blessing and whole-file anchoring it (the exact failure class rounds 004/006/009 exist for) and silently re-classifying WI-595's planned Drafted edits as Approved-cell amendments its scope never states; or it RETURNS and mints a second successor over the same cells with no edge to WI-595 — the runaway. Round 011's MINOR asked for the OPPOSITE order ("its LLR-207/TC-205 half must not be read before the successor's edit lands"); this rework inverted it and covered the inversion with an unsupported safety sentence -> re-point the edge trunk-side instead: put `needs = ["WI-595"]` on `docs/work/queued/WI-594-adjudicate-llr-207-llr-208.md` (or narrow its `Adjudicates` to `LLR-209`/`TC-207`, since LLR-207/TC-205's judgement is precisely what the successor is being built to make judgeable) and delete the "cannot produce a fourth return" claim; if the drafted direction must stand instead, replace the sentence with what is true — WI-594 is shown these rows as its own with none of this history — and state which WI-594 outcome the successor assumes and what re-scopes it under the other. This adds no guard, so no unrepresentable-state clause is owed for the re-point; naming why the defect stays representable at all: the first-approval brief has no vocabulary for "already returned, successor queued", and giving it one (deriving that from the row's own verdict history at composition rather than trusting a disposition's prose) is a mint/brief change well outside this diff -> @owner
- [MINOR] docs/work/complete/WI-590-adjudicate-llr-207-llr-208.md:77 -> for clarity: the bundling ground kept verbatim from the pre-rework draft — "`staged_drafted_rows` queues an approver only for rows a delta actually amends — a successor that edited `TC-205` alone would leave `LLR-207` with no queued approver" — now contradicts the paragraph 20 lines above it in the same draft, which states that WI-594 already queues a first-approval approver for both rows. A reader cannot tell which of the two the draft means, and this text ships verbatim into WI-595's `## Context` -> restate the ground as the post-WI-594 world ("once WI-594 has ruled, a delta that amended TC-205 alone would leave LLR-207 with no NEW approver queued"), or drop it and rest the bundling on the first clause, which stands on its own -> @owner

VERDICT: CHANGES-REQUESTED findings=2
