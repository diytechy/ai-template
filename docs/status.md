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

- **RESUME HERE:** start with [handoff-2026-09-06.md](handoff-2026-09-06.md),
  then the [redesign execution record](ai-template-redesign-2026-09-05-codex/EXECUTION-RECORD.md).
  Recheck Git and the generated frontier before choosing work; earlier handoffs
  and sitting checklists are historical context.
- **Assumption tier — the sitting (C1) is next:** every question in
  [the assumption-tier plan](plans/2026-09-20-validation-gap-and-the-assumption-tier.md)
  §12.1 is ruled (Q6 and Q16 revised 2026-09-24: `surrogate` rows, bundle
  `system = "operation" | "delivery"`). It is a core (the assumption tier)
  plus an extension (interface allocation at DevStg-Arch). The sitting also
  lands the sister plan's S3 (a provenance column on needs and the vision's two
  headline needs) and reverses parts of sitting 2 (its §5.2). The depth-0
  mockup in `docs/plans/mockups/` still renders the old `kit` value.
  **Nothing is built before the sitting.**
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

- **In stage:** **DevStg-Tests** (stage 6 of 8, test-case definition in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-Tests`, derived current **phase=5**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=27 SR=79 LLR=192 TC=194** (17 drafts) · 167 seams · 4 components.
- **Open items** _(pending rows of [requirements/open-items.toml](requirements/open-items.toml); each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-82** — WI-572 moved the first-approval act to the adjudicator and filtered the minted population by the human-approval dial at both adjudication ends (intake's mint and adjudicate_brief's composition, through agent_common.human_approves_spine). The plan's §2a table row 'Surfaces to the owner' says rows on a RELEASED rung no longer surface to the owner - but trace.py --approve modified still renders every Drafted chain, held or released, and calls human_approves_spine nowhere. Should the owner's approval brief narrow to the rungs the dial still HOLDS (so a sitting shows only what the owner actually owes a signature on), or keep rendering every Drafted chain (so the owner retains sight of what adjudicators are approving on their behalf)? WI-572 deliberately did not decide this: it changes what the owner sees at a sitting, which is the owner's call and not a side effect of moving who acts.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-582** `P4` — The WI-552 residual sweep: schedule-trace seam declared, needs read from the parsed value…
  - **WI-601** — adjudicate: LLR-061
  - **WI-602** — spot-check the clean close of WI-580
  - **WI-603** — adjudicate: LLR-167
  - **WI-604** — adjudicate: LLR-210, TC-208
  - **WI-551** `P7` — Re-land the adjudicator session-retention layer from its preserved patch, inert at dial 0…
  - **WI-581** `P6` — Lane-close hygiene: quarantine spares monotone and record paths, integrate.lock declared,…
  - **WI-570** `P5` — The typed open-item brief: an adjudicator-minted OI carries blast radius, options and a r…
  - **WI-612** `P5` — Make trunk bookkeeping commits stage and restore only what they wrote, so uncommitted edi…
  - **WI-607** `P4` — Route only on a committed verdict: read_verdict parses the file on disk, committed or not…
  - **WI-608** `P4` — Stop a later session rewriting an earlier review round's verdict file: reproduce first, t…
  - **WI-605** `P3` — Compute context occupancy from the latest request's prompt, not the session's cumulative…
  - _(+11 more ready — see the dashboard)_
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
