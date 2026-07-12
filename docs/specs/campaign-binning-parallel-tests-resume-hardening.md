# Campaign binning · parallel tests · dirty-tree resume hardening — PLAN

**Status:** 🟢 **RULED BY DIRECTION (owner, 2026-07-11)** — three items from
owner direction ("scope those in" + the interruption-safety recheck).
Ingested as **WI-074…WI-076**. Per the campaign cadence, WI sessions end at
the **commit bar**; the coordinating close runs the one full gate.

---

## P1 — `Campaign` column + When-view binning (owner-directed) — ✅ DONE (2026-07-11)

**Owner intent.** Add campaign details to work-item history so the WI DAG
can be **binned like the software architecture** (the FB5 symmetry: WHEN-axis
binning = campaign, HOW-axis binning = CMP).

**Why now.** A WI's campaign membership is only durable in the archived
spec's banner and the log narrative — `SpecRef` is cleared at close, so the
registry has no queryable campaign trace, and the 67-done-WI flat DAG is past
legibility.

**Model.**
- **`Campaign` column** on `work-items.template.csv` + the meta registry — a
  **grouping tag in the `Workstream` precedent** (a mutable binning category,
  not an id-checked reference; empty = standalone; legacy rows read empty —
  never-breaking). Values are short slugs (e.g.
  `capability-expansion-2026-07-11`); the archived spec + log remain the
  narrative record, the column is the mechanical one.
- **The When-view bins by it:** the WI DAG in `PROJECT_STATE.html`
  containerizes campaign members like How-SW containerizes modules into CMPs
  — collapsed campaign containers, expandable members, cross-campaign
  predecessor edges aggregated to the container boundary (reuse the FB5
  `<details>`/aggregation idiom). WIs with no campaign render as today.
- **No right-sizing rule** (deliberate asymmetry): campaigns are bounded by
  construction (one re-attestation sitting each) — binning is presentation +
  query, no new gate.
- **Backfill honestly:** tag WI-053…059, WI-067…070, WI-071…073 with their
  three campaign slugs; older rows stay empty (no retroactive invention).
- **Docs:** the PROCESS_OPTIONS campaign paragraph gains the column (one
  sentence); template explainer row updated.

**Spine (working default):** expected **no SR text change** — an optional
grouping column mirrors `Workstream` (not vocabulary-checked; SR-037 already
covers registry validation generically) and the binned render sits inside
SR-038's existing roadmap-DAG claim. Verify at build; if honesty demands a
clause, it rides the pending re-attestation.

**Tests.** Column parses (and absent column = today's behavior byte-for-byte);
binned render deterministic + `--check` stable; campaign-less rows render
flat; boundary edge aggregation dedupes; meta smoke (three campaign
containers render).

## P2 — Parallel test execution (owner-directed) — ✅ DONE (2026-07-11)

**Owner question answered 2026-07-11:** the suite is fully serial — 625
tests, ~386 s, time spread across hundreds of subprocess/scaffold tests
(~0.5 s each), no hotspot; the G3 `tests+coverage` step (~726 s) is the gate's
long pole. The shape is embarrassingly parallel (every test isolated in
`tmp_path`).

**Model.**
- **pytest-xdist, `-n auto`** — the primary lever. The stdlib-only rule
  governs kit *scripts*, not the test tooling (pytest/pytest-cov precedent).
  Wire: `dev-setup` check row + `--install` set; `stack.ini [product] test`
  gains `-n auto` (the gate + CI parallelize with it); the smoke tier
  untouched; the kit's **template** `stack.ini` keeps the plain command with
  a commented `-n auto` line (a downstream repo opts in knowingly — its
  suite may not be xdist-safe).
- **Verify, don't assume (test-first):** (a) **subprocess coverage under
  xdist workers** — the `Coverage.current()` detection in
  `conftest.augment_env` must hold per-worker and the combined total must
  still clear the 80 floor; (b) the handful of tests reading the **meta**
  repo tree stay read-only-concurrent-safe; (c) Windows spawn overhead is
  acceptable (measure before/after wall time and record both).
- **Explicitly rejected:** test-impact selection (the FB1 ruling stands).
  The session-scoped shared-scaffold fixture is the recorded **fallback
  lever** if xdist alone disappoints — filed, not built.

**Spine (working default):** no SR change (dev tooling + the declared stack
command; SR-035 cross-OS CI claim unchanged — CI inherits the stack.ini
command). Record measured before/after times in log.md.

## P3 — Dirty-tree resume hardening (the interruption-safety recheck)

**Owner question.** An interrupted agent session can leave working-tree
artifacts; on agent-resume, will the next session notice the in-flight work
and recover?

**Honest answer (recorded).** The *logical* layer is interruption-safe by
design: progress = commits; an uncommitted interruption leaves the WI open
(R-A), named in status.md, its spec's Done-when ticks marking the frontier;
and the hook floor (R-A coherence, trace integrity, freshness byte-compares)
blocks a confused mixed commit. But **noticing is not mechanized** — the
preflight checks command/CLI/git/privacy/locks, not tree cleanliness, and no
protocol text tells a fresh session to reconcile residue. Recovery currently
depends on the agent's own `git status` initiative.

**Model (the thin slice — full stash/rollback stays deferred as WI-060).**
- **Detect + surface, never auto-stash:** at loop start (and each session
  launch), if `git status --porcelain` is non-empty, the loop (a) logs one
  line naming the dirty state and the file count, and (b) **injects a
  reconcile instruction into the session prompt**: *the working tree carries
  uncommitted changes from an interrupted session — before new work,
  reconcile them against the open WI's spec/Done-when: verify-and-commit what
  is complete, discard what is not yours to keep, and say which in the log.*
  Warn-and-surface only; blocking/stashing judgment remains WI-060.
- **Protocol text:** the session-protocol skill gains the same rule (source +
  fan-out, skills-sync); PROCESS_OPTIONS unattended section gets one
  sentence.
- **Stale-lock recheck (verify + report):** confirm a killed session's lane
  lock cannot wedge the next run (read the WI-025 lock code; if a stale lock
  blocks resume, fix minimally in-scope and test it; if it's already handled,
  record how in log.md).

**Spine (working default):** extends **SR-026/027/028-adjacent loop text
only if honesty demands** (the injection is prompt composition inside the
existing session contract); prefer no SR change — verify at build.

**Tests.** Dirty tree at loop start → the prompt carries the reconcile
instruction + the log line (clean tree → byte-identical prompt); porcelain
detection cross-OS; the stale-lock behavior as found; skill fan-out stays
byte-identical.

---

## WI mapping

- **WI-074** — P1 campaign column + When-view binning.
- **WI-075** — P2 pytest-xdist wiring + verification (meta repo opts in;
  template opt-in commented).
- **WI-076** — P3 dirty-tree detect/surface + protocol text + stale-lock
  recheck (WI-060 full stash/rollback stays deferred).
