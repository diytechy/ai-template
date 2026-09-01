## 2026-09-01 — Supervised evening run: four rows merged, every rollup hand-compiled, the wi508 close landed and adjudicated under drawn review, the loop stopped on a C6 cycle

The owner confirmed the unpause at 19:23 UTC and directed two changes first:
pin the codex reasoning effort to medium on all three OPENAI rows (codex
0.145.0 has no `--effort` flag; the `-c model_reasoning_effort=` override is
the only CLI dial, and the two unpinned rows had been silently inheriting
`xhigh` from this box's `~/.codex/config.toml` — so the WI-548 C7 Terra
experiment compared medium against xhigh, not a provider default), then
delete the tracked pause. Both landed as reviewed trunk commits (`60801f12`,
`240dec3c`); the smoke tier was re-measured on a quiet box before the first
commit. The loop ran `./agent-resume.sh --wait-on-limit 14400` from the repo
root under supervision; the pause was re-armed by owner direction at 22:52
UTC (`b3658346`) while the last lane finished under it.

Deferred open items: OI-78

fig: smoke tier 1451 passed / 8 skipped in 21.43 s; `check_smoke_budget.py
--mode enforce` 23.1 s vs 60 s budget (within) — `python -m pytest -q -n auto
-m smoke && python scripts/check_smoke_budget.py --mode enforce` at
`1b460a4f`, load average 0.96, 2026-09-01 19:36 UTC.

### What merged, and what each merge cost

- **WI-567** (construction-first remedies in the reviewer contract): one Opus
  BUILD (420 s), one Terra round (APPROVE findings=0). The loop stopped at the
  verdict gate — nothing writes `docs/reviews/WI-<n>-REVIEW-A.md` — and the
  supervisor compiled it; merged `226ba5cc`.
- **WI-554** (the two approval-brief renderer defects): one Opus BUILD
  (1466 s), one Terra round (APPROVE findings=0). The in-slot refresh was
  REFUSED on `approval-fresh` because the lane changed the brief renderer;
  resolved by regenerating `docs/ratify/CURRENT.md` on the branch (never
  hand-merged), rollup compiled, merged `b336bd8c`. The unload was held by a
  36 MB `.venv/` the BUILD session created inside its worktree; deleted and
  unloaded by hand.
- **WI-555** (OI-71: the wi508 complete-close converted to a partial
  handback): one Opus-strong BUILD (1370 s) that performed the conversion
  directly on trunk under the ruling's manual special case (`979c3e5f`
  handback merge, `551d1b2c` WI-568 mint), then a Terra round that judged the
  record-only lane branch against its own stale tree (CHANGES-REQUESTED 1),
  a loop rework proving the finding a pre-refresh artifact, a Terra
  verification (APPROVE 0). The in-slot refresh was then REFUSED twice on
  `approval-fresh` + `registry-integrity`: the lane was cut BEFORE the
  handback merge moved `docs/archive/last_approved/`, and the station refresh
  (`merge --no-ff --no-commit`, `add -A`, bar) STAGES trunk's snapshot delta,
  which the staged mirror rule reads as a snapshot WRITE and `approval-fresh`
  compares against the committed old snapshot. A plain merge of trunk into
  the lane passes both checks (measured in a detached probe worktree), so the
  precedented remedy (`9bdd56b6`) was applied — merge trunk in as a plain
  commit — which staled the APPROVE and cost two supervisor-drawn Opus rounds:
  round 005 (CHANGES-REQUESTED 9; three record-level MAJORs, below) and round
  006 (APPROVE 5) after a record-only rework. Merged `77270030`.
- **WI-568** (the disposition adjudication of the wi508 close): the
  ADJUDICATE session ruled PARTIAL / keep-all / one successor but put its
  `## Dispositions` block in the verdict file; `handback.close_adjudication`
  refused the close and the loop stopped. Supervisor-drawn round 002
  (CHANGES-REQUESTED 7: two BLOCKERs — the placement, and the owner-owed
  baseline question decided by omission; two MAJORs — OI-71 decision 9
  miscited, the captured scope empty), a supervisor-dispatched rework, round
  003 (APPROVE 1). The loop's resume then scheduled a Terra round
  (CHANGES-REQUESTED 1: the scalar `open_item` mints a thin OI row) whose
  `implementer-touched-review-path` tripwire shifted routing, and
  re-adjudicated the finished lane in a cycle — sessions 003 DESIGN-CHECK and
  004 ADJUDICATE on Sol (both concurring), then 005 NO-COMMIT, 006 ERROR
  (Kimi), 007 WAITING (rate limit) — the C6 shape OI-70 named. The supervisor
  stopped the loop, carried the owner brief into the successor's captured
  scope, closed the row through `handback.close_adjudication` by hand
  (`4d9dba7f`), drew round 004 (CHANGES-REQUESTED 2 — the supervisor's own
  brief was wrong: external.toml DID move, and a byte-level RESTORE is
  unavailable under the mirror invariant), corrected it, drew round 005
  (APPROVE 2), compiled the rollup and merged `5ac6ef2b`. The merge minted
  **WI-569** (the spine reseal successor, strong tier) and **OI-78** (the
  baseline STAND vs REVIEW-THEN-STAND question) gating it.

### Findings the drawn rounds established (all on the record of the lanes)

- The wi508 handback merge carried the BRANCH's `docs/archive/last_approved/`
  bytes onto trunk: the off-spine re-attestation census in `CURRENT.md` fell
  from 132 changed / 30 added / 3 removed rows (rulings OI-64/65/67; rows
  WI-522/528/530/531/533/534/553) to 1 changed — trunk's unsigned off-spine
  approval debt absorbed into the approved baseline by a `partial` lane,
  undisclosed until round 005. Not an authority breach under
  `human_approval_through = "DevStg-Needs"`; now disclosed, and the owner's
  ruling is OI-78 (recommendation on the successor's spec: REVIEW-THEN-STAND —
  a byte-level restore is unrepresentable because `committed_snapshot_findings`
  reds a snapshot that is not a copy of live at its writing commit, and the
  lane's own decision 10 measured that red).
- The immutable handback report says "four Drafted" rows; LLR-203/LLR-204
  arrived Approved (the branch's own `580df781`), TC-199/TC-200 Drafted. WI-568
  KEPT the flips by name. OI-72's wording carries the same "four Drafted"
  error — the owner's to correct.
- The conversion resolved the `docs/log.md` conflict to trunk's side, so the
  branch's six 2026-08-30 entries (slice 6, two reworks, rounds 010/011/013)
  are absent from trunk's log and the archived spec's link to one of them is
  a broken anchor (`check_docs` FAIL on every trunk tree since `979c3e5f`).
  The text survives in history; the classifier blocked the restore script
  and even a `git show` of that branch's log, so the restoration is the
  owner's call (options in the RESUME HERE list).

### Kit findings, unfiled (a row each is warranted; minted only through intake)

1. A lane cut before a trunk commit that moves `docs/archive/last_approved/`
   cannot refresh: the station's staged merge makes the mirror rule and
   `approval-fresh` misfire on the index. Construction-first: the refresh
   should commit the trunk merge before the bar, or the two checks should
   read the merge result rather than the index.
2. The verdict rollup is still hand-compiled for every lane (four this run)
   and adjudication lanes get no mechanized round before their close
   (WI-558/WI-559 are queued for exactly this).
3. The disposition `open_item` mint writes only title/status/raised/one_line/
   wi_refs; a typed `[open_item]` table (blast_radius, options,
   recommendation) written verbatim by `_mint_open_item` would make a thin
   owner card unrepresentable.
4. A DONE adjudication lane whose close is refused is resumed as fresh
   ADJUDICATE sessions until the session cap — the refusal must be the stop.
5. The ADJUDICATE template's "block lives in the spec" rule is prose a strong
   session missed; `intake.parse_dispositions` could be run at the session's
   own exit as the machine check.
6. Fragments keep landing without a file-level `Deferred open items:` line or
   `fig:` provenance (three lanes this run); `gen_open_items --check` lets a
   single-section fragment through.
7. `station.render_report`'s `split_decided_by = "adjudicator"` boilerplate
   invents a "worker exited or crashed" reason; the minted WI-568 Title was 184
   chars against the 120 bound; `spec_move.move_spec` lacks the reverse
   un-close move, so the conversion used a bare `git mv`.
8. The integrator's RULING-6 audit flags intake's own OI mint
   (`f85f91e7`, `docs/requirements/open-items.toml`) as a non-merge product
   commit: the audit's product-path set and the mint's bookkeeping set
   disagree about that file.
9. The lane commit hook resolves ruff via the system python3 and prints a
   format-SKIP on every worktree commit (environmental; recorded again).
10. **The smoke tier is RED on a fully drained trunk.**
    `tests/test_wi_convert.py::test_the_live_registry_round_trips_in_whichever_home_is_authoritative`
    round-trips the folder home only when `docs/work/active/` holds no claim
    (otherwise `wi_convert` refuses by name, "drained-stop", and the test
    accepts the refusal); on the first drained trunk since WI-504 relocated
    the terminal folders, `wi_convert.read_specs` reads
    `docs/work/cancelled/README.md` as a spec and raises "does not start with
    a +++ frontmatter fence". Latent since 2026-08-2x, masked by every claim
    since, surfaced by this session's drain. A one-line reviewed fix (skip
    `README.md` / non-spec files in a status folder) belongs to a row; a
    supervisor may not land product code on trunk outside a merge.

### Bar

Trunk commits this session ran the hook's declared bar; the smoke tier and
budget were measured at the head of the session (figure above) and re-run
green before the unpause commit (1451 passed / 8 skipped, 21.13 s; budget
22.8 s). Every merge ran the integrator's full 11-step bar on the refreshed
tree (`bar PASS (11 steps, tier all)` in each refresh trailer).
`check_docs --stale` is RED on trunk since `979c3e5f` for the one broken
anchor named above and for no other reason. `check_trajectory --strict`
carries exactly one KNOWN ERROR now (the schedule→trace seam, queued as its
own row); the wi508 hold-ban ERROR cleared with the phantom head.
