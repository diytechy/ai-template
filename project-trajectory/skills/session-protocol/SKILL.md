---
name: session-protocol
description: Use when running a work-item (WI) or thread session in this template repo — how to read the plan, execute only the scoped work, pass the gates, write the session/WI log, and commit in this repo's style.
stacks: [any]
domains: [any]
phases: [dev, gate, release]
tags: [session, improvement-plan, workflow, commit-style, wi]
scope: this-repo
---

# Session protocol (this template repo)

How a WI/thread session runs here. The live homes: **`docs/status.md`** (what's
next), **`docs/work/`** (the WI registry — one spec file per item, status = its
directory), and
**`docs/log.md`** (the session/gate record). This skill is the fast path; the
process masters (`PROCESS.md` / `PROCESS_OPTIONS.md`) win when they disagree. The
kit's design history — the old thread specs and the WI-1.x log — is archived at
`docs/archive/IMPROVEMENT_PLAN.md` (context, not a working surface).

## 1. Read before doing

- Read `CLAUDE.md` (governs editing the kit) and `AGENTS.md` (the pointer stub).
- Read `docs/status.md` (the working surface — what's next) and the scoped WI's
  spec file under `docs/work/` (its directory is its status). The
  spec-of-record for a WI is what its `specref` points at (an SR and/or a plan doc); older landed work is in the
  archived plan. **Do only the scoped work** — no unrelated edits.
- If a stub is being revived, find and link its earlier backlogged form (search
  `docs/archive/scratch.md` + the stub threads) so the resolution is traceable.
- **Check `git status` first.** Residue in the working tree is from an
  interrupted session; reconcile it against the open WI's spec / Done-when
  *before* new work — verify-and-commit what is complete, discard what is not
  part of the scope, and record which in the log. (The unattended loop surfaces
  this into the session prompt; the judgment is yours — it never auto-stashes.)
- **Treat a declared-policy change as a status-staleness event.** In the same
  sitting, grep `docs/status.md` for pause/stop/approval
  language predicated on the old `gate_policy`, `push`, `review_rounds`, or
  `guardrails` value; point to `docs/process.toml` instead of paraphrasing it.

## 2. Respect the constraints

- **Byte budgets** on `AGENTS.template.md` (10,000) and `PROCESS.md` — see the
  `byte-budget-guard` skill. Push expansion to `PROCESS_OPTIONS.md` /
  `ADOPTING.md` / `EXAMPLE.md`.
- **Stdlib-only, cross-platform** kit scripts (Python 3.11+, Windows + POSIX).
- **Single source of truth:** state a fact once and link to it; don't paraphrase
  a rule into five files.

### Standing rules

Relocated here from `docs/status.md` (WI-477): they are durable doctrine, and
the working surface is forward-only — what must happen **next**, not what is
always true.

- **An id named in `docs/status.md`'s hand-authored prose CANNOT BE CLAIMED.**
  `integrate._status_prose_refusal` refuses it at claim time; generated blocks
  are exempt. Point at `docs/work/queued/` and let the generated frontier name
  ids.
- **Never revert a real fix, or sanction a check, to green a step.** Editing a
  declared list — a coverage floor, an orphan glob, a ratchet baseline — to
  clear a finding IS accepting what it measures. If a ratchet fires on
  legitimate work, re-stamp it deliberately and record the reason.
- **Signed claims + one-machine humility.** The recurring review-era defect was
  signed CLAIMS that pass every test (PROCESS_OPTIONS.md, "Signed
  measurements"), and **one machine is one data point** for any OS-behaviour or
  timing claim — state the condition, never the universal.
- **Measure on a tree whose line endings match the index.** Before trusting any
  byte count or hash, run `git ls-files --eol | grep 'w/crlf'` — only
  `*.ps1`/`*.cmd`/`*.bat` should appear.
- **Claiming runs through the integrator** (`integrate.py claim`); merges are
  its serial fail-closed queue, and a pause is a tracked `docs/work/pause`.
- **The coordinator adjudicates through `coordinator_adjudicate.py`, never a
  subagent.** Compose the brief, then run `python
  project-trajectory/scripts/coordinator_adjudicate.py adjudicate --brief-file
  <brief> --brief <class> --wi <WI> --verdict <path>` from the lane's
  worktree root (the primary checkout is refused), naming a verdict path not
  yet written, backgrounded (a call outlasts the shell's 10-minute cap). It
  rides the loop's keep operation and `out/adjudicator/` record, so successive
  adjudications resume one retained session. Its Claude home authenticates
  with the owner's long-lived token, read at each launch from the file the
  `AGENT_CLAUDE_TOKEN_FILE` environment variable names; the token is never
  read into a brief, log or commit. It is the launch's one environment
  credential: an ambient `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` or
  cloud-provider switch is left out, and a route declaring one (or `--bare`)
  is refused. Each retained launch runs the one registry row its caller
  selected. Settings-file credentials (`apiKeyHelper`, a
  settings `env` block, a managed gateway) are not checked: keep them out of
  this repo; store-lock contention is WI-858's.
  Exit 7 means that token is unset or unreadable, or the route conflicts:
  `... coordinator_adjudicate.py signin` reads the token, and the remedy is
  dev-setup's one-time `claude setup-token` step and that variable, never an
  interactive sign-in. Never substitute a fresh subagent.
- **A contested or repeated review finding goes to a dispute sitting before
  another build round.** When the builder or the coordinator contests a
  review finding, or a finding class reaches its third review round, the
  adjudicator rules it, not the coordinator by sending it back to the builder.
  Write the findings file (its shape: `scripts/kitlib/dispute.py`), compose
  the `dispute` brief over it (a row whose `Brief` is `dispute` and whose
  `Adjudicates` names that file, through `adjudicate_brief.compose`), and run
  the call above with `--brief dispute`. Each finding comes back FIX, DISMISS
  with a reason class, or ESCALATE to the owner; the ruling is final. Record
  each ruling in the response to the review and, when the run keeps one, in
  the lane's `docs/decisions/<branch>.toml`, as PROCESS.md §6 "Review threat
  model" says; a dismissed finding is never re-raised to the builder.
- **The coordinator renders its review and critique briefs; it never writes
  one by hand.** `python project-trajectory/scripts/review_brief.py review
  --wi <WI> --base <sha> --sha <tip> --scope narrow|full --tests <files>
  --scratch <dir> --out <brief>` fills the kit's reviewer template with the
  lane's facts: a narrow round adds `--findings <the round file it answers>`,
  and `--rubric docs/rubrics/kit-change-review.md` adds this repo's checks.
  `critique --wi <WI> --rubric docs/rubrics/scope-critique.md` renders the
  scope critique where a row is born. The reviewer writes its verdict to the
  scratch path the brief names, and `review_brief.py file --review <it> --sha
  <tip> --scope <scope>` validates it and writes the lane's round file
  (`docs/reviews/<lane>/NNN-REVIEW-A-<sha7>.md`), which the rollup reads.
- **A stopped lane CLOSES; it is never held by renaming its ref (OI-70).** The
  only sanctioned stop is the partial close (§4): the spec moves to the terminal
  `docs/archive/work/partial/` with a handback report an adjudicator then judges
  (queue a successor, or mint an open item). Parking a lane by renaming its
  branch ref away from its `docs/work/active/<branch>/` claim is BANNED — a lane
  must close or it gets lost, as the wi508 hold nearly was — and
  `check_trajectory` reports any active claim with no matching branch ref.

## 3. End green (gates)

Run the real checks and paste the real output — never a green you didn't produce:

```
python -m pytest -q -n auto -m smoke
python scripts/check_smoke_budget.py --mode enforce
python project-trajectory/scripts/check_docs.py --root . --stale
```

All three must pass before **each** commit — this is the **commit bar**, and it
means results AND seconds, not results alone (OI-52 ruling (a), 2026-08-23):
`-m smoke` is the fast per-commit tier; `check_smoke_budget.py --mode enforce`
is what makes the seconds a real bar rather than a claim a worker could read
"passed" over — it FAILS the commit when the tier's wall time breaches the
budget, instead of only being caught later in CI. The budget, re-tiered to fit
by WI-281, WI-496 (2026-08-23) and WI-652 (2026-09-27, OI-92 (b), after the
tier grew to 188 s on this repo's 4-core / 8-thread box): **≤ 60 s** wall,
declared in `docs/stack.ini` `[smoke-budget]` (26.4 / 26.4 / 25.7 s over three
quiet runs on that box at the WI-652 re-tier) so it stays a real smoke test —
"is it basically alive?", not a re-run of most of the suite. Tiering is
opt-out: smoke drops the **subprocess/scaffold-heavy** modules
(`tests/conftest.py` `SLOW_MODULES` — the hook/gate/scaffold/heavy-script runs
the commit hook and the gate re-exercise anyway), so a **new (in-process) test
is in the bar by default**. The runtime is its own budget item — declared
seconds (enforced locally now, not only in CI) + a deterministic membership
ratchet — in `docs/stack.ini` `[smoke-budget]` + `tests/test_smoke_budget.py`
(it bites if the tier grows back toward the full suite; re-stamp deliberately,
reason in the log). Run the **full** unfiltered suite (`pytest -q -n auto`)
once at phase close; mid-phase, only when it demonstrably fits inside one turn,
and never end a turn waiting on one. The
full `check.py --gate <gate>` is the **gate bar** (unfiltered suite + coverage):
it belongs to gate advancement, phase close, and CI, not to each
mid-phase slice; `--jobs 0` runs its independent steps concurrently. A per-WI
slice inside a phase ends at the commit bar (PROCESS_OPTIONS.md, "Phase
cadence"). New behavior needs new tests
(`tests/`); update `test_bootstrap.py` file lists and `README.md` kit-contents /
`bootstrap.py` `MAPPING` when the scaffold surface changes.

**A session's scratch has one dated root** (WI-840). Every review and
full-suite run passes `--basetemp`, and every reproduction file goes, under
`review-tmp/<date>-<session>/` (`review-tmp` beside the lane worktrees is the
one scratch root the review sandbox may write). Reuse one name per kind of run
across rounds, never a fresh name per round: pytest empties a literal
`--basetemp` only when that name runs again. Delete the dated root once the
session's results are recorded.

## 4. Record the work

- Close the WI by MOVING its spec file to the terminal directory its outcome
  names, under the archive (WI-504, OI-55 ruled (a)) —
  `docs/archive/work/complete/` when it shipped, `docs/archive/work/cancelled/`
  when it never will, `docs/archive/work/partial/` when you could not finish
  (that one is TERMINAL too, and it owes an immutable per-close report under
  `docs/handbacks/`: the report IS the close event, and the disposition row an
  adjudicator gets keys on its path) — and filling
  its `## Deliverable` body (status is the directory, never a field — and a
  `partial/` close leaves the Deliverable EMPTY, because the report carries the
  record and the spec's definition is deliberately byte-identical), and
  record a session entry for `docs/log.md`: one-line summary, deliverables,
  **deviations from spec**, **byte deltas on budgeted files**, and the
  `pytest -q` totals (match the style already there). A **driven figure** in
  the fragment/Deliverable — a total, a census count, a timing — follows the
  declared-figure convention (process-options.md "Signed measurements",
  WI-392): its line carries the producing command + revision (or its
  derivation) under the `fig:` marker, held to presence by
  `check_figures.py`. **Where it goes:** on
  the serial trunk lane, append to `docs/log.md` directly; on a work branch,
  write it as a fragment `docs/log.d/<WI-id>-<slug>.md` (starting with its
  `## <YYYY-MM-DD> — <title>` heading; links authored relative to
  `docs/log.d/`) — `trunk_step.py` compiles fragments into the log in merge
  order and deletes them. Never hand-edit `docs/log.md` on a work branch. A
  session that ends owing the owner a decision **declares it** in the fragment —
  `Deferred open items: OI-45` (or `… none — <why>`), checked at the commit bar
  by `gen_open_items.py --check` (process.md §5, OI-41 ARM 2).
- **A delegated decisions record is the owner's to rule.** Write each entry
  of `docs/decisions/<run>.toml` with `review` empty and no `owner` key. The
  owner sets `owner = "confirmed"` or `"overruled"`; an overrule's commit
  states the new direction in `review` and files or amends a queued or active
  work item citing `docs/decisions/<run>.toml#D-NNN`, or the ruling-sync step
  and the merge slot refuse it (process-options.md, "Delegated decisions
  record").
- **Section order inside the spec file is load-bearing.**
  `check_trajectory.parse_spec_deliverable` clips the body at `## Context`, so
  a `## Deliverable` placed *after* Context parses as EMPTY and the close reds
  (R-A hard error). `## Deliverable` before `## Context`, always.
- **Order the close against the verdict round.** Under `review_rounds >= 1` the
  merge queue wants a verdict that NAMES the branch's current **non-record**
  tree (`docs/reviews/` + `docs/log.d/` + `docs/iteration/` are excluded;
  `docs/work/` is not), so any commit after it that CHANGES that tree buys
  another round — and one that does not, cannot.
  Close **first** — Deliverable filled, spec moved to its terminal folder, any
  approving Status-change commit — and take the final verdict round **last**;
  never hand-merge trunk, since only the station's `refresh` commit is peeled.
  A correction the verdict itself demanded still costs a round: that is the gate
  working, not a defect (process-options.md, "The LLM-gate verdict protocol").
  **Do not hand-compile `docs/reviews/WI-<n>-REVIEW-A.md`.** Nothing in the kit
  writes it and the gate no longer asks for it: the round files a logged
  reviewer session produced ARE the record, and the readable per-scope summary
  is generated (`gen_verdict_rollup.py`). The legacy path still clears the gate
  during the migration window and says so on stderr — a WARN there means a lane
  merged on the fossil, not on its evidence.
- Update `docs/status.md` to point at what's next; don't leave a stale "next".
- **Coordinator close-out (the context guard, `[coordinator]` in
  `docs/process.toml`).** When the guard says drain mode is latched, the
  close-out is the same every time: (1) start no new claims or lanes (the
  claim refuses anyway); (2) bring every in-flight row to a safe point:
  land it, close it, or leave it committed on its lane and recorded in the
  handoff; (3) write `docs/status.md`, a handoff whose `## Session prompt`
  heading is followed by one fenced block the next session starts from, and a
  log fragment; (4) request the relaunch,
  `python project-trajectory/scripts/coordinator_guard.py request-relaunch --handoff <path>`,
  then end the session: the relaunch runs at its exit, never at `/clear` or
  `/resume`. Every coordinator close-out, latched or not, that requests no
  relaunch ends instead by handing the lease back as its last act after the
  handoff, `coordinator_guard.py handback --handoff <path>`, so the next
  session's `take` succeeds. The handoff also classifies each compaction the
  lease recorded (`coordinator_guard.py status`) as a **missed threshold**
  (auto-compaction before the latch), a **manual** compaction, or a
  compaction **during the drain**. A coordinator session takes the lease with `coordinator_guard.py
  take`; a crashed holder's lease is freed only by the owner's recorded
  `release --reason`, and a latch only by the owner's recorded `clear`, the
  holder's hand-back or the relaunched successor's take.
- WI ordering is derived from the registry by `schedule.py` (the DAG +
  `Priority` + gate class), not a hand-curated `docs/next-wi` — that pointer
  is retired (WI-180; process-options.md "Unattended operation"). When
  filing or triaging a WI, set `BuildTier` deliberately: `quick` for mechanical,
  off-spine work; `medium` by default; `strong` only for design-shaping or
  spine-touching changes — the worker session reads it from the WI row. Do
  not silently downgrade a declared route mid-loop.

## 5. Commit in this repo's style

- **Logical commits** — one per deliverable/thread, then a body explaining the
  *why* and any deviation (see recent `git log`). **Two subject forms, and the
  session type picks which** — enforced by nothing, stated here once so the
  `git log` stops looking like two conventions fighting:
  - `WI-<n>: <imperative subject>` — a session executing ONE work item. The id
    is the subject's first token so the log greps by id.
  - `<category>: <imperative subject>` — everything with no single WI to name:
    a sitting, a sweep, a merge, a review round, a triage
    (`sitting:`, `docs:`, `spine:`, `review:`, `tests:`, `open-items:`).
    Prefer a category that already appears in `git log`; the set is open.
- **Attribution footers are fine here** — add `Co-Authored-By:` as usual (this
  repo is not anonymous). Omit them only in a privacy-restricted / anonymous repo,
  where a tool trailer is itself a leak (process-options.md "Commit identity &
  privacy").
- **Do not push** unless explicitly asked; branch is whatever the plan header's
  **Branch:** line names.
