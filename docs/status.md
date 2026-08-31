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
the shipped S-1 budget of **120 lines** (`check_docs.py`). Backward-looking homes:
[log.md](log.md) (sessions, verdicts, **Decisions**), [open-items.html](open-items.html)
(the generated **Open items** owner surface), [docs/work/](work/) (the WI registry —
status = directory; terminal rows under [archive/work/](archive/work/)),
[archive/](archive/README.md), and the folder map [docs/README.md](README.md).

- **RESUME HERE — THE FRONTIER IS PAUSED (tracked `docs/work/pause`) AND THREE
  DECISIONS ARE YOURS.** The 2026-08-31 supervised run merged four rows, closed
  one partial and disposed it; its record is the sitting in [log.md](log.md) and
  decisions 40–46 of
  [decisions-for-review-2026-08-31.md](decisions-for-review-2026-08-31.md).
  Deleting `docs/work/pause` in a reviewed commit resumes the generated frontier
  below. **In order of weight:**
  1. **The queue does not move on its own, and why is a design question** —
     plan of record
     [plans/2026-08-31-verdict-record-and-queue-blockers.md](plans/2026-08-31-verdict-record-and-queue-blockers.md):
     is `docs/reviews/WI-<n>-REVIEW-A.md` the right verdict carrier (nothing
     writes it, it is not declared generated, and it is the only artifact the
     merge gate reads), three alternatives, a recommendation, eight more
     blockers. Every run of 2026-08-31 stopped at one lane.
  2. **Three open items are pending** — the generated block below names them and
     [open-items.html](open-items.html) carries each one's options and
     recommendation. `OI-70` is the one that let the rest hide.
  3. **To confirm or revert, all recorded in the sitting and decisions 40–46:**
     kit findings A–O; two supervisor trunk fixes (`out/agent-loop.lock` joins the
     unload residue, with test; the approval brief regenerated on trunk); two
     recorded re-stamps (module-size ratchet 2653 → 2655; two cognitive ceilings
     kept at 37 / 18 with their reasons — decomposition stays the debt owner's).
  4. **Yours as before:** the TERRA reasoning-effort dial, the re-attestation
     brief [ratify/CURRENT.md](ratify/CURRENT.md), the ratchet pointer the debt
     owner's successor moves. Approval authority is whatever
     [process.toml](process.toml) `human_approval_through` declares.
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). **Two records exist in this working copy
  only** — back them up before either branch is touched:
  `wi508-architectural-remap-HELD-for-owner-verdict` (43 commits, thirteen round
  files, a compiled verdict that is not on trunk; held by ref rename — `OI-71`)
  and `wi416-parked-handback-contract` (a 271-line pre-ruling draft, rows
  disposed; delete only after deciding it is not wanted).
- **Standing constraints:** the depth-0 frame is **LOCKED and APPROVED** — 4
  entities · 4 crossings · 3 relationships, ids spent and watermark-held; the
  repository is the system, the template is the deliverable. Owner-owed, not
  re-raised: `OI-49` (b)'s named exception reads, each with a recommendation in
  [plans/2026-08-22-interface-exception-dossier.md](plans/2026-08-22-interface-exception-dossier.md),
  **awaiting your approving Status-change commit**; `OI-61` (c), deferred; and the
  wording round's two banked findings about `Approved` text nobody may edit
  ([reviews/2026-08-24-draft-wording-round/RESUME.md](reviews/2026-08-24-draft-wording-round/RESUME.md)).
- **Grinding the frontier:** IN SERIES, one worker per row, routed by BuildTier;
  a full-suite run must be FOREGROUND with an explicit timeout (a backgrounded one
  dies with the session's turn — it closed a finished row `partial`).
- **Unfiled follow-ups** (topics, no ids): the stage-ladder program's deferred
  codex review round; the SN-036 per-decomposition coverage record (re-derive —
  the basis now reads `uncovered=0`); the two findings in the archived
  [2026-08-01 handoff §6](archive/history/handoff-2026-08-01.md); the residues + §8
  dead-symbol table in [spine-restructure-2026-08-08.md](spine-restructure-2026-08-08.md)
  (§7 items 2/4/5 need a destination before it can archive); PROCESS.md §4's stale
  "ordinal `0`–`4`" approval dial.
- **Conventions:** spec-of-record [specs/README.md](specs/README.md) · rubrics
  [rubrics/README.md](rubrics/README.md) · partial closes [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_GENERATED by `python project-trajectory/scripts/gen_trajectory.py --status` — do not hand-edit; cite the spine registries + `docs/stage`, not this rendering (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-LLReqs** (stage 5 of 8, LLR definition in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-LLReqs`, derived current **phase=5**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=27 SR=76 LLR=188 TC=186** (10 drafts) · 163 seams · 4 components.
- **Open items** _(pending rows of [requirements/open-items.toml](requirements/open-items.toml); each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-70** — rule how a lane stopped for the owner's own ruling is RECORDED and SURFACED - today it is a branch rename plus prose, invisible to open-items.html; recommendation: the hold must mint a row, because prose is exactly what failed here
  - **OI-71** — rule what happens to the 43-commit wi508 lane held since 2026-08-30 - it carries the architectural remap program and its evidence exists in one working copy only
  - **OI-72** — rule whether SR-163 keeps a directly-tracing TC, is covered only through its LLR arms, or has its Verification class amended - two review rounds of the same reviewer asked for opposite answers
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-508** `P2` — The architectural remapping program: blind minimal-map re-derivation, divergences filed a…
  - **WI-536** `P2` — Agent-brief and scope: the knowledge-pack review's six byte-paid edits and two kit findin…
  - **WI-539** `P2` — Ship the complexity sensor: MAPPING row, template step, the opt-in layer, the deep-module…
  - **WI-545** `P2` — The decomposition debt owner (cont.): three wide modules, check_trajectory's remaining fu…
  - **WI-551** `P2` — Re-land the adjudicator session-retention layer from its preserved patch, inert at dial 0…
<!-- END GENERATED STATUS -->

- **Bar (per commit)** and the **standing rules** (claim refusal on prose ids,
  never sanction a check to green a step, signed-claim/one-machine humility,
  line-ending hygiene, claiming through the integrator): the `session-protocol`
  skill §2–§3. Also: run `check_trajectory.py --strict` unfiltered before claiming
  anything done — the pre-commit floor is warn-first and never the strict bar; and
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
