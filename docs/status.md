<!--
Contracts: IF-163 — the interface seam this file declares (process.md §8; row of
record in requirements/interfaces.toml).

Contract IF-163: the forward-only blackboard's HAND-AUTHORED bytes — everything
    outside the GENERATED STATUS marker pair — read as data by the kit's checks
    and by a resuming session; the block between the markers is its writer's
    own row. Markdown with `##` sections: `## Current State` is the section a
    stopping coordinator excerpts into its exit banner (the generated block
    rides inside that excerpt as the writer's bytes). Only what must happen
    NEXT belongs here — what already happened lives in log.md — so a work-item
    id recorded closed must not appear in the hand-authored prose, and a claim
    naming one there is refused; inside the generated block that rule stands
    down, because the generated frontier legitimately names queued ids.
-->

# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself. **Forward-only**, held to
the declared S-1 budget (`docs/status-lint`; raised 2026-08-31 to carry the
supervisor prompt at the owner's request). Backward-looking homes:
[log.md](log.md) (sessions, verdicts, **Decisions**), [open-items.html](open-items.html)
(the generated **Open items** owner surface), [docs/work/](work/) (the WI registry —
status = directory; terminal rows under [archive/work/](archive/work/)),
[archive/](archive/README.md), and the folder map [docs/README.md](README.md).

- **RESUME HERE — THE FRONTIER IS PAUSED (tracked `docs/work/pause`); THE
  2026-08-31 RULINGS ARE LANDED AND THEIR ROWS ARE QUEUED.** `OI-70`..`OI-76`
  are ruled (the log's 2026-08-31 rulings entries); WI-552..WI-562 are
  filed — WI-552 re-scoped by `OI-73` (typed OI edges in `needs`, the
  mandatory successor, edges replaced at the mint), WI-557 owns the
  delegated-decisions record + `decision_recording` dial (`OI-74`/`OI-75`),
  WI-558..WI-562 the verdict-carrier rebuild and queue-blocker set (`OI-76`,
  plan [plans/2026-08-31-verdict-record-and-queue-blockers.md](plans/2026-08-31-verdict-record-and-queue-blockers.md)) —
  WI-543 is re-scoped and queued (SR-163's owner, frontier head), WI-541 is
  re-pointed to WI-551, WI-545 sequenced behind WI-552/WI-553.
  Nothing further is owner-owed here beyond the standing acts below.
  To resume the loop, paste the supervisor prompt below into a fresh session.
  A fresh reader starts at [handoff-2026-08-31.md](handoff-2026-08-31.md), the
  sitting in [log.md](log.md), and delegated decisions 1–46 in
  [decisions-for-review-2026-08-31.md](decisions-for-review-2026-08-31.md).
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). `wi416-parked-handback-contract` is still
  single-copy — delete only after deciding it is not wanted. The held wi508
  branch is on origin; WI-555 is the only sanctioned act on it (`OI-71`).
- **Standing constraints:** the depth-0 frame is **LOCKED and APPROVED** (4
  entities · 4 crossings · 3 relationships, watermark-held); owner-owed, not
  re-raised: `OI-49` (b)'s exception reads
  ([plans/2026-08-22-interface-exception-dossier.md](plans/2026-08-22-interface-exception-dossier.md)),
  `OI-61` (c) deferred, and the wording round's two banked findings
  ([reviews/2026-08-24-draft-wording-round/RESUME.md](reviews/2026-08-24-draft-wording-round/RESUME.md)).
- **Unfiled follow-ups** (topics, no ids): the stage-ladder program's deferred
  codex round; the SN-036 coverage record (re-derive — basis reads
  `uncovered=0`); the archived [2026-08-01 handoff §6](archive/history/handoff-2026-08-01.md)
  findings; the [spine-restructure-2026-08-08.md](spine-restructure-2026-08-08.md)
  residues (§7 items 2/4/5 need a destination); PROCESS.md §4's stale
  "ordinal `0`–`4`" approval dial.
- **Conventions:** [specs/README.md](specs/README.md) · [rubrics/README.md](rubrics/README.md) · partial closes [handbacks/](handbacks/README.md).
- **Supervisor prompt** (owner-authorized unpause — paste into a fresh session):

  ```text
  You are the supervisor of this repository's mechanized loop, on branch
  contract_split — the integrator's trunk is HEAD; stay on this branch, never
  merge to main, never push (push = "human"); commit is permitted. Read
  CLAUDE.md, the session-protocol skill, docs/status.md (RESUME HERE),
  docs/handoff-2026-08-31.md, docs/decisions-for-review-2026-08-31.md (46
  delegated decisions), and the memories unattended-run-2026-08-30-traps and
  unattended-run-2026-08-31-traps. Spin up opus subagents for edits and
  analysis to keep your own context low.
  State at handoff: OI-70..OI-76 are RULED (log.md, the 2026-08-31 rulings
  entries) and their rows are queued: WI-543 (SR-163 mechanism, spine, frontier
  head), WI-552/WI-553 (the OI-70 repairs; WI-552 re-scoped by OI-73),
  WI-554 (brief-renderer defects), WI-557 (delegated-decisions record + dial),
  WI-558..WI-562 (verdict-carrier rebuild + queue-blockers, OI-76),
  WI-555 (the wi508 partial close; needs WI-554), WI-556 (doctrine, quick);
  WI-541 waits on WI-551, WI-545 on WI-552/WI-553. The scheduler's generated
  frontier is the order of record. The wi508 row in active/ is a phantom head
  the dispatcher skips until WI-555 clears it; the held branch is pushed to
  origin — touch it only through WI-555's row.
  Unpause — the owner confirms it: delete docs/work/pause in a reviewed
  commit (regenerate docs/open-items.html in the same commit) and run the
  real loop (./agent-resume.sh --wait-on-limit 14400 from a terminal at the
  repo root — this box is macOS; agent-resume.cmd/PowerShell is the Windows
  form), supervising rather than replacing it: honour the
  12:00–19:00 UTC weekday blackout, intervene only through the kit's scripts,
  never a hand-minted id, never a hand-moved spec, never touch a tracked
  trunk file while the loop runs. Until WI-558 re-points the gate (OI-76,
  ruled B+C), compile the WI-level docs/reviews/WI-<n>-REVIEW-A.md from the
  round files (time-ordered, governing line last) after the loop's rounds
  APPROVE — the loop does not write it yet. Watch and record: the worker/adjudicator close
  ritual, the C2 REVIEW-OWED park + resume, the C4 probe lines, any -relaxed
  verdict, the C6 unload. Merge a hand-finished lane yourself from the trunk
  root (drains run only before exclusive claims); after merging a lane that
  regenerated docs/ratify/CURRENT.md, regenerate it again on trunk.
  Re-measure the smoke budget on a quiet box before the first commit
  (python -m pytest -q -n auto -m smoke && python
  scripts/check_smoke_budget.py --mode enforce; 60 s; this Mac read
  20.3-28.4 s quiet across 2026-08-31, full suite 602 s) and record it.
  Do not touch: main, the approval dial, [policies], the TERRA
  reasoning-effort dial, any ruled open item, or WI-543's ruled scope.
  Dispose NEEDS-HUMAN stops with the best decision the information supports,
  through the kit's own mechanisms, recording each with its alternative in
  docs/decisions-for-review-2026-08-31.md (continue numbering at 47; the
  format WI-557 builds replaces this file class when it lands). Traps: the
  PowerShell-absolute-path and agent_common._utf8_console() traps are
  Windows-only — moot on this Mac; write big patch scripts with the Write
  tool, not heredocs; the full suite is ~10 min here — run it FOREGROUND
  with an explicit timeout, never backgrounded. End by writing
  the session fragment under docs/log.d/ (then trunk_step.py --compile-log on
  trunk once committed), updating RESUME HERE with a "for the owner's
  review" list, and stopping with the repo drained and quiet.
  ```

## Current State

<!-- BEGIN GENERATED STATUS -->
_GENERATED by `python project-trajectory/scripts/gen_trajectory.py --status` — do not hand-edit; cite the spine registries + `docs/stage`, not this rendering (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-LLReqs** (stage 5 of 8, LLR definition in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-LLReqs`, derived current **phase=5**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=27 SR=76 LLR=188 TC=186** (10 drafts) · 163 seams · 4 components.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-543** `P3` — SR-163's owner: the tolerant requirement-reference cell, the four-class checker warn-firs…
  - **WI-508** `P2` — The architectural remapping program: blind minimal-map re-derivation, divergences filed a…
  - **WI-552** `P3` — The adjudicator's two exits: adjudication-row close, successor mint, OI mint with refusal…
  - **WI-553** `P3` — The hold ban mechanized: claim-ref check, blocked_pending retired, fragment declaration c…
  - **WI-554** `P3` — Approval-brief renderer defects: a Drafted row shown approved, a changed Method cell trun…
  - **WI-557** `P3` — The delegated-decisions record: per-run TOML file, close-time obligation under the decisi…
  - **WI-560** `P3` — One freshness definition for verdicts, and the approval brief's two staleness traps (OI-7…
  - **WI-561** `P3` — The quarantine spares what is monotone or record: the id watermark, docs/reviews, docs/lo…
  - **WI-562** `P3` — Unload residue and scratch: integrate.lock declared, the worker told where scratch belong…
  - **WI-551** `P2` — Re-land the adjudicator session-retention layer from its preserved patch, inert at dial 0…
  - **WI-536** `P2` — Agent-brief and scope: the knowledge-pack review's six byte-paid edits and two kit findin…
  - **WI-539** `P2` — Ship the complexity sensor: MAPPING row, template step, the opt-in layer, the deep-module…
  - _(+3 more ready — see the dashboard)_
<!-- END GENERATED STATUS -->

- **Bar (per commit)** and the **standing rules** (claim refusal on prose ids,
  never sanction a check to green a step, line-ending hygiene, claiming through
  the integrator): the `session-protocol` skill §2–§3. Run
  `check_trajectory.py --strict` unfiltered before claiming anything done;
  route a critique dispatch by PROVIDER, probing first.
- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) · working rules
  [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill · lock items
  [repo-lock.md](repo-lock.md) · external (not this repo's work): guardrails
  content in `TheColliny/FableClaudeMDForOpus`.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the `PROJECT-VISION:`
  tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only, Python 3.11+.
- **Non-goals (self-application boundary):** no product **launch** — the kit's
  "product" is `project-trajectory/` + `tests/`; an actions-menu launcher is in
  scope, a `run.*` product launcher is not. No scaffolded `docs/process.md` (the
  masters live in `project-trajectory/`).
