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

- **RESUME HERE:** start with the coordinator's
  [handoff-2026-09-26-coordinator.md](handoff-2026-09-26-coordinator.md), then
  [handoff-2026-09-26.md](handoff-2026-09-26.md)'s
  read order. The redesign's remaining threads keep their context in
  [handoff-2026-09-06.md](handoff-2026-09-06.md). Recheck Git and the generated
  frontier before choosing work; earlier handoffs and sitting checklists are
  historical context.
- **Assumption tier — the second build wave has landed:** next is the
  joint amendment adjudication the coordinator's handoff owes. The phase-6
  chains are approved down to test cases
  ([spine map](plans/2026-09-25-assumption-tier-spine-map.md)), the needs by
  the owner's stand-in, and the build proceeds test-first, one builder
  worktree per item in the generated frontier's order, each handed the
  [builder brief](plans/2026-09-26-assumption-tier-builder-brief.md). The C1
  sitting commit and the reversal sweep follow it. The full unfiltered suite is
  owed before any phase close. The owner ruled the pending open items on
  2026-09-26 except the Boundary-arm question, kept open for discussion
  ([rulings](log.d/2026-09-26-owner-rulings-oi82-oi94.md)); their follow-ups
  are in the queue. The depth-0 mockup in
  `docs/plans/mockups/` still renders the old `kit` value.
- **Sister plan — one plan still owed:** every question in the
  [notes on spine, sessions and tests](plans/2026-09-23-owner-notes-spine-sessions-and-tests.md)
  §5 is ruled except S11, whose direction (one trunk commit per work item)
  needs its own plan before any ruling; design S9's reviewer-commit check with
  it. S7's session service proceeds and writes S8's adopted OTel schema; S6 is
  designed with the assumption tier before its C3; S14's flag-axis count
  proceeds, its duplicate-detection research first.
- **Next implementation:** resolve the existing SR-161 per-decomposition
  perspective-record gap and complete TC-211's normal sample. Follow the
  existing artifact adjudication route for the Drafted amendments; passing an
  Inspection does not approve its requirement. Keep the scope proportional to
  the missing obligation.
- **Control launch:** retain the tracked `docs/work/pause` while preparing
  route-complete spending bounds, including in-flight drain, against the
  [settled control ruling](ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md#owner-ruling-2026-09-06).
  Revalidate the [preflight](ai-template-redesign-2026-09-05-codex/CONTROL-PREFLIGHT.md)
  at the proposed frozen launch commit, then obtain the ruling's owner-reviewed
  pause deletion. Replacement packages follow the control's evidence decision.
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). `wi416-parked-handback-contract` is still
  single-copy — delete only after deciding it is not wanted. The held wi508
  branch is on origin; the queued wi508-partial-close row is the only
  sanctioned act on it (`OI-71`).
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
  "ordinal `0`–`4`" approval dial; **owner intake 2026-09-22:** the self-test
  suite should fail fast when its dev toolchain is missing, and name the run
  menu's setup action as the fix. Today a missing pytest-xdist dies on
  `unrecognized arguments: -n`. This depends on the root launchers SN-034/SN-035
  require, which do not exist yet, and needs stepping through as a requirement
  before it is built.
- **Conventions:** [specs/README.md](specs/README.md) · [rubrics/README.md](rubrics/README.md) · partial closes [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_GENERATED by `python project-trajectory/scripts/gen_trajectory.py --status` — do not hand-edit; cite the spine registries + `docs/stage`, not this rendering (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-Tests** (stage 6 of 8, test-case definition in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-Tests;6=DevStg-Impl`, derived current **phase=6**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=31 SR=112 LLR=240 TC=235** (19 drafts) · 188 seams · 4 components.
- **Open items** _(pending rows of [requirements/open-items.toml](requirements/open-items.toml); each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-88** — OWNER DIRECTION 2026-09-26, not yet ruled: the owner leans to approving a level-0 interface that meets a boundary together with the assumption that needs it (an assumption cannot exist without its interface), or to baking the interface into the assumption, and asks for more discussion. The driver's reading: the frame's crossings ARE those level-0 interfaces and are approved at DevStg-Boundary, so SR-212 can gain a Boundary arm over crossings while its interface-row arm stays at Arch. Rule (a), (b), (c) or (d).
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-582** `P4` — The WI-552 residual sweep: the schedule-trace seam's test case, the validate docstring, t…
  - **WI-644** `P4` — Sweep the rows that restate a reversed sitting-2 ruling (LLR-051/056/057/124/139, SR-151/…
  - **WI-650** `P4` — Count a requirement's test case from its first approved-and-associated commit, and warn w…
  - **WI-673** `P4` — Amend SR-209's requirement and TC-242 to the loop-lane ownership rule its acceptance now…
  - **WI-655** `P3` — C2: write the assumption and surrogate rows, and each boundary interface's bridged_by or…
  - **WI-672** `P3` — Tie a test case's tier to the smoke tier's membership, and settle the older Smoke cases w…
  - **WI-626** `P2` — Make the shared-spec warning compare section anchors, so distinct sections of one plan ar…
  - **WI-604** — adjudicate: LLR-210, TC-208
  - **WI-674** — adjudicate: LLR-259, TC-252
  - **WI-581** `P6` — Lane-close hygiene: quarantine spares monotone and record paths, integrate.lock declared
  - **WI-663** `P6` — Fix the invalid noqa directive ruff reports in the stage-ladder test
  - **WI-570** `P5` — The typed open-item brief: an adjudicator-minted OI carries blast radius, options and a r…
  - _(+33 more ready — see the dashboard)_
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
