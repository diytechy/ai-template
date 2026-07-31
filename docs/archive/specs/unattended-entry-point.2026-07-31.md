# Effort — the unattended entry point

> **ARCHIVED 2026-07-31 — effort complete.** This was the spec-of-record for
> work items **WI-374** (S1, the drive loop — `scripts/drive.py`, IF-015 v3)
> and **WI-375** (S2, the process-text truth pass) — both `done`;
> deliverables in `docs/work/archive/`, session record in `docs/log.md`.
> Archived per the spec lifecycle: close date appended to the filename,
> attributed WIs named.

Two slices restoring the thing Phase 5 removed by accident. **S1 builds the
mechanism; S2 makes the shipped process text true again** — in that order,
because the text can only describe a flow that exists.

**WIs:** WI-374 (S1) · WI-375 (S2) · **Filed:** 2026-07-31 (owner-directed,
in-session)

## Problem

`concurrency-restructure` Phase 5 deleted the parallel dispatcher — 4,042 lines
whose lifetime record justified it (19 reservations → 8 integrations → **0**
gate-verified, 11 hand-rescues, 36 stale worktrees). But that module was doing
**two** jobs, and only one of them was bloat:

1. the train / worktree / reservation machinery — the genuine bloat, correctly deleted; and
2. the **scheduling front end**: read the ready frontier, pick the next WI in
   build order, claim it, cut the branch, launch a worker session, repeat.

Job 2 went out with job 1, and nothing replaced it. Measured on trunk
2026-07-31:

- **Nothing calls the claim.** The only occurrence of `integrate.py claim`
  anywhere else in `project-trajectory/scripts/` is `bootstrap.py:1289`, which
  is the MAPPING row that *ships* the file.
- **The single entry point refuses.** A plain `agent-resume` double-click runs
  `agent_loop.py --root . --session-timeout 7200` (the launcher forwards `%*`,
  empty on a double-click). Driven with a no-op wired into `AGENT_CMD` so no
  real session could start: it prints `agent_loop: no role given …` and exits
  **2**. Nothing launches.
- **The back half is already automatic.** `integrate.py integrate` really does
  drain the queue unattended — it ran the full 40-step bar and merged WI-372
  with no human step.

So the walk-away loop is **automatic at the end and manual at the front**: a
human (or an attending session) has to decide "next is WI-280", run the claim,
and launch the worker. That is not what the kit's own process text promises,
which is S2's problem.

## S1 — The claimer: pack the traincar and start the car

**WI-374.** Restore job 2 above, and *only* job 2.

### Approach

**Compose what already exists; build no new machinery.** Every part is present
and independently proven — the gap is that nothing joins them:

| Step | Existing component |
|---|---|
| next ready WI in build order | `schedule.py` — `ready [--explain\|--format json]` (IF-053) |
| claim it, cut the branch | `integrate.py claim` (IF-080), with its own refusal ladder |
| build it | `agent_loop.py --wi <id>` on the claimed branch (IF-015) |
| merge it | `integrate.py integrate` — the serial fail-closed queue (IF-080) |

**Explicitly NOT rebuilt** — the deleted dispatcher is the worked example of
what this must not become: worktree pools, reservations, train grouping,
`docs/run-state`, disposition arms. The 2026-07-28 audit's finding stands —
enforcement-layer growth is this repo's dominant failure mode — so **if the
implementation starts to approach the deleted module's shape, stop and escalate
as a written case** (process-options.md, the design-escalation clause) rather
than shipping it.

**Start at ONE lane.** The dispatcher's record shows the failures lived in
parallelism, not in sequencing. A serial driver is the whole of this slice; a
second lane is a later change with its own argument. (`schedule.py` already
ships `simulate --jobs N`, so the ordering question is answerable without
building the concurrency.)

**Adds no authority.** The driver decides *ordering only*. Every refusal stays
where it already lives — the tracked `docs/work/pause`, a dirty trunk, the
SpecRef and status-prose claim rungs, the composed-tree bar, the RULING-7
verdict gate, `docs/push-policy`. A driver that can talk its way past one of
those is a defect, not a feature.

### Interfaces

Acts across module boundaries. Consumed seams, all resolving today:
`IF-053` (schedule's ready-frontier CLI/library), `IF-080` (integrate's claim +
serial queue), `IF-015` (agent_loop's explicit session roles).

**Whether this slice *provides* a new seam is its first design call, and the
answer decides the seam paperwork** — so no `Proposed` row is filed here rather
than guessing one that may be wrong. The two shapes:

- **A mode on `agent_loop.py`** (a plain launch drives instead of refusing) —
  then `IF-015` is **amended**, not added to. Its contract today reads
  "explicit session roles only", which is precisely the sentence that changes.
- **A new driver script** with its own CLI — then that is a new `Provides` row,
  filed `Status=Proposed` at that point. Nearest existing is `IF-015`,
  insufficient for exactly the reason above.

Prefer the first if it does not grow `agent_loop.py`, which is already 3,006
lines and a named target of the H-2 decomposition program.

### Done-when

- [ ] A plain `agent-resume` launch (no arguments) selects the next ready WI in
      the scheduler's build order, claims it, runs a worker session against the
      claimed branch, and drains the merge queue — with **no human step in
      between**.
- [ ] An **empty frontier** ends in the drained-queue banner at **exit 0** — a
      finished queue is success, not an error.
- [ ] Every existing refusal still fires and still stops the run: tracked
      `docs/work/pause`, dirty trunk, the SpecRef rung (WI-370), the
      status-prose rung (WI-358), a red composed-tree bar, and a missing or
      non-APPROVE verdict under `docs/review-policy >= 1` (RULING-7).
- [ ] `docs/push-policy: human` is honored — the driver never pushes, including
      when asked.
- [ ] The stall guard and iteration ceiling that process-options.md already
      specifies for walk-away runs apply to the driver's own loop.
- [ ] `NEEDS-HUMAN` still surfaces as the stop banner + **exit 7** with its
      one-line `ask:` headline.
- [ ] New tests cover: empty frontier, a refusing claim rung, a red bar
      mid-drain, and pause-mid-run. The smoke tier stays inside its declared
      `[smoke-budget]`.
- [ ] The net new code is **small**, and the WI's own record states the line
      count against the 4,042 that were deleted.

## S2 — Make the process text true again

**WI-375.** Documentation only, and **hard-gated behind S1** because the
section must describe the flow that actually ships.

### Approach

Two defects exist in `project-trajectory/PROCESS_OPTIONS.md` **today**:

1. **The promise is false.** "Unattended operation (walk-away runs)" (`:542`)
   opens *"Applies when a repo wants a coordinator to grind work from a single
   entry point while nobody watches"* — and that entry point currently exits 2
   with a map. The section then describes the model in terms of `integrate.py
   claim` and `agent_loop.py --wi` as steps, never naming what invokes them.
2. **A cited artifact does not exist.** The capability table (`:29`) lists
   `docs/run-*` as a mechanism of unattended operation. `ls docs/run-*` →
   *No such file or directory*; it was deleted with the dispatcher at Phase 5.

**Defect 2 is wrong regardless of S1.** If S1 stalls or is re-scoped, split
that half out and fix it alone — shipped kit text citing a deleted artifact is
an adopter-facing error with no dependency on any new capability.

### Interfaces

No cross-module seam — edits process text only. If S1 amended `IF-015`, this
slice checks the seam row's prose matches the shipped contract; it does not
change the row.

### Done-when

- [ ] The "Unattended operation" section describes the **shipped** flow end to
      end, naming what performs each step, with the single entry point real.
- [ ] The capability table row cites only artifacts that exist.
- [ ] Any other kit text promising the retired dispatcher's behaviour is found
      and corrected — the search is part of the slice, not an assumption that
      these two sites are all of them.
- [ ] Byte budgets on the budgeted files hold (`byte-budget-guard`), with the
      deltas reported in the WI record.
- [ ] `check_docs.py --stale` clean: no broken links, no citation of a
      non-existent path.
