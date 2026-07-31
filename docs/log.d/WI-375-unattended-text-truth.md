## 2026-07-31 — WI-375: the unattended-operation text matches what ships (S2)

**One line:** every kit doc that promised the retired dispatcher's mechanisms
now describes the shipped flow — the plain-launch drive mode (WI-374),
`integrate.py`'s claim/queue, and nothing that no longer exists.

**Deliverables (all shipped kit text, no code):**
- `PROCESS_OPTIONS.md` "Unattended operation": the model paragraph now opens
  by naming the real single entry point — a plain `agent-resume` launch runs
  the drive mode (`drive.py`): frontier re-derived every cycle, claim →
  worker → serial merge queue, mid-run-filed WIs picked up in the same run,
  parked claims resuming on relaunch. The capability table row cites
  `drive.py`/`integrate.py` instead of the deleted `docs/run-*` (defect 2 of
  the spec — `ls docs/run-*` has been *No such file* since Phase 5).
- `PROCESS.md` §4: the coordinator sentence re-pointed from `docs/run-state`
  (deleted at Phase 5) to the stop banner + typed exit codes.
- `ADOPTING.md`: the "Unattended coordinator" bullet says what a plain launch
  now does; the v4 "Parallel dispatch" bullet is rewritten as the
  **retirement + upgrade recipe** (registry CSV → spec folder via
  `wi_convert.py`, drain old train worktrees, seed `[generated]`, delete
  retired-surface reliance — `AGENT_JOBS`, `docs/run-state`,
  `docs/rework-wi`, tracks/next-wi/run-phase, `refs/llm/*`,
  `docs/parallel-ready`); the WI-260 changelog bullet is marked *historical*
  with the serial verdict gate named as the same rule's live home.
- `skills/downstream-resync/SKILL.md` §3: the "Parallel-dispatch migration"
  recipe (AGENT_JOBS=2, --jobs 1 holds, parallel-ready sign-off — all
  retired) replaced by the **integration-seam migration**: registry flip,
  drain-the-old-scheme, retired-surface deletion, `[generated]` seeding, and
  the claim rung's SafetyClass note. Per-agent copies re-synced
  (`bootstrap.py --sync`; `skills-sync` OK, 12 copies match source).

**The sweep (part of the slice, per spec):** `docs/run-|run-state|AGENT_JOBS|
dispatcher` over `project-trajectory/**/*.md`. Remaining mentions are all
historical retirement records (PROCESS_OPTIONS' own "retired with the
dispatcher at Phase 5" notes, the seam section's design history) or generic
English ("gate or dispatcher" in EXTERNAL_SKILLS.md's mine-don't-install
rule) — none promises a retired mechanism as live.

**Byte deltas (byte-budget-guard):**
AGENTS.template.md untouched (10,000 budget n/a this WI);
PROCESS.md 64,301 → 64,319 (+18: the run-state → stop-banner truth fix);
PROCESS_OPTIONS.md 162,601 → 163,157 (+556: the entry-point model paragraph
+ the table-row citation fix). Both baselines re-stamped in
`byte-budget-guard/SKILL.md` (source + agent copies) in this commit.
ADOPTING.md 55,342 → 55,509 (+167, unbudgeted expansion home — the upgrade
recipe grew by what the deleted false promises had hidden).

**Deviations from spec:** none. Defect 1 needed WI-374 first (hard edge —
honored); defect 2 fixed here with it.
