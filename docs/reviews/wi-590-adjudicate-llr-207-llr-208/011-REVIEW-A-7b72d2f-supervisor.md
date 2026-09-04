# WI-590 REVIEW-A — round 011, tree 7b72d2fd

Model: claude-opus-5 (supervisor-drawn). Base trunk `e410d030` (= this lane's
merge base; the lane is fully refreshed).

Scope: `git -C <lane> diff e410d030...HEAD -- . ':!docs/reviews' ':!docs/log.d'
':!docs/iteration'` — 13 files, of which PROJECT_STATE.html, docs/stage,
docs/status.md, docs/ratify/CURRENT.md and docs/open-items.html are generated
and noted, not read for bytes. Product content: the approval act (LLR-208 and
TC-206 `Drafted` -> `Approved` plus the whole-file anchoring copy, `a1d80c6f`)
and the adjudication spec moved to `docs/work/complete/` carrying TWO
`## Dispositions` drafts.

Worst failure classes hunted, in order: (1) an Approved+anchored spine cell that
is FALSE against its own module — the same defect this lane returned LLR-207
for; (2) a debt that vanishes with the whole-file copy; (3) a draft that will not
mint, or mints a successor whose remedy cannot be executed.

## Instruments (each run once, on the lane worktree unless said otherwise)

- `gen_verdict_rollup.py --root .` (write arm, on the lane branch) →
  `REFUSED — wi-590-… is a work branch (trunk is contract_split) …`, exit 2;
  `git status --porcelain` empty before AND after. `--check` → `fresh (46 review
  scope(s))`, exit 0. Round 005's measured write is genuinely closed.
- `_off_trunk_refusal` read at `gen_verdict_rollup.py:225-248`; the single
  bypass is the `--trunk-step` flag, whose only caller is
  `trunk_step.py:589-591` (`_cmd("gen_verdict_rollup.py", "--trunk-step")`), and
  `tests/test_verdict_record.py::test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`
  → `1 passed in 0.73s`. No other write path found (grep over scripts/ci).
- `baseline_snapshot.refresh_ledger` at the merge base `e410d030`: absorbed =
  10 LLR (045, 058, 136, 140, 144, 158, 197, 198, 203, 204) + 4 TC (082, 138,
  147, 194), `flips=[]` — exactly draft 2's set. On the lane tree those two
  registries read `absorbed=0`, i.e. the copy did absorb them. (SR ×17 and
  CMP-006 ×1 also drift at the base but their registries were not named by the
  act and were not copied — correctly outside draft 2's scope.)
- Attribution re-derived independently by grepping `docs/reviews/` for
  `- [MEANING|CLARITY|APPROVE|RETURN] <id>` — WI-585: LLR-045, LLR-140, TC-082;
  WI-566: LLR-058, LLR-144, LLR-198, TC-138, TC-147, TC-194; WI-573: LLR-136,
  LLR-158; WI-578: LLR-158, LLR-203, LLR-204; LLR-197 has ZERO hits. 13 judged,
  1 unjudged — draft 2's ledger is honest row for row. `WI-593` exists at
  `docs/work/queued/WI-593-adjudicate-llr-197-approved.md`, `adjudicates`
  LLR-197, minted at `09193fea`; the reword landed at `8d751573` inside merge
  `14beba0a`.
- `intake.parse_dispositions` on the spec → `refusal=None`, **2** drafts,
  `kind='spine'` / `kind='ordinary'`, no unknown keys, both `specref` paths
  exist. `_mint_shape_refusal` → `None` for both; `schedule.classify` →
  `('exclusive',0)` and `('parallel',6)`.
- REAL MINT DRIVEN, not read: cloned the repo to scratch, merged this lane onto
  `contract_split` (`e410d030` → `ba251452`) and ran
  `intake.intake_after_merge(root, e410d030, HEAD, outcomes={'WI-590':'merged'})`
  → `refusal=None`, minted `WI-595-llr-207-tc-205-return-governi.md` and
  `WI-596-the-anchoring-copy-s-absorb-le.md`, committed as `81bb2a84`. Both
  files well-formed; draft 2's remedy targets verified to exist
  (`adjudicate_brief.py:788` renders `{approves_rows}`,
  `prompts/adjudicate-first-approval.template.md:92` consumes it, step 2 does
  carry the quoted "stay `Drafted` inside it", `scripts/acceptance_record.py`
  exists). Observation, not a finding: both draft titles exceed 120 chars (210
  and 155); no check enforces a title cap, so nothing reds.
- `check.py --jobs 0` on the lane → `RESULT: PASS` (derived-stage /
  approval-fresh / verdict-rollup SKIP as trunk-owned on a work branch);
  `trace.py --strict-integrity` → `SN=27 SR=76 LLR=191 TC=190 orphans=0
  integrity=0 … interface-findings=0 paraphrase-advisories=3`. On the MERGED
  clone all twelve steps PASS, including `approval-fresh` and
  `approval-immutable`.
- Scope: `git diff e410d030...HEAD -- docs/requirements docs/test` is exactly
  two lines, `status = "Drafted"` → `"Approved"` at
  `low-level-requirements.toml:2202` (LLR-208) and `test-cases.toml:2099`
  (TC-206) — nothing else. Only `a1d80c6f` touches
  `docs/archive/last_approved/`. The mechanical close `f0528530` is a single
  `R094` rename inside `docs/work/`. `git diff --name-only e410d030...HEAD`
  outside `docs/` is `PROJECT_STATE.html` alone — no product code on this lane;
  the rollup guard arrived through the refresh `7b72d2fd`, as draft 2 states.

## Findings

- [MAJOR] docs/requirements/low-level-requirements.toml:2199 -> LLR-208 was flipped to `Approved` and anchored, but at THIS tree its `Detail` is false against its own module: it asserts that trunk-regen-set membership "is the only thing that makes the exclusive-writer clause above true", and since `7ea3cce7` (in this tree via the refresh) `_off_trunk_refusal` (`gen_verdict_rollup.py:225-248`) is a SECOND, independent mechanism that makes it true — the one that actually refuses a work-branch write, which the cell never requires at all. `code_symbol` (`:2198`, `scopes/render/targets/_extra/main`) omits `_off_trunk_refusal`, TC-206's `Method` (`docs/test/test-cases.toml:2094`) describes only the freshness "work-branch stand-down set" and its `Evidence` (`:2098`) cites five tests, none of them `test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`; grep across every requirements and test registry returns ZERO rows naming the refusal or that test. This is the identical defect class the lane's own round-004/006/009 verdicts returned LLR-207 for — a shipped mechanism whose only possible home is silent about it — except that here the record is now BLESSED and copied whole into `docs/archive/last_approved/`, and neither `## Dispositions` draft carries it: draft 2 closes round 005's MAJOR by pointing at the code fix and never asks whether the approved row still describes the module -> draft a third `## Dispositions` block (or widen draft 1's IN SCOPE list) for LLR-208 `Detail` + `code_symbol` and TC-206 `Method` + `Evidence`, so the successor states the off-trunk refusal as part of the contract and cites its shipped test; this is a record correction, not a new guard, so no unrepresentable-state clause is owed -> @owner
- [MINOR] docs/work/complete/WI-590-adjudicate-llr-207-llr-208.md:53 -> draft 1's stated ground for bundling LLR-207 with TC-205 — "`staged_drafted_rows` queues an approver only for rows a delta actually amends — a successor that edited `TC-205` alone would leave `LLR-207` with no queued approver" — is stale at this tree: `docs/work/queued/WI-594-adjudicate-llr-207-llr-208.md` (minted on the trunk at `09193fea`, arrived via the refresh) already queues a first-approval approver whose `adjudicates` is `["LLR-207","LLR-208","LLR-209","TC-205","TC-206","TC-207"]`. Neither draft names it, so after this merge two live rows own the same pair with no ordering between them (WI-595 fixes the cells, WI-594 judges them) and the scheduler may run WI-594 first and produce a fourth return on unchanged text — the runaway this lane just came out of; WI-594 also still lists LLR-208/TC-206, which this act has now Approved -> name WI-594 in draft 1's scope prose, stating that its LLR-208/TC-206 half is discharged by `a1d80c6f` and that its LLR-207/TC-205 half must not be read before the successor's edit lands, so the coordinator has the ordering in the file rather than in this review -> @owner

VERDICT: CHANGES-REQUESTED findings=2
