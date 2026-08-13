# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. This file is **forward-only**:
only what must happen **next** lives here. Everything backward-looking has a
home elsewhere — don't restate it here:

- **What shipped / verdicts / session record:** [log.md](log.md).
- **Owner decision surface:** [open-items.html](open-items.html) — generated
  from [requirements/open-items.toml](requirements/open-items.toml): one row per
  pending decision (blast radius, options, recommendation) plus every spine row
  owing a ratification or re-attest, with its before/after. A ruling appends to
  the log's Decisions and the row leaves `pending`.
- **The WI registry (every backlog + deferred item, with its reason):**
  [docs/work/](work/) — one spec file per work item, **status = its
  directory** (the Phase 2c flip; the CSV is retired) — the dashboard is the
  root [`PROJECT_STATE.html`](../PROJECT_STATE.html).
- **Spec-of-record + rubric conventions:** [specs/README.md](specs/README.md) ·
  [rubrics/README.md](rubrics/README.md) (dogfooded scaffold boilerplate).
- **The restructure design (this branch's purpose):**
  [concurrency-restructure.md](concurrency-restructure.md) — parallel out of
  the box via git + a thin integration seam, **local-first**. **ALL FIVE
  PHASES ARE EXECUTED** (per-phase records in §7; all eight §9 rulings
  answered 2026-07-28). Phase 5 — the deletion — landed 2026-07-29: the
  dispatcher (4,042 lines) and its machinery are gone, the CSV registry home
  is dead (RULING-4 fully realized), PROCESS_OPTIONS rewrote onto the seam
  model, and the audit's approved WI retirements executed. **Its spine
  amendment window is CLOSED** — attested at the 2026-07-29 sitting, ruling
  in [log.md](log.md)'s Decisions; the restructure has no open act.
- **START HERE (current as of 2026-08-13, post-charge-through):**
  [handoff-2026-08-13-charge-through.md](handoff-2026-08-13-charge-through.md)
  is the boot document. The pre-absence batch ruling
  ([log.md](log.md#decisions-log), 2026-08-13) ruled all fourteen open items;
  the charge-through then EXECUTED fifteen of the sixteen opened programs —
  the re-attest batch applied, P5 adopted provisionally, the carrier program
  finished (every registry on TOML), the eight-rung stage ladder LIVE
  (`docs/gate` speaks DevBar/DevStg; author stage vocabulary, never G-tags),
  the hats roster, the re-sync pack. The remaining queue lives in the
  handoff, in order — the ladder program's deferred codex round, the boundary
  seeds, the common-module inversion, the Area→aspect execution, the
  perspective-coverage record. The owner's return reads
  [plans/2026-08-13-sitting-pack.md](plans/2026-08-13-sitting-pack.md); the
  owed human acts are the consolidated re-attest sitting and merge-to-main.
- **START HERE if you are picking up after 2026-08-01** (superseded by the
  line above for the sitting itself):
  [handoff-2026-08-01.md](handoff-2026-08-01.md). Most of the concurrency-v2
  program is built and merged. **The refresh red that blocked both open lanes is
  RESOLVED** (§2's resolution box; the account is in [log.md](log.md)): it was
  two causes, not one, and the hypothesis §2 records as "tested and refuted" was
  the correct one — so read §2 top to bottom, not just its opening claim. **Both
  lanes are now merged and NO lane is open** — the second merged as a
  **cancellation**, so the refutation is a trunk fact rather than a deleted
  branch. Every lane worktree has been unloaded, every lane branch and the
  leftover candidate branch deleted, and machine-local residue is back to none;
  what is claimable is the generated frontier below. The handoff also records
  which of the
  session's pitfalls came from the work and which came from driving four lanes
  by hand when the shipped loop is serial — read that before deciding how to run
  the rest, and read its **§6** for the two findings the resolution produced that
  have no id yet.
- **RESUME HERE (2026-08-11) — the carrier migration is LANDED; batch-2 is
  half done.** [repo-lock.md](repo-lock.md) **§2 D-5** ruled one TOML carrier and
  it is **executed**: all four spine tiers, then **§8.1's batch-2 first slice** —
  `open-items` and `agents`, with their templates. Nothing here needs applying;
  `docs/plans/2026-08-10-carrier-cutover.patch` is **spent history**, not an
  instruction.

  **§8.1 is FINISHED (2026-08-13):** the last two registries —
  `interfaces` and `components` — joined the TOML carrier once their rulings
  landed (OI-14 part B rewrote what an IF row holds; the partition ruling
  re-drew the CMP rows), each converting exactly once as sequenced. The IF
  tier changed shape with it: `Status` retired, `Signal`/`Rationale` added, a
  warn-first schema tier over both. The adopter recipe is the pack's
  carrier-batch-3 entry.

  **The one lesson a fresh session must not rediscover: THE CUTOVER IS THE
  DETECTOR.** Wiring readers while the old carrier still exists can never
  surface an unwired one, because every reader looks fine while the file it
  expects is still there. Run the conversion against a throwaway clone *first*,
  then fix what actually breaks. It caught three fail-open readers in batch-2
  alone; repo-lock §2 D-5 "Step 3" records the spine's.

  **Two rules that now hold for every registry on this carrier:** an id
  containing a `.` must be **quoted** in its table header (written bare it is
  still valid TOML and the row silently disappears), and a carrier that does not
  parse is reported **absent, never empty** — `{}` on a decision queue means
  "nothing is waiting on you".
- **THE PROGRAM IN FLIGHT — the fully mechanized loop (SN-028 · SN-029 ·
  SR-137…SR-146):**
  [plan-2026-08-08-mechanized-loop.md](plan-2026-08-08-mechanized-loop.md).
  Read its **§11 Addendum first** — it supersedes the earlier sections where
  they conflict — then **§12, the erratum**, which corrects six claims in the
  plan's own text that were re-verified against source (a function name that
  does not exist, a hook that reads a different file, an off-by-one line
  number, a column that is not on the TC registry, a mis-stated `Modified`
  count). Executed on a dedicated infra branch **outside the loop's own
  machinery**, per the plan's execution-mode directive: these changes rewrite
  that machinery, so the spine rows the program mints are the *record* of the
  work, ratified at the end, not the vehicle for it.
- **THE LOCK PROGRAM — living scope and decisions until the repo is locked:**
  [repo-lock.md](repo-lock.md). Where owner rulings accumulate while the
  mechanized-loop program is closed out: **D-1** (the attestation anchor moves
  onto the spine row; `attestations.csv` retired), **D-2** (stakeholder needs
  gain fields rather than a new carrier), the four open questions those raise,
  and the ordered close-out checklist that defines "locked". Read it *with* the
  handoff below, not instead of it — the handoff is the record of what was
  built, this is the record of what is being decided.
- **The drain plan for the remaining backlog:**
  [backlog-plan-2026-08-01.md](backlog-plan-2026-08-01.md) — the serial build
  order for the queued rows, the standing rules every builder inherits, and the
  owner rulings with their context. One of its rules still binds
  mechanically: **a work branch never mints a new work-item id** (the
  merge-slot rung shipped 2026-08-01). Its **park is LIFTED** — the two
  decisions that park waited on were ruled (no live row remains in
  [requirements/open-items.toml](requirements/open-items.toml)), the
  2026-08-02 park that replaced it was a context-budget pause only, and
  `docs/work/pause` was deleted in a tracked commit on 2026-08-02 to open
  this drain.
- **Resuming in a new session — boot HERE, then
  [concurrency-v2.md](concurrency-v2.md), which is the spec-of-record for the
  whole queued backlog; the design is CLOSED and its ten 2026-07-31 rulings are
  in the [log's Decisions](log.md#decisions-log).** The backlog is claimable as
  it stands, but **do not drain it with a plain `agent-resume` launch**: some
  queued rows rewrite the very machinery the loop runs (the dispatcher's
  banner arithmetic; `intake.py`'s sweep arm), and `integrate.py` calls
  intake at every merge slot — so an unattended pass would integrate the
  later rows through code the earlier ones had just rewritten, with nothing
  reviewing that composition. Owner direction 2026-08-02: drain the queue
  **serially through the station in a session**, and hold the spine-class
  program close for a sitting with the owner present. The row ids and the
  full reasoning are in the 2026-08-02 session entry in [log.md](log.md);
  the queue itself is [work/queued/](work/queued/).
  The older
  [handoff-2026-07-29.md](handoff-2026-07-29.md) is now **history, not a
  queue** — its sequenced work is all closed; read it for the post-Phase-5
  account only. The working
  program [concurrency-restructure.md](concurrency-restructure.md) is
  EXECUTED through Phase 5 (§7 records), its windows all closed (the fourth
  and last 2026-07-29 sitting blessed the Phase 5 amendment; gate **DevBar-Release, all
  four phases**). **The 2026-07-29 grind session built, reviewed and closed
  the entire queued backlog** (records in the registry and the log's session
  entry); **the 2026-07-30 session closed both render follow-ups through
  the integrator's queue — its first real drain — fixing the two latent
  integrator defects it surfaced** (the session entry in [log.md](log.md)
  records the drain, the RULING-8 attended-serial escape, and the R-E
  intake debt). **That follow-up queue is now drained too** (2026-07-30/31).
  **The walk-away loop is whole again end to end** (2026-07-31): a plain
  `agent-resume` launch drives frontier → claim → worker → serial merge
  queue, re-deriving the frontier every cycle (the unattended-entry-point
  effort closed through the integrator's own queue; spec archived at
  [archive/specs/](archive/specs/), record in [log.md](log.md)).
  **The H-2 decomposition program is EXECUTED and merged** (2026-07-31):
  the production split left `gen_trajectory.py` a 949-line facade over six
  sub-threshold siblings and `bootstrap.py`'s `main()` a 48-line sequencer
  (both size/complexity entries retired or deleted, not re-stamped up), and
  the test split followed it — all four monoliths cut along the same
  seams, proven by AST rather than asserted. **The one thing a successor
  most needs to know from that program:** a downstream migration found what
  no in-repo check could — `bootstrap.py`'s MAPPING had omitted
  `schedule.py`, so every *fresh scaffold* raised `ModuleNotFoundError` on
  its first claim while this repo stayed green, because the kit's own
  `scripts/` dir holds every file and an adopted repo carries the module
  from an older kit. The instance is fixed and the CLASS is now guarded
  (`test_every_sibling_imported_module_is_shipped_by_mapping`) — but the
  lesson is the general one: **a scaffold-surface change is only verified
  by bootstrapping a scaffold.** The frontier now holds the follow-ons
  filed this session; scope is in the rows.
  Standing habit that survives the restructure: run
  `check_trajectory.py --strict` directly, unfiltered, before claiming
  anything done — the DEFAULTED pre-commit floor stays warn-first by
  design, so the floor's output is never the strict bar. The
  [handoff-2026-07-28c.md](handoff-2026-07-28c.md) §3 deferred-row
  dispositions are RULED and EXECUTED (2026-07-29): six rows retired with
  their reasons in the registry, and the two survivors were promoted to
  `queued` on 2026-07-31 — **the deferred set is now empty**. The
  pre-restructure
  handoffs ([2026-07-28b](handoff-2026-07-28b.md) and earlier, plus
  [wrap-up-plan.md](wrap-up-plan.md)) are history: read them for the
  account, never as open tasks.
- **The concurrency-v2 design — [concurrency-v2.md](concurrency-v2.md) —
  is CLOSED and RULED** (2026-07-31; six entries in [log.md](log.md)'s
  Decisions). **The rows it produced are `queued` and claimable now** — read
  them in [work/queued/](work/queued/), which is where their ids and scope
  live. *(No id is named in this file on purpose: an id in hand-authored
  status prose is refused by the claim rung — see the standing note below.)*
  Its governing principle is the owner's: **prefer a constraint that makes a
  bad state unrepresentable over a check that detects it** — the answer to why
  enforcement-layer growth keeps recurring despite the 2026-07-28 audit naming
  it. Read the doc's **Part I**, where every statement is labelled `(OWNER)`
  or `(DERIVED)`; questions A–F and follow-on decisions 1–7 are all ruled.
  **What a successor most needs from it — the station protocol (§A2):** a
  branch may not enter the merge queue unless trunk is already its ancestor.
  That one line makes a merge conflict *unrepresentable*, collapses two bars
  into one run on the branch, and catches composition failures on the real
  composed tree for free — which is why the drain-grouping row retired unbuilt.
  It **works at `lanes = 1` and needs no dispatcher**, so it is the row to take
  first if only one is taken; three rows depend on nothing at all. §A2's single
  empirical precondition (lane-side `trunk_step` determinism) was **measured and
  holds**, and forced one rule that must be built with it — the refresh is a
  **disposable commit**, because `log.md` is append-compiled and a stacked
  second refresh would conflict. Also ruled: every lane ends in a merge
  (`merged | cancelled | partial`, no fourth option, so no branch hangs — SR-144 replaced `handback` with the TERMINAL `partial/` plus an immutable per-close report); the
  scheduler splits into two axes (`exclusive|parallel` + rank) and session
  grouping is removed, not wired; gate policy is the dispatcher's authority dial
  (`attestation` work drains-and-surfaces while the in-process tier is
  human-held, dispatches once it is not — ruled against the
  `attended`/`autonomous` enum, which has since become the
  `human_ratification_through` ordinal), and adjudication mints its WI
  **mechanically, with no model**.
  Two findings came out of ruling the follow-ons, both now in a row's scope: the
  **verdict gate must key off the outcome, not the claim** (else a handback
  deadlocks demanding an APPROVE for work being *returned*), and
  `retired`/`cancelled` are **one state one rename apart** — the two rows
  retired here are inputs to the state-model migration, not a competing
  vocabulary. A separate row carries the flow into
  [`PROJECT_STATE.html`](../PROJECT_STATE.html)'s **Process tab** (owner
  direction), verified with the `render-dashboard-critique` skill rather than by
  reading the generator — the tab still draws the two-intersecting-hoops picture
  that predates the station model, and a concurrency diagram is exactly the
  thing that reads correct in source and wrong on screen.
- **An id named in hand-authored `status.md` prose CANNOT BE CLAIMED.**
  `integrate._status_prose_refusal` (the claim-time rung) refuses it outright
  — not only for `done` ids, which is all the R-D guard catches. This bit for
  real: at the 2026-07-31 close the sole `ready` row on the frontier was
  **already unclaimable** at HEAD because an earlier session had named it in the
  prose here. Generated blocks are exempt (the frontier list legitimately names
  queued ids). **So: never write a live WI id into this file's hand prose** —
  point at [work/queued/](work/queued/) and let the generated block name it.
  The ratify/verdict-freshness row is reframed onto this design and now carries
  a hard predecessor edge on the cell-split row, so the ordering is mechanical
  rather than prose — read both in [work/queued/](work/queued/).
- **Design history:** [archive/](archive/README.md).
- **RULING CLOSED (2026-08-08), shipped as SR-144 + SR-145** (under SN-027; the
  obligation was written as SN-031 until the 2026-08-10 sitting ruled that tier
  mis-levelled and demoted it). [handback-contract.md](handback-contract.md) asked whether a returned lane writes a per-return document. It does: a lane that cannot finish closes into the TERMINAL `docs/work/partial/` and writes one immutable report under [`docs/handbacks/`](handbacks/README.md) naming the outcome, the reason, the commit range and the keep/discard split. The report IS the close event's identity, which is what dissolved the starvation class five mutable-proxy dedup mechanisms died on. The four rows that waited on it — WI-413, WI-416, WI-417, WI-418 — are all disposed in `docs/work/cancelled/`. **Nothing is paused.**


- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) (this repo has
  no scaffolded `docs/process.md`; the masters are the reference).
- **Working rules:** [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill.

---

## Current State

<!-- BEGIN GENERATED STATUS -->
_Derived facts — regenerated by `python project-trajectory/scripts/gen_trajectory.py --status`; do not hand-edit (the forward-only intent below is hand-authored)._

- **Stage:** **DevStg-Needs** (stage 0 of 8, vision and stakeholder needs in work) · next bar: **DevBar-Reqs** (per-phase `1=DevBar-Tests;2=DevBar-Tests;3=DevBar-Tests;4=DevBar-Below;5=DevBar-Below`, derived current **phase=4**) — a repo is IN a stage and CLEARS a bar; the harness at that bar is the bar. [`derive_gate.py`](../project-trajectory/scripts/derive_gate.py) derives both, cached to [`docs/gate`](gate).
- **Spine:** **SN=27 SR=148 LLR=151 TC=148** (51 drafts) · 113 seams · 4 components.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-448** `P3` — OI-16 execution (inversion confirmed by the owner 2026-08-13): the common-module program
  - **WI-442** `P2` — OI-28 execution beyond the boundary declaration WI-441 carries: land the spine rows
  - **WI-451** `P2` — The SR-tier boundary conformance pass (owner-raised 2026-08-13, sitting decision 2.7): a…
  - **WI-390** — PROGRAM CLOSE for concurrency-v2 (docs/concurrency-v2.md §A9 deletion ledger). NOT a swee…
<!-- END GENERATED STATUS -->

- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~3.3 min) +
  `python project-trajectory/scripts/check_docs.py --root . --ignore docs/test/report.md --ignore "docs/work/*" --stale`,
  both green. At slice/phase close: the full suite `pytest -q -n auto`
  (~4.2 min) and `check.py` at the derived gate — every DevBar-Release step, including the
  DevBar-Release-only `lint` and `--require-verified`, the `--strict` trajectory
  step, and the `status-map` freshness gate on the snapshot above. The
  forward-only intent lives **below** the marker; the derived snapshot above is
  generated (never hand-edited).
- **ONE test run is capped at 50% of the machine. Whether TWO share that 50% is
  the host's answer, not ours.** On Windows the root `conftest.py` puts a run's
  whole process tree — controller, xdist workers, and every subprocess they
  spawn — into one **named, hard-capped job object**, and drops it to
  `BelowNormal` so the desktop stays responsive. That tree-wide part is
  unconditional (job membership is inherited). Concurrency is not:
  `AssignProcessToJobObject` succeeds only if the process is in **no** job, or
  the target is empty or in its own parent job chain — so a second run **joins**
  the shared ceiling on a plain desktop, and gets **its own 50%** when something
  has already jobbed it (sandbox, container, CI agent), warning on stderr.
  On POSIX there is no cap at all — `os.nice(5)` is a priority bump. **Two
  claims here have already been wrong in opposite directions** — "all runs share
  one ceiling" ([127-REVIEW-A](reviews/127-REVIEW-A.md)) and then "a second
  process tree always gets its own" ([128-REVIEW-A](reviews/128-REVIEW-A.md),
  whose evidence was that the guard passed here and *failed* on the reviewer's
  host) — so state the condition, and note that
  `tests/test_cpu_cap.py` now **constructs** the topology it measures rather
  than inheriting the runner's. Dial with `PYTEST_CPU_CAP` (`off` disables); CI
  opts out. Measured cost on this suite: none worth reporting (it is
  subprocess/IO-bound). **Don't reach for the dial to make a slow run faster** —
  the 50% is the owner's declared constraint, pinned by a test, and changing it
  is a reviewed edit with a reason in the log.
- **AN AMENDMENT WINDOW IS OPEN, and it is the biggest one this repo has
  carried: `drafts=33 modified=21`, gate derived DevBar-Reqs.** That is not drift — it
  is the machinery reporting exactly what happened. The 2026-08-08
  mechanized-loop program ([plan](plan-2026-08-08-mechanized-loop.md)) built
  five needs' worth of machinery on a dedicated branch, outside the standard
  workflow the plan itself sanctions, and filed the spine rows as the
  **record** at the end rather than as the vehicle. Those rows are `Draft`
  because **ratification is the owner's act** and that program's §10 reserves
  it for the P0 sitting; a Draft SN reads DevBar-Below, so the gate dropped. The drop IS
  the signal — "a new phase is due" — and the honest state is that the code is
  built and tested while the requirements behind it are proposed, not accepted.

  **A full handoff for a fresh session** — the open design question on
  `attestations.csv`, what the sitting owes, the queued rows, the known
  warn-only residue, and this machine's environment gotchas — is
  [handoff-2026-08-08-mechanized-loop.md](handoff-2026-08-08-mechanized-loop.md).

  **What the sitting owes.** Ratify or amend SN-028..032 and their
  decomposition (SR-137..146, LLR-155..164, TC-150..157), combined with the
  re-attest already owed from 2026-08-07 — the per-cell before/after is in
  [open-items.html](open-items.html). Until then the loop's ADJUDICATE routing,
  the ordinal and the outcome model are live code answering unratified
  requirements — a legitimate state to be in, and a bad state to be in
  silently. **The attestation ledger is no longer among them:** D-1 retired
  `attestations.csv` (the anchor moves onto the artifact's own row), so SR-140
  and SN-029 are ratified in their amended, carrier-neutral form. The anchor
  itself — and with it the `intake.py attest` step this bullet used to name —
  waits on the registry-carrier ruling (OI-12). Scope, rulings owed and the
  ordered checklist: [repo-lock.md](repo-lock.md).

  **The spine being attested and the harness being green stay different
  claims.** The second one holds: the full unfiltered suite is green, and
  `check.py` runs at the derived gate. The first one does not, and will not
  until the sitting.
- **A window lowers the bar; it no longer blinds it** (owner ruling
  2026-07-27, implemented and then corrected). While pending rows hold the gate
  down, the steps the higher gate requires run **advisory** — reported,
  warn-only, exit code untouched — so a regression surfaces at the commit that
  causes it instead of in one lump when the window closes. Two things to know
  before reading the output: the advisory tier is built from the **higher
  gate's own step table**, so `traceability` legitimately appears in both tiers
  (the DevBar-Release form carries `--require-verified`, the gating DevBar-Tests form does not); and
  the trigger is **not** "any drafts" — `modified>0` alone opens a window, while
  drafts additionally need the spine to have **demonstrably climbed**. That last
  test is now measured rather than inferred: `derive_gate` publishes
  **`ex-draft=`** on the `# basis:` line — the same gate arithmetic run with the
  draft rows removed — and drafts open a window when that clears **DevBar-Tests** and sits
  above what the drafts produced. It replaced a per-phase heuristic that could
  not see a *single-phase* repo's maturity at all (a Draft there drops the only
  phase to DevBar-Below, erasing the evidence), which is the blind spot 128-REVIEW-A
  found; the heuristic survives only as the fallback for a gate file written
  before the field existed. **Downstream note:** `docs/gate` must be
  regenerated once for the new field to appear — the ordinary
  regenerate-a-generated-artifact step, and `--check` says so.
  **The standing lesson holds either way:** a window is a *cost* that accrues
  per day it stays open — and advisory output is a warning, not a gate.
- **Measure on a tree whose line endings match the index, or the measurement
  lies** (standing rule from the 2026-07-27 census fix; the account is in
  [log.md](log.md)). A tracked file can sit CRLF on disk against an LF index and
  an `eol=lf` attribute, invisible to `git status`, because the clean filter
  normalizes on the way in — and that one fact produced three separate false
  records here: a duplicate census stamped on a **mixed** tree (a different and
  wrong set of blocks, not merely mis-fingerprinted ones), the byte-budget delta
  [127-REVIEW-A](reviews/127-REVIEW-A.md) refuted, and a `pre-commit` hook in the
  CRLF form `.gitattributes` warns breaks `#!/bin/sh`. (The census itself is gone
  — repo-lock D-7, 2026-08-11 — but the EOL hazard it exposed is not, and the other two
  measurement classes are still taken here every week.)
  **Before trusting any byte count, hash, or fingerprint measured here, run
  `git ls-files --eol | grep 'w/crlf'`** and check the attribute column — only
  `*.ps1`/`*.cmd`/`*.bat` should appear. `check_vendored.py` carried the same
  flaw and no longer does — it hashes the CONTENT, sniffing binary so a PNG is
  not normalized into a false match (the close record is in [log.md](log.md)).
- **Standing rules from the 2026-07-25 close:** **never revert a real fix, or
  sanction a check, to green a step** — editing a declared list (a coverage
  floor, an orphan glob, a ratchet baseline) to clear a finding IS accepting
  what it measures. (The duplication census used to be the worked example of
  this; it was torn down 2026-08-11 under repo-lock D-7, and the rule is the half that
  survives.)
  (`perceptual-stale` retired with the SR-054 flip at the 2c amendment —
  render changes now owe the *periodic advisory* critique, not a gate.)

- **Claiming runs through the integrator.** Claims are `integrate.py
  claim` — the §2.3 serial trunk move + branch cut — and merges are its
  serial fail-closed queue; a future pause is a new tracked
  `docs/work/pause` (TOML `reason`/`since`), the ONE pause home since Phase
  5 deleted the legacy half. `agent-resume` now boots explicit session
  roles only (`--wi` on a claimed branch / `--interactive` / `--dual-plan`)
  — the dispatcher it once launched is DELETED, and a plain launch refuses
  with the map.
  **Route note that survives:** probe providers before planning a critique
  dispatch, and route by PROVIDER, not by gateway (the OpenCode-Go gateway
  returned nothing to a `kimi-k3` probe 2026-07-26; `codex` answered in
  seconds both times — a genuinely non-Anthropic critic is the *stronger*
  SR-084 path).
- **Machine-local residue: NONE** (re-verified 2026-08-01, after the four lane
  worktrees left loaded by the concurrency-v2 drain and the leftover candidate
  branch were unloaded):
  `git for-each-ref refs/llm/` is empty, `git worktree list` shows only the
  primary checkout (Phase 0 cleaned the train residue; the Phase 4
  acceptance's work and candidate worktrees were removed at drain), and no
  `wi-*`/`integrate/*`/`llm/*` branches exist. Standing rule if residue ever
  reappears: before deleting a worktree or branch, diff it for **orphaned
  files**, not just merged work — the 2026-07-26 train held two
  `docs/iteration/` session logs that existed nowhere else (see
  [log.md](log.md)).
- **Open-items policy** _(`OI-N` ids are stable and never renumbered;
  ratification history lives in [log.md](log.md) Decisions; the ratification
  level in [process.toml](process.toml) is
  **`human_ratification_through = 0`** — nothing is human-held, the owner's
  2026-07-15 directive carried onto the ordinal the retired
  `attended`/`single-ratify`/`autonomous` enum was replaced by — so the loop
  does **not** pause on the open items projected above; each item's depth is in
  [open-items.html](open-items.html))._
- **Ready frontier:** see the generated **Ready frontier** list in the snapshot
  above — derived from the scheduler in build order (`Priority 1` rows first);
  a closed WI drops out automatically, so this surface never strands a done id.
  The 2026-07-23 agent-resume run's outcome — what integrated, what parked, and
  the defects it surfaced — is in [log.md](log.md).
- **Deferred backlog: EMPTY.** The last two `deferred` rows — the H-2
  decomposition program — were promoted to `queued` on 2026-07-31 at the
  owner's direction, so the whole registry is now archive + frontier with
  nothing parked. Each row carries its own reason and scope in
  [docs/work/](work/); read it there, not here. Six earlier deferred rows
  retired at the 2026-07-29 ruling (reasons in their archived rows).
  **Two things neither the frontier list nor the rows say, and a claimer
  needs:** the ordering guard between the two halves is a **soft** edge
  (`~`-prefixed — it orders, it does not block), so nothing mechanical stops
  the test split being claimed first, out of order; and the production half
  touches **shipped** modules (`gen_trajectory.py`, `agent_loop.py` — both in
  `bootstrap.py`'s MAPPING), so its split changes MAPPING,
  `test_bootstrap.py`'s file lists and the README kit-contents, and would
  force adopting repos to resync. Expect an attestation window with it: the
  `Contracts:` seam declarations and the generated arch-map both move when a
  module splits.
- **Perceptual debt gates NOTHING since the 2c amendment.** SR-054 — the last
  `Verification=Critique` row — flipped to `Test` (RULING-5, attested
  2026-07-29), so `perceptual-stale` and the fail-closed critique gate are
  retired. What remains of the two half-bound clauses — T4's document-wide
  "is this truncation actionable" and T8's "crossings minimized, in open
  space" — is judged by the **periodic advisory critique** (spec §3.3/§4);
  T8's shared-corridor half got its design pass 2026-07-29 (the port-fan
  residue is the advisory's to judge), and `TC-055`'s anchor-list copy is
  retired.
  Standing rules that survive the flip: a critic finding a bound clause
  violated routes through change-intake to harden the owning TC, never
  through a verdict; do not quietly mechanize reader-experience clauses into
  proxies; and *measure before writing a clause off as needing eyes* — nearly
  every clause measured 2026-07-25/26 failed on first measurement. The
  decomposition history (nine anchors bound, the T1/T3 rulings, the critique
  evidence chain [115](reviews/115-CRITIQUE.md)→[123](reviews/123-CRITIQUE.md))
  is in [log.md](log.md).
- **Retired:** **WI-082** 2026-07-22 (decompose `bootstrap.py main()`) —
  superseded by the H-2 decomposition row on the frontier, which now owns it
  as a concrete first slice. And
  the `--border` boundary-contrast row 2026-07-24 — retired rather than
  deleted so an over-claimed critic finding and its refutation stay
  traceable; that is evidence about critique reliability, not dead weight.
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **The standing lesson from the review-round era keeps its homes, not a
  status block**: the recurring defect on this branch was signed CLAIMS that
  pass every test, and one machine is one data point for OS-behavior claims —
  both live in process-options.md ("Signed measurements"); the round-by-round
  account (127→131) is in [log.md](log.md).
- **Render rows.** The `render` class is a **batching tag** (§3.3, post
  RULING-5) — no gate hangs on it and no render work is queued; the periodic
  advisory critique judges the T8 port-fan residue when it next runs (do
  **not** mechanize the clause into a crossing-count proxy — standing rule).
- **The owner decision surface is now [open-items.html](open-items.html)**,
  generated from [requirements/open-items.toml](requirements/open-items.toml) plus
  every `Draft`/`Modified` spine row's per-cell before/after. Read it there, not
  in a markdown file — there is no longer one. Two things it will tell you that
  the old pointer block could not: **which chain rows re-attest with an SR**, and
  **the baseline revision each diff was computed against**. A section with no
  cells means *check the baseline* (`--since`), never *nothing changed*.
  **OI-4 and OI-8 are ruled** (2026-07-25 — Apache-2.0, and hosted CI on every
  branch push; rulings in [log.md](log.md)'s Decisions), the **T1/T3
  critique-retirement call is ruled** (2026-07-26), and **OI-7 is ruled**
  (keep per-slice review; WI-123 `retired`, spec archived). With all four
  2026-07-29 sittings closed (above), the owner queue held no decision brief and
  no pending attestation until the **2026-08-07 owner-directed stakeholder-need
  cleanup opened one**: it amended SN-011, narrowed SN-025 and minted SN-026
  (multi-family LLM configuration) + SN-027 (parallel throughput), flipping
  **20 SRs to `Modified`** and dropping the derived gate **DevBar-Release → DevBar-Tests**
  (`ex-draft=DevBar-Tests` — amendment pressure, not new drafting). **One re-attest sitting
  over those 20 rows is owed**; read the per-cell before/after in
  [open-items.html](open-items.html) and the account in that day's
  [log.md](log.md) entry, not here. Alongside it stands the standing
  item the loop won't make:
  **merge-to-`main`** for `dualplan-routing-fix` (and the push before it,
  per `push-policy: human`; `ConcurrencyTrainRewrite` joins that list now
  its windows are closed). Per the 2026-07-27 sitting's own finding, the
  shorter the window, the less it can hide.
  The remaining archive-anchored rows **WI-061 / WI-063**
  (deferred) still want per-row re-specification versus the now-available
  `retired` disposition. The two cheap
  growth sensors from the review tail already landed as tests — the per-module
  size ratchet (`tests/test_module_size_ratchet.py`) and the dashboard size
  budget (`tests/test_dashboard_size_budget.py`).
- **Merge-to-main** for `dualplan-routing-fix` (+ `guardrails-fable-method`)
  stays a deliberate owner decision (push-policy: human). OPENCODE-KIMI/GROK
  enabled; builder preference Anthropic-led per tier (Fable strong / Opus
  medium).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.11+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
