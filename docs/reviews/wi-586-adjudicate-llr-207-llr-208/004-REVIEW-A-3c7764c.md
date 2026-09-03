# REVIEW-A — WI-586 adjudicate LLR-207/LLR-208/TC-205/TC-206 @ 3c7764c

Scope: `git diff contract_split...HEAD` minus records/generated — one file,
`docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md`
(+140), appending a `## Dispositions` section with two drafts.

Worst failure classes this change admits, hunted in this order: (1) SILENT WRONG
CONTENT — a durably-minted successor row asserting a false fact about spine
approval state or about what a module does; (2) FAIL-OPEN — a draft that will not
parse, or that under-declares the bar its successor lane must clear; (3) SCOPE
BREACH — the lane performing the approval act it is forbidden to perform.

## Instruments (run here, summaries only)

`python3 project-trajectory/scripts/check.py --jobs 0` — `RESULT: PASS`
(stage DevStg-LLReqs, tier all; `registry-integrity` / `vocabulary` /
`need-form` / `privacy` / `doc-navigability` / `skills-index` /
`prompt-catalog` / `staged-divergence` / `approval-immutable` PASS,
three trunk-owned freshness steps SKIP on a work branch).

`python3 project-trajectory/scripts/trace.py --strict-integrity` — final line:
`Traceability: SN=27 SR=76 LLR=190 TC=189 orphans=2 integrity=0 ... provenance-findings=1`
(the one provenance finding is LLR-197 citing WI-448 — pre-existing, not this diff).

## What I drove (real shipped code paths, not reading)

- `intake.parse_dispositions(<this spec>, ...)` → `refusal=None`, **2 drafts**,
  each carrying `kind='spine'`, `bar='DevStg-Reqs'`, `title`, `workstream`,
  `buildtier`, `specref`, `priority`, `scope`. The section parses; it will mint.
- Finding 1's evidence REPRODUCES exactly. `kv.refresh_attestation(root,
  'wi-585-adjudicate-llr-045-llr-140', 'c16246e0')` →
  `('e2b3cf8af0a1fcffd2d2888c78d692ba3cd24f10', 'bar PASS (12 steps, tier all)')`,
  `kv.governing_identity(...)` → `ce5e2550be0a…`; with `'HEAD'` (and with either
  live branch name) → `att=None`, id `2c9a184049f8…`. Two identities across one
  refresh commit, as claimed.
- Finding 2's evidence REPRODUCES exactly. `kv.governing_rev(root, <branch>,
  '0e6bad3b')` → `d202c9f3cd66d57d61d8eb662605a21b80f8f616` with
  `refresh_attestation` `None` — the walk does not terminate on a peel.
- Finding 3's gap is REAL. Mutated `verdict.py:608` from `if len(ph) == 1` to a
  last-wins `sorted(ph)[-1]`: `tests/test_verdict_record.py
  tests/test_score_reviews.py` → `72 passed`. Reverted clean.
- Finding 4's gap is REAL. Deleted `verdict.py:802-803` (the carrier check):
  `72 passed`. Reverted clean. `branch_trailers`/`format_trailer`/`Review-Verdict`
  appear in no test module but `test_verdict_record.py`, as claimed.
- Disposition 2's gap is REAL. Deleted the `verdict-rollup` row from
  `trunk_step.REGEN_STEPS`: TC-206's four cited evidence nodes → `4 passed`, and
  the whole of `tests/test_trunk_step.py` → `16 passed`. Reverted clean.
  (`test_regen_runs_in_declared_dependency_order` asserts on a name list that
  omits `verdict-rollup`.)
- Every cited line reference checks out: `verdict.py` 50 / 256 / 398 / 467 / 470 /
  473 / 608 / 738-740 / 802-803; `tests/test_verdict_record.py:401` ("one session
  log") and `:81-90` (only the `src/widget.py` entry is changed, and the second
  assertion DROPS the spec entry — finding 6 is right); `test_integrate_station.py`
  527/690/755/764/808/832/838/964; TC-205's `evidence` cites no
  `test_integrate_station` node; `agent_loop.py:317` + `:4170`;
  `score_reviews.py:72` against `IF-175.requestors`; `CMP-006`'s stale note.
- Scope breach: none. Only the spec file changed; LLR-207/208 and TC-205/206 are
  still `Status = "Drafted"`; nothing under `docs/archive/last_approved/` moved.

The evidentiary work here is unusually honest — I tried to break the six findings
and the eleven line citations and could not. The three findings below are all in
the drafts' own text.

## Findings

- [BLOCKER] docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md:47 -> the first draft's Scope asserts "`LLR-208` and `TC-206` were APPROVED by that act", which is false three ways: the same sentence quotes that act's own governing line `OUTCOME: RETURN rows=4`; `001-ADJUDICATE-d7ffb41.md:59` heads a section "The approval act on LLR-208/TC-206 is WITHHELD" and `:65` records the flip being reverted; and the SECOND draft in this very file (`:168`) says "All four rows were returned by this act, so they stay `Drafted`" — I confirmed `Status = "Drafted"` on all four rows in the registries. Once intake mints this draft, a durable successor row tells its builder two Drafted spine rows are blessed, which is exactly the class of false claim the approval ledger exists to prevent, and it will read as an approval this lane had no authority to record -> replace the clause with the true reason those rows are out of scope (they were RETURNED by the same act and are the SECOND draft's scope), and re-point `VERDICT THIS CONTINUES:` at `003-ADJUDICATE-9c563df.md` — the latest adjudication, which returned all four — rather than the superseded `001`; no guard is being added here, and the defect is unrepresentable-by-construction only if a draft's continued-verdict citation is resolved from the ONE latest record for the lane instead of hand-copied, which is beyond this diff's scope (`antidote`'s "smallest change that makes this fix unnecessary") -> @owner
- [MAJOR] docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md:41 -> both drafts declare `bar = "DevStg-Reqs"`, but their deliverable is not requirements-only: draft 1's findings 3 and 4 and draft 2's whole scope are NEW pytest regressions plus TC evidence edits — "the test set for those obligations in work" is `kitlib/ladder.py:79`'s own definition of `DevStg-Tests`. Driven: `check.py --stage DevStg-Reqs --list` yields 12 steps and `--stage DevStg-Tests --list` yields 14, the two dropped being `design-flows` (`check_flows.py --no-placeholders`) and `trajectory` (`check_trajectory.py`) — so as drafted these successor lanes land new test modules and rewritten TC/LLR cells without the trajectory check ever running -> set `bar = "DevStg-Tests"` on both draft blocks (line 41 and line 146); this changes a declared value rather than adding a check, so no compensating guard is proposed -> @owner
- [MINOR] docs/work/active/wi-586-adjudicate-llr-207-llr-208/WI-586-adjudicate-llr-207-llr-208.md:58 -> for clarity: finding 1's reproduction instruction never names the branch. "under the branch name `refresh_attestation` answers …" reads as if `refresh_attestation` were the branch; the branch that actually yields the quoted `('e2b3cf8a…', 'bar PASS (12 steps, tier all)')` / `ce5e2550…` pair is `wi-585-adjudicate-llr-045-llr-140` (c16246e0's refresh subject), which I had to guess — every live branch name in the tree, and `HEAD`, all answer `None` / `2c9a1840…`, so a builder following the sentence literally reproduces the WRONG half of the contrast and may conclude the finding is bogus -> rewrite as "passing the refresh subject's branch name `wi-585-adjudicate-llr-045-llr-140`, `refresh_attestation` answers …" -> @owner

VERDICT: CHANGES-REQUESTED findings=3
