# WI-590 — REVIEW-A round 013 (supervisor-drawn independent reviewer)

- train: `wi-590-adjudicate-llr-207-llr-208`
- tree: `98908416` (merge-base with trunk `e410d030`; trunk now `bfe2bda7`)
- model: claude-opus-5 (supervisor-drawn)
- scope: `git -C <lane> diff e410d030...HEAD -- . ':!docs/reviews' ':!docs/log.d' ':!docs/iteration'`
  (generated artifacts — PROJECT_STATE.html, docs/open-items.html, docs/stage,
  docs/ratify/CURRENT.md, docs/log.md — noted, not reviewed)

## Instruments driven

1. `adjudicate_brief.first_approval_values` for WI-594 on a scratch clone of trunk
   `bfe2bda7` merged with the lane (`4b5db0eb`) -> `WHY: None`, `ADJUDICATES:
   'LLR-209;TC-207'`; the rendered brief contains LLR-209 x5 and TC-207 x5 and
   **zero** occurrences of LLR-207 / TC-205 / LLR-208 / TC-206. `approves_rows`
   names only LLR-209 and TC-207. Overlap gone.
2. `grep -rn adjudicates docs/work/queued/` on trunk -> only
   `WI-594-adjudicate-llr-209-tc-207.md:9: adjudicates = ["LLR-209", "TC-207"]`
   (plus a prose mention in WI-583). `grep -rl 'LLR-207\|TC-205'
   docs/work/queued/` -> only WI-594's NARROWED explanatory paragraph, which
   states those four rows are WI-590's. WI-593's title covers LLR-197 only.
3. `intake.parse_dispositions` on the closed spec -> `DRAFTS: 2 REFUSAL: None`.
4. `intake.intake_after_merge(root, "bfe2bda7", "4b5db0eb", outcomes={"WI-590":
   "merged"})` on the merged clone -> `REFUSAL: None`; minted **WI-595**
   (`docs/work/queued/WI-595-llr-207-tc-205-return-and-llr.md`, no `needs`) and
   **WI-596** (`docs/work/queued/WI-596-the-anchoring-copy-s-absorb-le.md`). No
   third row minted for the lane's own flip — the act stays the lane's.
5. `check.py --jobs 0` on that merged+minted tree -> `RESULT: PASS`
   (registry-integrity, derived-stage, vocabulary, need-form, privacy,
   doc-navigability, approval-fresh, skills-index, prompt-catalog,
   verdict-rollup, staged-divergence, approval-immutable all PASS);
   `Traceability: SN=27 SR=76 LLR=191 TC=190 orphans=0 integrity=0 drafts=13`.
6. Amendment trigger (a) driven for real: with `LLR-208.detail` edited and staged
   on the merged tree, `acceptance_record.staged_spine_amendments` returns one
   entry `{'id': 'LLR-208', 'approved': {'Detail': (before, after)}}`.
   `spine_cell_class`: LLR `Detail` = approved, `CodeSymbol` = traced; TC
   `Method` = approved, `Evidence` = traced — so draft 1's cell set arms the
   amendment adjudication through Detail and Method as it claims.
7. `gen_verdict_rollup.py --root .` in a faithful worktree fixture (scratch clone
   of the trunk on `contract_split` + `git worktree add` at `98908416`) ->
   `REFUSED — wi-590-... is a work branch (trunk is contract_split)`, `exit=2`,
   `git status --porcelain` empty before and after. (A flat clone of the lane is
   NOT a valid fixture: `agent_common.trunk_name` reads the primary checkout's
   branch, so a single-checkout clone is its own trunk and the generator writes
   46 rollups at exit 0 — noted so a later round does not misread it.)
8. `baseline_snapshot.refresh_ledger` at the merge base `e410d030` ->
   low-level-requirements: exactly LLR-045, LLR-058, LLR-136, LLR-140, LLR-144,
   LLR-158, LLR-197, LLR-198, LLR-203, LLR-204 (10); test-cases: exactly TC-082,
   TC-138, TC-147, TC-194 (4). Draft 2's list is exact. Attributions spot-checked
   against the cited verdict files: LLR-140/TC-082 -> WI-585, LLR-144/TC-194 ->
   WI-566, LLR-158 -> WI-573 and WI-578, LLR-204 -> WI-578; LLR-197 -> WI-593
   (queued, amendment brief, LLR-197 only). Arithmetic checks: 3+6+2+3 minus the
   LLR-158 duplicate = 13 judged + 1 unjudged = 14.
9. Scope: `git diff e410d030...HEAD -- docs/requirements docs/test` changes
   exactly two lines, both `status = "Drafted"` -> `"Approved"` (LLR-208,
   TC-206); LLR-207/TC-205 untouched. `git log e410d030..HEAD --
   docs/archive/last_approved` -> `a1d80c6f` only. `git diff --name-only
   e410d030...HEAD -- project-trajectory tests scripts` -> empty. The mechanical
   close `f0528530` touches only
   `docs/work/complete/WI-590-adjudicate-llr-207-llr-208.md`. `grep WI-590
   docs/status.md` -> no hits (forward-only scrub clean).

## Findings

- [MAJOR] docs/work/complete/WI-590-adjudicate-llr-207-llr-208.md:206 -> draft 2's closing sentence still reads "the amendment half of the FIRST draft above, **ordered behind `WI-594`**", which is exactly the ordering round 012 killed: draft 1 four paragraphs above now states the successor "needs no ordering against it", the `needs = ["WI-594"]` cell is gone, and WI-594 on the trunk no longer adjudicates LLR-208/TC-206 at all — so the drafts contradict each other and the surviving clause is false. It is not inert prose: `parse_dispositions` carries it into the `scope` cell and the mint reproduces it verbatim as the last line of `docs/work/queued/WI-596-the-anchoring-copy-s-absorb-le.md` (driven, instrument 4), where "the FIRST draft above" also dangles because WI-596 is its own file. The rework commit message asserts "the ordering against WI-594 dropped", which this line falsifies -> in draft 2 replace "ordered behind `WI-594`" with the successor's actual id-free statement ("the amendment half of the return successor drafted above, which carries no ordering against WI-594 — that row was narrowed on the trunk to LLR-209/TC-207"), and while there make the cross-reference name the draft by its title rather than by position, since the mint splits the drafts into separate files. No check is added, so no unrepresentable-clause is owed; the structural note for a later kit lane is that the ordering fact has two homes in one section — stating it once in draft 1 and having draft 2 point at that draft (the `antidote` skill's "smallest change that makes this fix unnecessary") is what makes the contradiction unrepresentable, but that is a spec-format change beyond this diff's scope -> @owner

VERDICT: CHANGES-REQUESTED findings=1
