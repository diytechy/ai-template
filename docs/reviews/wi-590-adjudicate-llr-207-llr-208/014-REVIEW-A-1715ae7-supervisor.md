# WI-590 — REVIEW-A round 014 (supervisor-drawn independent reviewer)

- train: `wi-590-adjudicate-llr-207-llr-208`
- tree: `1715ae78` (merge-base with trunk `e410d030`; trunk now `bfe2bda7`)
- model: claude-opus-5 (supervisor-drawn)
- scope: `git -C <lane> diff e410d030...HEAD -- . ':!docs/reviews' ':!docs/log.d' ':!docs/iteration'`
  (generated artifacts — PROJECT_STATE.html, docs/open-items.html, docs/stage,
  docs/ratify/CURRENT.md, docs/log.md, docs/status.md — noted, not read for bytes)

Worst failure classes hunted first: (1) a draft that mints into a successor
carrying a FALSE or dangling sentence (round 013's class); (2) an approval act
that blessed more than it names; (3) a stale pointer a builder would follow.

## Instruments driven (each once)

1. REAL MINT. Scratch clone of trunk `bfe2bda7`, merged the lane (`d70c8df7`;
   the only conflict was the generated `PROJECT_STATE.html`, resolved to the
   lane side and regenerated with `gen_trajectory.py`, then
   `intake.intake_after_merge(root, "bfe2bda7", "d70c8df7",
   outcomes={"WI-590": "merged"})` -> `refusal=None`, minted **WI-595**
   `docs/work/queued/WI-595-llr-207-tc-205-return-and-llr.md` and **WI-596**
   `docs/work/queued/WI-596-the-anchoring-copy-s-absorb-le.md` (commit
   `c6f04bd0`). BOTH MINTED SPECS READ TOP TO BOTTOM: round 013's finding is
   DISCHARGED — neither file contains "ordered behind", "the first draft above"
   or any `needs`; WI-596's closing sentence names the successor by TITLE
   ("LLR-207/TC-205 return and LLR-208/TC-206 amendment", a literal prefix of
   WI-595's minted `title`, greppable) and the mint header line
   ("Drafted by WI-590 (its ## Dispositions section)") resolves "this same
   verdict". WI-595's internal "round 011 MAJOR, below" resolves inside its own
   `## Context`.
2. `intake.parse_dispositions(text, path)` on the closed spec -> `refusal=None`,
   **2** drafts, `kind='spine'` (priority 2, `bar='DevStg-Tests'`, NO `needs`)
   and `kind='ordinary'` (priority 3).
3. `adjudicate_brief.first_approval_values` for **WI-594** on the merged+minted
   tree -> `why=None`; the composed values contain LLR-209 x4 and TC-207 x4 and
   **ZERO** occurrences of LLR-207 / LLR-208 / TC-205 / TC-206; `approves_rows`
   covers LLR-209 and TC-207 only. `grep -rn '^adjudicates' docs/work/queued/`
   -> WI-594 only, `["LLR-209","TC-207"]`. `grep -rn '^needs'` -> no hits
   anywhere in `docs/work/queued/`. The overlap draft 1 asserts is gone is gone.
4. `check.py --jobs 0` on the merged+minted tree -> `RESULT: PASS` (all twelve
   steps incl. `approval-fresh`, `approval-immutable`, `verdict-rollup`);
   `Traceability: SN=27 SR=76 LLR=191 TC=190 orphans=0 integrity=0
   interface-findings=0 drafts=13`.
5. `gen_verdict_rollup.py --root .` in the REAL lane worktree -> `REFUSED —
   wi-590-… is a work branch (trunk is contract_split)`, `exit=2`;
   `git status --porcelain` = 0 lines before AND after. Nothing written.
6. `baseline_snapshot.refresh_ledger` on a worktree at the merge base
   `e410d030` -> LLR file: exactly LLR-045, 058, 136, 140, 144, 158, 197, 198,
   203, 204 (10); TC file: exactly TC-082, 138, 147, 194 (4); `flips=0` in every
   file. Draft 2's set is exact. (The ledger ALSO reports 17 SR rows and CMP-006
   drifted — correctly OUTSIDE draft 2's claim, because the act named only the
   two registries: `docs/archive/last_approved/README.md` records "Copied:
   low-level-requirements.toml (ref: WI-590); test-cases.toml (ref: WI-590).
   Registries not named by this act keep their prior snapshot bytes.")
7. Attribution re-derived INDEPENDENTLY (grep of `^- \[(MEANING|CLARITY|APPROVE
   |RETURN)\] <id>` across `docs/reviews/`): WI-585 -> LLR-045/LLR-140/TC-082;
   WI-566 -> LLR-058/LLR-144/LLR-198/TC-138/TC-147/TC-194; WI-573 ->
   LLR-136/LLR-158; WI-578 -> LLR-158/LLR-203/LLR-204; LLR-197 -> ZERO hits.
   13 distinct judged + 1 unjudged = 14, as drafted. LLR-197's amendment judge
   WI-593 exists (`docs/work/queued/WI-593-adjudicate-llr-197-approved.md`,
   `brief="amendment"`, its Context lists LLR-197 `Detail`/`Rationale`), minted
   at `09193fea`; the reword commit `14beba0a` is a trunk integrate, not a lane.
8. Draft-1 row claims re-driven against the lane tree: LLR-207 `Status=Drafted`,
   `detail` still carries "peeling any verified refresh", no "mechanical"
   anywhere in it, `code_symbol` omits `mechanical_close_attestation`; TC-205
   `Drafted`, `Tier="Smoke"`, 46 `::` citations, no "mechanical" in `method`;
   LLR-208 `Approved` with `_off_trunk_refusal` absent from `code_symbol`;
   TC-206 `Approved`. `grep -c mechanical_close_attestation` over ALL nine
   requirement/test registries -> 0 in every one, and 0 citations of the three
   mechanical-close tests in `test-cases.toml`: the "only possible home" and
   "cited by no test case" claims hold. `kitlib/verdict.py` citations check out
   on this tree: `mechanical_close_attestation` def :376, `_peel_target` :431
   (returns :442), `work_tip` docstring :448-455 carries the
   "measures code-time here" sentence, `refresh_attestation` called directly at
   :469-ish inside :464-470 — the ":466" pointer lands in that loop.
9. SCOPE. `git diff e410d030...HEAD -- docs/requirements docs/test` = exactly
   two changed lines, both `status = "Drafted"` -> `"Approved"` (LLR-208,
   TC-206); LLR-207/TC-205 untouched. `git log e410d030..HEAD --
   docs/archive/last_approved` -> `a1d80c6f` ONLY. `git diff --name-only
   e410d030...HEAD -- project-trajectory tests scripts` -> EMPTY (no product
   code). The mechanical close `f0528530` touches only
   `docs/work/…/WI-590-….md`. `grep WI-590 docs/status.md` -> no hits.
10. `schedule.py --root . ready --explain` on the merged+minted tree ->
    `WI-595 ready exclusive rank=0 P2` and `WI-596 ready parallel rank=6 P3`
    (WI-593/WI-594 rank=1, `exclusive:adjudication`). WI-595 runs first
    (finding 2).

## Findings

- [MINOR] docs/work/complete/WI-590-adjudicate-llr-207-llr-208.md:125-129 -> draft 1's item 3 cites the three mechanical-close tests at `:1600`, `:1628` and `:1640`, which are STALE on this tree: the defs are at `tests/test_verdict_record.py:1626`, `:1654` and `:1666`, and `:1600` lands inside an unrelated `_mechanical_close` fixture. Driven: at `0a36090b` (when the draft was written) the first def WAS at 1600; the station refresh `7b72d2fd` onto `e410d030` shifted the file by 26 lines and the citation was never re-driven — and the numbers mint VERBATIM into `docs/work/queued/WI-595-…md` (instrument 1), so WI-595's builder follows them into the wrong code. The fully-qualified `::test_…` names beside them are correct and unambiguous, which is why this is MINOR and not a defect in the ruling -> re-drive the three numbers, or simply DROP them: the `::name` is the durable pointer and a bare line number in a spec restates a fact git already owns and staled once already in this lane's own lifetime — deleting the line-number form is the smallest change that makes the defect unrepresentable (the `antidote` skill's question), and no check is added, so nothing here compensates for a reachable bad state -> @owner
- [MINOR] docs/work/complete/WI-590-adjudicate-llr-207-llr-208.md:206-208 -> for clarity: draft 2's closing clause claims the amendment half "needs no ordering against ANY other row", but the only ground it offers is WI-594's narrowing — and there is one other candidate ordering the sentence forecloses without arguing it, namely draft 2's own successor. Driven: on the merged+minted tree WI-595 is `rank=0 P2 exclusive:spine` and WI-596 is `rank=6 P3 parallel:ordinary`, so WI-595 merges first, its merge mints an amendment adjudication, and THAT approval act takes another whole-file snapshot before the absorb ledger WI-596 builds exists — re-absorbing whatever has drifted by then with nothing naming it, which is precisely round 008's finding recurring one iteration later. The claim is not false about WI-594; it is wider than its evidence -> narrow the clause to what was driven ("no ordering against `WI-594`, which was narrowed on the trunk to LLR-209 and TC-207"), and if the ordering against the ledger successor was considered and declined, say so in one clause with the reason (the ledger row is a mechanism improvement, not a precondition of the amendment) rather than leaving a reader to infer it. No guard is added -> @owner

VERDICT: APPROVE findings=2
