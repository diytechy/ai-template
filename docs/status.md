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
  [handoff-2026-10-04-wave11-coordinator.md](handoff-2026-10-04-wave11-coordinator.md).
  It is an unattended build session: its order of work, the deltas since wave 10,
  how assumptions are recorded (`docs/decisions/`), and the session prompt to
  paste. The wave-8 and wave-10 handoffs it names still carry the roles, the
  tools and the in-lane cycle. Approval acts run to seq 28.
  1. The rows on the generated ready frontier, in the handoff's order. Every open
     item that held them is ruled (OI-100 to OI-103, 2026-10-03/04). The
     largest row stops at its design-note checkpoint for the owner.
  2. Owner signatures still owed: the four MEANING-ruled needs (SN-003, SN-008,
     SN-025, SN-043; the adjudicator recommends restoring SN-025's exclusions
     before signing).
  3. OI-98: the owner re-syncs `C:\Projects\FileBackup` (stamp `9b697cc`) as a
     scratch trial, after TC-036's inputs gain `RESYNC_PACK.md`, then rules it.

  `docs/work/pause` is still tracked (since 2026-09-04): the unattended
  dispatcher claims nothing until a reviewed commit deletes it, so work is
  taken by a coordinator session, not the loop. The roles (owner, 2026-10-04): Claude Opus builds and plans at medium
  effort and the coordinator commits for it; GPT Terra (`gpt-5.6-terra`,
  medium) authors spine rows; Codex 6.1 (`gpt-6.1-sol`, high) reviews code
  through the CLI; and an independent Opus agent adjudicates and resolves
  disputes. File new work as a row; an open item is filed together with the queued row
  that cites it (OI-102). The reviewers' `codex exec` launch
  runs under a temporary `Bash(codex exec *)` allow rule in
  `.claude/settings.local.json` (owner, 2026-09-28): remove it when the
  queue drains. Recheck Git and the generated frontier before choosing
  work; earlier handoffs are historical context.
- **Assumption tier — C1 and C2 have landed and are approved:** the
  redrawn frame, checkpoint re-judging of observation tests, the assumption
  gate's four steps (behind `[checks] assumption_gate = false`), and C2's
  assumption and surrogate rows with every SR's bridging. The owner signed
  the assumption ruling on 2026-10-02: an assumption carries status and standing
  only, falsification is the one signal, and there is no evidence ladder, so
  C3 shrinks to the falsification route and C5 loses its evidence arm. OI-97's joint-delivery class has
  landed and is anchored.
- **Sister plan — one plan still owed:** every question in the
  [notes on spine, sessions and tests](plans/2026-09-23-owner-notes-spine-sessions-and-tests.md)
  §5 is ruled except S11. The owner said yes to adjudication inside the lane
  (2026-10-03): a return is fixed in the lane, not minted as a follow-up row.
  Its plan, with S9's reviewer-commit check, is
  [plans/2026-10-03-s11-in-lane-adjudication.md](plans/2026-10-03-s11-in-lane-adjudication.md).
  Its §6 questions are ruled as recommended (owner, 2026-10-03, recorded with
  OI-101 Q6). Hand integration already follows it (owner direction 2026-09-28): one
  squash commit per item, with lane tips kept reachable in `archive/lanes`. S7's session service has landed, writing S8's adopted OTel schema, with
  retention shipped off; its live verification closed 2026-10-03 (a real adjudication peaked at 44% of the codex window), and the dial stays off. S6 is designed
  with the assumption tier before its C3. S14's flag-axis count and
  duplicate-detection research have both landed.
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
- **Unfiled follow-ups** (topics, no ids): the wave-9 log's session-close list (removed approved rows mint no adjudication; six batch-R row-text residues); the stage-ladder program's deferred
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

- **In stage:** **DevStg-Impl** (stage 7 of 8, implementation in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-Impl;6=DevStg-Impl`, derived current **phase=6**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=31 SR=120 LLR=277 TC=282** (21 drafts) · 221 seams · 4 components.
- **Open items** _(pending rows of [requirements/open-items.toml](requirements/open-items.toml); each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-98** — The owner must perform the re-sync from 2026-10-03 and rule this item to release WI-684.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-788** `P3` — Session families with reset terms, a glossary, per-route provider homes, and new routes
  - **WI-790** `P3` — Work items cite the open items they wait on; open items stop carrying wi_refs
  - **WI-791** `P3` — Route amended needs to the meaning-or-clarity adjudication; CLARITY re-attests on a held…
- **Blocked** _(owner gates; see IF-073):_
  - **WI-684** — re-judge TC-036: no result recorded [sha256:2f2f30dfba87] at merge 77fb093 — [OI-98 — Owner re-sync from 2026-10-03](open-items.html#OI-98)
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
