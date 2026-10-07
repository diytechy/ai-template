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
  [handoff-2026-10-06-wave18-coordinator.md](handoff-2026-10-06-wave18-coordinator.md):
  one lane is open (the in-lane Done-when blessing) with its owed steps, the
  corrections, the owner's questions, and the session prompt to paste.
  Delegated decisions take the owner's verdict as `owner = "confirmed"` or
  `"overruled"`; entries not yet seen, high-risk first, render under "Decisions
  to review" in [open-items.html](open-items.html), and an overrule must change
  open work citing it in the same commit.
  Approval acts run to seq 43 on trunk. The context guard is live: take the coordinator
  lease (`coordinator_guard.py take`) before any claim, and hand it back
  (`coordinator_guard.py handback --handoff <path>`) as the close-out's last act.
  0. **Finish the in-lane Done-when blessing, then the blackout row.** The
     blessing's lane is claimed and committed; the handoff lists what is owed
     (one builder round for the markdown needs carrier, a Terra round, Sol's
     narrow round, two adjudication sittings, the landing). Then claim the
     blackout row (the blackout pause, run's workstation check, the entry
     points in the README) under one scoped unpause; its adjudications use the
     combined sitting. The owner's sign-in question for the adjudicator's
     dedicated home (handoff) belongs to that row's sign-in step.
  1. **Build the S788-* successor rows** of the approved design note
     ([plans/2026-10-04-wi788-design/README.md](plans/2026-10-04-wi788-design/README.md),
     its ruling section first; it overrides the chapters), in their `needs`
     order with the wave-11 cycle, claiming each batch under one scoped unpause.
     The generated ready frontier below lists the rows that can start; the
     handoff names them. The owner directed (2026-10-04) that this campaign
     runs by coordinator session, not the unattended loop. OI-105 (the
     FreeLLMAPI endpoint and pinned models) waits for the owner's router; it
     holds only the FreeLLMAPI row of S788-routes.
  2. OI-98: the owner re-syncs `C:\Projects\FileBackup` (stamp `9b697cc`) as a
     scratch trial, after TC-036's inputs gain `RESYNC_PACK.md`, then rules it.

  `docs/work/pause` is still tracked (since 2026-09-04): the unattended
  dispatcher claims nothing until a reviewed commit deletes it, so work is
  taken by a coordinator session, not the loop. Owner direction 2026-10-04: a coordinator
  session claims its whole batch of rows under ONE scoped unpause (a reviewed
  deletion commit, the claims, then a byte-identical restore), not one per row;
  the control ruling's pause deletion is not spent. The roles (owner, 2026-10-04): Claude Opus builds and plans at medium
  effort and the coordinator commits for it; GPT Terra (`gpt-5.6-terra`,
  medium) authors spine rows; Codex 6.1 (`gpt-6.1-sol`, high) reviews code
  through the CLI; and an independent Opus agent adjudicates and resolves
  disputes. File new work as a row; an open item is filed together with the queued
  placeholder row whose `needs` cites it, and the commit that rules it updates
  that row's Done-when (OI-102). The reviewers' `codex exec` launch
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
  and this branch (`push = "human"`). The held wi508
  branch is on origin; the queued wi508-partial-close row is the only
  sanctioned act on it (`OI-71`).
- **Standing constraints:** the depth-0 frame is **LOCKED and APPROVED** (4
  entities · 4 crossings · 3 relationships, watermark-held); `OI-61` (c) stays deferred
  on its condition (a demonstrated residual drift class), not owner-owed.
- **Unfiled follow-ups** (topics, no ids): the wave-11 log's follow-ups (the claim
  reads the working-tree pause; an in-lane act never meets the held-rung
  re-attestation refusal; a refresh merge must carry a citer's update for a
  trunk ruling); the wave-9 log's session-close list (removed approved rows mint no adjudication; six batch-R row-text residues); the stage-ladder program's deferred
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
- **Spine:** **SN=31 SR=123 LLR=285 TC=294** (21 drafts) · 235 seams · 4 components.
- **Open items** _(the pending rows of [requirements/open-items.toml](requirements/open-items.toml) a queued work item cites; each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-98** — The owner must perform the re-sync from 2026-10-03 and rule this item to release WI-684. _(holds WI-684)_
  - **OI-105** — When the owner's FreeLLMAPI router is running, name its endpoint and the models to pin, and confirm it holds a one-model chain per pinned id, so the FreeLLMAPI route row can ship and take its one live call. _(holds WI-795)_
  - **OI-106** — Sign the two-clause amendment of SN-029 (owner-held): its acceptance calls amend-and-flip in one commit 'the sanctioned path', and its why argues from that path, but since WI-806 spine text is committed before the act that blesses it. _(holds WI-827)_
  - **OI-107** — Decide whether a delegated run's decisions record needs an identity of its own: today a/b and a-b, or two lanes reusing one branch name, write one docs/decisions/<run>.toml, and any fix moves record paths (a forced migration). _(holds WI-832)_
- **Decisions to review:** 170 — [open-items.html](open-items.html#decisions-to-review)
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-831** — re-judge TC-055: declared trigger fired [sha256:463ba32184eb] at merge a8458c2
  - **WI-841** `P9` — An in-lane Done-when change is blessed in the lane before the lane builds on it or closes
  - **WI-834** `P8` — Blackout pauses lanes on both routes; run checks the workstation first; the entry points…
  - **WI-798** `P3` — Account tables and per-account homes for every CLI route
  - **WI-799** `P3` — Lane-state provider that derives each lane's state from evidence, representation only
  - **WI-823** `P3` — TC-055's rubric binds T2 and T5 to their test rows, and the shot matrix covers every rend…
  - **WI-828** `P3` — A hand merge on trunk judges the commits it brings in, as the squash landing does
  - **WI-833** `P3` — An owner's verdict stays bound to the decision text it judged
- **Blocked** _(held by a pending open item its `needs` cites):_
  - **WI-684** — re-judge TC-036: no result recorded [sha256:2f2f30dfba87] at merge 77fb093 — [OI-98 — Owner re-sync from 2026-10-03](open-items.html#OI-98)
  - **WI-795** — Owner provisioning: the FreeLLMAPI endpoint and pinned models — [OI-105 — FreeLLMAPI provisioning: the endpoint and the pinned models](open-items.html#OI-105)
  - **WI-827** — Owner signs SN-029's amendment after text-before-act — [OI-106 — SN-029: two clauses untrue since text-before-act landed](open-items.html#OI-106)
  - **WI-832** — A decisions record has an identity no other run can share — [OI-107 — Decisions record identity: a run's record is named by a lossy, reusable branch name](open-items.html#OI-107)
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
