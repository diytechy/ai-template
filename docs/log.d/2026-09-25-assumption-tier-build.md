## 2026-09-25 — The assumption tier's build, test-first (WI-627 onward)

The build of the phase-6 chains approved at cbb6649f, one work item at a time
in the generated frontier's order, each test written from its approved test
case and seen failing before the code that turns it green (SN-042's own rule).
Reviews are codex Sol (medium); a Fable (medium) agent arbitrates any
disagreement. Attended, on `refactor_again`, with the loop paused.

Deferred open items: OI-82, OI-86, OI-87, OI-88, OI-89, OI-90, OI-91, OI-92,
OI-93, OI-94 — the owner's decisions this build surfaced, filed as open items
on 2026-09-26 (the declaration read `none` before they were filed).

### WI-627 — a crossing's system of interest, and a requirement's derived one

- **Built:** `kitlib.spine.SYSTEM_VALUES = ("operation", "delivery")` and the
  crossing tier's optional `system` key, mapped both ways by the carrier
  (`System`); the template's example crossing carries it, and its header says
  what it means. `frame_rules.py`, a pure sibling of `coherence.py`:
  `frame_system_findings` (an out-of-pair value joins the frame class and fails
  `--strict`; a missing one is one advisory), `crossing_systems` and
  `sr_system_advisories` (a requirement naming crossings of both systems is one
  advisory naming it and a crossing of each). `trace.analyze` composes them.
- **Tests first:** `tests/test_frame_rules.py` (TC-213, in-memory, per-commit
  tier) failed at collection before the module existed;
  `tests/test_frame_system.py` (TC-212, scaffold + `trace.py`, registered in
  `SLOW_MODULES`) had 4 of 7 failing, the 3 vacuous cases passing. Both green
  after the build (15 and 7 passed), with `tests/test_external_frame.py`'s 20
  still green.
- **This repo's own frame** now prints one advisory per crossing (B-01, B-02,
  B-04, B-05) declaring no system. That is expected until the C1 sitting commit
  (WI-643) writes the cells; it never moves the exit code.
- **Ratchet:** `trace.py` 3372 -> 3377 (the composition lines alone, per D21)
  and `bootstrap.py` 1665 -> 1666 (the MAPPING entry), re-stamped with the
  reason at each entry.
- **Seam:** IF-180 (`scripts/frame_rules` called by `scripts/trace`), its
  contract body in the module header, cited by TC-213's `verifies`, a traced
  pointer cell that re-opens no attestation. `check_trajectory` requires a
  citing test case for every seam.
- **Sol review:** NOT YET SOUND, 2 major, 1 minor, all applied. The interface
  row was first left out on `coherence.py`'s precedent; Sol held the Done-when
  to its word. TC-212's live-frame leg: LLR-211 keeps the cell out of this
  repository's frame until the sitting, so the scaffold's frame is the live
  leg now, and WI-643's Done-when tightens the assertion when the cells land.
  Added a case pinning that an out-of-pair crossing places nothing.
- **Back-link coverage** reads 45.2% against the 50% dial. That predates this
  item (the 47 phase-6 design rows landed at c47143d4 with no code) and rises as
  the build lands.
- **Adopters:** `RESYNC_PACK.md` entry "A boundary crossing names its system of
  interest", anchored at the preceding commit per the pack's rule.
- **Commit bar:** smoke **1696 passed, 3 skipped** in 366.6 s; the slow frame,
  bootstrap and dogfood modules 124 passed, 1 skipped. Seconds **FAIL** at
  367.6 s against 60 s (D10; the box was loaded), recorded, not re-stamped.
  `check_docs --stale` OK; `check_trajectory --strict` clean; `trace.py
  --strict-integrity` 0 integrity; `CURRENT.md` fresh; the open-items view up
  to date.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=cbb6649f -->

### Builders in parallel, and the worktree base

From WI-639 on, each item is built by a builder session in its own git worktree
under the session scratchpad, cut at the trunk's tip, with one shared brief (the
conventions WI-627 surfaced). The integrator reviews each commit with codex
Sol, squash-merges it onto `refactor_again`, closes the spec, regenerates and
runs the bar. The harness's own worktree isolation was tried first and dropped:
it cut the worktrees from the default branch's July commit (3abeb636), 2,948
commits behind; those builders were stopped before they committed anything and
their worktrees deleted. A session limit then interrupted all four builders
mid-work, and each resumed from its own worktree.

### WI-639 — the per-change readability report

- **Built:** `check_readability.py` over a new `[readability]` profile section
  and `[step:readability]`; the complexity adapter reuses `check_complexity`'s
  census, now factored as `functions()`, rather than copying it. This repo
  declares `measures = complexity` with no gating.
- **Tests first:** `tests/test_check_readability.py` (TC-249, slow): red `2
  failed, 9 errors`; green 12, then 15 after the rework.
- **Deviations, accepted at review:** `check_complexity.py` now ships to
  adopters (the shipped report imports it); the template carries its first
  active `[step:]`, and the template-plan identity tests exclude exactly it; the
  measure covers the profile's source and test roots only.
- **Sol review:** NOT YET SOUND, 1 blocker: the build exited 2 on an unknown
  name and 1 on an unreadable change, against approved LLR-256's "nonzero only
  for a worsening in a gating measure". The code was conformed rather than the
  row amended. And 1 major: the merge-base test could not tell merge-base from
  the previous commit, now mutation-checked against both wrong readings. Both
  fixed in the builder's rework.
- **Seams:** IF-187, IF-188, IF-189; watermark IF 180 -> 189. `bootstrap.py`
  ratchet 1666 -> 1668 (two MAPPING rows).
- **Findings for later filing** (not in scope): trace's IF-owner reachability
  advisory does not split `;`-joined `module` cells and builds
  `scripts/scripts/<mod>` keys, so IF-187 gets a false advisory;
  `check_complexity.py --mode enforce` already fails at 76a235bb
  (`route_session` 37 -> 38, stale `traj_*` paths after the `rendering/` move).

- **Commit bar:** smoke **1696 passed, 3 skipped** in 408.1 s; `check.py
  --run-step readability` PASS ("no worsening"); `check_docs --stale` OK;
  `check_trajectory --strict` clean; `trace.py --strict-integrity` 0 integrity;
  `CURRENT.md` fresh; the open-items view up to date. Seconds **FAIL** at 411.8 s
  against 60 s (D10; four builders were loading the box), recorded, not
  re-stamped. The builder's run of the affected slow modules (467 passed, 2
  skipped; then 51 after the rework) stands for the identical squashed tree.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=76a235bb -->

### WI-612 — trunk bookkeeping commits stage and restore only what they wrote

Not in the phase-6 chains, but ahead of WI-638, which files through the mint.

- **Built:** `scripts/bookkeeping.py` (IF-186), the one helper the claim and
  the intake mint commit through. It refuses by name on dirt in the step's
  scope before anything is written. It commits the in-scope changes from a
  temporary index seeded from HEAD and advances trunk with a compare-and-swap
  `update-ref`. `REGEN_STEPS` rows name their writes. The dispatcher's and the
  merge slot's clean-trunk checks ignore `OWNER_ONLY_PATHS`.
- **Tests first:** `tests/test_bookkeeping.py` (slow) plus cases in
  `test_integrate.py` and `test_dispatch.py`: 8 red, then green. Affected
  modules: 468 passed, 2 skipped; after the rework 269 passed, 1 skipped.
- **Sol review:** NOT YET SOUND, 1 blocker, 3 major, 1 minor. The blocker, a
  time-of-check/time-of-use race on an in-scope path the owner edits during the
  step, went to a Fable arbiter, which ruled B. The Done-when is met as
  written, and an isolated build would only narrow the window, not close it.
  The arbiter also corrected the integrator's proposed late drift refusal:
  that refusal's own restore would destroy the edit it had detected. So the
  helper's contract states the window honestly, and its restore leaves and
  names any in-scope path edited after the step wrote it. The isolated build is
  filed as WI-647, after WI-636. The majors were fixed: a failed restore rides
  the re-raised exception; the pre-check tests count writes, and a mutation
  proves it; six approved rows amended.
- **Amended approved rows**, status left Approved and nothing re-anchored:
  LLR-140, LLR-143, LLR-151 `detail`; TC-132, TC-144, TC-145 `method`. Their
  adjudication is filed as WI-648.
- **Bytes:** `PROCESS_OPTIONS.md` 189,535 -> 189,549 (+14; "a dirty path it
  must write", not "a dirty tree"), re-stamped in the byte-budget-guard skill's
  three copies. The skill's own baseline is 4,613 -> 4,533.
- **Merge:** squashed onto the trunk after WI-639. Resolved: the watermark (IF
  189, the higher), interfaces (IF-186 before IF-187..189), the RESYNC entries
  (both kept, oldest first) and the `bootstrap.py` ratchet (1666 + 2 + 1 = 1669).
- **Findings for later filing:** the `[generated]` list in the shipped stack
  profile lags what the regeneration writes; the regeneration reads the working
  tree, so an uncommitted generator input shapes committed artifacts; a relink
  can rewrite the owner's scratchpad, so a dirty scratchpad refuses that claim
  by name; LLR-140 still lists a safety-class rung WI-381 deleted.

- **Commit bar:** smoke **1696 passed, 3 skipped** in 706.8 s;
  `tests/test_bookkeeping.py` 9 passed on the merged tree; `check_docs --stale`
  OK; `check_trajectory --strict` clean (645 work items); `trace.py
  --strict-integrity` 0 integrity; `CURRENT.md` fresh; the open-items view up
  to date. Seconds **FAIL** at 710.9 s against 60 s (D10; three builders and a
  full-suite run were loading the box), recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=2be2894f -->

### WI-635 — row-level refusal in the snapshot refresh

- **Built:** an act refuses while any drifted approved row it neither flips
  nor names with the new `--reattests` stands in a registry it copies.
  `--approves` clears no row. A removed approved row counts as drifted.
  `--reattests` is validated before every copy and refused on a first signing.
  The rule iterates `SNAPSHOT_TIERS`. Prompts, the gate-advance skill and the
  reference docs say `--reattests`.
- **Tests first:** `tests/test_baseline_snapshot.py`: red 24 failed, 47 passed
  (TC-240 subset 13 failed, 3 passed, the 3 vacuous or regression pins named
  in the builder's report); green 71 passed. After the rework, 12 new cases red
  11 of 12 before the fix, green after. Two tests in `test_trace_briefs.py`
  that re-anchored with `--approves` alone were red at the first commit and
  now name their row.
- **Sol review:** NOT YET SOUND, 1 blocker (a removed approved row was
  invisible) and 2 major (the seed path; the assumption tiers not yet
  exercised). The first two were fixed. The third is sequenced: the tests pick
  up any tier added to `SNAPSHOT_TIERS`, and WI-629's Done-when now requires the
  recorded run.
- **Merge:** after WI-612; the `RESYNC_PACK.md` conflict was resolved by keeping
  both entries. `intake.py` auto-merged; the size ratchet holds.
- **Resume surface:** the handoff's `--approves` trap is rewritten for
  row-level refusal.

- **Commit bar:** smoke **1696 passed, 3 skipped** in 560.2 s; `check_docs
  --stale` OK; `check_trajectory --strict` clean; `trace.py --strict-integrity`
  0 integrity; `CURRENT.md` fresh; the prompt catalogue fresh; the open-items
  view up to date. Seconds **FAIL** at 562.6 s against 60 s (D10), recorded,
  not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=c429dd0c -->

### WI-628 — the stakeholder list and the needs' source pointer

- **Built:** a `[stakeholder.STK-##]` tier in the needs file, loaded by its own
  id column; each need's `stakeholder_refs` and `source`. `frame_rules` gains
  `stakeholder_findings` and `need_source_findings`. `trace.analyze` composes
  them: failures into the frame class, advisories into the warn pipe.
  `STATUS_VALUES` moves to `kitlib.spine` so the pure module can read it. The
  STK id space joins the watermark.
- **Tests first:** `tests/test_stakeholders.py` (TC-215, slow) red 11 failed, 4
  passed, the 4 vacuous no-finding cases. TC-216's cases in
  `tests/test_trace_rules.py`: 2 red, 5 pinning existing behaviour. Green 57.
  After the rework, the review's cases were added: 3 red (the carrier) and the
  rest pinning behaviour already built.
- **Sol review:** NOT YET SOUND, 2 major, 1 minor. A comment-only TOML needs
  file read as markdown, so a need id in a comment joined the need universe;
  the carrier now comes from the file's suffix. Tests now pin both status
  findings, a citation with no table, and the source semantics. PROCESS.md +19
  bytes was re-stamped at merge.
- **Decision for the owner (spine map §6 style):** an out-of-vocabulary
  stakeholder status prints twice under `--strict`, as an integrity finding
  (TC-215) and as a frame finding (LLR-216), because the two approved rows
  name different classes. An amendment choosing one would remove the
  duplicate.
- **Ratchet:** `trace.py` 3377 -> 3405 (+28: the composition, the stakeholder
  loader, the enum sweep and the source-anchor read in `main`), re-stamped.
- **Bytes:** PROCESS.md 88,990 -> 89,009 (+19), re-stamped in the
  byte-budget-guard skill's three copies. The skill itself is 4,533 -> 4,519.
- **Merge:** conflicts in `tests/conftest.py` (both slow modules kept) and
  `RESYNC_PACK.md` (four entries, oldest first).
- **Owed by WI-643:** retire `LIVE_ROWS_PENDING`'s `STK-ID` in the commit that
  writes STK-01..04, now in its Done-when.
- **Finding for later filing:** `spine_carrier.draft_ids_from_text` still
  sniffs the needs carrier from content.

- **Commit bar:** targeted modules (ratchets, rule and dogfood sync, resync
  pack, skills sync, frame rules, spine rules, watermark, the byte-cap tests)
  179 passed, 1 skipped; smoke **1697 passed, 3 skipped** in 427.8 s;
  `check_docs --stale` OK; `check_trajectory --strict` clean; `trace.py
  --strict-integrity` 0 integrity; `CURRENT.md` fresh; the open-items view up
  to date. Seconds **FAIL** at 430.2 s against 60 s (D10), recorded, not
  re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=e123eb6d -->

### WI-648 — the six rows WI-612 amended, adjudicated and re-anchored

- **Verdict:** `MEANING rows=6` by an independent adjudicator session (the
  integrator had directed the amendments, so it did not judge them), all six
  blessable. It checked scope by diffing every key of all 239 LLR and 234 TC
  rows against the record, confirmed the new text against the code, and ran the
  suites the cases name (141 and 36 passed). Recorded at 0c2228b1. No Sol
  review of this verdict: the session was wrapping up, and the next session
  may run one.
- **Re-anchor:** `intake.py snapshot --reattests
  LLR-140,LLR-143,LLR-151,TC-132,TC-144,TC-145`, the first use of WI-635's
  row-level refusal. It copied two records and stamped the six ids.
- **Found, not acted on:** LLR-140's stale safety-class rung (predates the
  amendment); `tests/test_bookkeeping.py` cited by no test case's Evidence;
  LLR-154's "declared generated set" no longer matches the mint's scope.

- **Commit bar (the re-anchor):** smoke **1697 passed, 3 skipped** in 822.4 s;
  `check_docs --stale` OK; `check_trajectory --strict` clean; `trace.py
  --strict-integrity` 0 integrity; `CURRENT.md` fresh; the open-items view up
  to date. Seconds **FAIL** at 824.5 s against 60 s (D10), recorded, not
  re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=0c2228b1 -->

### Session end (2026-09-26): the resume surface

- **Wrapped up at the owner's request**, with the builds of WI-627, WI-639,
  WI-612, WI-635 and WI-628, and the WI-648 adjudication, landed. The
  full-suite run started at 2be2894f was stopped unfinished; the full suite is
  owed. The merged builder worktrees and branches were removed.
- **Resume surface:** `docs/handoff-2026-09-26.md` replaces the 2026-09-25
  handoff, and `docs/status.md`, the root README and `docs/README.md` point at
  it. The builder brief every builder is handed is now
  `docs/plans/2026-09-26-assumption-tier-builder-brief.md`.
- **Byte deltas on budgeted files this session:** `PROCESS_OPTIONS.md` +14 and
  `PROCESS.md` +19 (both watched, re-stamped); the byte-budget-guard skill
  4,613 -> 4,519 (capped at 5,000). No other capped file edited.

### Session resumed (2026-09-26): the owed full suite, and a second wave of builders

Resumed from `docs/handoff-2026-09-26.md` on the owner's direction: run the
full unfiltered suite first and fix or report what it finds, then continue
the build in the handoff's order. Reviews stay codex Sol (medium), with a
Fable (medium) arbiter for disagreements.

- **The full suite at b14d1808**, in a detached worktree: **1 failed, 3771
  passed, 14 skipped** in 4128.6 s (1:08:48) on this 4-core, 8-thread box.
  <!-- fig: cmd="python -m pytest -q -n 4" rev=b14d1808 -->
  The failure was `tests/test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans`:
  `docs/Inspiration.md` and `docs/external-skills/architect/{SKILL,PROVENANCE}.md`,
  added by the owner's 1e3178fd (2026-09-20), had no path from an entry root.
  The per-commit bar reads orphans as warnings, so only the full suite's
  strict test saw it, six days late. Fixed by linking them from the `docs/`
  folder map rather than by an allow-list glob, which would have accepted the
  orphaning instead of repairing it.
- **Builders started before the suite finished**, a deviation from the
  owner's order: the suite's early modules read as a three-hour run, so the
  four ready items (WI-629, WI-636, WI-640, WI-645) were built in worktrees
  cut at b14d1808 while it ran, and nothing merged until the suite was
  handled. It finished in 69 minutes.
- **Codex's login was revoked** (`refresh_token_invalidated`) at session
  start, so no Sol review could run; the owner was notified to log in again.
  The catch-up review of WI-648's verdict, which the last session left
  unreviewed, waits with the rest.

- **Commit bar (the orphan fix):** smoke **1697 passed, 3 skipped** in
  284.2 s; the orphan test passes; `check_docs --stale` OK (0 broken, 1 orphan
  warning); `check_trajectory --strict` clean; `trace.py --strict-integrity`
  0 integrity; `CURRENT.md` fresh; the open-items view up to date. Seconds
  **FAIL** at 285.4 s against 60 s (D10; two builders were loading the box),
  recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=b14d1808 -->

### WI-645 — TC-061 and TC-161 brought up to their amended design rows

- **Built:** `TC-061.method` and `TC-161.method` re-drafted so each clause is
  held by a named test in its evidence file; `amendment_values` and
  `first_approval_values` named on LLR-167's `code_symbol`; the stale
  "unrouted brief" docstring and comments corrected. No behavior change, so
  no red run: both evidence modules ran before and after (44 and 57 passed).
- **Sol review** (the first this session, after the owner's re-login and a
  Windows sandbox fix, `-c windows.sandbox="elevated"`): NOT YET SOUND, one
  major, TC-161 still `Smoke` while its method drives git and subprocesses and
  its module is slow. Fixed by amending the tier to Full.
- **Amended approved cells, status left Approved and nothing re-anchored:**
  TC-061 `method`, TC-161 `method` and `tier`. They join the wave's joint
  amendment adjudication with LLR-167 (WI-646 and the follow-up that corrects
  its "falls back" clause).
- **Stacked builds, and the review wait:** codex was unauthorized from session
  start until the owner logged in again, so the builds of WI-629, WI-630,
  WI-631, WI-632, WI-636, WI-637, WI-640, WI-646 and WI-647 were cut one or two
  deep on unreviewed bases to keep the critical path moving; nothing merged
  unreviewed. Each stack was then reviewed as one chain.
- **Commit bar:** smoke **1 failed, 1692 passed, 3 skipped, 4 errors** in
  954.5 s; all five in `tests/test_wi_convert.py`, caused by the integrator's
  own close: the Deliverable edit wrote the archived spec with CRLF line
  endings, which the spec parser refuses. Converted to LF; the module re-ran
  **22 passed**; `git ls-files --eol` shows no stray CRLF. The slow evidence
  modules (`test_adjudicate_brief`, `test_agent_loop_worker`) **101 passed**.
  `check_docs --stale` OK; `check_trajectory --strict` clean; `trace.py
  --strict-integrity` 0 integrity; `CURRENT.md` fresh; the open-items view up
  to date. Seconds **FAIL** at 956.7 s against 60 s (D10; eight builders were
  loading the box), recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=938348c1 -->

### Pause (2026-09-26): the second wave mid-review, handed to a coordinator

- **Reviews ran as chains** once codex answered (the Windows read-only
  sandbox needs `-c windows.sandbox="elevated"`; a first run without it was
  refused by policy on every command and produced no review). All seven came
  back NOT YET SOUND; the record and six arbitration rulings are in
  `docs/reviews/2026-09-26-assumption-tier-wave2/`.
- **Landed:** WI-645. **Ready:** WI-646 (reviewed, fixed). **Fixed, awaiting
  rebase:** WI-630. **Follow-ups interrupted by a session limit, uncommitted
  in their worktrees:** WI-629, WI-631, WI-632, WI-636, WI-637, WI-640.
  **Not started:** WI-647's (it waits for WI-636's).
- **Drafted, not filed:** twelve work items from the handoff's findings and
  this wave's, preserved in `docs/plans/2026-09-26-wave2-drafts/`; a
  backlog audit's cancellations, merges and re-scopes await the owner.
- **Resume surface:** `docs/handoff-2026-09-26-coordinator.md`, written for a
  coordinator that arbitrates and drives builders and Sol reviews; the status
  surface and both READMEs point at it.
- **Commit bar (the pause):** smoke **1697 passed, 3 skipped** in 188.1 s;
  `check_docs --stale` OK (0 broken, after flattening the copied reviews'
  absolute worktree links to plain `file:line` text); `check_trajectory
  --strict` clean; `trace.py --strict-integrity` 0 integrity; `CURRENT.md`
  fresh; the open-items view up to date. Seconds **FAIL** at 189.3 s against
  60 s (D10), recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=5c546358 -->

### The owner's decisions as open items, and the backlog cleanup (2026-09-26)

At the owner's request, before resuming from the coordinator's handoff.

- **Open items OI-86 to OI-94** (`docs/requirements/open-items.toml`, the
  OI watermark 85 -> 94), each with options, blast radius and a
  recommendation: the stand-in's re-attestations of SN-041..SN-044 (OI-86;
  the need tier has no drift detector, so neither the approval brief nor the
  open-items view surfaced them), SR-217's association timing (OI-87), the
  reserved D8, D14, D22, D29 and D10 (OI-88..OI-92), the stakeholder-status
  double report (OI-93) and SR-211's missing vacuity (OI-94). D30 needs no
  ruling. The spine map §6 and the handoff point at them.
- **Backlog cleanup**, from a read-only audit of the 41 unstarted items, the
  deferred one and the drafts, each verdict checked against code or commits:
  cancelled WI-596 and WI-597 (WI-635 removed their premise and wording);
  merged WI-607 into WI-621 (extended to the critique arm) and WI-611 into
  WI-606; rewrote WI-551 as WI-620's keep operation; re-scoped WI-539, WI-581
  and WI-582 to what remains (WI-582's satisfied `needs` removed); lowered
  WI-541 and WI-551 from P7 to P3; marked WI-644 `spine`; backfilled
  Done-when on ten items (WI-536 and WI-539 also gained the Context their
  bodies lacked); pointed WI-623 at the readability report's measures. The
  drafts: H folded into K (one amendment adjudication for the LLR registry),
  B widened, O added (census routing, ruling 2).
- **Deviation:** a stray re-run of the integrator's cleanup script doubled
  the four cancelled specs' Deliverable and one WI-606 bullet before the
  moves; found by count and removed, each spec verified to one Deliverable
  and one Context heading.
- **Findings, not acted on:** OI-82 and WI-577 attribute the "Surfaces to the
  owner" table row to PROCESS_OPTIONS.md §2a; it is §2a of
  `docs/plans/2026-09-01-approval-act-adjudicator-only.md`. WI-545's first
  obligation (re-point the size ratchet's debt owner from WI-521) has not
  happened; its Done-when now requires it.
- **Commit bar:** smoke **1697 passed, 3 skipped** in 398.3 s (a second run
  on the same tree; the first's result line was not captured and it measured
  440.8 s); `check_docs --stale` OK; `check_trajectory --strict` clean (645
  work items, 25 cancelled); `trace.py --strict-integrity` 0 integrity;
  `CURRENT.md` fresh; the open-items view up to date; `docs/status.md` 140 of
  its 160 lines. Seconds **FAIL** (D10, now OI-92), recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=afacb371 -->

### Coordinator session (2026-09-26): WI-646 lands

Resumed from `docs/handoff-2026-09-26-coordinator.md` as coordinator: four
builders at a time finish the interrupted follow-ups in their worktrees
(WI-629, WI-636, WI-640, WI-631 first, then WI-637 and WI-632), while the
coordinator integrates in the handoff's order.

- **WI-646 integrated** by cherry-picking its own commits (0312d591,
  91781421) without its stale WI-645 base. One conflict, TC-161: kept
  WI-646's method (a superset of trunk's) with WI-645's `tier = "Full"`.
  RESYNC entry re-anchored `[since 4aec3a2a]` -> `[since 1e20f9fb]`.
- **Amended, status left Approved, for the joint adjudication:** LLR-167
  `detail`, TC-161 `method` (already listed in the handoff's table).
- **This fragment's deferred-open-items line** read `none` although it cites
  OI-82 and OI-86..OI-94 since the owner's decisions were filed; corrected to
  name them (`gen_open_items --check` flagged the contradiction).
- **Commit bar:** smoke **1697 passed, 3 skipped** in 1261.6 s; the touched
  modules (`test_adjudicate_brief`, `test_baseline_snapshot`,
  `test_module_size_ratchet`, `test_resync_pack`) **159 passed**;
  `check_docs --stale` OK (0 broken); `check_trajectory --strict` clean;
  `trace.py --strict-integrity` 0 integrity; `CURRENT.md` current; the
  open-items view up to date. Seconds **FAIL** at 1270.4 s against 60 s
  (OI-92; four builders were loading the box), recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=1e20f9fb -->

### WI-629 lands — the assumptions registry, surrogates, requirement classification and form

- **Follow-up 6271c4b0** (the predecessor's uncommitted work, verified and
  finished by a fresh builder in the same worktree): TC-222 to Full in the
  slow module `tests/test_cell_classes.py` (ruling 1); `sr_form_findings(srs)`
  one-argument per LLR-224, adoption decided in `assumption_tier_findings`;
  the missing-copy exception narrowed to the assumptions registry
  (`FIRST_COPY_AT_APPROVAL`), with a conviction test that an established
  registry deleted with its copy is still reported. Red, taken by restoring
  5453f920's scripts: the form tests 6 failed; the ESTABLISHED cases 3 failed,
  1 passed (the SR-copy case the old code already reported, because SR has an
  approved row).
- **Integrated** by squash (base b14d1808). Conflicts: `docs/id-watermark`
  (highest marks; `--bump-ids` rewrote it), `RESYNC_PACK.md` (both entries,
  landing order; WI-629's re-anchored `[since 26c086dd]`).
- **Amended, status left Approved, for the joint adjudication:** TC-222
  `tier`. Traced pointer moved: TC-222 `evidence`.
- **Smoke membership re-stamped 1702 -> 1810** in `docs/stack.ini`: the
  +38 in-process pure-rule tests put the tier at a measured 1740; reason in
  the stamp's comment. The seconds budget is not moved.
- **Commit bar:** smoke **1 failed, 1736 passed, 3 skipped** in 2065.7 s,
  the failure being the membership ratchet above, then
  `test_smoke_budget.py` **3 passed** after the re-stamp; the touched slow
  modules (`test_assumptions_registry`, `test_cell_classes`,
  `test_baseline_snapshot`, `test_bootstrap`, `test_module_size_ratchet`,
  `test_resync_pack`, `test_trace`) **246 passed, 1 skipped**;
  `check_docs --stale` OK; `check_trajectory --strict` clean; `trace.py
  --strict-integrity` 0 integrity; `CURRENT.md` current; the open-items view
  up to date. Seconds **FAIL** at 2073.8 s against 60 s (OI-92; four builders
  loading the box), recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=26c086dd -->

### WI-630 lands — the reach check, the mediates cell and the need-frame gap advisory

- **Integrated** by cherry-picking its build commit b501e5f4 and applying
  its follow-up d1665f5c (ruling 3: the reach reports stay composed by
  `trace.analyze` into the warn pipe, pinned by a test driving it; IF-190's
  rationale reworded; fidelity judged only when `RealizedBy` resolves; the
  negative fidelity test asserts both findings) onto WI-629's landed form.
  No conflict: the handoff's warning that it edits the moved TC-222 test
  did not hold, since it touches neither `test_acceptance_record.py` nor
  `test_cell_classes.py`. RESYNC entry re-anchored `[since b0e693ac]`.
- No approved-row cell changed.
- **Commit bar:** smoke **1769 passed, 3 skipped** in 1410.0 s; the touched
  modules (`test_trace`, `test_cell_classes`, `test_resync_pack`,
  `test_module_size_ratchet`, `test_dogfood_sync`, `test_rule_sync`)
  **168 passed, 2 skipped**; `test_assumption_rules` + `test_stakeholders`
  **87 passed**; `check_docs --stale` OK; `check_trajectory --strict` clean;
  `trace.py --strict-integrity` 0 integrity; `CURRENT.md` current; the
  open-items view up to date. Seconds **FAIL** at 1412.8 s against 60 s
  (OI-92; builders loading the box), recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=b0e693ac -->

### WI-631 lands — assumption evidence on test cases, and the observation declaration

- **Follow-up 4b7b18f2** (ruling 6): an empty `AcceptanceRule` reads as
  absent again, reversing c6a43dd9's key-presence reading; each case asserts
  its exact findings. Red against c6a43dd9's rules: 2 failed, 67 passed (the
  two whitespace cases are the kept strengthening, green under both).
- **Integrated** by cherry-picking 378a49e9 and applying c6a43dd9 +
  4b7b18f2 onto WI-630's landed form. Conflicts, all additive (WI-630 and
  WI-631 each appended contracts, imports and rule sections to
  `assumption_rules.py`, `trace.py` and `test_assumption_rules.py`): both
  sides kept, WI-630 first; the two `kitlib.spine` import hunks merged;
  `trace.py`'s size ratchet summed (3425 +8 +34 -> 3467, confirmed by the
  ratchet test); `docs/id-watermark` highest marks; RESYNC entry
  re-anchored `[since 06ba0b1b]`.
- **Integrator's fix:** `gen_cases.py`'s legacy CSV paste header lacked the
  six test-case keys WI-631 added to the template
  (`test_gen_cases::test_csv_format_stays_available_for_the_legacy_carrier`
  failed on the merged tree: 11 columns against 17); header and row
  extended in template order.
- **Smoke membership re-stamped 1810 -> 1890** (measured 1816: WI-630's and
  WI-631's in-process rule tests), reason in the stamp's comment.
- No approved-row cell changed.
- **Commit bar:** smoke **2 failed, 1811 passed, 3 skipped** in 758.2 s:
  the CSV header and the membership ratchet, both fixed above;
  `test_gen_cases` **9 passed** after. The touched modules
  (`test_smoke_budget`, `test_evidence_partition`, `test_trace_coherence`,
  `test_trace_golden`, `test_trace`, `test_dogfood_sync`, `test_rule_sync`,
  `test_resync_pack`, `test_bootstrap`) **241 passed, 2 skipped**, with
  `test_derive_stage` erroring at collection under xdist (the known
  lone-module `kitlib` import, draft L) and **21 passed** run with
  `-p no:xdist`. `check_docs --stale` OK; `check_trajectory --strict` clean;
  `trace.py --strict-integrity` 0 integrity; `CURRENT.md` current; the
  open-items view up to date. Seconds **FAIL** at 760.8 s against 60 s
  (OI-92), recorded, not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=06ba0b1b -->
