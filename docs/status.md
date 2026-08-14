# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. This file is
**forward-only**: only what must happen **next** lives here. Backward-looking
homes: [log.md](log.md) (sessions, verdicts, **Decisions**),
[open-items.html](open-items.html) (the generated owner surface),
[docs/work/](work/) (the WI registry — status = directory; dashboard
[`PROJECT_STATE.html`](../PROJECT_STATE.html)), and
[archive/](archive/README.md) (design history, with per-file dispositions).
Rewritten 2026-08-13w to the forward-only shape; everything the old file
narrated is in those homes.

- **THE TARGET — the SR/LLR/TC RE-TIER CAMPAIGN against the locked depth-0
  frame.** The frame is **LOCKED**: 5 entities · **6 crossings** · 3
  relationships; the repository is the system, the template is the deliverable
  (log Decisions `2026-08-13k`/`o`/`u`). **Sitting 2 is CLOSED — all twelve
  decisions ruled** (`2026-08-13l`…`v`); it ruled the frame and deliberately
  signed no spine. The rulings live in
  [plans/2026-08-13-sitting-2-boundary-and-context.md](plans/2026-08-13-sitting-2-boundary-and-context.md)
  (§1R the frame · §3R the form rule · §4.0 the closed-decision ledger). The
  schema row is **LANDED** (2026-08-14: `external.toml` minted,
  `interfaces.toml` slimmed to the approval schema, both sharp hazards held
  in-commit) and the re-tier's slice-1 **census is COMPLETE on its open lane**
  (all 148 SRs classified against the 6 crossings, demotion sized; the census
  doc also sits on trunk at
  [plans/2026-08-14-wi451-slice1-sr-census.md](plans/2026-08-14-wi451-slice1-sr-census.md)).
  **The census is RATIFIED and slice 2 is UNBLOCKED** (log `2026-08-14b`/`c`):
  34 hold · 15 re-state · 73 demote · **26 tombstones DELETE per D-4** (one
  forwarding log entry, citing IFs go with their rows, `trace.py`'s
  supersession machinery + TC-099 retire by ruling), and B-05 gains the
  declared **package-wide-property** sixth bucket so SR-031/034/035/114 each
  stay one row. What executes next: **slice 2** — every demotion needs a
  parent SR; the one-shall rule applies as a **guideline with recorded
  waivers** (`2026-08-13v`); the **token-verification bar** governs
  re-statement — no obligation weakened, every re-stated cell token-compared
  (the method is recorded in [log.md](log.md) and in sitting-3 §1
  precondition 5). The findings the
  campaign exposes are **a deliverable of it, not a failure of it** (owner,
  13s). The remaining rows are in [work/queued/](work/queued/); the generated
  frontier below names them in build order.
- **The amendment window closes at SITTING 3, not before.** `drafts=27
  modified=51 uncovered=7`, gate `DevBar-Reqs`, stage `DevStg-Boundary` (1/8)
  — the snapshot below. The window stays open **deliberately** through the
  re-tier;
  [plans/2026-08-13-sitting-3-spine-verification.md](plans/2026-08-13-sitting-3-spine-verification.md)
  owns its close — its **§0.3 decision ledger is 7-of-9 ruled** (`2026-08-14b`
  …`f`); the TC-159 chain fix is **DONE** (`14f`, the crossed carrier pairs
  aligned). What remains there: the LLR/TC draft ratifications (27 rows), and
  — folded in by 13u decision 12 — the **one shared status vocabulary across
  every registry** (per-registry subsets; change detection deferred
  off-spine), ruled `14e` to execute as **ONE SEQUENCE with the ratification
  wave** right after slice 2's drafts land, carrying `Planned`'s fate and the
  off-spine flip authority with it (checklist archived at
  [archive/plans/2026-08-11-status-ladder-migration.md](archive/plans/2026-08-11-status-ladder-migration.md);
  figures stale — re-derive). One item still re-lands as execution reaches
  it: `check_flows`'s Runtime-flows obligation (moved with the flows to
  `docs/runtime-flows.md` on the retirement lane — never lapsed; re-check at
  that lane's merge). Crossing ownership is **deferred by name** to after
  slice 2 populates the boundary refs (`14d`), and the human-agent entity
  call is **confirmed** — five entities, the human inside EXT-001 (`14d`).
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). Known residue, kept deliberately: the
  `wi416-parked-handback-contract` branch holds a 271-line pre-ruling draft
  that exists nowhere else (its rows are disposed; the 2026-08-08 handback
  ruling superseded it) — delete only after deciding the draft is not wanted.
- **Unfiled follow-ups** (from the archived charge-through handoff; no ids
  yet, so listed as topics): the stage-ladder program's deferred codex review
  round; the SN-036 per-decomposition coverage record (its need is in the
  `uncovered=8`); the two findings named in the archived
  [2026-08-01 handoff §6](archive/history/handoff-2026-08-01.md); and the
  three unruled residues + §8 dead-symbol table in
  [spine-restructure-2026-08-08.md](spine-restructure-2026-08-08.md) (its §7
  items 2/4/5 need a destination before that file can archive).
- **Conventions:** spec-of-record [specs/README.md](specs/README.md) · rubrics
  [rubrics/README.md](rubrics/README.md) · partial-close reports
  [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_Derived facts — regenerated by `python project-trajectory/scripts/gen_trajectory.py --status`; do not hand-edit (the forward-only intent below is hand-authored)._

- **Stage:** **DevStg-Boundary** (stage 1 of 8, system boundary interfaces in work) · next bar: **DevBar-Reqs** (per-phase `1=DevBar-Tests;2=DevBar-Tests;3=DevBar-Tests;4=DevBar-Below;5=DevBar-Below`, derived current **phase=5**) — a repo is IN a stage and CLEARS a bar; the harness at that bar is the bar. [`derive_gate.py`](../project-trajectory/scripts/derive_gate.py) derives both, cached to [`docs/gate`](gate).
- **Spine:** **SN=27 SR=123 LLR=152 TC=147** (27 drafts) · 115 seams · 4 components.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-448** `P3` — OI-16 execution (inversion confirmed by the owner 2026-08-13): the common-module program
  - **WI-455** `P3` — The docs/architecture.md RETIREMENT program (owner-ruled 2026-08-13u, sitting-2 decision…
  - **WI-451** `P2` — THE SR RE-TIER CAMPAIGN (owner-ruled 2026-08-13q/s/u; supersedes this row's ~25/~50 confo…
  - **WI-390** — PROGRAM CLOSE for concurrency-v2 (docs/concurrency-v2.md §A9 deletion ledger). NOT a swee…
  - **WI-452** `P3` — Resurface LLR-165's carrier converter as the downstream-resync helper it now is (owner-ru…
<!-- END GENERATED STATUS -->

- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` +
  `python project-trajectory/scripts/check_docs.py --root . --ignore docs/test/report.md --ignore "docs/work/*" --stale`,
  both green. At slice/phase close: the full unfiltered suite (`pytest -q -n
  auto`) and `check.py` at the derived gate. Also run
  `check_trajectory.py --strict` directly, unfiltered, before claiming
  anything done — the DEFAULTED pre-commit floor stays warn-first by design,
  so the floor's output is never the strict bar.
- **Standing rules with no other home (do not delete without relocating):**
  - **An id named in this file's hand-authored prose CANNOT BE CLAIMED**
    (`integrate._status_prose_refusal` refuses it at claim time; generated
    blocks are exempt). Point at [work/queued/](work/queued/) and let the
    generated frontier name ids.
  - **Never revert a real fix, or sanction a check, to green a step** —
    editing a declared list (a coverage floor, an orphan glob, a ratchet
    baseline) to clear a finding IS accepting what it measures.
  - **Signed claims + one-machine humility:** the recurring review-era defect
    was signed CLAIMS that pass every test ("Signed measurements",
    process-options.md), and **one machine is one data point for OS-behavior
    claims** — state the condition, not the universal.
  - **Measure on a tree whose line endings match the index** — before
    trusting any byte count or hash, `git ls-files --eol | grep 'w/crlf'`
    (only `*.ps1`/`*.cmd`/`*.bat` should appear).
- **Claiming runs through the integrator** (`integrate.py claim`; merges are
  its serial fail-closed queue; a pause is a tracked `docs/work/pause`).
  Probe providers before planning a critique dispatch, and route by PROVIDER,
  not gateway.
- **External follow-up** *(not this repo's work)*: guardrails content
  enrichment lives in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) · working
  rules [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill · still-owed
  lock items [repo-lock.md](repo-lock.md) (its §1 now defers to the generated
  surfaces).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.11+.
- **Non-goals (self-application boundary):** no product **launch** — the
  kit's "product" is `project-trajectory/` + `tests/`, a meta-repo has no
  product to launch, and an actions-menu launcher is in scope (amended from
  "no `run.*` product launchers" at the 2026-08-13 sitting, on SN-035's
  attestation); no scaffolded `docs/process.md` (the masters live in
  `project-trajectory/`).
